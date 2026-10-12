# murnana-agent-config

Claude Code 自体の設定（rules、skills など）の作成を支援するプラグイン。

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
| [skill-create](skill-create.md) | `/murnana-agent-config:skill-create` | `.claude/skills/`（プロジェクト）、`~/.claude/skills/`（個人）、またはプラグインの `skills/` にスキルを作成・更新し、評価の雛形も作る |

## ファイル構成

```
plugins/murnana-agent-config/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    ├── rule-create/
    │   ├── SKILL.md
    │   └── references/
    │       ├── rule-format.md
    │       ├── rule-vs-alternatives.md
    │       └── rule-content-by-purpose.md
    └── skill-create/
        ├── SKILL.md
        └── references/
            ├── skill-format.md
            ├── skill-vs-alternatives.md
            ├── writing-guide.md
            └── evals.md
```

## 今後

現在は `rule-create` と `skill-create` を収録している。今後、Claude Code の他の設定（hooks、subagents、CLAUDE.md など）を作成するスキルを同じプラグインに追加していく想定。追加時はこのディレクトリに `<スキル名>.md` を並べる。
