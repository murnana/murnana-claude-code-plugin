# murnana-tech-docs

技術ドキュメントの作成を支援するプラグイン。

## インストール

```
claude plugin marketplace add murnana/murnana-claude-code-plugin --sparse .claude-plugin
claude plugin install murnana-tech-docs@murnana-claude-code-plugin
```

`plugin.json` の `defaultEnabled` が `false` なので、インストール後に別途有効化が必要（`/plugin` コマンドから対象プラグインを有効化する）。

## 収録スキル

| スキル | 起動 | 概要 |
|---|---|---|
| [changelog-write](changelog-write.md) | `/murnana-tech-docs:changelog-write` | Keep a Changelog の最新版に沿って CHANGELOG.md を作成・追記し、依頼されたときはバージョンを切る |

## ファイル構成

```
plugins/murnana-tech-docs/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── changelog-write/
        ├── SKILL.md
        └── references/
            ├── keep-a-changelog.md
            ├── entry-writing.md
            ├── release.md
            └── project-rules.md
```

## 今後

現時点のスキルは `changelog-write` の 1 つのみ。今後、README や設計ドキュメントなど技術ドキュメントを書くスキルを同じプラグインに追加していく想定。追加時はこのディレクトリに `<スキル名>.md` を並べる。
