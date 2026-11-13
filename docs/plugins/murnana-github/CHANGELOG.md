# 変更履歴

このプラグインの注目すべき変更はすべてこのファイルに記録します。

フォーマットは [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) に基づいており、
このプラグインは [Semantic Versioning](https://semver.org/spec/v2.0.0.html) に準拠しています。

## [Unreleased]

### Removed

- pr-create / stack-pr-message スキルから、PR 本文の末尾に `🤖 Generated with [Claude Code]` の行を付ける指示を削除した

### Security

- pr-create / stack-create スキルの事前許可を絞った。`git config` と `git remote` は読み取りだけ、`git branch` は現在のブランチ名の取得だけ、`git push` は素の push と `-u origin <branch>` だけを許可する。force-push、リモートやブランチの変更・削除、git 設定の書き換えには確認が出る

### Changed

- pr-create / stack-create / stack-pr-message / stack-rebase スキルで、ユーザーへの質問と承認の確認を必ず AskUserQuestion ツールで行い、未回答の質問は 1 回の呼び出しにまとめるようにした
- pr-create スキルの description を、スキルが行うことを表す文に書き直した
- pr-create スキルの push 手順を、upstream の有無ごとに実行するコマンドを明記する形にした

### Fixed

- pr-create / stack-create / stack-pr-message / stack-rebase スキルの「Current state」が、注入されない通常のコードブロックなのに「上の出力を見る」前提で書かれていたのを修正した。最初に各コマンドを実行する手順として明記し、`gh stack view` は終了コードが読めるよう `|| true` を付けずに実行する
- pr-create スキルの本文が、テンプレートが無いときの見出しを「理由」と書いていたのを、references と同じ「なぜ」に揃えた

## [0.2.1] - 2026-11-01

### Changed

- THIRD_PARTY_NOTICES.md を、同梱している資料の出典・ライセンスと商標だけを書く形に整理した（実行時に参照する資料や利用規約の確認メモを削除）

## [0.2.0] - 2026-10-20

### Changed

- pr-create スキル: 現在のブランチが `gh stack` のスタックに属する場合（`gh stack view --short` で検出）、`git push` / `gh pr create` の代わりに `gh stack submit --auto` と `gh pr edit` で PR を作成するようにした

## [0.1.0] - 2026-10-17

### Added

- Stacked PR 用スキル（stack-create / stack-rebase / stack-pr-message）

## [0.0.1] - 2026-09-20

### Added

- pr-create スキル

[unreleased]: https://github.com/murnana/murnana-claude-code-plugin/compare/8502458...main
[0.2.1]: https://github.com/murnana/murnana-claude-code-plugin/tree/8502458/plugins/murnana-github
[0.2.0]: https://github.com/murnana/murnana-claude-code-plugin/tree/014d844/plugins/murnana-github
[0.1.0]: https://github.com/murnana/murnana-claude-code-plugin/tree/4cf5e55/plugins/murnana-github
[0.0.1]: https://github.com/murnana/murnana-claude-code-plugin/tree/40e2dd2/plugins/murnana-github
