# sokoshi

Shadertoy / WebGL生GLSL でのシェーダー芸を、Claude Codeに「学習させる」ためのプラグインです。

技法(SDF・レイマーチング・ノイズ等)、パターン(エフェクトレシピ)、ハマりどころ(精度・プラットフォーム差)、ターゲット環境ごとの定型を、Markdownの知識ファイルとして蓄積します。Claude Codeはこの知識を参照しながらコード生成・レビューを行います。

## インストール

```
/plugin marketplace add <your-repo>
/plugin install shader-art-knowledge@<marketplace-name>
```

## 知識の追加方法

知識は3つのカテゴリに分かれています。それぞれ`skills/shader-art/references/`配下にMarkdownを追加してください。

- `techniques/` — 個別技法(SDF、ノイズ、ドメイン操作 等)
- `patterns/` — 技法を組み合わせたエフェクトレシピ(グロー、万華鏡 等)
- `gotchas/` — ハマりどころ・教訓(精度問題、プラットフォーム差 等)
- `targets/` — ターゲット環境ごとの定型(Shadertoy、WebGL生 等)

各ファイルのテンプレートは `references/_template.md` を参照してください。

## 自分専用の追加知識を持ちたい場合

プラグイン本体に手を入れず、`extra_knowledge_path` を設定してください。指定したディレクトリのMarkdownも併せて参照されます。

```
/plugin config shader-art-knowledge
```

## 動作の概要

1. ユーザがシェーダー関連の指示を出す(例: 「Shadertoyで使えるレイマーチングのテンプレを書いて」)
2. Claude Codeが`shader-art`スキルを起動
3. SKILL.mdの指示に従い、`references/`の関連ファイルを段階的に読む
4. 読んだ知識に基づいてコード生成・レビューを行う

## ライセンス

MIT
