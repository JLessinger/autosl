#!/usr/bin/env python

import subprocess as sp
import logging, os, signal, sys, time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

def sl():
    sp.Popen(['clear']).wait()
    sl_proc = sp.Popen(['script', '-q', '/dev/null', 'git', '--no-pager', 'sl'], stdout=sp.PIPE)
    tail_proc = sp.Popen(['tail', '-r'], stdin=sl_proc.stdout, stdout=sys.stdout)
    sl_proc.wait()
    tail_proc.wait()
    code = 0
    if sl_proc.returncode != 0 or tail_proc.returncode != 0:
        code = -1
    return code

class SLEventHandler(LoggingEventHandler):
    def __init__(self):
        super(SLEventHandler, self).__init__()
        self.last_sec = None

    def dispatch(self, event):
        while True:
            sec = datetime.now().second
            if sec == self.last_sec:
                return
            rc = sl()
            if rc == 0:
                self.last_sec = sec
                return

def watch():
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    sl_handler = SLEventHandler()
    observer = Observer()
    observer.schedule(sl_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    watch()
