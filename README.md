`ansi_svg.py`
------------

Convert text file with embedded ANSI color escape sequences to SVG.

I needed to import some colored terminal dumps into an SVG document and I couldn't find anything at the appropriate level of abstraction:

- convert ANSI colors to SVG colors
- leave text as editable, flowable text

So I made this script.

It takes ANSI text on stdin and writes SVG on stdout.

e.g.,

`ls --color | ./ansi_svg.py > listing.svg`

The SVG file loads in Inkscape. That's all the testing I've done.

Only foreground color is supported.  Other ANSI escape sequences are ignored.

Parsing is just a stupid regex.

`ansi_enscript.py`
------------------

This script converts ANSI color escape sequences to enscript escape sequences.

This is another way to get ANSI-colored text to a printable format.

Use the -e option to enscript to ask it to honor escape codes, e.g:

`ls --color | ./ansi_enscript.py | enscript -e -f CourierBold10 -o ls.pdf`
