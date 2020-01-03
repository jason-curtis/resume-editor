resume editor by Jason Curtis, Aug. 2011.

## how to run:
run `python -m simpleHTTPServer` and then open `http://localhost:8000/resumeEditor.html#` in a Web browser. 
If the resume shows up, you're golden.

## usage:
Drag things around to move them, double-click to edit them. CSS editing not currently supported -- I use devtools for live edits and then copy stuff to file.
Click a grey plus sign (+) to create a new sub-element from your template, or a minus (-) to delete an element. If you change your mind, you can get back all deleted elements by hitting 'unelete all' in the menu at the top.

## printing:
ctrl+p just like a regular webpage. I generally print to PDF.

## saving:
does not work automatically in the current iteration, though that should be a relatively easy fix. You have to 'view source' and paste the shown source into a file. The "X" to close the 'view source' window may not be visible, but it is there where you would expect it to be :p.

Also, try tictactoe.py in an interactive terminal. I wrote it over a semester ago, but it's fun -- it uses a tree search with alpha-beta pruning to kick your butt at tic-tac-toe if you give it a chance. It currently spits out a bunch of stats on how each tree search went, so you can have some fun figuring out what it's talking about :).

## License:
[Creative Commons Attribution-ShareAlike 4.0](https://creativecommons.org/licenses/by-sa/4.0/legalcode)