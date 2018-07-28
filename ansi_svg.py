#!/usr/bin/python

import re

def rgb(r,g,b): return "#%02x%02x%02x"%(r,g,b)

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


class AnsiSvg(object):
    head="""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- Created with Inkscape (http://www.inkscape.org/) -->

<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   width="210mm"
   height="297mm"
   viewBox="0 0 744.09448819 1052.3622047"
   id="svg2"
   version="1.1"
   inkscape:version="0.91 r13725"
   sodipodi:docname="two_lines.svg">
  <defs
     id="defs4" />
  <sodipodi:namedview
     id="base"
     pagecolor="#ffffff"
     bordercolor="#666666"
     borderopacity="1.0"
     inkscape:pageopacity="0.0"
     inkscape:pageshadow="2"
     inkscape:zoom="0.87327348"
     inkscape:cx="376.62771"
     inkscape:cy="526.1811"
     inkscape:document-units="px"
     inkscape:current-layer="layer1"
     showgrid="false"
     inkscape:window-width="1851"
     inkscape:window-height="1056"
     inkscape:window-x="1989"
     inkscape:window-y="24"
     inkscape:window-maximized="1" />
  <metadata
     id="metadata7">
    <rdf:RDF>
      <cc:Work
         rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type
           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
        <dc:title />
      </cc:Work>
    </rdf:RDF>
  </metadata>
  <g
     inkscape:label="Layer 1"
     inkscape:groupmode="layer"
     id="layer1">
    <flowRoot
       xml:space="preserve"
       id="flowRoot4136"
       style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-size:12.5px;line-height:125%;font-family:Helvetica;-inkscape-font-specification:'Helvetica Bold';text-align:start;letter-spacing:0px;word-spacing:0px;text-anchor:start;fill:#000000;fill-opacity:1;stroke:none;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1"><flowRegion
         id="flowRegion4138"><rect
           id="rect4140"
           width="8in"
           height="1024in"
           x="1in"
           y="1in" /></flowRegion>"""
    line = """<flowPara
         id="%s"
         style="-inkscape-font-specification:'Courier Bold';font-family:Courier;font-weight:bold;font-style:normal;font-stretch:normal;font-variant:normal">%s</flowPara>"""

    color="""<flowSpan
   style="fill:#008000"
   id="flowSpan4138">asdfa</flowSpan>  asdf"""

    tail="""</flowRoot>  </g>
</svg>
"""

    def interp_ansi(self, line):
        ret = ''

        # Look for 'm' command
        parse=re.split(r'\x1b\[([0-9;]*)m',line)

        while parse:
            ret += parse.pop(0)
            if not parse: break
            csr = parse.pop(0)
            if not csr:
                args = []
            else:
                args = [int(a) for a in csr.split(';') if a]

            if len(args)==2:
                intensity, color = args
            elif len(args)==1:
                intensity, color = [0]+args
            else:
                intensity, color = 0,0

            if self.ansicolor != (intensity,color):
                if self.ansicolor != (0,0):
                    ret += '</flowSpan>'

                if (intensity,color) != (0,0):
                    try:
                        ret += '<flowSpan style="fill:%s">'%colortab[(intensity,color)]
                    except KeyError:
                        ret += '<flowSpan id="unknown_%s">'%repr((intensity,color))

                self.ansicolor = intensity,color

        if self.ansicolor != (0,0):
            ret += '</flowSpan>'

        self.ansicolor = (0,0)

        return ret

    def __init__(self, outfd):
        self.outfd = outfd
        self.idct = 0
        self._print(self.head)
        self.ansicolor = (0,0)

    def __call__(self, line):
        id_ = "line_%d"%self.idct

        line = self.interp_ansi(line)
        self.idct += 1
        self._print(self.line%(id_,line))

    def __enter__(self, *args):
        return self

    def __exit__(self, *args):
        self._print(self.tail)

    def _print(self, string):
        self.outfd.write(string + '\n')

import sys

if __name__=="__main__":
    with AnsiSvg(sys.stdout) as as_:
        for line in sys.stdin:
            as_(line)
