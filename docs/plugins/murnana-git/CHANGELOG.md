# 変更履歴

このプラグインの注目すべき変更はすべてこのファイルに記録します。

フォーマットは [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) に基づいており、
このプラグインは [Semantic Versioning](https://semver.org/spec/v2.0.0.html) に準拠しています。

## [Unreleased]

## [0.1.1] - 2026-10-25

### Fixed

- commit スキルの PostToolUse Hook が短縮ハッシュ（`git log --oneline`）を返していたため、完全なハッシュを返すよう修正

## [0.1.0] - 2026-10-17

### Changed

- commit スキルのコミット結果確認を PostToolUse Hook に移した

## [0.0.1] - 2026-09-18

### Added

- commit スキル

### Fixed

- コミット0件のリポジトリで commit スキルが起動できない不具合

[unreleased]: https://github.com/murnana/murnana-claude-code-plugin/compare/795acc0...main
[0.1.1]: https://github.com/murnana/murnana-claude-code-plugin/tree/795acc0/plugins/murnana-git
[0.1.0]: https://github.com/murnana/murnana-claude-code-plugin/tree/4cf5e55/plugins/murnana-git
[0.0.1]: https://github.com/murnana/murnana-claude-code-plugin/tree/bb469bf/plugins/murnana-git
