# 変更履歴

このプラグインの注目すべき変更はすべてこのファイルに記録します。

フォーマットは [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) に基づいており、
このプラグインは [Semantic Versioning](https://semver.org/spec/v2.0.0.html) に準拠しています。

## [Unreleased]

## [0.2.0] - 2026-10-20

### Changed

- pr-create スキル: 現在のブランチが `gh stack` のスタックに属する場合（`gh stack view --short` で検出）、`git push` / `gh pr create` の代わりに `gh stack submit --auto` と `gh pr edit` で PR を作成するようにした

## [0.1.0] - 2026-10-17

### Added

- Stacked PR 用スキル（stack-create / stack-rebase / stack-pr-message）

## [0.0.1] - 2026-09-20

### Added

- pr-create スキル

[unreleased]: https://github.com/murnana/murnana-claude-code-plugin/compare/014d844...main
[0.2.0]: https://github.com/murnana/murnana-claude-code-plugin/tree/014d844/plugins/murnana-github
[0.1.0]: https://github.com/murnana/murnana-claude-code-plugin/tree/4cf5e55/plugins/murnana-github
[0.0.1]: https://github.com/murnana/murnana-claude-code-plugin/tree/40e2dd2/plugins/murnana-github
