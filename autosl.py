#!/usr/bin/env python

import subprocess as sp
import logging, os, signal, sys, time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

MAX_RETRIES = 3

def sl(vc):
    sp.Popen(['clear']).wait()
    sl_proc = sp.Popen(['script', '-q', '/dev/null', vc, '--no-pager', 'sl'], stdout=sp.PIPE)
    tail_proc = sp.Popen(['tail', '-r'], stdin=sl_proc.stdout, stdout=sys.stdout)
    sl_proc.wait()
    tail_proc.wait()
    code = 0
    if sl_proc.returncode != 0 or tail_proc.returncode != 0:
        code = -1
    return code

class SLEventHandler(LoggingEventHandler):
    def __init__(self, vc):
        super(SLEventHandler, self).__init__()
        self.last_sec = None
        self.vc = vc

    def dispatch(self, event):
        for i in xrange(MAX_RETRIES):
            sec = datetime.now().second
            if sec == self.last_sec:
                return
            rc = sl(vc)
            if rc == 0:
                self.last_sec = sec
                return

def watch(vc):
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    sl_handler = SLEventHandler(vc)
    observer = Observer()
    observer.schedule(sl_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def get_vc():
    vc_map = {
        'git' : os.path.isdir('.git'),
        'hg' : os.path.isdir('.hg'),
        'svn' : os.path.isdir('.svn')
    }
    existing = [v for v in vc_map if vc_map[v]]
    if len(existing) == 1:
        return existing[0]
    else:
        return raw_input('what is your version control executable?\n').strip()

if __name__ == "__main__":
    vc = get_vc()
    watch(vc)
