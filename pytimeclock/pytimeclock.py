#!/usr/bin/env python


# https://docs.python.org/3/library/curses.html
# https://www.devdungeon.com/content/curses-programming-python#toc-11

import _thread
import os
import time
from datetime import datetime
from pyfzf.pyfzf import FzfPrompt
import pytodotxt
import json
import sys
import curses
import asyncio
import re
import os.path

state_file = "state.json"

if os.path.exists(state_file):
    task_list = json.loads(open(state_file).read() )
else:
    task_list = [ {'name': 'start', 'min': 0} ]

def debug(s):
    with open("debug.txt", "a") as f:
        f.write("{}\n".format(s))

def read_todo():
    path = re.search('TODO_DIR="(.[^"]*)', open( os.path.expanduser("~/.todo.cfg"), "r").read())[1] + "/todo.txt"
    todotxt = pytodotxt.TodoTxt(path)
    todotxt.parse()

    a = []
    for task in todotxt.tasks:
        if not task.is_completed:
            a.append(task.description)
    a = a + ['journal','sketchbook','quit','sleep', 'interupt', 'chat','browsing', 'break','walk','exercise','read', 'meditate']
    fzf = FzfPrompt()
    return fzf.prompt(a)

def input_thread(stdscr):
    while True:
        stdscr.getch()

def main(stdscr):
    height, width = stdscr.getmaxyx()
    curses.curs_set(0)
    stdscr.clear()
    stdscr.nodelay(True)
    stdscr.refresh()

    start=time.time()
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)

    k = 0
    refresh=False
    first_run=True
    new_task=False
    while True:

       
        k = stdscr.getch()

        # when starting get a task
        if first_run:
            k = 10
            first_run=False

        if k != -1:
            #debug(k)
            if k == 117: #u
                if len(task_list) > 1:
                    task_list.pop() # undo last
                    refresh=True
            if k == 105: #i
                new_task='interupt'
            elif k == 98: #b
                new_task='break'
            elif k == 10: #<enter>
                try:
                    a = read_todo()[0]
                    new_task=a
                except:
                    new_task=False
            elif k == 113 or k == 27: #<q> or <esc>
                new_task = 'quit'

        if new_task:
            if new_task == "quit":
                stdscr.clear()
                stdscr.refresh()
                quit()

            start=time.time()
            task_list.append({'name': new_task, 'min': 0})
            refresh=True
            new_task=False

        if refresh or round(time.time() - start) % 60 == 0:
            curses.update_lines_cols()
            height, width = stdscr.getmaxyx()
            stdscr.clear()
            stdscr.refresh()
            refresh=False
            
            task_list[-1]['min'] = round((time.time() - start)/60)

            # update the history
            for idx, x in enumerate(reversed(task_list[0:-1])):
                if idx > height-4:
                    break
                #debug("{},{},{}".format(idx,x,height-idx))
                stdscr.addstr(height-idx-3,0, "{} : {}min".format(x['name'], x['min']), curses.color_pair(2))

            # update current
            # TODO make this the default time in the task
            if task_list[-1]['min'] > 20:
                c = 3
            else:
                c = 1

            # current task
            stdscr.addstr(height-2,0, "{} : {}min".format(task_list[-1]['name'], task_list[-1]['min']), curses.color_pair(c) | curses.A_BOLD )
    
            stdscr.refresh()
            with open(state_file , "w") as f:
                f.write(json.dumps(task_list ,indent=2))
 
        time.sleep(.1)

curses.wrapper(main)

