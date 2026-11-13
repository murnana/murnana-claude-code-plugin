# 変更履歴

このプラグインの注目すべき変更はすべてこのファイルに記録します。

フォーマットは [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) に基づいており、
このプラグインは [Semantic Versioning](https://semver.org/spec/v2.0.0.html) に準拠しています。

## [Unreleased]

### Security

- commit スキルの事前許可を `git config *` から読み取りだけの `git config --get *` に絞った。git 設定の書き換えには確認が出る

### Changed

- commit / gitignore スキルで、ユーザーへの質問と承認の確認を必ず AskUserQuestion ツールで行い、未回答の質問は 1 回の呼び出しにまとめるようにした
- commit スキルの description を、スキルが行うことを表す文に書き直した

### Fixed

- gitignore スキルが、冒頭の動的コンテキスト注入の権限チェックで弾かれて起動できないことがあったのを修正した（パイプ先の `head` と素の `grep` が `allowed-tools` に無かったため。`git ls-files` と `git grep --no-index` だけで取得するようにした）
- commit スキルの「Current state」が実際には注入されておらず、「注入済みなので再実行しない」という指示と食い違っていたのを修正した。ブランチ・未ステージ・ステージ済み・直近の履歴を、見出し付きで読み込み時に注入する

## [0.2.1] - 2026-11-01

### Changed

- THIRD_PARTY_NOTICES.md を、同梱している資料の出典・ライセンスと商標だけを書く形に整理した（実行時に参照する資料や利用規約の確認メモを削除）

## [0.2.0] - 2026-10-25

### Added

- murnana/gitignore のテンプレートで `.gitignore` を作成・更新する gitignore スキルを追加した。テンプレートごとに取得元のコミットを記したマーカー付きブロックで書き込むので、あとから `update` で最新に差し替えたり `remove` で外したりできる。ブロック外のユーザー独自の行は承認なしに動かさない

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

[unreleased]: https://github.com/murnana/murnana-claude-code-plugin/compare/8502458...main
[0.2.1]: https://github.com/murnana/murnana-claude-code-plugin/tree/8502458/plugins/murnana-git
[0.2.0]: https://github.com/murnana/murnana-claude-code-plugin/tree/0f332ec/plugins/murnana-git
[0.1.1]: https://github.com/murnana/murnana-claude-code-plugin/tree/795acc0/plugins/murnana-git
[0.1.0]: https://github.com/murnana/murnana-claude-code-plugin/tree/4cf5e55/plugins/murnana-git
[0.0.1]: https://github.com/murnana/murnana-claude-code-plugin/tree/bb469bf/plugins/murnana-git
