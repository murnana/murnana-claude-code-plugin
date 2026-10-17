# murnana-github

GitHub ワークフロー支援プラグイン。

## インストール

```
claude plugin marketplace add murnana/murnana-claude-code-plugin --sparse .claude-plugin
claude plugin install murnana-github@murnana-claude-code-plugin
```

`plugin.json` の `defaultEnabled` が `false` なので、インストール後に別途有効化が必要（`/plugin` コマンドから対象プラグインを有効化する）。

## 収録スキル

| スキル | 起動 | 概要 |
|---|---|---|
| [pr-create](pr-create.md) | `/murnana-github:pr-create` | プロジェクトの規約に従い、チェック→push→テンプレート検出→承認を経て PR を作成する |
| [stack-create](stack-create.md) | `/murnana-github:stack-create` | 変更を層に分割する設計→承認→`gh stack init/add`→チェック→`gh stack submit --auto` で Stacked PR を作成する |
| [stack-rebase](stack-rebase.md) | `/murnana-github:stack-rebase` | `gh stack rebase` / `sync` でスタックをカスケード rebase し、コンフリクトを解決して承認後に push する |
| [stack-pr-message](stack-pr-message.md) | `/murnana-github:stack-pr-message` | スタック内の各 PR のタイトル・本文を層ごとに作成し、承認後に `gh pr edit` で反映する |

Stacked PR 系の 3 スキルは [`gh stack`](https://github.com/github/gh-stack) 拡張（`gh extension install github/gh-stack`）を前提とする。

## ファイル構成

```
plugins/murnana-github/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    ├── pr-create/
    │   ├── SKILL.md
    │   └── references/
    │       ├── project-rules.md
    │       ├── pr-template-discovery.md
    │       ├── pr-message.md
    │       └── gh-fallback-mcp.md
    ├── stack-create/
    │   ├── SKILL.md
    │   └── references/
    │       ├── layer-design.md
    │       └── command-reference.md
    ├── stack-rebase/
    │   ├── SKILL.md
    │   └── references/
    │       └── conflict-resolution.md
    └── stack-pr-message/
        ├── SKILL.md
        └── references/
            └── stack-message.md
```

Stacked PR 系スキルは、プロジェクト規約・PR テンプレート探索・フォールバック形式を `pr-create/references/` から `${CLAUDE_PLUGIN_ROOT}` 経由で共有している（同一プラグイン内なので参照が解決できる）。

## 今後

GitHub 関連スキル（issue 対応、PR レビュー、リリースノート作成など）を今後同じプラグインに追加していく想定。追加時はこのディレクトリに `<スキル名>.md` を並べる。
