# 変更履歴

このプラグインの注目すべき変更はすべてこのファイルに記録します。

フォーマットは [Keep a Changelog](https://keepachangelog.com/en/2.0.0/) に基づいており、
このプラグインは [Semantic Versioning](https://semver.org/spec/v2.0.0.html) に準拠しています。

## [Unreleased]

## [0.0.2] - 2026-10-24

### Changed

- changelog-write スキルが Unity Manual（docs.unity3d.com）を自動で取得しないようにした。Unity 利用規約 §17.2 が自動手段によるサイトへのアクセスを制限しているため。references の Unity の規則が古そうなときは、出典の Manual ページを案内してユーザーに確認してもらう

## [0.0.1] - 2026-10-24

### Added

- Unity Package Manager (UPM) パッケージの CHANGELOG.md を、Keep a Changelog と Unity のバージョニング規則に沿って作成・追記できる changelog-write スキルを追加した。依頼されたときはバージョンを切り、`package.json` の `version` も更新する

[unreleased]: https://github.com/murnana/murnana-claude-code-plugin/compare/c013a3e...main
[0.0.2]: https://github.com/murnana/murnana-claude-code-plugin/tree/main/plugins/murnana-unity-package
[0.0.1]: https://github.com/murnana/murnana-claude-code-plugin/tree/c013a3e/plugins/murnana-unity-package
