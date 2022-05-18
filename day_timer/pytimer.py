#!/usr/bin/env python

# https://github.com/Textualize/textual

import _thread
import os
import time
from rich import print
from datetime import datetime
from pyfzf.pyfzf import FzfPrompt
import pytodotxt
import json
import sys

print('\33]0;pyTimer\a', end='')

state_file = "state.json"

if os.path.exists(state_file):
    task_list = json.loads(open(state_file).read() )
else:
    task_list = [ {'name': 'start', 'min': 0} ]

def read_todo():
    path="/Users/mattpoepping/pcloud/reference/cli/todo/todo.txt"
    todotxt = pytodotxt.TodoTxt(path)
    todotxt.parse()

    a = ['quit','interupt', 'chat','internet', 'bathroom','walk','exercise','read']
    for task in todotxt.tasks:
        if not task.is_completed:
            a.append(task.description)
    fzf = FzfPrompt()
    return fzf.prompt(a)

def input_thread(a_list):
    input()             # use input() in Python3
    a_list.append(True)

def refresh():
    os.system('clear||cls')
    for a in task_list[0:-1]:
        print("[bold magenta]{} : {}min[/bold magenta]".format(a['name'], a['min'] ) )

    print("[bold white]* {} : {}min[/bold white]".format( task_list[-1]['name'], task_list[-1]['min']) )

a_list = []
a = read_todo()[0]
if a == "quit":
    quit()
start=time.time()
task_list.append({'name': a, 'min': 0})
while True:

    # wait for input
    a_list = []
    _thread.start_new_thread(input_thread, (a_list,))
    refresh()

    while not a_list:
        # refrest every 1 minute
        if round(time.time() - start) % 60 == 0:
            task_list[-1]['min'] = round((time.time() - start)/60)
            refresh()
        time.sleep(0.5)


    with open(state_file , "w") as f:
        f.write(json.dumps(task_list))

    a = read_todo()[0]
    if a == "quit":
        quit()
    start=time.time()
    task_list.append({'name': a, 'min': 0})
