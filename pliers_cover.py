#
# -*- coding: utf-8 -*-
#
# (c) Yoichi Tanibayashi
#
import inkex
import simplestyle
import math
"""
??
$ sudo apt install python-lxml
"""
inkex.localize()


class SvgObj(object):
    DEF_COLOR = '#00FF00'
    DEF_STROKE_WIDTH = 0.3
    DEF_STROKE_DASHARRAY = 'none'

    def __init__(self, parent):
        self.parent = parent
        self.type = None
        self.attr = {}

    def mkstyle(self, color=DEF_COLOR, stroke_width=DEF_STROKE_WIDTH,
                stroke_dasharray=DEF_STROKE_DASHARRAY):
        style = {
            'stroke': color,
            'stroke-width': str(stroke_width),
            'stroke-dasharray': str(stroke_dasharray),
            'fill': 'none'
        }

        # inkex.errormsg('style=%s' % str(style))

        return style

    def draw(self, x, y,
             color=DEF_COLOR,
             stroke_width=DEF_STROKE_WIDTH,
             stroke_dasharray=DEF_STROKE_DASHARRAY):
        '''
        (x, y): offset
        '''
        # inkex.errormsg('color=%s' % color)

        style = self.mkstyle(color=color, stroke_width=stroke_width,
                             stroke_dasharray=stroke_dasharray)

        self.attr['style'] = simplestyle.formatStyle(style)
        return inkex.etree.SubElement(self.parent,
                                      inkex.addNS(self.type, 'svg'),
                                      self.attr)


class SvgCircle(SvgObj):
    DEF_COLOR = '#FF0000'
    DEF_STROKE_WIDTH = 0.3
    DEF_STROKE_DASHARRAY = 'none'

    def __init__(self, parent, r):
        super(SvgCircle, self).__init__(parent)

        self.r = r

        self.type = 'circle'

    def draw(self, x, y,
             color=DEF_COLOR,
             stroke_width=DEF_STROKE_WIDTH,
             stroke_dasharray=DEF_STROKE_DASHARRAY):

        self.attr['cx'] = str(x)
        self.attr['cy'] = str(y)
        self.attr['r'] = str(self.r)

        return super(SvgCircle, self).draw(x, y, color,
                                           stroke_width, stroke_dasharray)


class SvgButtonHole1(SvgCircle):
    def __init__(self, parent, dia):
        self.r = dia / 2
        super(SvgButtonHole1, self).__init__(parent, self.r)


class SvgButtonHole2(SvgCircle):
    def __init__(self, parent, dia):
        self.r = dia / 2
        super(SvgButtonHole2, self).__init__(parent, self.r)


class SvgPath(SvgObj):
    DEF_COLOR = '#0000FF'
    DEF_STROKE_WIDTH = 0.3
    DEF_STROKE_DASHARRAY = 'none'

    def __init__(self, parent, points):
        super(SvgPath, self).__init__(parent)

        self.points = points

        self.type = 'path'

    def mk_svg_d(self, x, y, points):
        '''
        to be override

        This is sample code of SvgLine
        '''
        svg_d = ''

        for i, (px, py) in enumerate(points):
            (x1, y1) = (px + x, py + y)
            if i == 0:
                svg_d = 'M %f,%f' % (x1, y1)
            else:
                svg_d += ' L %f,%f' % (x1, y1)

        return svg_d

    def draw(self, x, y,
             color=DEF_COLOR, stroke_width=DEF_STROKE_WIDTH,
             stroke_dasharray=DEF_STROKE_DASHARRAY):

        svg_d = self.mk_svg_d(x, y, self.points)

        self.attr['d'] = svg_d

        # inkex.errormsg('svg_d=%s' % (svg_d))

        return super(SvgPath, self).draw(x, y, color,
                                         stroke_width, stroke_dasharray)


class SvgLine(SvgPath):
    # exactly same as SvgPath
    pass


class SvgPolygon(SvgPath):
    def mk_svg_d(self, x, y, points):
        svg_d = super(SvgPolygon, self).mk_svg_d(x, y, points)
        svg_d += ' Z'
        return svg_d


class SvgPattern1Base(SvgPath):
    def __init__(self, parent, points, bw_bf):
        super(SvgPattern1Base, self).__init__(parent, points)

        self.bw_bf = bw_bf

    def mk_svg_d(self, x, y, points, bw_bf=1):
        for i, (px, py) in enumerate(points):
            (x1, y1) = (px + x, py + y)
            if i == 0:
                d = 'M %f,%f' % (x1, y1)
            elif i == 7:
                d += ' L %f,%f' % (x1, y1)
                x2 = x1
                y2 = y1 + self.bw_bf
            elif i == 8:
                d += ' C %f,%f %f,%f %f,%f' % (x2, y2, x1, y2, x1, y1)
            else:
                d += ' L %f,%f' % (x1, y1)
        d += ' Z'

        return d


class Pattern1:
    def __init__(self, parent,
                 w1, w2, h1, h2, bw, bl, bf, dia1, d1, d2, dia3):
        self.parent = parent
        self.w1 = w1
        self.w2 = w2
        self.h1 = h1
        self.h2 = h2
        self.bw = bw
        self.bl = bl
        self.bf = bf
        self.dia1 = dia1
        self.d1 = d1
        self.d2 = d2
        self.dia3 = dia3

        self.points_base = self.mk_points(w1, w2, h1, h2, bw, bl)
        self.base = SvgPattern1Base(self.parent, self.points_base,
                                    (self.bw * self.bf))
        self.hole = SvgCircle(self.parent, self.dia1 / 2)

        self.points_needle = self.get_needle_points(self.points_base,
                                                    self.d1, self.d2,
                                                    self.dia3)

        self.needle_hole = []
        for p in self.points_needle:
            self.needle_hole.append((SvgCircle(self.parent, dia3), p))

    def mk_points(self, w1, w2, h1, h2, bw, bl):
        points = []

        (x0, y0) = (-(w2 / 2), 0)

        (x, y) = (x0, y0 + h1 + h2)
        points.append((x, y))

        y = y0 + h1
        points.append((x, y))

        x = -(w1 / 2)
        y = y0
        points.append((x, y))

        x = w1 / 2
        points.append((x, y))

        x = w2 / 2
        y += h1
        points.append((x, y))

        y += h2
        points.append((x, y))

        x = bw / 2
        points.append((x, y))

        y += bl - bw / 2
        points.append((x, y))

        x = -(bw / 2)
        points.append((x, y))

        y = y0 + h1 + h2
        points.append((x, y))

        return points

    def get_needle_points(self, points_base, d1, d2, dia):
        points = []

        for i, (px, py) in enumerate(points_base):
            (nx, ny) = (px, py)
            if i == 0:
                nx += d1
                ny -= d1
                points.append((nx, ny))
            if i == 1:
                nx += d1
                ny += dia / 2
                points.append((nx, ny))
            if i == 2:
                nx += d1 - dia / 2
                ny += d1
                points.append((nx, ny))
            if i == 3:
                nx -= d1 - dia / 2
                ny += d1
                points.append((nx, ny))
            if i == 4:
                nx -= d1
                ny += dia / 2
                points.append((nx, ny))
            if i == 5:
                nx -= d1
                ny -= d1
                points.append((nx, ny))
            if i > 5:
                break

        return points

    def draw(self, x, y):
        self.base.draw(x + self.w2 / 2, y, color='#0000FF')
        self.hole.draw(x + self.w2 / 2,
                       y + self.h1 + self.h2 + self.bl - self.bw / 2,
                       color='#FF0000')
        for (nh, p) in self.needle_hole:
            (px, py) = p
            nh.draw(x + px + self.w2 / 2, y + py)


class Pattern2:
    def __init__(self, parent, pattern1, dia2):
        self.parent = parent
        self.pattern1 = pattern1
        self.dia2 = dia2

        self.points_base = self.mk_points_from_pattern1(self.pattern1)
        self.base = SvgPolygon(self.parent, self.points_base)

        self.hole = SvgCircle(self.parent, self.dia2 / 2)

        self.points_needle = self.reverse_points(self.pattern1.points_needle)

        self.needle_hole = []
        for p in self.points_needle:
            self.needle_hole.append((SvgCircle(self.parent,
                                               self.pattern1.dia3),
                                     p))

    def reverse_points(self, points):
        new_points = []

        for (x, y) in points:
            new_x = -x
            new_points.append((new_x, y))

        return new_points

    def mk_points_from_pattern1(self, pattern1):
        points = []

        for i, (px, py) in enumerate(pattern1.points_base):
            if i > 5:
                break
            points.append((px, py))

        return self.reverse_points(points)

    def draw(self, x, y):
        self.base.draw(x + self.pattern1.w2 / 2, y,
                       color='#0000FF')
        self.hole.draw(x + self.pattern1.w2 / 2,
                       y + self.pattern1.h1 + self.pattern1.h2
                       - self.hole.r - self.pattern1.d1,
                       color='#FF0000')
        for (nh, p) in self.needle_hole:
            (px, py) = p
            nh.draw(x + px + self.pattern1.w2 / 2, y + py)


class PlierCover(inkex.Effect):
    DEF_OFFSET_X = 20
    DEF_OFFSET_Y = 20

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
        offset_x = self.DEF_OFFSET_X
        offset_y = self.DEF_OFFSET_Y

        pattern1 = Pattern1(self.current_layer,
                            w1, w2, h1, h2, bw, bl, bf, dia1, d1, d2, dia3)
        pattern1.draw(offset_x, offset_y)

        offset_x += w2 + 10
        
        pattern2 = Pattern2(self.current_layer, pattern1, dia2)
        pattern2.draw(offset_x, offset_y)
        return

        points_base = self.mkpoints_pattern1_base(w1, w2, h1, h2, bw, bl)
        points_needle1 = self.mkpoints_needle(points_base,
                                              w1, w2, h1, d1, d2)

        self.draw_pattern1((offset_x, offset_y), points_base, bw*bf, dia1)
        self.draw_needle((offset_x, offset_y), points_needle1, d2, dia3)

        offset_x += w + 10
        points_base2 = self.reverse_points_points(points_base)
        self.draw_pattern2((offset_x, offset_y), points_base2, bw*bf, dia2)
        points_needle2 = self.reverse_points_points(points_needle1)
        self.draw_needle((offset_x, offset_y), points_needle2, d2, dia3)

        return

    def mkpoints_pattern1_base(self, w1, w2, h1, h2, bw, bl):
        points = []

        (x0, y0) = (-(w2 / 2), 0)

        (x, y) = (x0, y0 + h1 + h2)
        points.append((x, y))

        y = y0 + h1
        points.append((x, y))

        x = -(w1 / 2)
        y = y0
        points.append((x, y))

        x = w1 / 2
        points.append((x, y))

        x = w2 / 2
        y += h1
        points.append((x, y))

        y += h2
        points.append((x, y))

        x = bw / 2
        points.append((x, y))

        y += bl - bw / 2
        points.append((x, y))

        x = -(bw / 2)
        points.append((x, y))

        y = y0 + h1 + h2
        points.append((x, y))

        return points

    def mkpoints_needle(self, points_base, w1, w2, h1, d1, d2):
        points = []

        a1 = 2

        b = (w2 - w1) * d1 / (2 * h1)
        a2 = math.sqrt(b ** 2 + d1 ** 2) - b

        (x1, y1) = points_base[0]
        (x2, y2) = (x1 + d1, y1 - d2)
        points.append((x2, y2))

        (x1, y1) = points_base[1]
        (x2, y2) = (x1 + d1, y1 + a1)
        points.append((x2, y2))

        (x1, y1) = points_base[2]
        (x2, y2) = (x1 + a2, y1 + d1)
        points.append((x2, y2))

        (x1, y1) = points_base[3]
        (x2, y2) = (x1 - a2, y1 + d1)
        points.append((x2, y2))

        (x1, y1) = points_base[4]
        (x2, y2) = (x1 - d1, y1 + a1)
        points.append((x2, y2))

        (x1, y1) = points_base[5]
        (x2, y2) = (x1 - d1, y1 - d2)
        points.append((x2, y2))

        return points

    def draw_obj_path(self,
                      svg_d='M 0,0 L 100,0 L 100,100 Z',
                      color='#000000',
                      stroke_width=0.3,
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

    def mkstyle(self, color='#000000', stroke_width=0.3,
                stroke_dasharray='none'):

        style = {
            'stroke': color,
            'stroke-width': str(stroke_width),
            'stroke-dasharray': str(stroke_dasharray),
            'fill': 'none'
        }

        return style


if __name__ == '__main__':
    e = PlierCover()
    e.affect()
