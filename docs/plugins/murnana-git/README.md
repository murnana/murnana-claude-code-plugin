# murnana-git

Git ワークフロー支援プラグイン。

## インストール

```
/plugin marketplace add murnana/murnana-claude-code-plugin
/plugin install murnana-git@murnana-claude-code-plugin
```

`plugin.json` の `defaultEnabled` が `false` なので、インストール後に別途有効化が必要（`/plugin` コマンドから対象プラグインを有効化する）。

## 収録スキル

| スキル | 起動 | 概要 |
|---|---|---|
| [commit](commit.md) | `/murnana-git:commit` | プロジェクトの規約に従い、Why 単位でコミットする |

## ファイル構成

```
plugins/murnana-git/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── commit/
        ├── SKILL.md
        └── references/
            ├── commit-message.md
            └── project-rules.md
```

## 今後

現時点のスキルは `commit` の 1 つのみ。今後 Git 関連のスキルを同じプラグインに追加していく想定。追加時はこのディレクトリに `<スキル名>.md` を並べる。
