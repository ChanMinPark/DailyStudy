#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *


global which_task
which_task = 0

global is_lock
is_lock = False

def setTask(wtask):
    global which_task
    which_task = wtask
    
def getTask():
    global which_task
    return which_task

def setLock(lock):
    global is_lock
    is_lock = lock
    
def getLock():
    global is_lock
    return is_lock
