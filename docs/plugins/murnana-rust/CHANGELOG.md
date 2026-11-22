# 変更履歴

このプラグインの注目すべき変更はすべてこのファイルに記録します。

フォーマットは [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) に基づいており、
このプラグインは [Semantic Versioning](https://semver.org/spec/v2.0.0.html) に準拠しています。

## [Unreleased]

## [0.1.0] - 2026-11-22

### Added

- Rust のコードをレビューする review スキル（`/murnana-rust:review`）を追加した。メモリーリーク・リソースリーク、不具合、プロジェクトのルール違反、命名を確かめて報告する。ファイルは変更しない
- プロジェクトに命名規則がないときは、言語の開発元が使っている命名規則で確かめる
- 同じ基準で独立にレビューする読み取り専用のサブエージェント code-reviewer（`@agent-murnana-rust:code-reviewer`）を追加した
- `/murnana-rust:test-case` スキルを追加した。テストリストを先に書き、1 つずつテストにして、失敗するところを一度確かめてから報告する
- `test-case-writer` サブエージェントを追加した。すでにあるプログラムのテストを別の Claude に任せて、報告だけを受け取れる

### Changed

- `plugin.json` の `version` を外す変更を取りやめ、マーケットプレイスのエントリーと同じ値を `plugin.json` にも書くようにした

## [0.0.2] - 2026-11-14

### Changed

- comment スキルの description と when_to_use を 1 つの短い description にまとめ、常時コンテキストに載る量を減らした
- `allowed-tools` の Bash 指定を、旧式の `:*` から ` *` に揃えた

## [0.0.1] - 2026-11-01

### Added

- マーケットプレイスに登録し、公開できる状態にした（ライセンス・リポジトリ情報の追加、インストール手順の修正）

### Changed

- evals をリポジトリルートの `evals/plugins/murnana-rust/` に移した

[unreleased]: https://github.com/murnana/murnana-claude-code-plugin/compare/894f706...main
[0.1.0]: https://github.com/murnana/murnana-claude-code-plugin/tree/894f706/plugins/murnana-rust
[0.0.2]: https://github.com/murnana/murnana-claude-code-plugin/tree/03dfea1/plugins/murnana-rust
[0.0.1]: https://github.com/murnana/murnana-claude-code-plugin/tree/8502458/plugins/murnana-rust
