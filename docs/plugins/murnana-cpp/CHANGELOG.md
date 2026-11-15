# 変更履歴

このプラグインの注目すべき変更はすべてこのファイルに記録します。

フォーマットは [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) に基づいており、
このプラグインは [Semantic Versioning](https://semver.org/spec/v2.0.0.html) に準拠しています。

## [Unreleased]

### Added

- C++ のコードをレビューする review スキル（`/murnana-cpp:review`）を追加した。メモリーリーク・リソースリーク、不具合、プロジェクトのルール違反、命名を確かめて報告する。ファイルは変更しない
- プロジェクトに命名規則がないときは、言語の開発元が使っている命名規則で確かめる
- 同じ基準で独立にレビューする読み取り専用のサブエージェント code-reviewer（`@agent-murnana-cpp:code-reviewer`）を追加した

### Changed

- comment スキルの description と when_to_use を 1 つの短い description にまとめ、常時コンテキストに載る量を減らした

## [0.0.1] - 2026-11-01

### Added

- マーケットプレイスに登録し、公開できる状態にした（ライセンス・リポジトリ情報の追加、インストール手順の修正）

### Changed

- evals をリポジトリルートの `evals/plugins/murnana-cpp/` に移した

[unreleased]: https://github.com/murnana/murnana-claude-code-plugin/compare/8502458...main
[0.0.1]: https://github.com/murnana/murnana-claude-code-plugin/tree/8502458/plugins/murnana-cpp
