#!/usr/bin/env python

import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

import subprocess as sp

def sl():
    sp.Popen(['clear'])
    child = sp.Popen(['git', 'sl'], stdout=sp.PIPE)
    streamdata = child.communicate()[0]
    return streamdata, child.returncode

class SLEventHandler(LoggingEventHandler):
    def dispatch(self, event):
        print 'go'
        while True:
            out, rc = sl()
            if rc == 0:
                print out
                return

def watch():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
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
