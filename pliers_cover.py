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
    DEF_COLOR = '#000000'
    DEF_STROKE_WIDTH = 0.2
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
        return style

    def draw(self, color=DEF_COLOR, stroke_width=DEF_STROKE_WIDTH,
             stroke_dasharray=DEF_STROKE_DASHARRAY):

        style = self.mkstyle(color=color, stroke_width=stroke_width,
                             stroke_dasharray=stroke_dasharray)

        self.attr['style'] = simplestyle.formatStyle(style)
        return inkex.etree.SubElement(self.parent,
                                      inkex.addNS(self.type, 'svg'),
                                      self.attr)

class SvgCircle(SvgObj):
    DEF_COLOR = '#FF0000'
    DEF_STROKE_WIDTH = 0.2
    DEF_STROKE_DASHARRAY = 'none'

    def __init__(self, parent, cx, cy, r):
        super(SvgCircle, self).__init__(parent)
        
        self.cx = cx
        self.cy = cy
        self.r = r

        self.type = 'circle'

    def draw(self, color=DEF_COLOR, stroke_width=DEF_STROKE_WIDTH,
             stroke_dasharray=DEF_STROKE_DASHARRAY):

        self.attr['cx'] = str(self.cx)
        self.attr['cy'] = str(self.cy)
        self.attr['r'] = str(self.r)

        return super(SvgCircle, self).draw(color,
                                           stroke_width, stroke_dasharray)


class SvgButtonHole1(SvgCircle):
    def __init__(self, parent, offset, base_xy, dia1):
        (x0, y0) = offset
        (x1, y1) = base_xy
        self.r = dia1 / 2
        self.cx = x1 / 2 + x0
        self.cy = y1 + y0
        super(SvgButtonHole1, self).__init__(parent, self.cx, self.cy, self.r)


class SvgButtonHole2(SvgCircle):
    def __init__(self, parent, offset, base_xy, dia2):
        (x0, y0) = offset
        (x1, y1) = base_xy
        self.r = dia2 / 2
        self.cx = x1 / 2 + x0
        self.cy = y1 - self.r - 5 + y0
        super(SvgButtonHole2, self).__init__(parent, self.cx, self.cy, self.r)


class SvgPath(SvgObj):
    DEF_COLOR = '#0000FF'
    DEF_STROKE_WIDTH = 0.2
    DEF_STROKE_DASHARRAY = 'none'

    def __init__(self, parent, svg_d):
        super(SvgPath, self).__init__(parent)

        self.svg_d = svg_d

        self.type = 'path'

    def draw(self, color=DEF_COLOR, stroke_width=DEF_STROKE_WIDTH,
             stroke_dasharray=DEF_STROKE_DASHARRAY):

        self.attr['d'] = self.svg_d

        return super(SvgPath, self).draw(color,
                                         stroke_width, stroke_dasharray)


class SvgPattern(SvgPath):
    def __init__(self, parent, offset, points_base, bw_bf):
        self.svg_d = self.mkpath(offset, points_base, bw_bf)
        super(SvgPattern, self).__init__(parent, self.svg_d)

    def mkpath(self, offset, points_base, bw_bf=1):
        '''
        to be override
        '''
        pass


class SvgPattern1(SvgPattern):
    def mkpath(self, offset, points_base, bw_bf):
        (x0, y0) = offset

        for i, (x, y) in enumerate(points_base):
            (x1, y1) = (x + x0, y + y0)
            if i == 0:
                d = 'M %f,%f' % (x1, y1)
            elif i == 7:
                d += ' L %f,%f' % (x1, y1)
                x2 = x
                y2 = y + bw_bf
            elif i == 8:
                d += ' C %f,%f %f,%f %f,%f' % (x2 + x0, y2 + y0,
                                               x1     , y2 + y0,
                                               x1     , y1)
            else:
                d += ' L %f,%f' % (x + x0, y + y0)
        d += ' Z'

        return d


class SvgPattern2(SvgPattern):
    def mkpath(self, offset, points_base, bw_bf):
        (x0, y0) = offset

        for i, (x, y) in enumerate(points_base):
            (x1, y1) = (x + x0, y + y0)
            if i == 0:
                d = 'M %f,%f' % (x1, y1)
            elif i >= 6:
                break
            else:
                d += ' L %f,%f' % (x1, y1)
        d += ' Z'

        return d


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

        w = w2
        offset_x = self.DEF_OFFSET_X + w / 2
        offset_y = self.DEF_OFFSET_Y

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

        offset_x += w + 10
        points_base2 = self.mirror_points(points_base)
        self.draw_pattern2((offset_x, offset_y), points_base2, bw*bf, dia2)
        points_needle2 = self.mirror_points(points_needle)
        self.draw_needle((offset_x, offset_y), points_needle2, d2, dia3)

        return

    def mirror_points(self, points):
        new_points = []

        for (x, y) in points:
            new_x = -x
            new_points.append((new_x, y))

        return new_points

    def mkpoints_pattern1_base(self, w1, w2, h1, h2, bw, bl):
        points = []

        dw1 = (w2 - w1) / 2
        dw2 = (w2 - bw) / 2

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

    def mkstyle(self, color='#000000', stroke_width=0.2,
                stroke_dasharray='none'):

        style = {
            'stroke': color,
            'stroke-width': str(stroke_width),
            'stroke-dasharray': str(stroke_dasharray),
            'fill': 'none'
        }

        return style

    def draw_pattern1(self, offset, points_base, bw_bf, dia1,
                      stroke_width=0.2,
                      stroke_dasharray='none'):

        p = SvgPattern1(self.current_layer, offset,
                        points_base, bw_bf)
        p.draw(color='#0000FF', stroke_width=stroke_width,
               stroke_dasharray=stroke_dasharray)

        c = SvgButtonHole1(self.current_layer, offset,
                           (0, points_base[7][1]), dia1)
        c.draw(color='#FF0000', stroke_width=stroke_width,
               stroke_dasharray=stroke_dasharray)

    def draw_pattern2(self, offset, points_base, bw_bf, dia2,
                      color='#000000',
                      stroke_width=0.2,
                      stroke_dasharray='none'):

        p = SvgPattern2(self.current_layer, offset,
                        points_base, bw_bf)
        p.draw(color='#0000FF', stroke_width=stroke_width,
               stroke_dasharray=stroke_dasharray)

        c = SvgButtonHole2(self.current_layer, offset,
                           (0, points_base[0][1]), dia2)
        c.draw('#FF0000', stroke_width, stroke_dasharray)

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
