#!/usr/bin/python

import re
import sys

def fg_rgb(r,g,b): return "\0color{%f %f %f}"%(r/255.,g/255.,b/255.)
def bg_rgb(r,g,b): return "\0bgcolor{%f %f %f}"%(r/255.,g/255.,b/255.)

# These are PuTTY colors.
# From https://en.wikipedia.org/wiki/ANSI_escape_code#Colors

br_on = 255
br_off = 85

boldtab = {
    30:fg_rgb( br_off, br_off, br_off), # black
    31:fg_rgb(  br_on, br_off, br_off), # red
    32:fg_rgb( br_off,  br_on, br_off), # green
    33:fg_rgb(  br_on,  br_on, br_off), # yellow
    34:fg_rgb( br_off, br_off,  br_on), # blue
    35:fg_rgb(  br_on, br_off,  br_on), # magenta
    36:fg_rgb( br_off,  br_on,  br_on), # cyan
    37:fg_rgb(  br_on,  br_on,  br_on), # white

    40:bg_rgb( br_off, br_off, br_off), # black
    41:bg_rgb(  br_on, br_off, br_off), # red
    42:bg_rgb( br_off,  br_on, br_off), # green
    43:bg_rgb(  br_on,  br_on, br_off), # yellow
    44:bg_rgb( br_off, br_off,  br_on), # blue
    45:bg_rgb(  br_on, br_off,  br_on), # magenta
    46:bg_rgb( br_off,  br_on,  br_on), # cyan
    47:bg_rgb(  br_on,  br_on,  br_on), # white
}

norm_on = 187
norm_off = 0
normtab = {
    30:fg_rgb(norm_off, norm_off, norm_off), # black
    31:fg_rgb( norm_on, norm_off, norm_off), # red
    32:fg_rgb(norm_off,  norm_on, norm_off), # green
    33:fg_rgb( norm_on,  norm_on, norm_off), # yellow
    34:fg_rgb(norm_off, norm_off,  norm_on), # blue
    35:fg_rgb( norm_on, norm_off,  norm_on), # magenta
    36:fg_rgb(norm_off,  norm_on,  norm_on), # cyan
    37:fg_rgb( norm_on,  norm_on,  norm_on), # white

    40:bg_rgb(norm_off, norm_off, norm_off), # black
    41:bg_rgb( norm_on, norm_off, norm_off), # red
    42:bg_rgb(norm_off,  norm_on, norm_off), # green
    43:bg_rgb( norm_on,  norm_on, norm_off), # yellow
    44:bg_rgb(norm_off, norm_off,  norm_on), # blue
    45:bg_rgb( norm_on, norm_off,  norm_on), # magenta
    46:bg_rgb(norm_off,  norm_on,  norm_on), # cyan
    47:bg_rgb( norm_on,  norm_on,  norm_on), # white
}

class AnsiEnscript(object):

    def interp_ansi(self, line):
        ret = ''

        # Look for 'm' command
        parse=re.split(r'\x1b\[([0-9;]*)([a-zA-Z])',line)

        while parse:
            colortab = normtab

            ret += parse.pop(0)
            if not parse: break

            args = parse.pop(0)
            code = parse.pop(0)

            if code=='m':
                args = [int(a) for a in args.split(';') if a]

                if not args:
                    args = [0]

                if args==[0]:
                    ret += '\0color{default}'
                    ret += '\0bgcolor{default}'

                else:
                    if 0 in args:
                        colortab = normtab
                    elif 1 in args:
                        colortab = boldtab

                    for arg in args:
                        try:
                            ret += colortab[arg]
                        except KeyError:
                            pass

        return ret

    def __init__(self, outfd):
        self.outfd = outfd

    def __call__(self, line):
        line = self.interp_ansi(line)
        self.outfd.write(line)

    def __enter__(self, *args):
        return self

    def __exit__(self, *args):
        pass

if __name__=="__main__":
    with AnsiEnscript(sys.stdout) as ae:
        for line in sys.stdin:
            ae(line)
