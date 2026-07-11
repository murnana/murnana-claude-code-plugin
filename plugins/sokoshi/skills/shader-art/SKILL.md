---
name: shader-art
description: Shadertoy / WebGL生GLSL でのシェーダー芸(creative coding)に関する技法・パターン・教訓を参照する。fragment shader、GLSL、raymarching、SDF(signed distance function)、procedural noise、fBm、domain repetition、kaleidoscope、glow、bloom、palette、UV manipulation、mainImage関数、gl_FragColor、precision qualifier 等のキーワードが登場する場面、または「シェーダーで〜を描いて」「Shadertoyで動くコードを書いて」「このフラグメントシェーダーをレビューして」「GLSLで〜エフェクトを作って」といった依頼が来た場合は、必ずこのスキルを参照すること。コード生成・レビュー・最適化・移植のいずれの場面でも有用。
---

# shader-art

Shadertoy および WebGL生GLSL でのシェーダー芸に関する知識を、4つのカテゴリで保持しています。タスクに応じて必要なファイルだけを段階的に読んで使ってください。

## 知識カテゴリ

`references/` 配下に4つのサブディレクトリがあります。

| カテゴリ | 用途 | ディレクトリ |
|---|---|---|
| 技法 | 個別の数学・アルゴリズム単位の知識(SDF、レイマーチング、ノイズ等) | `references/techniques/` |
| パターン | 技法を組み合わせた完成形エフェクトのレシピ | `references/patterns/` |
| 教訓 | ハマりどころ・バグ・プラットフォーム差 | `references/gotchas/` |
| 環境 | Shadertoy / WebGL生 等のターゲット環境ごとの定型 | `references/targets/` |

## タスクごとの参照戦略

このスキルでは「全部読む」ことを禁じます。トークン消費が大きいため、以下の戦略で**必要なファイルだけ**を読んでください。

### 戦略1: 新規コード生成

依頼例: 「Shadertoyでレイマーチングの球を描いて」

1. まず `references/targets/` の中から、該当する環境ファイル(Shadertoy なら `shadertoy.md`)を読み、ボイラープレートを確認
2. `references/techniques/` の **ファイル名一覧をlsで取得**
3. 依頼内容に該当しそうな技法ファイルだけを読む(例: `sdf-basics.md`, `raymarching-template.md`)
4. もし複合エフェクト依頼なら `references/patterns/` も同様にファイル名一覧から該当を選ぶ
5. 生成後、`references/gotchas/` のファイル名一覧を見て、該当しそうな教訓があれば最終チェックする

### 戦略2: 既存コードのレビュー

依頼例: 「このフラグメントシェーダーをレビューして」

1. まず対象コードを読み、使われている技法を把握
2. `references/gotchas/` の**ファイル名一覧から、該当しそうな教訓**を選んで読む
3. 必要に応じて `references/techniques/` の該当技法ファイルを読み、誤用がないか確認
4. ターゲット環境が判明していれば `references/targets/` も確認(precision、gl_FragColor等の互換性)
5. 該当しない教訓を**無理に当てはめない** — 該当が無ければ「該当なし」で良い

### 戦略3: コード最適化

1. `references/gotchas/precision-and-platform.md` をまず確認
2. 関連技法の `references/techniques/` を確認(より速い書き方が記載されている可能性)
3. 環境固有の最適化があれば `references/targets/` も参照

### 戦略4: 環境間の移植(Shadertoy ⇔ WebGL生)

1. **両方の環境ファイル** `references/targets/shadertoy.md` と `references/targets/webgl-vanilla.md` を読む
2. 差分(uniform名、エントリポイント、precision宣言、テクスチャ取得 等)を把握して書き換える
3. `references/gotchas/precision-and-platform.md` の互換性教訓を最終チェック

## 段階的読み込みの具体的手順

`references/` を読むときは、まず以下を実行してください:

```
ls references/techniques/
ls references/patterns/
ls references/gotchas/
ls references/targets/
```

ファイル名から内容の見当をつけ、**関連しそうな最大3〜5ファイル**を選んで読みます。すべて読むのは禁止です。

## 知識ファイルの形式

各知識ファイルは決まった構造を持ちます。詳細は `references/_template.md` を参照。重要なのは:

- 技法ファイルは「数式の意図」「最小コード断片」「使い所」「落とし穴」のセクションを持つ
- 教訓ファイルは「症状」「原因」「検出可能なパターン」「修正パターン」のセクションを持つ
- 環境ファイルは「ボイラープレート」「組み込みuniform」「制約」「デバッグ手段」のセクションを持つ

レビュー時には**「検出可能なパターン」セクションだけを先に読む**ことで、ファイル本体を全部読まずに該当判定ができるよう設計されています。

## 利用者拡張(extra_knowledge_path)

`${user_config.extra_knowledge_path}` が設定されている場合、そこも追加の知識ディレクトリとして同じ戦略で扱ってください。利用者個人の知識(Shadertoyアカウントの過去作からの抜粋等)が置かれます。

未設定の場合はこの参照をスキップしてください(エラーにしない)。

## 出力に関する注意

シェーダーコードを生成する際は:

- ターゲット環境が明示されていない場合は **必ずユーザに確認**(Shadertoyかブラウザ生GLSLで定型が違うため)
- precision宣言の要否は環境による(`shadertoy.md` / `webgl-vanilla.md` を参照)
- **動作確認できないコードを「動きます」と断定しない** — 数学的に正しいことと描画が意図通りになることは別
