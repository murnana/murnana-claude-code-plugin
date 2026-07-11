# SDF基礎(Signed Distance Function)

## 概要

ある点から「形状の表面までの最短距離」を返す関数。内部は負、外側は正(または逆)で符号付き。レイマーチングの土台であり、なめらかな形状合成・変形に必須。

## 数式の意図

形状 S に対し SDF d(p) は:

- p が S の外側 → d(p) = (S までの最短距離、正)
- p が S の内側 → d(p) = -(S までの最短距離、負)
- p が S の表面 → d(p) = 0

距離関数なので「形状そのもの」ではなく「空間全体の距離場」を表現している。これにより以下が自然に実現できる:

- **和**(union): `min(d1, d2)` — どちらか近い方
- **積**(intersection): `max(d1, d2)` — 両方含まれる領域
- **差**(subtraction): `max(d1, -d2)` — 1から2を引く
- **smooth blend**: `min` を `smin` に置換

## 最小コード断片(GLSL)

```glsl
// 球(中心原点、半径r)
float sdSphere(vec3 p, float r) {
    return length(p) - r;
}

// 軸並行直方体(半サイズ b)
float sdBox(vec3 p, vec3 b) {
    vec3 q = abs(p) - b;
    return length(max(q, 0.0)) + min(max(q.x, max(q.y, q.z)), 0.0);
}

// なめらかな和(k: ブレンドの広がり)
float smin(float a, float b, float k) {
    float h = max(k - abs(a - b), 0.0) / k;
    return min(a, b) - h * h * k * 0.25;
}

// シーン: 2つの球をなめらかに結合
float scene(vec3 p) {
    float s1 = sdSphere(p - vec3(-0.5, 0.0, 0.0), 0.6);
    float s2 = sdSphere(p - vec3( 0.5, 0.0, 0.0), 0.6);
    return smin(s1, s2, 0.3);
}
```

## 使い所

- レイマーチングのシーン定義(`raymarching-template.md` と組み合わせる)
- 法線推定(数値微分: `normalize(vec3(d(p+e.xyy)-d(p-e.xyy), ...))`)
- アンビエントオクルージョン・ソフトシャドウ
- 2DでもSDFは便利(滑らかな図形合成、エッジのアンチエイリアス)

## 落とし穴

- **本当の距離**を返さないとレイマーチングが破綻する
  - スケーリング `p * 2.0` を SDF 内でやると返り値も補正が必要(`sdSphere(p*s, r) / s`)
  - 非一様変形(剪断・任意行列)を入れると Lipschitz 性が壊れて、レイマーチングのステップが過大になり貫通する
- `smin` の k を大きくしすぎると、形がにじむのではなく**膨らむ**(質量保存しない)
- 距離場のゼロ等高線だけでなく、**勾配が連続**であることもレイマーチングには重要
- パフォーマンス: シーン関数が重いと描画コストが線形に効く。複雑形状はバウンディングで早期return

## 関連

- techniques/raymarching-template.md (TODO: 追加予定)
- techniques/domain-repetition.md (TODO: 追加予定)
- gotchas/precision-and-platform.md
