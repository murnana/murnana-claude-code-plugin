# murnana-unity

Unity Editor の操作を支援するプラグイン。

## インストール

```
claude plugin marketplace add murnana/murnana-claude-code-plugin --sparse .claude-plugin
claude plugin install murnana-unity@murnana-claude-code-plugin
```

`plugin.json` の `defaultEnabled` が `false` なので、インストール後に別途有効化が必要（`/plugin` コマンドから対象プラグインを有効化する）。

## 収録スキル

| スキル | 起動 | 概要 |
|---|---|---|
| [launch](launch.md) | `/murnana-unity:launch [プラットフォーム] [プロジェクトパス]`（手動起動のみ。Claude が自動では起動しない） | Unity プロジェクトを、指定したプラットフォーム（`-buildTarget`）で Unity Editor に開く。最初に指定したプラットフォームをプロジェクトの既定として保存する |

## 収録エージェント

| エージェント | 起動 | 概要 |
|---|---|---|
| [terms-checker](terms-checker.md) | 「Unity の規約に違反していないか確認して」などの依頼で Claude が委任、または `@murnana-unity:terms-checker` | Unity 関連のツール・プラグイン・パッケージ・プロジェクトを、最新の Unity 利用規約、Editor Software Terms、商標ガイドラインなどと照合し、条項つきでリスクを報告する（読み取り専用） |

## ファイル構成

```
plugins/murnana-unity/
├── .claude-plugin/
│   └── plugin.json
├── agents/
│   └── terms-checker.md
└── skills/
    └── launch/
        ├── SKILL.md
        └── references/
            └── editor-cli.md
```

## 商標

Unity は Unity Technologies またはその関連会社の米国およびその他の国における商標または登録商標です。
このプラグインは、Unity Technologies およびその関連会社が後援・提携するものではありません。
