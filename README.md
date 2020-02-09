# Inkscape 拡張テスト

## 1. インストール

### 1.1 Linux

```
$ git clone ...
$ cd inkscape_test
$ ./setup-linux.sh
```

### 1.2 Mac

???

### 1.3 Windows

以下の２つのファイルを所定のフォルダにコピーする。
(管理権限が必要)

コピーするファイル
* ytani_foo.inx
* ytani_foo.py

コピー先フォルダ
```
C:\Program Files\Inkscape\share\extensions
```


## 2. 使い方

* メニューから以下を選択

[拡張(extensions, エクステンション)]-[ytani]-[工具カバー] 

* ダイヤログにサイズを入力

* 適用してもダイヤログは消えないので、Ctrl-Z(Undo)して何度でも実行可


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
