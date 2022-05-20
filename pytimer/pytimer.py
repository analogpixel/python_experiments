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

state_file = "state.json"

if os.path.exists(state_file):
    task_list = json.loads(open(state_file).read() )
else:
    task_list = [ {'name': 'start', 'min': 0} ]

def debug(s):
    with open("debug.txt", "a") as f:
        f.write("{}\n".format(s))

def read_todo():
    path="/Users/mattpoepping/pcloud/reference/cli/todo/todo.txt"
    todotxt = pytodotxt.TodoTxt(path)
    todotxt.parse()

    a = ['quit','sleep', 'interupt', 'chat','browsing', 'break','walk','exercise','read', 'meditate']
    for task in todotxt.tasks:
        if not task.is_completed:
            a.append(task.description)
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

    k = 0
    start=time.time()
    refresh=False

    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)

    while k != 27:

        if refresh or round(time.time() - start) % 60 == 0:
            stdscr.clear()
            stdscr.refresh()
            refresh=False
            
            task_list[-1]['min'] = round((time.time() - start)/60)

            # update the history
            for idx, x in enumerate(reversed(task_list[0:-1])):
                if idx > height-2:
                    break
                #debug("{},{},{}".format(idx,x,height-idx))
                stdscr.addstr(height-idx-2,0, "{} : {}min".format(x['name'], x['min']), curses.color_pair(2))

            # update current
            stdscr.addstr(height-1,0, "{} : {}min".format(task_list[-1]['name'], task_list[-1]['min']), curses.color_pair(1))
    
            with open(state_file , "w") as f:
                f.write(json.dumps(task_list))
        
        k = stdscr.getch()
        if k != -1:
            debug(k)
            if k == 105: #i
                task_list.append({'name': 'interupt', 'min': 0})
                refresh=True
            if k == 10:
                a = read_todo()[0]
                if a == "quit":
                    quit()
                start=time.time()
                task_list.append({'name': a, 'min': 0})
                refresh=True

        time.sleep(.1)

curses.wrapper(main)

