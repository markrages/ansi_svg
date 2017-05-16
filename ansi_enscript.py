#!/usr/bin/python2

import re

def rgb(r,g,b): return "\0color{%f %f %f}"%(r,g,b)

# These are PuTTY colors.
# From https://en.wikipedia.org/wiki/ANSI_escape_code#Colors

br_on = 255
br_off = 85
norm_on = 187

colortab = {(0,30):rgb( br_off, br_off, br_off), # black
            (0,31):rgb(  br_on, br_off, br_off), # red
            (0,32):rgb( br_off,  br_on, br_off), # green
            (0,33):rgb(  br_on,  br_on, br_off), # yellow
            (0,34):rgb( br_off, br_off,  br_on), # blue
            (0,35):rgb(  br_on, br_off,  br_on), # magenta
            (0,36):rgb( br_off,  br_on,  br_on), # cyan
            (0,37):rgb(  br_on,  br_on,  br_on), # white
            (1,30):rgb(      0,      0,      0), # black
            (1,31):rgb(norm_on,      0,      0), # red
            (1,32):rgb(      0,norm_on,      0), # green
            (1,33):rgb(norm_on,norm_on,      0), # yellow
            (1,34):rgb(      0,      0,norm_on), # blue
            (1,35):rgb(norm_on,      0,norm_on), # magenta
            (1,36):rgb(      0,norm_on,norm_on), # cyan
            (1,37):rgb(norm_on,norm_on,norm_on)  # white
            }

class AnsiEnscript(object):

    def interp_ansi(self, line):
        ret = ''

        # Look for 'm' command
        parse=re.split(r'\x1b\[([0-9]*);?([0-9]+)?m',line)

        while parse:
            ret += parse.pop(0)
            if not parse: break
            intensity = parse.pop(0)
            color = parse.pop(0)

            if not intensity:
                intensity = 0
            else:
                intensity = int(intensity)

            if not color:
                color = 0
            else:
                color = int(color)

            if (intensity,color) != (0,0):
                ret += colortab[(intensity,color)]
            else:
                ret += '\0color{default}'

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

import sys

if __name__=="__main__":
    with AnsiEnscript(sys.stdout) as ae:
        for line in sys.stdin:
            ae(line)
