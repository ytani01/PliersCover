//
// (c) 2020 Yoichi Tanibayashi
//

class Point {
  constructor(x, y) {
    this.x = x;
    this.y = y;
  }

  distance(c) {
    return Math.sqrt((c.x - this.x) ** 2 + (c.y - this.y) ** 2);
  }

  rotate(self, rad) {
    let new_x = Math.cos(rad) * this.x - Math.sin(rad) * this.y;
    let new_y = Math.sin(rad) * this.x + Math.cos(rad) * this.y;
    this.x = new_x;
    this.y = new_y;
    return this;
  }

  mirror() {
    this.x = -this.x;
    return this;
  }
}

class Vpoint extends Point {
  constructor(x, y, rad) {
    super(x, y);
    this.rad = rad;
  }

  rotate(rad) {
    super.rotate(rad);
    this.rad += rad;
    return this;
  }

  mirror() {
    super.mirror();
    this.rad = -this.rad;
    return this;
  }
}

class SvgObj {
  constructor(parent) {
    this.parent = parent;
    this.type = "";
    this.svg_param = "";
  }

  draw(color, stroke_width) {
    let style = 'fill:none;';
    style = "fill:none;";
    style += `stroke:${color};`;
    style += `stroke-width:${stroke_width};`;
    style += "stroke-dasharray:none";
    
    this.svg_text = `<${this.type} style="${style}" ${this.param} />`;
    this.parent.draw(this.svg_text);
  }
}

class SvgCircle extends SvgObj {
  constructor(parent, r) {
    super(parent);
    this.type = "circle";
    this.r = r;
  }

  draw(origin, color, stroke_width) {
    let vp_origin = new Vpoint(origin[0], origin[1], origin[2]);
    this.param = `cx="${vp_origin.x}" cy="${vp_origin.y}" r="${this.r}"`;
    super.draw(color, stroke_width);
  }
}

class SvgPath extends SvgObj {
  constructor(parent, points) {
    super(parent);
    this.type = "path";
    
    this.p_points = [];
    for (let p of points) {
      this.p_points.push(new Point(p[0], p[1]));
    }
  }

  create_svg_d(vp_origin, p_points) {
    let svg_d = "";
    let p0 = p_points.shift();

    svg_d = `M ${p0.x + vp_origin.x},${p0.y + vp_origin.y}`;

    for (let p1 of p_points) {
      svg_d += ` L ${p1.x + vp_origin.x},${p1.y + vp_origin.y}`;
    }
    return svg_d;
  }

  draw(origin, color, stroke_width) {
    let vp_origin = new Vpoint(origin[0], origin[1], origin[2]);
    
    this.svg_d = this.create_svg_d(vp_origin, this.p_points);
    this.param = `d="${this.svg_d}"`;
    super.draw(color, stroke_width);
  }

  rotate(rad) {
    for (let p of this.p_points) {
      p.rotate(rad);
    }
    return this;
  }

  mirror() {
    for (let p of this.p_points) {
      p.mirror();
    }
    return this;
  }
}

class SvgLine extends SvgPath {
  // exactly same as SvgPath
}

class SvgPolygon extends SvgPath {
  create_svg_d(vp_origin, p_points) {
    return super.create_svg_d(vp_origin, p_points) + " Z";
  }
}

class SvgPart1Outline extends SvgObj {
  constructor(parent, w1, w2, h1, h2, bw, bl, bf) {
    super(parent);
    this.type = "path";
    
    this.p_points = this.create_p_points(w1, w2, h1, h2, bw, bl);
    this.bw_bf = bw * bf;
  }

  draw(origin, color, stroke_width) {
    let vp_origin = new Vpoint(origin[0], origin[1], origin[2]);
    
    this.svg_d = this.create_svg_d(vp_origin, this.p_points);
    this.param = `d="${this.svg_d}"`;
    super.draw(color, stroke_width);
  }

  rotate(rad) {
    for (let p of this.p_points) {
      p.rotate(rad);
    }
    return this;
  }

  mirror() {
    for (let p of this.p_points) {
      p.mirror();
    }
    return this;
  }

  create_p_points(w1, w2, h1, h2, bw, bl) {
    // 外枠の座標を生成
    let p_points = [];
    let x0 = -(w2 / 2);
    let y0 = 0;

    let x = x0;
    let y = y0 + h1 + h2;
    p_points.push(new Point(x, y));

    y = y0 + h1;
    p_points.push(new Point(x, y));

    x = -(w1 / 2);
    y = y0;
    p_points.push(new Point(x, y));

    x = w1 / 2;
    p_points.push(new Point(x, y));

    x = w2 / 2;
    y += h1;
    p_points.push(new Point(x, y));

    y += h2;
    p_points.push(new Point(x, y));

    x = bw / 2;
    p_points.push(new Point(x, y));

    y += bl - bw / 2;
    p_points.push(new Point(x, y));

    x = -(bw / 2);
    p_points.push(new Point(x, y));

    y = y0 + h1 + h2;
    p_points.push(new Point(x, y));

    return p_points;
  }

  create_svg_d(vp_origin, p_points) {
    let x0 = vp_origin.x;
    let y0 = vp_origin.y;
    let x1 = 0; let y1 = 0;
    let x2 = 0; let y2 = 0;
    
    let d = "";

    for (let i=0; i < p_points.length; i++) {
      x1 = x0 + p_points[i].x;
      y1 = y0 + p_points[i].y;

      if ( i == 0 ) {
	d = `M ${x1},${y1}`;
      } else if ( i == 7 ) {
	d += ` L ${x1},${y1}`;
	x2 = x1;
	y2 = y1 + this.bw_bf;
      } else if ( i == 8 ) {
	d += ` C ${x2},${y2} ${x1},${y2} ${x1},${y1}`;
      } else {
	d += ` L ${x1},${y1}`;
      }
    }
    d += ' Z';
    return d;
  }
}

class SvgNeedleHole extends SvgObj {
  constructor(parent, w, h, tf) {
    super(parent);
    this.type = "path";
    
    this.w = w;
    this.h = h;
    this.tf = tf;

    this.p_points = this.create_p_points();
  }

  draw(origin, color, stroke_width) {
    let vp_origin = new Vpoint(origin[0], origin[1], origin[2]);

    this.svg_d = this.create_svg_d(vp_origin, this.p_points);
    this.param = `d="${this.svg_d}"`;
    super.draw(color, stroke_width);
  }

  rotate(rad) {
    for (let p of this.p_points) {
      p.rotate(rad);
    }
    return this;
  }

  mirror() {
    for (let p of this.p_points) {
      p.mirror();
    }
    return this;
  }

  create_p_points() {
    let p_points = [];
    p_points.push(Point(-w / 2,  h * tf));
    p_points.push(Point( w / 2,  h * (1 - tf)));
    p_points.push(Point( w / 2, -h * tf));
    p_points.push(Point(-w / 2, -h * (1 - tf)));
    return p_points;
  }
}

class Part1 {
  constructor(parent,
	      w1, w2, h1, h2, bw, bl, bf, dia1, d1, d2,
	      needle_w, needle_h, needle_tf, needle_corner_rotation) {
    this.parent = parent;
    this.w1 = w1;
    this.w2 = w2;
    this.h1 = h1;
    this.h2 = h2;
    this.bw = bw;
    this.bl = bl;
    this.bf = bf;
    this.dia1 = dia1;
    this.d1 = d1;
    this.d2 = d2;
    this.needle_w = needle_w;
    this.needle_h = needle_h;
    this.needle_tf = needle_tf;
    this.needle_corner_rotation = needle_corner_rotation;

    // 図形作成
    this.svg_outline = new SvgPart1Outline(parent,
					   w1, w2, h1, h2, bw, bl, bf);
    this.svg_hole = new SvgCircle(parent, this.dia1 / 2);
  }

  draw(origin) {
    let x0 = origin[0];
    let y0 = origin[1];
    let rad0 = origin[2];
    
    let x = x0 + this.w2 / 2;
    let y = y0;
    this.svg_outline.draw([x, y, rad0], "#0000FF", 0.5);

    x = x0 + this.w2 / 2;
    y = y0 + this.h1 + this.h2 + this.bl - this.bw / 2;
    this.svg_hole.draw([x, y, rad0], "#FF0000", 0.5);
  }

}

class Part2 {
  constructor(parent, part1, dia2) {
    this.parent = parent;
    this.part1 = part1;
    this.dia2 = dia2;

    this.points_outline = [];
    for (let i=0; i < 6; i++) {
      let pp = this.part1.svg_outline.p_points[i];
      pp.mirror();
      this.points_outline.push([pp.x, pp.y]);
    }
    this.svg_outline = new SvgPolygon(parent, this.points_outline);

    this.svg_hole = new SvgCircle(parent, this.dia2 / 2);
  }

  draw(origin) {
    let x0 = origin[0];
    let y0 = origin[1];
    let rad0 = origin[2];

    let x = x0 + this.part1.w2 / 2;
    let y = y0;
    this.svg_outline.draw([x, y, rad0], "#0000FF", 0.5);

    x = x0 + this.part1.w2 / 2;
    y = y0 + this.part1.h1 + this.part1.h2
      - this.svg_hole.r - this.part1.d1;
    this.svg_hole.draw([x, y, rad0], "#FF0000", 0.5);
  }
}

class SvgCanvas {
  constructor(id, w, h) {
    this.id = id;

    this.header = '<svg xmlns="http://www.w3.org/2000/svg"';
    this.header += ' version="1.1"';
    this.header += ' width="500" height="400"';
    this.header += ` viewBox="0 0 ${w} ${h}">\n`;

    this.footer = '</svg>\n';

    this.objs = "";

    this.svg_text = this.header + this.footer;
  }

  draw(obj) {
    this.objs += obj + '\n';
  }

  display() {
    this.svg_text = this.header + this.objs + this.footer;
    document.getElementById(this.id).innerHTML = this.svg_text;
  }

  set_download(id) {
    let blob = new Blob([ this.svg_text ], {"type": "text/plain"});
    document.getElementById(id).href = window.URL.createObjectURL(blob);
  }
}

function gen_svg(id_canvas, id_download) {
  const OFFSET_X = 10;
  const OFFSET_Y = 10;

  // parameters
  let w1 = parseFloat(document.getElementById("w1").value);
  let w2 = parseFloat(document.getElementById("w2").value);
  let h1 = parseFloat(document.getElementById("h1").value);
  let h2 = parseFloat(document.getElementById("h2").value);

  let bw = parseFloat(document.getElementById("bw").value);
  let bl = parseFloat(document.getElementById("bl").value);

  let dia1 = parseFloat(document.getElementById("dia1").value);
  let dia2 = parseFloat(document.getElementById("dia2").value);

  let d1 = parseFloat(document.getElementById("d1").value);
  let d2 = parseFloat(document.getElementById("d2").value);

  let bf = parseFloat(document.getElementById("bf").value);

  let needle_w = parseFloat(document.getElementById("needle_w").value);
  let needle_h = parseFloat(document.getElementById("needle_h").value);
  let needle_tf = parseFloat(document.getElementById("needle_tf").value);

  // make objects and draw them
  let x0 = OFFSET_X;
  let y0 = OFFSET_Y;
  
  let canvas_width = x0 + w2 + x0 + w2 + x0;
  let canvas_height = y0 + h1 + h2 + bl + y0;
  let canvas = new SvgCanvas("canvas", canvas_width, canvas_height);

  let frame = new SvgPolygon(canvas, [[0,0],
				      [canvas_width, 0],
				      [canvas_width, canvas_height],
				      [0, canvas_height]]);
  frame.draw([0, 0, 0], "#000000", 1);

  let part1 = new Part1(canvas, w1, w2, h1, h2, bw, bl, bf, dia1, d1, d2,
			0, 0, 0, true);
  part1.draw([x0, y0, 0]);

  x0 += w2 + 10;
  let part2 = new Part2(canvas, part1, dia2);
  part2.draw([x0, y0, 0]);

  canvas.display();
  canvas.set_download(id_download);
}
