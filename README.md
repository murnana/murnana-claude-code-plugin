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
| `murnana-agent-config` | Claude Code の設定作成支援。`/murnana-agent-config:rule-create` でルールファイル作成、`/murnana-agent-config:skill-create` でスキル作成 |
| `murnana-tech-docs` | 技術ドキュメントの作成支援。`/murnana-tech-docs:changelog-write` で Keep a Changelog に沿った CHANGELOG.md の作成・追記 |

## ライセンス

このリポジトリのコードおよびプラグインは、特に明示のない限り個人利用を前提として提供されます。
