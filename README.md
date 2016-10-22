automatically run smart log on any file change

**** tested on macOS Sierra with Python 2.7.12 in iTerm 3.0.10

run ./autosl in its own terminal in your repo, and it will automatically run sl

HOW TO USE:

1. Open your repo in window/pane (A)
2. Open a new window (B)
3. Run autosl (no arguments) in (B)
4. Interact with your repo as usual in (A)

TODO:

make sl print forwards (lines are reversed because of paging problem)
* if we run sl with pager (less) then we have to figure out how to quit it (send "q") before rerunning
* if we run sl --no-pager, then the output is hard to read because you will see the oldest commits on screen (at the bottom of the output)
* temporary solution is to reverse the lines of the output, so that the newest is at the bottom.
