function gen_svg() {
    var e = document.getElementById("target");

    var svg1 = "<svg xmlns=\"http://www.w3.org/2000/svg\" version=\"1.1\" width=\"200mm\" height=\"200mm\" viewBox=\"0 0 200 200\">";
    var svg2 = "</svg>";

    svg_d = "M 0,0 L 100,0 L 100,100 L 0,100 Z";

    var svg_text = svg1 + svg_d + svg2;

    var blob = new Blob([svg_txt], {"type": "text/plain"});

    document.getElementById("download").href = window.URL.createObjectURL(blob);
    window.alert("Finish !");
}
