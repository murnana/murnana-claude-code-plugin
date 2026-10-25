# 変更履歴

このプラグインの注目すべき変更はすべてこのファイルに記録します。

フォーマットは [Keep a Changelog](https://keepachangelog.com/en/2.0.0/) に基づいており、
このプラグインは [Semantic Versioning](https://semver.org/spec/v2.0.0.html) に準拠しています。

## [Unreleased]

## [0.2.0] - 2026-10-25

### Added

- launch スキルが起動後に Editor の応答を待つようにした。`unity status --until-ready` で ready になるまで待ち、Unity MCP や `unity command` が使える状態になってから作業を始める。`com.unity.pipeline` が未導入のときは待機を省いてその旨だけ報告し（導入は案内しない）、Safe Mode のとき、ダイアログで止まっているときは待たずに原因を伝える

### Changed

- launch スキルが Editor 起動時に `-logFile` で `<プロジェクト>/Logs/Editor_<yyyyMMdd_HHmmss>.log` を指定するようにした。起動コマンド実行時の日時をファイル名にするため、他の Unity とログが混ざらない。ユーザーが別の `-logFile` を求めたときはそちらを使う
- launch スキルの起動前に `date` を別コマンドで実行し、結果をリテラルとして埋め込むようにした。`unity open --args` の分割規則が不明なため、パスに空白があるときは Editor 本体を直接起動する。起動完了の待機には `unity status --timeout` を使う
- launch スキルの `allowed-tools` に、Windows の既定パスにある Editor（`Unity.exe`）の直接起動を許可するパターンを追加した（Git Bash 形式の `/c/Program Files/…` と `C:/Program Files/…` の両方）。起動コマンドは実行ファイルのパスを引用符で囲むため、macOS・Linux・Windows のすべてについて引用符つきのパターンも追加した

## [0.1.0] - 2026-10-24

### Changed

- launch スキルが Unity のドキュメント（docs.unity3d.com、docs.unity.com）を自動で取得しないようにした。Unity 利用規約 §17.2 が自動手段によるサイトへのアクセスを制限しているため。引数を確かめたいときは `unity open --help` を使うか、該当バージョンのページ URL を案内してユーザーに確認してもらう

### Added

- Unity 関連のツール、Claude Code プラグイン、UPM パッケージ、Unity プロジェクトが Unity の規約に違反していないかを点検する terms-checker エージェントを追加した。最新の Unity 利用規約、Editor Software Terms、商標ガイドライン、Package Guidelines、Manual の利用条件を毎回取得して照合し、該当条項と対処案を報告する。判定は「規約への当てはまり方」と「影響の大きさ」の 2 軸で示し、規約に関する記述には出典タグを付ける。引用は取得した本文と照合し、前提条件（Unity との契約や配布形態など）も報告に明記する。ファイルは編集しない

## [0.0.1] - 2026-10-24

### Added

- Unity プロジェクトを指定したプラットフォームで Unity Editor に開く launch スキルを追加した。Unity CLI で Editor の検索・インストールを行い、Editor 本体の `-projectPath` と `-buildTarget` で起動する。最初に指定したプラットフォームをプロジェクトの既定として保存し、指定がなければそれを使う

[unreleased]: https://github.com/murnana/murnana-claude-code-plugin/tree/main/plugins/murnana-unity
[0.2.0]: https://github.com/murnana/murnana-claude-code-plugin/tree/main/plugins/murnana-unity
[0.1.0]: https://github.com/murnana/murnana-claude-code-plugin/tree/main/plugins/murnana-unity
[0.0.1]: https://github.com/murnana/murnana-claude-code-plugin/tree/b55cccb/plugins/murnana-unity
