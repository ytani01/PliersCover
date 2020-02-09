import inkex
import simplestyle
"""
$ sudo apt install python-lxml
"""
inkex.localize()
# inkex.errormsg(_("Hello, world."))

class ytaniFoo(inkex.Effect):
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
        self.OptionParser.add_option("--r1", action="store", type="float",
                                     dest="r1", help="")
        self.OptionParser.add_option("--r2", action="store", type="float",
                                     dest="r2", help="")
        
        self.OptionParser.add_option("--d1", action="store", type="float",
                                     dest="d1", help="")
        self.OptionParser.add_option("--d2", action="store", type="float",
                                     dest="d2", help="")
        self.OptionParser.add_option("--r3", action="store", type="float",
                                     dest="r3", help="")

    def effect(self):
        """
        main
        """
        # parameters
        stroke_width = 0.2

        x_offset = 20
        y_offset = 20

        w1 = self.options.w1
        w2 = self.options.w2
        h1 = self.options.h1
        h2 = self.options.h2

        bw = self.options.bw
        bl = self.options.bl
        r1 = self.options.r1
        r2 = self.options.r2

        d1 = self.options.d1
        d2 = self.options.d2
        r3 = self.options.r3

        x1 = x_offset + ((w2 - w1) / 2)
        y1 = y_offset

        cx1 = x_offset + (w2 / 2) - (stroke_width * 0.5)
        cy1 = y_offset + h1 + h2 + bl - (bw / 2)

        x2 = x_offset + w2 + 10 + ((w2 - w1) / 2)
        y2 = y_offset

        cx2 = x_offset + w2 + 10 + (w2 / 2) - (stroke_width * 0.5)
        cy2 = y_offset + h1 + h2 - (r1 / 2) - 5

        # inkex.errormsg('x1=%d, cx=%d' % (x1, cx))

        # error check
        if w1 >= w2:
            msg = "Error: w1(%d) >= w2(%d) !" % (w1, w2)
            inkex.errormsg(_(msg))
            return

        if r1 >= bw:
            msg = "Error: r1(%d) >= bw(%d) !" % (r1, bw)
            inkex.errormsg(_(msg))
            return
            

        # draw
        parent = self.current_layer
        style = {
            'stroke': '#000000',
            'stroke-width': str(stroke_width),
            'fill': 'none'
        }
        
        """
        attribs1 = {
            'style': simplestyle.formatStyle(style),
            'height': str(self.options.h1),
            'width': str(self.options.w1),
            'x': str(self.options.bw),
            'y': str(self.options.bl)
        }
        obj1=inkex.etree.SubElement(parent,
                                    inkex.addNS('rect', 'svg'),
                                    attribs1)
        """

        # base
        d_base = self.mkpath_base(x1, y1,
                                  w1, w2, h1, h2,
                                  bw, bl)
        attribs_base = {
            'style': simplestyle.formatStyle(style),
            'd': d_base
        }
        obj_base = inkex.etree.SubElement(parent,
                                          inkex.addNS('path', 'svg'),
                                          attribs_base)
        attribs_hole1 = {
            'style': simplestyle.formatStyle(style),
            'r': str('%.1f' % (r1 / 2)),
            'cx': str(cx1),
            'cy': str(cy1)
        }
        obj_hole1 = inkex.etree.SubElement(parent,
                                           inkex.addNS('circle', 'svg'),
                                           attribs_hole1)

        # top
        d_top = self.mkpath_top(x2, y2,
                                w1, w2, h1, h2)
        attribs_top = {
            'style': simplestyle.formatStyle(style),
            'd': d_top
        }
        obj_top = inkex.etree.SubElement(parent,
                                         inkex.addNS('path', 'svg'),
                                         attribs_top)

        attribs_hole2 = {
            'style': simplestyle.formatStyle(style),
            'r': str('%.1f' % (r2 / 2)),
            'cx': str(cx2),
            'cy': str(cy2)
        }
        obj_hole2 = inkex.etree.SubElement(parent,
                                          inkex.addNS('circle', 'svg'),
                                          attribs_hole2)
        
        # hari
        n_hari = int(round((w1 - d1) / d2))
        d1a = float(w1 - d1) / float(n_hari)
        x3 = x1 + (d1 / 2)
        y3 = y1 + d1

        x4 = x2 + (d1 / 2)
        
        for i in range(n_hari):
            attribs_hari = {
                'style': simplestyle.formatStyle(style),
                'r': str('%.2f' % (r3 / 2)),
                'cx': str(x3),
                'cy': str(y3) 
            }
            obj_hari = inkex.etree.SubElement(parent,
                                              inkex.addNS('circle', 'svg'),
                                              attribs_hari)

            attribs_hari = {
                'style': simplestyle.formatStyle(style),
                'r': str('%.2f' % (r3 / 2)),
                'cx': str(x4),
                'cy': str(y3) 
            }
            obj_hari = inkex.etree.SubElement(parent,
                                              inkex.addNS('circle', 'svg'),
                                              attribs_hari)
            x3 += d1a
            x4 += d1a

    def mkpath_base(self, x, y, w1, w2, h1, h2, bw, bl):
        p1 = 0.75

        d = 'M %d,%d' % (x, y)
        d += ' h %d' % (w1)
        d += ' l %.1f,%d' % ((w2 - w1) / 2, h1)
        d += ' v %d' % (h2)
        d += ' h %.1f' % ((w2 - bw) / -2)
        d += ' v %.1f' % (bl - (bw / 2))
        d += ' c %.1f,%.1f %.1f,%.1f %.1f,%.1f' % (
            0,   bw * p1,
            -bw, bw * p1,
            -bw, 0)
        d += ' v %.1f' % (-(bl - (bw / 2)))
        d += ' h %.1f' % ((w2 - bw) / -2)
        d += ' v %d' % (-h2)
        d += ' Z'

        return d
        
    def mkpath_top(self, x, y, w1, w2, h1, h2):
        p1 = 0.75

        d = 'M %d,%d' % (x, y)
        d += ' h %d' % (w1)
        d += ' l %.1f,%d' % ((w2 - w1) / 2, h1)
        d += ' v %d' % (h2)
        d += ' h %.1f' % (-w2)
        d += ' v %d' % (-h2)
        d += ' Z'

        return d
        

if __name__ == '__main__':
    e = ytaniFoo()
    e.affect()
