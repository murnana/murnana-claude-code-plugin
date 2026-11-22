# 変更履歴

このプラグインの注目すべき変更はすべてこのファイルに記録します。

フォーマットは [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) に基づいており、
このプラグインは [Semantic Versioning](https://semver.org/spec/v2.0.0.html) に準拠しています。

## [Unreleased]

## [0.3.0] - 2026-11-22

### Changed

- skill-create スキルが、プロジェクトの CLAUDE.md・AGENTS.md・`.claude/rules/` を最初に集め、そこにあるルールをスキルの既定より優先するようにした。適用したルールは表にして、承認を求めるときに示す
- skill-create スキルが、設計の前にスキルの公式ドキュメントと、作るスキルが扱うツールの公式ドキュメントを調べ、その結果（出典 URL つき）を下書きと提示内容に反映するようにした
- skill-create スキルが作るスキルを、Haiku や Sonnet でも手順を飛ばさずに動くように書くようにした（番号付きの手順、結果ごとの分岐、既定値、完了条件）。書き方ガイドにその節を追加し、Haiku / Sonnet での確認方法と評価の実行方法も案内する
- skill-create スキル自身の手順も、Haiku や Sonnet で実行しても迷わない書き方に改めた
- skill-create スキルが作るスキルを Claude Code 専用とし、claude.ai や Skills API と共通の項目・上限に合わせないようにした
- skill-create スキルが作るスキルの `description` を、スキルが何かを表す短い一文だけにした。発動条件は `when_to_use` に箇条書きし、2つ合わせて約100トークン以内に収める
- skill-create スキルが、作るスキルの手順にトークンを節約する工夫（出力を絞る、必要な範囲だけ読む、冗長な作業をサブエージェントに任せるなど）を入れるようにした。ベストプラクティスの調査でも、トークンを減らす方法を調べる
- skill-create スキル自身も、自動で読み込まれている CLAUDE.md やルールを読み直さないなど、使うトークンを減らした
- `plugin.json` の `version` を外す変更を取りやめ、マーケットプレイスのエントリーと同じ値を `plugin.json` にも書くようにした

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

[unreleased]: https://github.com/murnana/murnana-claude-code-plugin/compare/78b9359...main
[0.3.0]: https://github.com/murnana/murnana-claude-code-plugin/tree/78b9359/plugins/murnana-agent-config
[0.2.0]: https://github.com/murnana/murnana-claude-code-plugin/tree/03dfea1/plugins/murnana-agent-config
[0.1.0]: https://github.com/murnana/murnana-claude-code-plugin/tree/8502458/plugins/murnana-agent-config
[0.0.1]: https://github.com/murnana/murnana-claude-code-plugin/tree/278ceff/plugins/murnana-agent-config
