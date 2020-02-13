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


class Point(object):
    '''
    (x, y)座標と方向(rad)を持つ点

    rad: 方向(真上: 0, 右: math.pi / 2, ..)
    '''
    def __init__(self, x, y, rad=0):
        self.x = x
        self.y = y
        self.rad = rad

    def get(self):
        return (self.x, self.y, self.rad)

    def set(self, x, y, rad=0):
        self.x = x
        self.y = y
        self.rad = rad

    def rotate(self, rad=0):
        new_x = math.cos(rad) * self.x - math.sin(rad) * self.y
        new_y = math.sin(rad) * self.x + math.cos(rad) * self.y
        self.x = new_x
        self.y = new_y


class SvgObj(object):
    DEF_COLOR = '#00FF00'
    DEF_STROKE_WIDTH = 0.2
    DEF_STROKE_DASHARRAY = 'none'

    def __init__(self, parent):
        self.parent = parent
        self.type = None
        self.attr = {}

    def draw(self, point,
             color=DEF_COLOR,
             stroke_width=DEF_STROKE_WIDTH,
             stroke_dasharray=DEF_STROKE_DASHARRAY):

        self.attr['style'] = simplestyle.formatStyle({
            'stroke': str(color),
            'stroke-width': str(stroke_width),
            'stroke-dasharray': str(stroke_dasharray),
            'fill': 'none'})
        return inkex.etree.SubElement(self.parent,
                                      inkex.addNS(self.type, 'svg'),
                                      self.attr)


class SvgCircle(SvgObj):
    DEF_COLOR = '#FF0000'
    DEF_STROKE_WIDTH = 0.2
    DEF_STROKE_DASHARRAY = 'none'

    def __init__(self, parent, r):
        super(SvgCircle, self).__init__(parent)
        self.r = r
        self.type = 'circle'

    def draw(self, point,
             color=DEF_COLOR,
             stroke_width=DEF_STROKE_WIDTH,
             stroke_dasharray=DEF_STROKE_DASHARRAY):
        self.attr['cx'] = str(point.x)
        self.attr['cy'] = str(point.y)
        self.attr['r'] = str(self.r)

        return super(SvgCircle, self).draw(point,
                                           color,
                                           stroke_width,
                                           stroke_dasharray)


class SvgPath(SvgObj):
    DEF_COLOR = '#0000FF'
    DEF_STROKE_WIDTH = 0.2
    DEF_STROKE_DASHARRAY = 'none'

    def __init__(self, parent, points):
        super(SvgPath, self).__init__(parent)
        self.points = points
        self.type = 'path'

    def mk_svg_d(self, origin_point, points):
        '''
        to be override

        This is sample code.
        '''
        svg_d = ''
        for i, p in enumerate(points):
            (x1, y1) = (p.x + origin_point.x, p.y + origin_point.y)
            if i == 0:
                svg_d = 'M %f,%f' % (x1, y1)
            else:
                svg_d += ' L %f,%f' % (x1, y1)
        return svg_d

    def rotate(self, rad=0):
        for p in self.points:
            p.rotate(rad)

    def draw(self, origin,
             color=DEF_COLOR, stroke_width=DEF_STROKE_WIDTH,
             stroke_dasharray=DEF_STROKE_DASHARRAY):

        self.rotate(origin.rad)

        svg_d = self.mk_svg_d(origin, self.points)
        self.attr['d'] = svg_d
        return super(SvgPath, self).draw(origin, color,
                                         stroke_width, stroke_dasharray)


class SvgLine(SvgPath):
    # exactly same as SvgPath
    pass


class SvgPolygon(SvgPath):
    def mk_svg_d(self, origin, points):
        svg_d = super(SvgPolygon, self).mk_svg_d(origin, points)
        svg_d += ' Z'
        return svg_d


class SvgPart1Base(SvgPath):
    def __init__(self, parent, points, bw_bf):
        super(SvgPart1Base, self).__init__(parent, points)
        self.bw_bf = bw_bf

    def mk_svg_d(self, origin, points, bw_bf=1):
        for i, p in enumerate(points):
            (x1, y1) = (p.x + origin.x, p.y + origin.y)
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


class SvgNeedleHole(SvgPolygon):
    def __init__(self, parent, w=2, hf=0.7, rf=0.2):
        '''
        w: width
        hf: height factor
        rf: rotation factor
        '''
        self.w = w
        self.hf = hf
        self.rf = rf
        self.gen_points(self.w, self.hf, self.rf)
        super(SvgNeedleHole, self).__init__(parent, self.points)

    def gen_points(self, w, hf, rf):
        self.points = []
        self.points.append(Point(-w / 2,  w * hf * rf))
        self.points.append(Point( w / 2,  w * hf * (1 - rf)))
        self.points.append(Point( w / 2, -w * hf * rf))
        self.points.append(Point(-w / 2, -w * hf * (1 - rf)))

    def reverse(self):
        for i in range(len(self.points)):
            self.points[i].x = -self.points[i].x
        return self


class Part1:
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
        self.base = SvgPart1Base(self.parent, self.points_base,
                                 (self.bw * self.bf))
        self.hole = SvgCircle(self.parent, self.dia1 / 2)

        self.points_needle = self.get_needle_points(self.points_base,
                                                    self.w1, self.w2,
                                                    self.h1,
                                                    self.d1, self.d2,
                                                    self.dia3)

        self.needle_hole = []
        for p in self.points_needle:
            self.needle_hole.append((SvgNeedleHole(self.parent, self.dia3), p))

    def mk_points(self, w1, w2, h1, h2, bw, bl):
        points = []

        (x0, y0) = (-(w2 / 2), 0)

        (x, y) = (x0, y0 + h1 + h2)
        points.append(Point(x, y))

        y = y0 + h1
        points.append(Point(x, y))

        x = -(w1 / 2)
        y = y0
        points.append(Point(x, y))

        x = w1 / 2
        points.append(Point(x, y))

        x = w2 / 2
        y += h1
        points.append(Point(x, y))

        y += h2
        points.append(Point(x, y))

        x = bw / 2
        points.append(Point(x, y))

        y += bl - bw / 2
        points.append(Point(x, y))

        x = -(bw / 2)
        points.append(Point(x, y))

        y = y0 + h1 + h2
        points.append(Point(x, y))

        return points

    def get_needle_points(self, points_base, w1, w2, h1, d1, d2, dia):
        rad1 = math.atan((w2 - w1) / (2 * h1))
        rad1a = (math.pi - rad1) / 2
        a1 = d1 / math.tan(rad1a)

        rad2 = (math.pi / 2) - rad1
        rad2a = (math.pi - rad2) / 2
        a2 = d1 / math.tan(rad2a)

        #
        # 頂点
        #
        points1 = []
        for i, p in enumerate(points_base):
            (nx, ny) = (p.x, p.y)
            if i == 0:
                nx += d1
                ny -= d1 * 1.5
                points1.append(Point(nx, ny, 0))
            if i == 1:
                nx += d1
                ny += a1
                points1.append(Point(nx, ny, rad1))
            if i == 2:
                nx += a2
                ny += d1
                points1.append(Point(nx, ny, math.pi / 2))
            if i == 3:
                nx -= a2
                ny += d1
                points1.append(Point(nx, ny, (math.pi / 2) + rad2))
            if i == 4:
                nx -= d1
                ny += a1
                points1.append(Point(nx, ny, math.pi))
            if i == 5:
                nx -= d1
                ny -= d1 * 1.5
                points1.append(Point(nx, ny, math.pi))
            if i > 5:
                break

        #
        # 頂点を補完する点
        #
        points2 = []
        for i in range(len(points1)-1):
            d = self.distance(points1[i], points1[i+1])
            n = int(abs(round(d / d2)))
            for p in self.split_points(points1[i], points1[i+1], n):
                points2.append(p)
        points2.insert(0, points1[0])

        return points2

    def distance(self, p1, p2):
        return math.sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2)

    def split_points(self, p1, p2, n):
        if n == 0:
            return [p1]
        (dx, dy) = ((p2.x - p1.x) / n, (p2.y - p1.y) / n)

        p = []
        for i in range(n):
            p.append(Point(p1.x + dx * (i + 1), p1.y + dy * (i + 1), p1.rad))

        p[-1].rad = (p1.rad + p2.rad) / 2
        return p

    def draw(self, point):
        self.base.draw(Point(point.x + self.w2 / 2, point.y), color='#0000FF')
        self.hole.draw(Point(point.x + self.w2 / 2,
                             point.y + self.h1 + self.h2 + self.bl
                             - self.bw / 2),
                       color='#FF0000')
        for (nh, p) in self.needle_hole:
            nh.draw(Point(point.x + p.x + self.w2 / 2, point.y + p.y, p.rad),
                    color='#FF0000')


class Part2:
    def __init__(self, parent, part1, dia2):
        self.parent = parent
        self.part1 = part1
        self.dia2 = dia2

        self.points_base = self.mk_points_from_part1(self.part1)
        self.base = SvgPolygon(self.parent, self.points_base)
        self.hole = SvgCircle(self.parent, self.dia2 / 2)
        self.points_needle = self.reverse_points(self.part1.points_needle)

        self.needle_hole = []
        for p in self.points_needle:
            nh = SvgNeedleHole(self.parent, self.part1.dia3).reverse()
            self.needle_hole.append((nh, p))

    def reverse_points(self, points):
        new_points = []
        for p in points:
            new_points.append(Point(-p.x, p.y, -p.rad))
        return new_points

    def mk_points_from_part1(self, part1):
        points = []
        for i, p in enumerate(part1.points_base):
            if i > 5:
                break
            points.append(Point(p.x, p.y))
        return self.reverse_points(points)

    def draw(self, origin):
        self.base.draw(Point(origin.x + self.part1.w2 / 2, origin.y),
                       color='#0000FF')
        self.hole.draw(Point(origin.x + self.part1.w2 / 2,
                             origin.y + self.part1.h1 + self.part1.h2
                             - self.hole.r - self.part1.d1),
                       color='#FF0000')
        for (nh, p) in self.needle_hole:
            nh.draw(Point(origin.x + p.x + self.part1.w2 / 2, origin.y + p.y,
                          p.rad),
                    color='#FF0000')


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
            inkex.errormsg(msg)
            return

        if dia1 >= bw:
            msg = "Error: dia1(%d) >= bw(%d) !" % (dia1, bw)
            inkex.errormsg(msg)
            return

        #
        # draw
        #
        origin_point = Point(self.DEF_OFFSET_X, self.DEF_OFFSET_Y)

        part1 = Part1(self.current_layer,
                      w1, w2, h1, h2, bw, bl, bf, dia1, d1, d2, dia3)
        part1.draw(origin_point)

        origin_point.x += w2 + 10

        part2 = Part2(self.current_layer, part1, dia2)
        part2.draw(origin_point)

        return


if __name__ == '__main__':
    e = PlierCover()
    e.affect()
