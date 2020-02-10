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
        self.OptionParser.add_option("--bf", action="store", type="float",
                                     dest="bf", help="")

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
        bf = self.options.bf

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

        #
        # draw
        #
        base_points = self.mkpoints_pattern1_base(w1, w2, h1, h2, bw, bl)
        self.draw_pattern1((offset_x, offset_y), base_points, bw*bf, dia1)

        new_points = self.zoom_points(base_points, 0.9)
        self.draw_pattern1((offset_x + 100, offset_y), new_points, bw*bf, dia1)

        return

    def mkstyle(self, color='#000000', stroke_width=0.2):
        style = {
            'stroke': color,
            'stroke-width': str(stroke_width),
            'fill': 'none'
        }
        return style

    def draw_pattern1(self, offset, base_points, bw_bf, dia1,
                      color='#000000',
                      stroke_width=0.2,
                      parent=None):

        self.draw_pattern1_base(offset, base_points, bw_bf,
                                color, stroke_width, parent)
        self.draw_pattern1_button_hole(offset, base_points, dia1,
                                       color, stroke_width, parent)

    def draw_pattern1_base(self, offset, base_points, bw_bf,
                           color='#000000',
                           stroke_width=0.2,
                           parent=None):

        svg_d = self.mkpath_pattern1_base(offset, base_points, bw_bf)
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

    def mkpoints_pattern1_base(self, w1, w2, h1, h2, bw, bl):
        points = []

        (x0, y0) = (0, 0)
        (x, y) = (x0, y0)

        dw1 = (w2 - w1) / 2
        dw2 = (w2 - bw) / 2

        x += dw1
        points.append((x, y))

        x += w1
        points.append((x, y))

        x = x0 + w2
        y += h1
        points.append((x, y))

        y += h2
        points.append((x, y))

        x -= dw2
        points.append((x, y))

        y += bl - bw / 2
        points.append((x, y))

        x = x0 + dw2
        points.append((x, y))

        y = y0 + h1 + h2
        points.append((x, y))

        x = x0
        points.append((x, y))

        y = y0 + h1
        points.append((x, y))

        return points

    def zoom_points(self, points, zf=1.0):
        new_points = []

        for (x, y) in points:
            (x2, y2) = (x * zf, y * zf)
            new_points.append((x2, y2))

        return new_points

    def mkpath_pattern1_base(self, offset, base_points, bw_bf):

        (x0, y0) = offset

        (x, y) = base_points[0]
        d = 'M %f,%f' % (x + x0, y + y0)

        (x, y) = base_points[1]
        d += ' L %f,%f' % (x + x0, y + y0)

        (x, y) = base_points[2]
        d += ' L %f,%f' % (x + x0, y + y0)

        (x, y) = base_points[3]
        d += ' L %f,%f' % (x + x0, y + y0)

        (x, y) = base_points[4]
        d += ' L %f,%f' % (x + x0, y + y0)

        (x, y) = base_points[5]
        d += ' L %f,%f' % (x + x0, y + y0)

        x1 = x
        y1 = y + bw_bf
        (x, y) = base_points[6]
        d += ' C %f,%f %f,%f %f,%f' % (x1 + x0, y1 + y0,
                                       x + x0, y1 + y0,
                                       x + x0, y + y0)

        (x, y) = base_points[7]
        d += ' L %f,%f' % (x + x0, y + y0)

        (x, y) = base_points[8]
        d += ' L %f,%f' % (x + x0, y + y0)

        (x, y) = base_points[9]
        d += ' L %f,%f' % (x + x0, y + y0)

        d += ' Z'
        return d

    def draw_pattern1_button_hole(self, offset, base_points, dia1,
                                  color='#000000',
                                  stroke_width=0.2,
                                  parent=None):
        if parent is None:
            parent = self.current_layer

        (x0, y0) = offset
        (x, y) = (x0, y0)

        x = base_points[2][0] / 2 + x0
        y = base_points[5][1] + y0
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


if __name__ == '__main__':
    e = PlierCover()
    e.affect()
