# 変更履歴

このプラグインの注目すべき変更はすべてこのファイルに記録します。

フォーマットは [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) に基づいており、
このプラグインは [Semantic Versioning](https://semver.org/spec/v2.0.0.html) に準拠しています。

## [Unreleased]

### Changed

- ue5-docs スキルのバージョン確認を AskUserQuestion ツールで行い、会話ごとに 1 回だけ聞くようにした
- ue5-docs スキルを手順（バージョンの確定 → 検索 → 回答）ごとに書き直した。`.uproject` の `EngineAssociation` からバージョンを読めるときは質問しない。検索結果に無いことを記憶で補わない
- ue5-docs スキルの description と when_to_use を 1 つの短い description にまとめ、常時コンテキストに載る量を減らした
- 使えない WebFetch を `allowed-tools` から外した

## [0.0.2] - 2026-11-01

### Changed

- THIRD_PARTY_NOTICES.md を、同梱している資料の出典・ライセンスと商標だけを書く形に整理した（実行時に参照する資料や利用規約の確認メモを削除）

## [0.0.1] - 2026-05-17

### Added

- ue5-docs スキル

[unreleased]: https://github.com/murnana/murnana-claude-code-plugin/compare/8502458...main
[0.0.2]: https://github.com/murnana/murnana-claude-code-plugin/tree/8502458/plugins/murnana-unreal-engine
[0.0.1]: https://github.com/murnana/murnana-claude-code-plugin/tree/6c53594/plugins/murnana-unreal-engine
