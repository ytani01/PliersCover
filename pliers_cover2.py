import inkex
import simplestyle
"""
$ sudo apt install python-lxml
"""
inkex.localize()
# inkex.errormsg(_("Hello, world."))


class PlierCover(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option("--w1", action="store", type="float",
                                     dest="w1", help="")
        self.OptionParser.add_option("--w2", action="store", type="float",
                                     dest="w2", help="")
        self.OptionParser.add_option("--h1", action="store", type="float",
                                     dest="h1", help="")
        self.OptionParser.add_option("--h2", action="store", type="float",
                                     dest="h2", help="")

        self.OptionParser.add_option("--bw", action="store", type="float",
                                     dest="bw", help="")
        self.OptionParser.add_option("--bl", action="store", type="float",
                                     dest="bl", help="")
        self.OptionParser.add_option("--dia1", action="store", type="float",
                                     dest="dia1", help="")
        self.OptionParser.add_option("--dia2", action="store", type="float",
                                     dest="dia2", help="")

        self.OptionParser.add_option("--d1", action="store", type="float",
                                     dest="d1", help="")
        self.OptionParser.add_option("--d2", action="store", type="float",
                                     dest="d2", help="")
        self.OptionParser.add_option("--dia3", action="store", type="float",
                                     dest="dia3", help="")

    def effect(self):
        """
        main
        """
        # parameters
        offset_x = 20
        offset_y = 20

        w1 = self.options.w1
        w2 = self.options.w2
        h1 = self.options.h1
        h2 = self.options.h2

        bw = self.options.bw
        bl = self.options.bl
        dia1 = self.options.dia1
        dia2 = self.options.dia2

        d1 = self.options.d1
        d2 = self.options.d2
        dia3 = self.options.dia3

        #
        # error check
        #
        if w1 >= w2:
            msg = "Error: w1(%d) >= w2(%d) !" % (w1, w2)
            inkex.errormsg(_(msg))
            return

        if dia1 >= bw:
            msg = "Error: dia1(%d) >= bw(%d) !" % (dia1, bw)
            inkex.errormsg(_(msg))
            return

        self.draw_pattern1((offset_x, offset_y),
                           w1, w2, h1, h2, bw, bl, dia1)

        return

    def mkstyle(self, color='#000000', stroke_width=0.2):
        style = {
            'stroke': color,
            'stroke-width': str(stroke_width),
            'fill': 'none'
        }
        return style

    def draw_pattern1(self, offset, w1, w2, h1, h2, bw, bl, dia1,
                      color='#000000',
                      stroke_width=0.2,
                      parent=None):

        self.draw_pattern1_base(offset, w1, w2, h1, h2, bw, bl,
                                color, stroke_width, parent)
        self.draw_pattern1_button_hole(offset, w1, w2, h1, h2, bw, bl, dia1,
                                       color, stroke_width, parent)

    def draw_pattern1_base(self, offset, w1, w2, h1, h2, bw, bl,
                           color='#000000',
                           stroke_width=0.2,
                           parent=None):

        svg_d = self.mkpath_pattern1_base(offset, w1, w2, h1, h2, bw, bl)
        return self.draw_path(svg_d,
                              color=color,
                              stroke_width=stroke_width,
                              parent=parent)

    def draw_path(self,
                  svg_d='M 0,0 L 100,0 L 100,100 Z',
                  color='#000000',
                  stroke_width=0.2,
                  parent=None):
        if parent is None:
            parent = self.current_layer

        style = self.mkstyle(color, stroke_width)

        attr = {
            'style': simplestyle.formatStyle(style),
            'd': svg_d
        }
        return inkex.etree.SubElement(parent,
                                      inkex.addNS('path', 'svg'),
                                      attr)

    def mkpath_pattern1_base(self, offset, w1, w2, h1, h2, bw, bl):
        p1 = 0.75

        (x0, y0) = offset
        (x, y) = (x0, y0)

        dw1 = (w2 - w1) / 2
        dw2 = (w2 - bw) / 2

        x += dw1
        d = 'M %f,%f' % (x, y)

        x += w1
        d += ' L %f,%f' % (x, y)

        x = x0 + w2
        y += h1
        d += ' L %f,%f' % (x, y)

        y += h2
        d += ' L %f,%f' % (x, y)

        x -= dw2
        d += ' L %f,%f' % (x, y)

        y = y0 + h1 + h2 + bl - bw / 2
        d += ' L %f,%f' % (x, y)

        x1 = x
        y1 = y + bw * p1
        x = x0 + dw2
        d += ' C %f,%f %f,%f %f,%f' % (x1, y1, x, y1, x, y)

        y = y0 + h1 + h2
        d += ' L %f,%f' % (x, y)

        x = x0
        d += ' L %f,%f' % (x, y)

        y = y0 + h1
        d += ' L %f,%f' % (x, y)

        d += ' Z'
        return d

    def draw_pattern1_button_hole(self, offset, w1, w2, h1, h2,
                                  bw, bl, dia1,
                                  color='#000000',
                                  stroke_width=0.2,
                                  parent=None):
        if parent is None:
            parent = self.current_layer

        (x0, y0) = offset
        (x, y) = (x0, y0)

        x += w2 / 2
        y += h1 + h2 + bl - bw / 2
        r = dia1 / 2

        style = self.mkstyle(color, stroke_width)

        attr = {
            'style': simplestyle.formatStyle(style),
            'r': str(r),
            'cx': str(x),
            'cy': str(y)
        }
        return inkex.etree.SubElement(parent,
                                      inkex.addNS('circle', 'svg'),
                                      attr)

    #####
    def draw_pattern2(self, style, parent,
                      x, y, w1, w2, h1, h2,
                      cx, cy, r, d1):

        # pattern
        d_pattern2 = self.mkpath_pattern2(x, y, w1, w2, h1, h2)
        attribs_pattern2 = {
            'style': simplestyle.formatStyle(style),
            'd': d_pattern2
        }
        inkex.etree.SubElement(parent,
                               inkex.addNS('path', 'svg'),
                               attribs_pattern2)

        # hole
        attribs_hole2 = {
            'style': simplestyle.formatStyle(style),
            'r': str('%.1f' % (r / 2)),
            'cx': str(cx),
            'cy': str(cy)
        }
        inkex.etree.SubElement(parent,
                               inkex.addNS('circle', 'svg'),
                               attribs_hole2)

    def mkpath_pattern2(self, x, y, w1, w2, h1, h2):
        d = 'M %d,%d' % (x, y)
        d += ' h %d' % (w1)
        d += ' l %.1f,%d' % ((w2 - w1) / 2, h1)
        d += ' v %d' % (h2)
        d += ' h %.1f' % (-w2)
        d += ' v %d' % (-h2)
        d += ' Z'

        return d


if __name__ == '__main__':
    e = PlierCover()
    e.affect()
