# 変更履歴

このプラグインの注目すべき変更はすべてこのファイルに記録します。

フォーマットは [Keep a Changelog](https://keepachangelog.com/en/2.0.0/) に基づいており、
このプラグインは [Semantic Versioning](https://semver.org/spec/v2.0.0.html) に準拠しています。

## [Unreleased]

### Changed

- changelog-write スキルで、ユーザーへの質問と承認の確認を必ず AskUserQuestion ツールで行い、未回答の質問は 1 回の呼び出しにまとめるようにした。新規作成時の言語は聞かずに会話の言語を使い、振る舞いとして書けない変更の扱いは承認の確認と同じ呼び出しで聞く

## [0.0.2] - 2026-11-01

### Changed

- THIRD_PARTY_NOTICES.md を、同梱している資料の出典・ライセンスと商標だけを書く形に整理した（実行時に参照する資料や利用規約の確認メモを削除）

## [0.0.1] - 2026-10-24

### Added

- Keep a Changelog の最新版に沿って CHANGELOG.md を作成・追記し、依頼されたときにバージョンを切れる changelog-write スキルを追加した

[unreleased]: https://github.com/murnana/murnana-claude-code-plugin/compare/8502458...main
[0.0.2]: https://github.com/murnana/murnana-claude-code-plugin/tree/8502458/plugins/murnana-tech-docs
[0.0.1]: https://github.com/murnana/murnana-claude-code-plugin/tree/05c5eaa/plugins/murnana-tech-docs
