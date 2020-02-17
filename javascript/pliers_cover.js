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
	style += 'stroke:' + color + ';';
	style += 'stroke-width:' + String(stroke_width) + ';';
	style += 'stroke-dasharray:none';
	
	this.svg_text = '<' + this.type + ' ';;
	this.svg_text += 'style="' + style + '" ';
	this.svg_text += this.param;
	this.svg_text += ' />';
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
	let vp = new Vpoint(origin[0], origin[1], origin[2]);
	this.param =  'cx="' + String(vp.x) + '"';
	this.param += ' cy="' + String(vp.y) + '"';
	this.param += ' r="' + String(this.r) + '"';
	super.draw(color, stroke_width);
    }
}

class SvgPath extends SvgObj {
    constructor(parent, points) {
	super(parent);
	this.type = "path";
	
	this.points = [];
	for (let p of points) {
	    this.points.push(new Point(p[0], p[1]));
	}
    }

    create_svg_d(origin, points) {
	let svg_d = "";
	let p0 = points.shift();

	svg_d = "M ";
	svg_d += String(p0.x + origin.x) + ",";
	svg_d += String(p0.y + origin.y);

	for (let p1 of points) {
	    svg_d += " L ";
	    svg_d += String(p1.x + origin.x) + ",";
	    svg_d += String(p1.y + origin.y);
	}
	return svg_d;
    }

    draw(origin, color, stroke_width) {
	let vp = new Vpoint(origin[0], origin[1], origin[2]);
	
	this.svg_d = this.create_svg_d(vp, this.points);
	this.param = 'd="' + this.svg_d + '"';
	super.draw(color, stroke_width);
    }
}

class SvgLine extends SvgPath {
    // exactly same as SvgPath
}

class SvgPolygon extends SvgPath {
    create_svg_d(origin_vpoint, points) {
	let svg_d = super.create_svg_d(origin_vpoint, points);
	svg_d += " Z";
	return svg_d;
    }
}

class SvgCanvas {
    constructor(id, w, h) {
	this.id = id;

	this.header = '<svg xmlns="http://www.w3.org/2000/svg"';
	this.header += ' version="1.1"';
	this.header += ' width="' + String(w) + '" height="' + String(h) + '"';
	this.header += ' viewBox="0 0 ' + String(w) + ' ' + String(h); + '"';
	this.header += '">\n';

	this.footer = '</svg>\n';

	this.objs = "";

	this.svg_text = this.header + this.footer;
    }

    draw(obj) {
	this.objs += obj + '\n';
    }

    display(id_download) {
	this.svg_text = this.header;
	this.svg_text += this.objs;
	this.svg_text += this.footer;

	console.log(this.id);
	document.getElementById(this.id).innerHTML = this.svg_text;

	this.set_download(id_download);
    }

    set_download(id) {
	let blob = new Blob([ this.svg_text ], {"type": "text/plain"});

	document.getElementById(id).href =
	    window.URL.createObjectURL(blob);
    }

}

function gen_svg(id_canvas, id_download) {
    let canvas = new SvgCanvas(id_canvas, 200, 200);

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

    let p = [[w1, w2], [h1, h2], [bw, bl], [dia1, dia2], [d1, d2]];

    let obj1 = new SvgLine(canvas, p);
    obj1.draw([10,10,0], "blue", 1);

    let obj2 = new SvgPolygon(canvas, [[0,0],[100,0],[100,100],[0,100]]);
    obj2.draw([50, 50, 0], "red", 1);
    
    let obj3 = new SvgCircle(canvas, dia1);
    obj3.draw([70,70,0], "green", 2);

    canvas.display(id_download);
}

function do_download(id) {
    // document.getElementById(id).click();
}
