import inkex
import simplestyle
import math
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
        points_base = self.mkpoints_pattern1_base(w1, w2, h1, h2, bw, bl)
        points_needle = self.mkpoints_needle(points_base,
                                             w1, w2, h1, d1, d2)

        self.draw_pattern1((offset_x, offset_y), points_base, bw*bf, dia1)
        self.draw_needle((offset_x, offset_y), points_needle, d2, dia3)

        offset_x += points_base[4][0] + 10
        self.draw_pattern2((offset_x, offset_y), points_base, bw*bf, dia2)
        self.draw_needle((offset_x, offset_y), points_needle, d2, dia3)

        '''
        offset_x += points_base[2][0] + 10
        new_points = self.zoom_points(points_base, 0.9)
        self.draw_pattern1((offset_x, offset_y), new_points, bw*bf, dia1)
        '''

        return

    def mkpoints_pattern1_base(self, w1, w2, h1, h2, bw, bl):
        points = []

        (x0, y0) = (0, 0)
        (x, y) = (x0, y0)

        dw1 = (w2 - w1) / 2
        dw2 = (w2 - bw) / 2

        y = y0 + h1 + h2
        points.append((x, y))

        y = y0 + h1
        points.append((x, y))

        x += dw1
        y = y0
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

        return points

    def mkpoints_needle(self, points_base, w1, w2, h1, d1, d2):
        points = []

        b = (w2 - w1) * d1 / (2 * h1)
        a = math.sqrt(b ** 2 + d1 ** 2) - b
        c = 2

        (x1, y1) = points_base[0]
        (x2, y2) = (x1 + d1, y1 - d2)
        points.append((x2, y2))

        (x1, y1) = points_base[1]
        (x2, y2) = (x1 + d1, y1 + c)
        points.append((x2, y2))

        (x1, y1) = points_base[2]
        (x2, y2) = (x1 + a, y1 + d1)
        points.append((x2, y2))

        (x1, y1) = points_base[3]
        (x2, y2) = (x1 - a, y1 + d1)
        points.append((x2, y2))

        (x1, y1) = points_base[4]
        (x2, y2) = (x1 - d1, y1 + c)
        points.append((x2, y2))

        (x1, y1) = points_base[5]
        (x2, y2) = (x1 - d1, y1 - d2)
        points.append((x2, y2))

        return points

    def zoom_points(self, points, zf=1.0):
        new_points = []

        for (x, y) in points:
            (x2, y2) = (x * zf, y * zf)
            new_points.append((x2, y2))

        return new_points

    def draw_obj_path(self,
                      svg_d='M 0,0 L 100,0 L 100,100 Z',
                      color='#000000',
                      stroke_width=0.2,
                      stroke_dasharray='none',
                      parent=None):
        if parent is None:
            parent = self.current_layer

        style = self.mkstyle(color=color,
                             stroke_width=stroke_width,
                             stroke_dasharray=stroke_dasharray)

        attr = {
            'style': simplestyle.formatStyle(style),
            'd': svg_d
        }
        return inkex.etree.SubElement(parent,
                                      inkex.addNS('path', 'svg'),
                                      attr)

    def draw_obj_circle(self, cx, cy, r,
                        color='#000000',
                        stroke_width=0.2,
                        stroke_dasharray='none',
                        parent=None):
        style = self.mkstyle(color=color,
                             stroke_width=stroke_width,
                             stroke_dasharray=stroke_dasharray)

        attr = {
            'style': simplestyle.formatStyle(style),
            'cx': str(cx),
            'cy': str(cy),
            'r': str(r)
        }

        return inkex.etree.SubElement(parent,
                                      inkex.addNS('circle', 'svg'),
                                      attr)

    def mkstyle(self, color='#000000', stroke_width=0.2,
                stroke_dasharray='none'):
        style = {
            'stroke': color,
            'stroke-width': str(stroke_width),
            'stroke-dasharray': str(stroke_dasharray),
            'fill': 'none'
        }
        return style

    #
    # pattern1
    #
    def draw_pattern1(self, offset, points_base, bw_bf, dia1,
                      stroke_width=0.2,
                      stroke_dasharray='none',
                      parent=None):

        self.draw_pattern1_base(offset, points_base, bw_bf,
                                color='#0000FF',
                                stroke_width=stroke_width,
                                stroke_dasharray=stroke_dasharray,
                                parent=parent)

        self.draw_pattern1_button_hole(offset, points_base, dia1,
                                       color='#FF0000',
                                       stroke_width=stroke_width,
                                       stroke_dasharray=stroke_dasharray,
                                       parent=parent)

    def draw_pattern1_base(self, offset, points_base, bw_bf,
                           color='#000000',
                           stroke_width=0.2,
                           stroke_dasharray='none',
                           parent=None):

        svg_d = self.mkpath_pattern1_base(offset, points_base, bw_bf)

        return self.draw_obj_path(svg_d,
                                  color=color,
                                  stroke_width=stroke_width,
                                  stroke_dasharray=stroke_dasharray,
                                  parent=parent)

    def mkpath_pattern1_base(self, offset, points_base, bw_bf):

        (x0, y0) = offset

        for i, (x, y) in enumerate(points_base):
            if i == 0:
                d = 'M %f,%f' % (x + x0, y + y0)
            elif i == 7:
                d += ' L %f,%f' % (x + x0, y + y0)
                x1 = x
                y1 = y + bw_bf
            elif i == 8:
                d += ' C %f,%f %f,%f %f,%f' % (x1 + x0, y1 + y0,
                                               x + y0, y1 + y0,
                                               x + x0, y + y0)
            else:
                d += ' L %f,%f' % (x + x0, y + y0)
        d += ' Z'

        return d

    def draw_pattern1_button_hole(self, offset, points_base, dia1,
                                  color='#000000',
                                  stroke_width=0.2,
                                  stroke_dasharray='none',
                                  parent=None):
        if parent is None:
            parent = self.current_layer

        (x0, y0) = offset
        r = dia1 / 2
        x = points_base[4][0] / 2 + x0
        y = points_base[7][1] + y0

        return self.draw_obj_circle(x, y, r,
                                    color=color,
                                    stroke_width=stroke_width,
                                    stroke_dasharray=stroke_dasharray,
                                    parent=parent)

    #
    # pattern2
    #
    def draw_pattern2(self, offset, points_base, bw_bf, dia2,
                      color='#000000',
                      stroke_width=0.2,
                      stroke_dasharray='none',
                      parent=None):

        self.draw_pattern2_base(offset, points_base, bw_bf,
                                color='#0000FF',
                                stroke_width=stroke_width,
                                stroke_dasharray=stroke_dasharray,
                                parent=parent)

        self.draw_pattern2_button_hole(offset, points_base, dia2,
                                       color='#FF0000',
                                       stroke_width=stroke_width,
                                       stroke_dasharray=stroke_dasharray,
                                       parent=parent)

    def draw_pattern2_base(self, offset, points_base, bw_bf,
                           color='#000000',
                           stroke_width=0.2,
                           stroke_dasharray='none',
                           parent=None):

        svg_d = self.mkpath_pattern2_base(offset, points_base, bw_bf)
        return self.draw_obj_path(svg_d,
                                  color=color,
                                  stroke_width=stroke_width,
                                  stroke_dasharray=stroke_dasharray,
                                  parent=parent)

    def mkpath_pattern2_base(self, offset, points_base, bw_bf):
        (x0, y0) = offset

        for i, (x, y) in enumerate(points_base):
            if i == 0:
                d = 'M %f,%f' % (x + x0, y + y0)
            if i >= 6:
                break
            else:
                d += ' L %f,%f' % (x + x0, y + y0)
        d += ' Z'

        return d

    def draw_pattern2_button_hole(self, offset, points_base, dia2,
                                  color='#FF0000',
                                  stroke_width=0.2,
                                  stroke_dasharray='none',
                                  parent=None):
        if parent is None:
            parent = self.current_layer

        r = dia2 / 2

        (x0, y0) = offset
        (x1, y1) = points_base[5]
        x = x1 / 2 + x0
        y = y1 - r - 5 + y0

        return self.draw_obj_circle(x, y, r,
                                    color=color,
                                    stroke_width=stroke_width,
                                    stroke_dasharray=stroke_dasharray,
                                    parent=parent)

    #
    # common
    #
    def draw_needle(self, offset, points_needle, d2, dia3,
                     color='#FF0000',
                     parent=None):

        stroke_width='%f' % (dia3)
        stroke_dasharray='%f,%f' % (dia3, d2)

        svg_d = self.mkpath_needle(offset, points_needle)

        return self.draw_obj_path(svg_d,
                                  color=color,
                                  stroke_width=stroke_width,
                                  stroke_dasharray=stroke_dasharray,
                                  parent=parent)

    def mkpath_needle(self, offset, points_needle):
        (x0, y0) = offset

        for i, (x, y) in enumerate(points_needle):
            if i == 0:
                d = 'M %f,%f' % (x + x0, y + y0)
            else:
                d += ' L %f,%f' % (x + x0, y + y0)

        return d


if __name__ == '__main__':
    e = PlierCover()
    e.affect()
