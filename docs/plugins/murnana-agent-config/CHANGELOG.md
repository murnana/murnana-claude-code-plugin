# 変更履歴

このプラグインの注目すべき変更はすべてこのファイルに記録します。

フォーマットは [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) に基づいており、
このプラグインは [Semantic Versioning](https://semver.org/spec/v2.0.0.html) に準拠しています。

## [Unreleased]

## [0.2.0] - 2026-11-14

### Added

- agent-create スキル（サブエージェントを、仕事・置き場所・できること・任せ方のヒアリングを先に行ってから作成・更新する）

### Changed

- rule-create / skill-create スキルで、ユーザーへの質問と承認の確認を必ず AskUserQuestion ツールで行い、未回答の質問は 1 回の呼び出しにまとめるようにした。skill-create のセルフレビューにも、作るスキルが同じ方針に沿っているかの項目を追加した
- project-instructions-create スキルの聞き取りを、ラウンドごとの 3 回から最大 2 回の呼び出しに減らした。既定値で埋められる項目は聞かずに、提示時に既定値として報告する
- skill-create スキルの形式リファレンスに、動的コンテキスト注入で通る複合コマンドの形（リダイレクトと `|| true` のみ）と通らない形（パイプ、`echo`、クォートしない波括弧）を追記した
- rule-create スキルの「Current state」に、最初に実行するコマンドであることを明記した

## [0.1.0] - 2026-11-01

### Added

- project-instructions-create スキル（claude.ai の Project の「指示」を作成・見直す）

### Changed

- skill-create スキルが、プロジェクトの CLAUDE.md やルールで eval の置き場所が決まっている場合はそちらに eval を作るようにした
- THIRD_PARTY_NOTICES.md を、同梱している資料の出典・ライセンスと商標だけを書く形に整理した（実行時に参照する資料や利用規約の確認メモを削除）

## [0.0.1] - 2026-10-12

### Added

- rule-create スキル
- skill-create スキル

[unreleased]: https://github.com/murnana/murnana-claude-code-plugin/compare/03dfea1...main
[0.2.0]: https://github.com/murnana/murnana-claude-code-plugin/tree/03dfea1/plugins/murnana-agent-config
[0.1.0]: https://github.com/murnana/murnana-claude-code-plugin/tree/8502458/plugins/murnana-agent-config
[0.0.1]: https://github.com/murnana/murnana-claude-code-plugin/tree/278ceff/plugins/murnana-agent-config
