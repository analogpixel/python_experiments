#!/usr/bin/env python


# https://blessed.readthedocs.io/

from __future__ import division, print_function

import os
import time
from datetime import datetime
from pyfzf.pyfzf import FzfPrompt
import pytodotxt
import json
import sys
import re
import os.path
from blessed import Terminal
from functools import partial

term = Terminal()
echo = partial(print, end='', flush=True)

state_file = "state.json"

if os.path.exists(state_file):
    task_list = json.loads(open(state_file).read() )
else:
    task_list = [ {'name': 'start', 'min': 0} ]

def readline(term, init, width=120):
    """A rudimentary readline implementation."""
    echo( term.move_xy(0, term.height-1), term.on_red, term.clear_eol)
    #echo( term.move_xy(1, term.height-1) + init )
    echo ( term.on_red, init)
    text = init
    while True:
        inp = term.inkey()
        if inp.code == term.KEY_ENTER:
            break
        elif inp.code == term.KEY_ESCAPE or inp == chr(3):
            text = None
            break
        elif not inp.is_sequence and len(text) < width:
            text += inp
            echo(inp)
        elif inp.code in (term.KEY_BACKSPACE, term.KEY_DELETE):
            text = text[:-1]
            # https://utcc.utoronto.ca/~cks/space/blog/unix/HowUnixBackspaces
            #
            # "When you hit backspace, the kernel tty line discipline rubs out
            # your previous character by printing (in the simple case)
            # Ctrl-H, a space, and then another Ctrl-H."
            echo(u'\b \b')
    return text

def debug(s):
    with open("debug.txt", "a") as f:
        f.write("{}\n".format(s))

def read_focus():
    fzf = FzfPrompt()
    return fzf.prompt(["math","art","music","devops"])

def read_todo():
    path = re.search('TODO_DIR="(.[^"]*)', open( os.path.expanduser("~/.todo.cfg"), "r").read())[1] + "/todo.txt"
    todotxt = pytodotxt.TodoTxt(path)
    todotxt.parse()

    a = []
    for task in todotxt.tasks:
        if not task.is_completed:
            a.append(task.description)
    a = a + ['journal','sketchbook','quit','sleep', 'interupt', 'chat','browsing', 'unscheduled','walk','exercise','read', 'meditate', 'Listen Music','Daily Pages', 'Planning', 'Khan', 'cooking']
    fzf = FzfPrompt()
    return fzf.prompt(a)[0]

def draw_tasklist(tasklist,index):

    bw = lambda x: term.on_blue(term.bright_white(x))
    gw = lambda x: term.on_green(term.bright_white(x))

    i = len(tasklist)-1
    h = term.height-2
    echo( term.on_blue(term.clear) )
    while i > 0 and h > 2: 
        if i == index:
            echo( term.move_xy(1,h) + bw("*"))

        if tasklist[i]['name'] == "---":
            echo( term.move_xy(2,h) + bw(term.bright_white( "-----------" )))
        else:
            echo( term.move_xy(2,h) + bw(term.bright_white( "{}:{}".format( tasklist[i]['name'], tasklist[i]['min']) )))

        h = h -1
        i = i -1

    # update the timer
    #echo( term.move_xy(1, term.height-1), bw(term.bright_white( str(tasklist[-1]['min']) + " min" )))
    echo( term.move_xy(0, term.height-1), term.on_green, term.clear_eol)
    echo( gw(term.bright_white( str(tasklist[-1]['min']) + " min" )))

def main():
    echo(term.move_yx(1, 1))

    inp = None
    index = -1
    updated=False
    with term.hidden_cursor(), term.cbreak(), term.location():
        while inp not in (u'q', u'Q'):
            # https://blessed.readthedocs.io/en/latest/keyboard.html#keycodes
            inp = term.inkey(timeout=0.04)
            if inp.code == term.KEY_ENTER or index == -1:
                task_list.append( {'name': read_todo(), 'min': 0 } )
                index = len(task_list) -1
                start = time.time()
                updated = True
            if inp in (u'd', u'D'):
                del task_list[index]
                if index > len(task_list) -1 :
                    index = len(task_list) -1
                start = time.time() - task_list[-1]['min'] * 60
                updated = True
            if inp.code == term.KEY_UP:
                index = index - 1
                updated = True
            if inp.code == term.KEY_DOWN:
                index = index + 1
                if index > len(task_list)-1:
                    index = len(task_list)-1
                updated = True
            if inp in (u'u', u'U'):
                task_list.append( {'name': 'unscheduled', 'min': 0} )
                start = time.time()
                updated=True
                index = len(task_list) -1
            if inp in (u'i', u'I'):
                task_list.append( {'name': 'interupt', 'min': 0} )
                start = time.time()
                updated=True
                index = len(task_list) -1
            if inp in (u'e', u'E'):
                text = readline(term, task_list[index]['name'] + "|" + str(task_list[index]['min']) )
                (n,m) = text.split('|')
                task_list[index]['name'] = n
                task_list[index]['min'] = int(m)
                updated=True
                if index == len(task_list)-1:
                    start = time.time() - task_list[-1]['min'] * 60

            if inp in (u's', u'S'):
                task_list.insert( index+1, {'name': '---', 'min': 0} )
                updated=True

            if round(time.time() - start) % 60 == 0:
                task_list[-1]['min'] = round((time.time() - start)/60)
                updated = True

            # Redraw the screen
            if updated:
                debug("Updated called")
                draw_tasklist(task_list, index)
                time.sleep(.1)
                updated = False
             
                with open(state_file , "w") as f:
                    f.write(json.dumps(task_list ,indent=2))

           

main()
