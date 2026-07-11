# 精度・プラットフォーム差で詰む典型パターン

## 症状

- Shadertoyで作ったコードを WebGL生に持ってきたら **モバイルだけ画面が真っ黒・ブロック状ノイズ・ガクガク**
- レイマーチングのシーンが、デスクトップChromeでは綺麗、iPhoneのSafariでは表面が破綻
- 大きな `iTime` 経過後、アニメーションが**カクつく・ジャギる**
- `mod(iTime, 6.28)` のような剰余を取っても症状が再発する

## 原因

GLSL ES 1.0(WebGL 1.0)の `mediump float` は **約16bit浮動小数**で、IEEE 754 単精度(32bit)に比べて精度がかなり粗い:

- `mediump` の指数範囲は約 [-14, 14]、仮数は約10bit
- iPhoneのGPU(PowerVR系)は仕様通り mediump で動かすため、デスクトップの highp 動作と差が顕著

特に問題になるのは:

1. **長時間経過後の `uTime`** — 値が大きくなると相対精度が落ち、sin/cos がガタつく
2. **小さいスケールの座標** — 拡大したUV座標で `sin(uv * 1000.0)` 等を計算すると mediump の限界に当たる
3. **法線推定の数値微分** — epsilon が小さすぎると0引き算で精度消失
4. **長距離レイマーチング** — 累積誤差で表面を貫通

## 検出可能なパターン

レビュー時に以下があれば **このgotchaに該当する可能性あり**:

- `precision mediump float;` で `uTime` を使った長時間アニメーション
- `sin(uv.x * <大きな定数>)` のような高周波パターン
- `uv * <大きな定数>`(例: 1000.0以上)を SDF やノイズに渡している
- レイマーチング関数で `MAX_STEPS` が大きい(>128)のに `precision mediump`
- 法線推定の epsilon が極小(1e-4 以下)
- `uniform float uTime;` をそのまま `mod` せずに `sin(uTime * X)` に渡し続けるアニメーション
- Shadertoyから移植したコードで、precision宣言が `mediump` のまま

## 修正パターン

### 修正1: precision を highp に上げる

```glsl
// Before
precision mediump float;

// After
precision highp float;
```

ただしモバイルGPUによっては highp が mediump にフォールバックする実装もある。最も確実な修正と組み合わせるべき。

### 修正2: 時間を周期で剰余する(精度を消費しない)

```glsl
// Before
float t = uTime;
vec3 col = vec3(sin(t), cos(t), sin(t * 0.5));

// After
float t = mod(uTime, 6.28318530718);  // 2π周期
vec3 col = vec3(sin(t), cos(t), sin(t * 0.5));
```

長時間アニメ用には `mod(uTime, LOOP_PERIOD)` を一貫して使う。

### 修正3: 高周波の前にUVを正規化

```glsl
// Before(uv が大きい時に破綻)
float n = sin(uv.x * 1000.0);

// After(まず必要な範囲にfract)
float n = sin(fract(uv.x) * 1000.0 * 6.28318530718);
```

### 修正4: 数値微分のepsilonを精度に合わせる

```glsl
// Before(mediumpでは精度不足)
const float EPS = 0.0001;

// After
#ifdef HIGH_PRECISION
    const float EPS = 0.0001;
#else
    const float EPS = 0.001;
#endif
```

## 関連

- targets/webgl-vanilla.md (precision宣言の必要性)
- targets/shadertoy.md (Shadertoyは自動でhighp相当)
