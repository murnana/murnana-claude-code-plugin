# murnana-claude-code-plugin

murnana が個人利用を目的として管理する Claude Code プラグインマーケットプレイスです。

> **注意:** このマーケットプレイスおよび各プラグインは個人用途で作成・公開されています。  
> **動作保証は一切致しかねます。** 自己責任のもとでご利用ください。

## マーケットプレイスの追加

リポジトリー全体をダウンロードしないよう、シェルから `--sparse` を付けて追加します。

```
claude plugin marketplace add murnana/murnana-claude-code-plugin --sparse .claude-plugin
```

セッション内の `/plugin marketplace add murnana/murnana-claude-code-plugin` でも追加できますが、リポジトリー全体をクローンします。
すでに追加済みの場合は、`claude plugin marketplace remove murnana-claude-code-plugin` で削除してから追加し直してください。

## プラグインのインストール

```
claude plugin install <plugin-name>@murnana-claude-code-plugin
```

各プラグインは、インストール時にそのディレクトリーだけが取得されます。

## 公開プラグイン

| プラグイン | 説明 |
|---|---|
| `murnana-unreal-engine` | Unreal Engine の公式ドキュメント検索 |
| `murnana-git` | Git ワークフロー支援。`/murnana-git:commit` でコミット |
| `murnana-github` | GitHub ワークフロー支援。`/murnana-github:pr-create` で PR 作成、`/murnana-github:stack-create` / `stack-rebase` / `stack-pr-message` で Stacked PR の作成・rebase・メッセージ作成 |
| `murnana-agent-config` | Claude Code の設定作成支援。`/murnana-agent-config:rule-create` でルールファイル作成、`/murnana-agent-config:skill-create` でスキル作成、`/murnana-agent-config:project-instructions-create` で claude.ai Project の指示作成 |
| `murnana-tech-docs` | 技術ドキュメントの作成支援。`/murnana-tech-docs:changelog-write` で Keep a Changelog に沿った CHANGELOG.md の作成・追記 |
| `murnana-unity-package` | Unity Package Manager (UPM) パッケージの保守支援。`/murnana-unity-package:changelog-write` で Unity のバージョニング規則に沿った CHANGELOG.md の作成・追記とリリース（`package.json` の版更新を含む） |
| `murnana-unity` | Unity Editor の操作支援。`/murnana-unity:launch` で Unity プロジェクトを指定プラットフォームで起動（最初に指定したプラットフォームを既定として保存）、`terms-checker` エージェントで Unity の規約への適合を点検 |

## 開発

ブランチ運用やリリース手順は [CONTRIBUTING.md](CONTRIBUTING.md) を参照してください。

## 商標

Unity は Unity Technologies またはその関連会社の米国およびその他の国における商標または登録商標です。
このリポジトリーおよび各プラグインは、Unity Technologies およびその関連会社が後援・提携するものではありません。

サードパーティーの資料と権利表記は、各プラグインの `plugins/<plugin-name>/THIRD_PARTY_NOTICES.md` を参照してください。

## ライセンス

このリポジトリーの内容は [BSD Zero Clause License (0BSD)](LICENSE) で公開します。誰でも自由に使え、改変・再配布でき、権利表記も不要です。動作保証はありません。

ただし、他者の資料を取り込んだ部分は、その権利者のライセンスに従います。該当するものは各プラグインの `THIRD_PARTY_NOTICES.md` に載せています。

## 貢献

外部からの Issue や Pull Request は歓迎しますが、取り入れるかどうかはメンテナーが判断します。必ず取り入れるとは限りません。詳しくは [CONTRIBUTING.md](CONTRIBUTING.md) を参照してください。セキュリティ上の問題は [SECURITY.md](SECURITY.md) に従って報告してください。
