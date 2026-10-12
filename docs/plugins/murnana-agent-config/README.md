# murnana-agent-config

Claude Code 自体の設定（rules など）の作成を支援するプラグイン。

## インストール

```
/plugin marketplace add murnana/murnana-claude-code-plugin
/plugin install murnana-agent-config@murnana-claude-code-plugin
```

`plugin.json` の `defaultEnabled` が `false` なので、インストール後に別途有効化が必要（`/plugin` コマンドから対象プラグインを有効化する）。

## 収録スキル

| スキル | 起動 | 概要 |
|---|---|---|
| [rule-create](rule-create.md) | `/murnana-agent-config:rule-create` | `.claude/rules/`（プロジェクト）または `~/.claude/rules/`（ユーザー）にルールファイルを作成・更新する |

## ファイル構成

```
plugins/murnana-agent-config/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── rule-create/
        ├── SKILL.md
        └── references/
            ├── rule-format.md
            ├── rule-vs-alternatives.md
            └── rule-content-by-purpose.md
```

## 今後

第一弾として `rule-create` を収録。今後、Claude Code の他の設定（skills、hooks、subagents、CLAUDE.md など）を作成するスキルを同じプラグインに追加していく想定。追加時はこのディレクトリに `<スキル名>.md` を並べる。
