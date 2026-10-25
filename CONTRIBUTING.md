# CONTRIBUTING

このリポジトリーの開発フローをまとめます。Claude Code 向けの詳細なルールは `.claude/rules/` にあります。

> このリポジトリーは個人利用を目的としており、動作保証は一切ありません。

## ブランチ運用

| ブランチ | 役割 |
|---|---|
| `main` | 公開状態。マーケットプレイスの各プラグインは `main` から配布されます |
| `develop` | 開発の統合先。リリース前の変更が集まります |
| `feature/*` | 機能追加・変更・ドキュメント更新用。`develop` から切ります |
| `bugfix/*` | バグ修正用。`develop` から切ります |

`main` と `develop` には直接コミットしません。

## 開発の流れ

1. `develop` ブランチを探します（`git fetch origin develop`）。ない場合は、最新の `main` から `develop` を作成してプッシュします。
2. `develop` から `feature/<topic>` または `bugfix/<topic>` を切ります。
3. 変更し、`docs/plugins/<plugin-name>/CHANGELOG.md` の `## [Unreleased]` に日本語で追記します（[Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) のカテゴリー）。
4. `develop` 向けに PR を作り、マージします。**この時点ではプラグインのバージョンを上げません。**

手元で動作確認するときは、`claude --plugin-dir plugins/<plugin-name>` を使います。マーケットプレイス経由では `main` の内容しか取得されないためです。

## リリースの流れ

`develop` から `main` へのマージ PR（リリース PR）で、変更のあったプラグインのバージョンを上げます。

1. 変更のあったプラグインを調べます: `git diff --name-only origin/main...origin/develop -- plugins/`
2. 該当プラグインの `plugins/<plugin-name>/.claude-plugin/plugin.json` の `version` を上げます。
3. `.claude-plugin/marketplace.json` の同じプラグインの `version` を `plugin.json` と一致させます。
4. CHANGELOG の `[Unreleased]` の内容を `## [x.y.z] - YYYY-MM-DD` に移し、末尾のリンク参照を更新します。
5. `claude plugin validate .` を実行し、変更のあったプラグインごとに `claude plugin validate plugins/<plugin-name>` も実行します。
6. `main` にマージします。その後、バージョン更新が `develop` にも反映されるよう `main` を `develop` にマージします。

バージョンは [Semantic Versioning](https://semver.org/) に従います（`v` は付けません）。

- パッチ: 後方互換のある修正、プラグイン内のドキュメント修正
- マイナー: 後方互換のあるスキル・コマンド・フックの追加や変更
- メジャー: 破壊的変更（スキルやコマンドの改名・削除など）。`0.y.z` の間はマイナーで構いません

上げ幅は、`[Unreleased]` に溜まった変更のうち最大のものに合わせます。`plugins/` の外の変更（README、`docs/`、`.claude/`、CLAUDE.md）ではバージョンを上げません。

## サードパーティーの資料

他者の文章・コード・テンプレート・仕様などを複製、要約、翻案して取り込むときは、出典のライセンスを確認し、同じ PR で [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) を更新します。ライセンスが許さない使い方は避け、リンクか自分の言葉での要約にとどめます。

## 関連ファイル

- `.claude/rules/branch-workflow.md`: ブランチ運用
- `.claude/rules/plugin-version-bump.md`: バージョン更新
- `.claude/rules/marketplace-manifest.md`: `marketplace.json` の書き方
- `.claude/rules/third-party-notices.md`: 権利の確認と THIRD_PARTY_NOTICES.md の更新
