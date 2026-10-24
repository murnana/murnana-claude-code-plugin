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

## ファイル構成

```
plugins/murnana-unity/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── launch/
        ├── SKILL.md
        └── references/
            └── editor-cli.md
```
