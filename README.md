automatically run smart log on any file change
run ./autosl in its own terminal in your repo, and it will automatically run sl

TODO:
* make sl print forwards (lines are reversed because of paging problem)
** if we run sl with pager (less) then we have to figure out how to quit it (send "q") before rerunning
** if we run sl --no-pager, then the output is hard to read because you will see the oldest commits on screen (at the bottom of the output)
** temporary solution is to reverse the lines of the output, so that the newest is at the bottom.
** support git/hg