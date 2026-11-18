# CONTRIBUTING

このリポジトリーの開発フローをまとめます。Claude Code 向けの詳細なルールは `.claude/rules/` にあります。

> このリポジトリーは個人利用を目的としており、動作保証は一切ありません。

## 貢献について

- Issue や Pull Request は歓迎しますが、取り入れるかどうかはメンテナーが判断します。必ず取り入れるとは限りません。
- 返信や対応の期限は約束できません。取り入れない場合は、理由を短く書いて閉じることがあります。
- 大きな変更は、先に Issue で相談してください。
- 貢献された内容は、このリポジトリーと同じ [0BSD](LICENSE) で公開されるものとして扱います。
- Pull Request は `develop` に向けてください。ブランチ運用は下の「ブランチ運用」に従います。

## ブランチ運用

| ブランチ | 役割 |
|---|---|
| `main` | 公開状態。正式版のマーケットプレイス（`murnana-claude-code-plugin`）は `main` から配布されます |
| `develop` | 開発の統合先。リリース前の変更が集まり、アーリーアクセス版のマーケットプレイス（`murnana-claude-code-plugin-dev`）から配布されます |
| `feature/*` | 機能追加・変更・ドキュメント更新用。`develop` から切ります |
| `bugfix/*` | バグ修正用。`develop` から切ります |
| `hotfix/*` | リリース済みの `main` の緊急修正用。`main` から切ります |

ブランチ名は `<種別>/<topic>` で、topic は英小文字とハイフンで短く書きます（例: `feature/unity-launch`）。

`main` と `develop` には直接コミットしません。

### hotfix

リリース済みの内容に緊急の問題があるときだけ使います。

1. `main` から `hotfix/<topic>` を切って修正し、変更したプラグインのパッチバージョンを同じ PR で上げます（`marketplace.json` のエントリーと CHANGELOG）。
2. `claude plugin validate .` を実行し、`main` 向けに PR を作ってマージします。
3. 修正とバージョン更新が失われないよう、すぐに `main` を `develop` にマージします。

## コミットメッセージ

`murnana-git` プラグインの `commit` スキルに準じます。スキルが更新されたときは、このセクションと `.claude/rules/commit-message.md` も合わせて直します。

- 先頭に gitmoji（GitHub の絵文字コード）を付けた短い題名（約 50 字）を日本語で書きます。例: `:memo: インストール手順にマーケットプレイス追加の前提を追記`
- 本文は任意ですが、題名と差分だけでは理由が分からないときは必須です。何をしたか（How）ではなく、なぜ必要だったか（Why）を書きます。
- 1 コミットは 1 つの理由にまとめます。理由を説明するのに複数の文が要るときは分けます。
- よく使う gitmoji: `:sparkles:` 機能追加、`:bug:` バグ修正、`:recycle:` リファクタリング、`:memo:` ドキュメント、`:fire:` 削除、`:wrench:` 設定、`:bookmark:` バージョン更新。全一覧は `.claude/rules/commit-message.md` を参照してください。

## プルリクエストのメッセージ

`murnana-github` プラグインの `pr-create` スキルに準じます。スキルが更新されたときは、このセクションと `.claude/rules/pr-message.md` も合わせて直します。

- 向き先は、`feature/*` と `bugfix/*` が `develop`、リリースと `hotfix/*` が `main` です。
- PR テンプレートがあればそれを使います。なければ、先頭に gitmoji を付けた短い題名（約 50 字、日本語）と、本文の「なぜ」「影響範囲」「デバッグ方法」の 3 節を書きます。
- 影響範囲には具体的なファイルや利用者を書き、デバッグ方法には実行するコマンドや確認の手順を書きます。差分の言い換えは書きません。
- 本文は一時ファイル（`.git/PR_BODY.md`）に書き出してから、`gh pr create --body-file <path>` で渡します。

## 開発の流れ

1. `develop` ブランチを探します（`git fetch origin develop`）。ない場合は、最新の `main` から `develop` を作成してプッシュします。
2. `develop` から `feature/<topic>` または `bugfix/<topic>` を切ります。
3. 変更し、`docs/plugins/<plugin-name>/CHANGELOG.md` の `## [Unreleased]` に日本語で追記します（[Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) のカテゴリー）。
4. `.claude-plugin/marketplace.json` を変えたときは、`sh scripts/build-dev-marketplace.sh` で `channels/dev/.claude-plugin/marketplace.json` を作り直して一緒にコミットします。手では編集しません。
5. `develop` 向けに PR を作り、マージします。**この時点ではプラグインのバージョンを上げません。** マージした時点で、アーリーアクセス版の利用者に届きます。

手元で動作確認するときは、`claude --plugin-dir plugins/<plugin-name>` を使います。マーケットプレイス経由では、push 済みの `main`（正式版）か `develop`（アーリーアクセス版）の内容しか取得されないためです。

## リリースチャンネル

| チャンネル | カタログ | 取得元 | バージョン |
|---|---|---|---|
| 正式版 `murnana-claude-code-plugin` | `main` の `.claude-plugin/marketplace.json` | `main` | エントリーの `version` |
| アーリーアクセス版 `murnana-claude-code-plugin-dev` | `develop` の `channels/dev/.claude-plugin/marketplace.json`（raw URL で追加） | `develop` | なし（コミット SHA） |

アーリーアクセス版のカタログは、正式版のカタログから `scripts/build-dev-marketplace.sh` で生成します。名前に `-dev` を付け、このリポジトリーのプラグインの `version` を消して取得元を `develop` にします。`unity-ariadne` は正式版と同じエントリーのままです。詳しくは `.claude/rules/release-channels.md` を参照してください。

## リリースの流れ

`develop` から `main` へのマージ PR（リリース PR）で、変更のあったプラグインのバージョンを上げます。

1. 変更のあったプラグインを調べます: `git diff --name-only origin/main...origin/develop -- plugins/`
2. 該当プラグインごとに `sh scripts/set-plugin-version.sh <plugin-name> <x.y.z>` を実行します。`.claude-plugin/marketplace.json` のエントリーの `version` と、取得元のタグ `source.ref`（`<plugin-name>--v<x.y.z>`）を書き換え、アーリーアクセス版のカタログも作り直します。`plugin.json` には `version` を書きません（書くとエントリーより優先され、ブランチを追従するインストールに更新が届かなくなります）。
3. CHANGELOG の `[Unreleased]` の内容を `## [x.y.z] - YYYY-MM-DD` に移し、末尾のリンク参照を更新します。新しいリンクはタグ（`tree/<plugin-name>--vx.y.z/plugins/<plugin-name>`、`compare/<plugin-name>--vx.y.z...main`）を指します。
4. `claude plugin validate .` を実行し、変更のあったプラグインごとに `claude plugin validate plugins/<plugin-name>` も実行します。
5. `main` にマージします。マージ後、`Tag plugin releases` ワークフローが `<plugin-name>--v<version>` のタグを作ります。タグができるまでの間（通常 1 分以内）は、正式版の新しいバージョンをインストールできません。ワークフローが成功したことを確認します。
6. バージョン更新が `develop` にも反映されるよう、`main` を `develop` にマージします。

バージョンは `marketplace.json` の各エントリーで管理し、リリースごとにプラグイン単位のタグ `<plugin-name>--v<version>` を付けます。正式版のエントリーはこのタグに固定されるため、`main` が先に進んでも、利用者にはリリースした時点のファイルが届きます。タグは手で作らず、ワークフローに任せます。GitHub Release は使いません。

バージョンは [Semantic Versioning](https://semver.org/) に従います（`v` は付けません）。

- パッチ: 後方互換のある修正、プラグイン内のドキュメント修正
- マイナー: 後方互換のあるスキル・コマンド・フックの追加や変更
- メジャー: 破壊的変更（スキルやコマンドの改名・削除など）。`0.y.z` の間はマイナーで構いません

上げ幅は、`[Unreleased]` に溜まった変更のうち最大のものに合わせます。`plugins/` の外の変更（README、`docs/`、`.claude/`、CLAUDE.md）ではバージョンを上げません。

## 外部リポジトリーのプラグイン（unity-ariadne）

`unity-ariadne` は [murnana/unity-ariadne](https://github.com/murnana/unity-ariadne) の `claude-plugins/` にあり、このリポジトリーの `plugins/` にはありません。`marketplace.json` のエントリーだけを管理します。

- `unity-ariadne` を更新（リリース）したら、このリポジトリーの `marketplace.json` の `unity-ariadne` の `version` を、`unity-ariadne` 側の `claude-plugins/.claude-plugin/plugin.json` の `version` に合わせます。これを上げないと、利用者のキャッシュが更新されません。
- 通常の `feature/*` と同じく `develop` から `feature/unity-ariadne-<version>` を切り、`develop` 向けに PR を作ります。エントリーを変えたら `sh scripts/build-dev-marketplace.sh` も実行します。アーリーアクセス版には `develop` へのマージ後、正式版にはリリース PR（`develop` → `main`）のマージ後に届きます。
- `Check plugin versions` ワークフローはこのプラグインを調べません。バージョンの一致は手で確認します。
- 詳しい手順と参照方式（`git-subdir` / `archive`）は [docs/plugins/unity-ariadne/README.md](docs/plugins/unity-ariadne/README.md) を参照してください。

## サードパーティーの資料

他者の文章・コード・テンプレート・仕様などを複製、要約、翻案して取り込むときは、出典のライセンスを確認し、同じ PR で、使うプラグインの `plugins/<plugin-name>/THIRD_PARTY_NOTICES.md` を更新します。リポジトリーのルートには置きません。ライセンスが許さない使い方は避け、リンクか自分の言葉での要約にとどめます。

## 関連ファイル

- `.claude/rules/branch-workflow.md`: ブランチ運用
- `.claude/rules/plugin-version-bump.md`: バージョン更新
- `.claude/rules/marketplace-manifest.md`: `marketplace.json` の書き方
- `.claude/rules/release-channels.md`: 正式版とアーリーアクセス版のチャンネル
- `.claude/rules/commit-message.md`: コミットメッセージ（`murnana-git` の `commit` スキルに準拠）
- `.claude/rules/commit-message-sync.md`: スキル更新時にコミットメッセージのルールを合わせる手順
- `.claude/rules/pr-message.md`: PR のタイトルと本文（`murnana-github` の `pr-create` スキルに準拠）
- `.claude/rules/pr-message-sync.md`: スキル更新時に PR メッセージのルールを合わせる手順
- `.claude/rules/third-party-notices.md`: 権利の確認とプラグインごとの `THIRD_PARTY_NOTICES.md` の更新
