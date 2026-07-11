# WebGL生 GLSL(GLSL ES 1.0 / WebGL 1.0)

ブラウザの WebGL コンテキストに直接 fragment shader を渡す形式。フレームワーク無し、自前で頂点シェーダーとフルスクリーン四角形を用意する。

## ボイラープレート

### 頂点シェーダー(画面全体を覆う三角形)

```glsl
attribute vec2 aPosition;
void main() {
    gl_Position = vec4(aPosition, 0.0, 1.0);
}
```

JS側で `[-1,-1, 3,-1, -1,3]`(big triangle technique)を流すのが定番。

### フラグメントシェーダー

```glsl
precision mediump float;

uniform vec2 uResolution;
uniform float uTime;
uniform vec2 uMouse;

void main() {
    vec2 uv = gl_FragCoord.xy / uResolution.xy;
    vec3 col = vec3(uv, 0.5 + 0.5 * sin(uTime));
    gl_FragColor = vec4(col, 1.0);
}
```

## 組み込みuniform/関数

GLSL ES 1.0 には Shadertoy のような自動uniformは**無い**。すべて自前で:

| 自前で定義 | 役割 | 推奨型・命名 |
|---|---|---|
| 解像度 | viewport幅高さ | `uniform vec2 uResolution;` |
| 時間 | アニメーション用 | `uniform float uTime;` |
| マウス | インタラクション | `uniform vec2 uMouse;` |
| テクスチャ | 画像・他パスの結果 | `uniform sampler2D uTex;` |

ビルトインで使えるのは `gl_FragCoord`(ピクセル座標)、`gl_FragColor`(出力)、`gl_PointCoord`(point primitive使用時)など。

## 制約・特徴

- **precision宣言は必須**。fragment shaderの先頭に `precision mediump float;`(または `highp`)を必ず書く。書かないとコンパイルエラー。
- ループは**コンパイル時に上限が決まる必要がある**(GLSL ES 1.0の制約)。
  - 動的な break/continue は使えるが、`for(int i=0; i<N; i++)` の N は const か即値である必要がある
- `texture2D(sampler, uv)` を使う(`texture` ではない)。
- 関数定義の前方参照は不可(C言語的に上から順)。
- 配列の動的index は実装依存で動かないことがある(多くの環境で `const int` index しか許されない)。

## デバッグ手段

- ブラウザのコンソールに `gl.getShaderInfoLog(shader)` を出すユーティリティを必ず用意
- 値を色で可視化(Shadertoyと同じ)
- WebGL Inspector / Spector.js を使うとパス間の状態が見える
- mediump で精度足りない時は highp に切り替えて再現性を確認

## 他環境との差分(Shadertoyからの移植時チェックリスト)

| 項目 | 必要な変更 |
|---|---|
| エントリポイント | `mainImage(out vec4 fragColor, in vec2 fragCoord)` → `void main()` |
| 出力先 | `fragColor` → `gl_FragColor` |
| 座標 | `fragCoord` → `gl_FragCoord.xy` |
| 解像度 | `iResolution.xy` → `uResolution`(自前定義必要) |
| 時間 | `iTime` → `uTime`(自前定義必要) |
| precision | `precision mediump float;` を先頭に追加 |
| テクスチャ取得 | `texture(...)` → `texture2D(...)` |

注意: Shadertoyで動いていたコードが mediump で破綻することがある(後述: gotchas/precision-and-platform.md)。
