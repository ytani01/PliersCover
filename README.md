# Inkscape extension: 工具カバー型紙自動作成

## 概要

ラジオペンチやニッパーなどの工具のカバーの型紙を自動作成する
Inkscape用のエクステンション(拡張機能)です。

各部分のサイズを入力すると、レーザーカッター用の型紙を自動作成します。
ライブビュー機能を利用すると、画面上で形を確認しながらサイズ調整できます。

角に必ず針穴が来るように自動調整されます。

Inkscapeなので、もちろん、自動生成したあとに、追加・修正は自由にできます。


## 1. インストール

### 1.0 Inkscape

``Inkscape`` の拡張機能なので、まずは、``Inkscape`` をインストールして下さい。

=> [Inkscape 公式サイト](https://inkscape.org/ja/)


### 1.1 ダウンロード

サイトのURL

```
https://github.com/ytani01/PlierCover/
```


#### 1.1.1 ZIPファイルをダウンロードして展開する方法

![](docs/github1.png)


#### 1.1.2 Gitリポジトリをクローン(clone)する方法

* 通常のやり方

```bash
$ git clone https://github.com/ytani01/PlierCover.git
```

* githubにsshの設定をしている場合、以下の方法でも可

```bash
$ git clone git@github.com:ytani01/PlierCover.git
```


### 1.2 ファイルのコピー

以下の２つのファイルを所定のフォルダにコピーする。

コピーするファイル
* plier_cover.inx
* plier_cover.py


#### 1.2.1 Linux

コピー先ディレクトリ(フォルダ)
* ユーザー毎
```
~/.config/inkscape/extensions
```

``setup.sh`` で自動的に上記ディレクトにコピーすることができます。
```bash
$ ./setup-linux.sh
```

* 全ユーザー(管理者権限が必要)
```
/usr/share/inkscape/extensions
```


#### 1.2.2 Mac

linuxと同じ？？


#### 1.2.3 Windows

コピー先フォルダ

* ユーザー毎
```
C:\Users\ユーザー名\AppData\Roaming\inkscape\extensions
```

* 全ユーザー(管理者権限が必要)
```
C:\Program Files\Inkscape\share\extensions)
```


## 2. 使い方

* メニューから以下を選択

[拡張(extensions, エクステンション)]-[ytani]-[工具カバー] 

![menu](docs/inkscape1.png)

* ダイヤログにサイズを入力

![Inkscape extension: 工具カバー](docs/inkscape2.png)

* ``[ライブビュー]`` をチェックすると、画面で確認しながらサイズを調整できます。

* ``[Apply(適用)]`` をクリックすると、確定されて、キャンパスに描画されます。
(ダイヤログは自動的に閉じません。)


### 2.1 注意・コツなど

* ``[Apply(適用)]`` を何度もクリックすると、クリックした回数重ね描きされます。
([編集]-[元に戻す]、または、[Ctrl]-[Z]で、元に戻すことができます。)

* ``[ライブビュー]``がチェックされている状態では、
画面の拡大縮小などの操作ができません。
拡大率や表示位置などを調整したい場合は、
一旦、``[ライブビュー]``のチェックをはずして下さい。

* 角に、針穴が来るように自動調節するので、針穴の間隔が多少不揃いになります。
縫いしろや針穴のパラメータを微調整調整して、
針穴がきれいに並ぶようにしましょう。



## A. Memo

### A.1 SVG パスのコマンド

```
(大文字: 絶対座標、小文字: 相対座標)

M: moveto (始点座標)
L: lineto
  H: 水平
  V: 垂直
C: curveto: "{C|c} c1x,c1y c2x,c2y x,y"
  (c1x, c1y), (c2x, c2y): 制御点
  x,y: 終点

  * 正円(半円)の場合、制御点までの距離は、直径の約0,75倍(?)
Z: closepath
```

```
ex: d="M 50,60 H 60 l 20,50 Z"
```


### A.2 Inkscape extension 描画

#### 基本書式

```python
import inkex
import simplestyle

inkex.localize()

class Foo(inkex.Effect):
    def __init__(self):
	    inkex.Effect.__init__(self)
		self.OptionParser.add_option("--opt", action="store", type="float",dest="opt", help="...")
		

    def effect(self):
	    :
		
```

現在のレイヤーに、``object``を描画。

* ``style``: 線のスタイル、
* ``attribute``: 座標、サイズ
* ``inkex.addNS()``: 図形の種類(長方形、円、パスなど)と形式(SVGなど)


ex.1
```python
parent = self.current_layer
style = { ... }
attribute = { ... }
object = inkex.etree.SubElement(parent,
	inkex.addNS('rect', 'svg'),
	attribute)
```

#### style: 線のスタイル
ex.1
```python
style = {
  'stroke': '#000000',
  'stroke-width': '0.2',
  'fill': 'none'
}
```


#### attributes: 座標、サイズ

ex.1: rect
```python
attribs_rect = {
  'style': simplestyle.formatStyle(style),
  'width': '30',
  'height': '20',
  'x': '100',
  'y': '200'
}
```

ex.2: circle
```python
attribs_circle = {
  'style': simplestyle.formatStyle(style),
  'r': '100',
  'cx': '150',
  'cy': '200'
}
```

ex.3: path
```python
attribs_path = {
  'style': simplestyle.formatStyle(style),
  'd': 'M 50,60 H 60 l 20,50 Z'
}
```
