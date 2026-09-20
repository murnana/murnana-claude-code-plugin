# murnana-github

GitHub ワークフロー支援プラグイン。

## インストール

```
/plugin marketplace add murnana/murnana-claude-code-plugin
/plugin install murnana-github@murnana-claude-code-plugin
```

`plugin.json` の `defaultEnabled` が `false` なので、インストール後に別途有効化が必要（`/plugin` コマンドから対象プラグインを有効化する）。

## 収録スキル

| スキル | 起動 | 概要 |
|---|---|---|
| [pr-create](pr-create.md) | `/murnana-github:pr-create` | プロジェクトの規約に従い、チェック→push→テンプレート検出→承認を経て PR を作成する |

## ファイル構成

```
plugins/murnana-github/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── pr-create/
        ├── SKILL.md
        └── references/
            ├── project-rules.md
            ├── pr-template-discovery.md
            ├── pr-message.md
            └── gh-fallback-mcp.md
```

## 今後

現時点のスキルは `pr-create` の 1 つのみ。GitHub 関連スキル（issue 対応、PR レビュー、リリースノート作成など）を今後同じプラグインに追加していく想定。追加時はこのディレクトリに `<スキル名>.md` を並べる。
