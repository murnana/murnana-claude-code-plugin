# Shadertoy

ブラウザ上で動く GLSL fragment shader 実行環境(https://www.shadertoy.com)。

## ボイラープレート

```glsl
void mainImage(out vec4 fragColor, in vec2 fragCoord)
{
    vec2 uv = fragCoord / iResolution.xy;        // [0,1]
    // または中央原点・アスペクト補正:
    // vec2 p = (2.0 * fragCoord - iResolution.xy) / iResolution.y;

    vec3 col = vec3(uv, 0.5 + 0.5 * sin(iTime));
    fragColor = vec4(col, 1.0);
}
```

エントリポイントは `mainImage`。`gl_FragCoord` ではなく引数の `fragCoord` を使う。`gl_FragColor` ではなく out 引数の `fragColor` に書き込む。

## 組み込みuniform

| 名前 | 型 | 内容 |
|---|---|---|
| `iResolution` | vec3 | 描画解像度(xy)とピクセルアスペクト(z) |
| `iTime` | float | 経過秒 |
| `iTimeDelta` | float | 直前フレームからの経過秒 |
| `iFrame` | int | フレーム番号 |
| `iMouse` | vec4 | xy=現在座標(クリック時)、zw=クリック開始座標 |
| `iChannel0`〜`iChannel3` | sampler2D 等 | テクスチャ・他バッファ参照(設定で割り当て) |
| `iDate` | vec4 | year, month, day, time-in-sec |

## 制約・特徴

- **precision宣言は不要**(自動で `highp` 相当が付く)。WebGL生に移植する時は手動で付ける必要がある。
- マルチパスは `Buffer A`〜`Buffer D` の追加タブで実現。
- `texture` 関数(GLSL ES 3.0風)が使える。`texture2D` も互換のため使える。
- `#define` でのプリプロセス、`const` 配列の初期化が可能。
- 自前で頂点シェーダを書くことはできない(常に画面全体の三角形)。

## デバッグ手段

- 値を色として可視化する
  ```glsl
  fragColor = vec4(vec3(myValue), 1.0);  // myValueを白〜黒で表示
  fragColor = vec4(myUV.x, myUV.y, 0.0, 1.0);  // UVを赤緑で
  ```
- NaN/Infが出ると **真っ黒**になる(色がclampされ表示されない)ので、急に黒くなったら数値破綻を疑う
- `iMouse` を使ってインタラクティブに探索する
- ループ内に `if(iFrame > N) break;` を入れて段階確認

## 他環境との差分(WebGL生への移植時チェックリスト)

| 項目 | Shadertoy | WebGL生(GLSL 1.0) |
|---|---|---|
| エントリポイント | `void mainImage(out vec4, in vec2)` | `void main()` |
| 出力 | `fragColor` 引数 | `gl_FragColor` |
| 入力座標 | `fragCoord` 引数 | `gl_FragCoord` |
| precision | 不要 | `precision mediump float;` 等が必須 |
| 解像度uniform | `iResolution` 自動 | 自前で `uniform vec2 uResolution;` |
| 時間uniform | `iTime` 自動 | 自前で `uniform float uTime;` |
| テクスチャ関数 | `texture` 推奨 | `texture2D`(GLSL ES 1.0) |

詳細は `webgl-vanilla.md` を参照。
