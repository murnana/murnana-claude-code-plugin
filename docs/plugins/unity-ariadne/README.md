# unity-ariadne

Unity プロジェクトの依存関係グラフ（SQLite）を MCP で照会するプラグインです。`ariadne serve` を MCP サーバーとして登録します。

- 利用者向けの導入手順: [unity-ariadne のマニュアル](https://github.com/murnana/unity-ariadne/blob/main/docs/manual/claude-code-plugin.md)（先に `ariadne` コマンドのインストールが必要です）
- インストール: `claude plugin install unity-ariadne@murnana-claude-code-plugin`

## このリポジトリーでの位置づけ

他のプラグインと違い、プラグイン本体はこのリポジトリーの `plugins/` にはありません。[murnana/unity-ariadne](https://github.com/murnana/unity-ariadne) リポジトリーの `claude-plugins/` にあり、`marketplace.json` のエントリーがそこを指します。

```json
{
  "name": "unity-ariadne",
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/murnana/unity-ariadne.git",
    "path": "claude-plugins"
  },
  "description": "...",
  "version": "x.y.z"
}
```

- `ref` は付けません。他のプラグインと同じく `unity-ariadne` の `main` に追従します。
- `plugins/unity-ariadne/` も `docs/plugins/unity-ariadne/CHANGELOG.md` も作りません。変更履歴は `unity-ariadne` リポジトリーの GitHub Release で管理します。
- `Check plugin versions` ワークフローは `plugins/*/` だけを調べるため、このプラグインは対象外です。バージョンの一致は手で確認します。
- プラグイン名は `unity-ariadne` です（`murnana-<name>` の命名規則の例外）。名前は `unity-ariadne` 側の `plugin.json` の `name` と一致している必要があります。

## unity-ariadne のプラグインを更新したとき

利用者は、`marketplace.json` の `version` 文字列が変わるまでキャッシュ済みのコピーを使い続けます。`unity-ariadne` 側を更新したら、次の手順でこのリポジトリーのエントリーを追従させます。

1. `unity-ariadne` 側のリリース作業（`develop` → `main`、`claude-plugins/.claude-plugin/plugin.json` の `version` 更新、タグ付け）が終わり、`main` に新しい `version` が入っていることを確認します。手順は [unity-ariadne のリリース手順](https://github.com/murnana/unity-ariadne/blob/main/docs/development/release.md) にあります。
   ```sh
   curl -fsSL https://raw.githubusercontent.com/murnana/unity-ariadne/main/claude-plugins/.claude-plugin/plugin.json | jq -r .version
   ```
2. このリポジトリーで `develop`（なければ `main` から作成して push）から `feature/unity-ariadne-<version>` を切ります。
3. `.claude-plugin/marketplace.json` の `unity-ariadne` エントリーの `version` を、手順 1 で確認した値に書き換えます。説明文（`description`）が変わっていれば、`plugin.json` に合わせて直します。
4. `claude plugin validate .` を実行します。`git-subdir` のプラグインは `plugin.json` を読まないので、`version` の一致は目視で確認します。
5. コミットして `develop` 向けに PR を作ります。タイトルとコミットの例: `:bookmark: unity-ariadne を x.y.z に更新する`
6. 利用者に届くのは、`develop` → `main` のリリース PR がマージされた後です（[CONTRIBUTING.md](../../../CONTRIBUTING.md) の「リリースの流れ」）。

`unity-ariadne` が `ariadne` コマンドの新しい版を必要とする変更（MCP ツールの追加など）のときは、利用者が先に `ariadne` を入れ直す必要があります。`unity-ariadne` 側のリリースノートに書かれていることを確認し、必要ならこのプラグインの `description` にも反映します。

## 参照方式を変えるとき

`unity-ariadne` のリリースタグができたら、次の `archive` 形式に切り替えられます。`sha256` で改ざんを検出できるため、`unity-ariadne` のリリース手順は `archive` を推奨しています。

```json
{
  "name": "unity-ariadne",
  "source": {
    "source": "archive",
    "url": "https://github.com/murnana/unity-ariadne/releases/download/vX.Y.Z/unity-ariadne-X.Y.Z-claude-plugin.zip",
    "sha256": "<.sha256 ファイルの値>"
  },
  "version": "X.Y.Z"
}
```

この形式にすると、リリースごとに `url` と `sha256` も更新が必要です。切り替えるときは、このファイルと `.claude/rules/marketplace-manifest.md`（`git-subdir` で `ref` を付けない規則）の例外も合わせて書き換えてください。
