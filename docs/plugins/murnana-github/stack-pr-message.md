# stack-pr-message スキル

`/murnana-github:stack-pr-message` — スタック内の各 PR について、その層の差分に即したタイトルと本文を作成し、`gh pr edit` で反映する。

## 使い方

- 起動は**明示的なスラッシュコマンドのみ**（`disable-model-invocation: true`）。
- 現在のブランチが属するスタックの、open な PR すべてが対象（マージ済み・キュー投入済みは対象外）。
- `$ARGUMENTS` にスタック全体の目的のヒントを渡せる。

| Step | やること |
|---|---|
| 1 | `gh stack view --json` でスタックと PR 番号を取得 |
| 2 | 層ごとに `gh pr view --json` と `gh pr diff --name-only` を取得 |
| 3 | プロジェクト規約・PR テンプレートの探索（pr-create と共通） |
| 4 | 下の層から順にタイトル・本文を作成 |
| 5 | 全層分を提示し**承認待ち** |
| 6 | 本文を `.git/PR_BODY.md` に書き出し、`gh pr edit --title … --body-file <path>` で反映 |

## メッセージ形式

pr-create と同じ優先順位（プロジェクト規約 → テンプレート → `:emoji:` タイトル + なぜ/影響範囲/デバッグ方法）に、**スタック** セクション（位置・この層の役割・後の層に回したもの・レビュー順）を加える。仕様と例 → [`references/stack-message.md`](../../../plugins/murnana-github/skills/stack-pr-message/references/stack-message.md)。

## 設計判断とその理由

- **なぜ pr-create の references を共有するか** — 同一プラグイン内なので `${CLAUDE_PLUGIN_ROOT}/skills/pr-create/references/` が解決できる。規約・テンプレート探索・emoji 表を複製すると同期漏れが起きる。
- **なぜタイトルに位置（2/3 など）を入れないか** — 層の挿入・統合・部分マージで番号がずれ、タイトルが嘘になる。位置は再生成しやすい本文側に置く。
- **なぜ全層のリンク一覧を書かないか** — GitHub が PR ページにスタックマップを表示するため冗長。隣接層の `#n` だけ書く。
- **なぜ「後の層に回したもの」を書くか** — 層単体では未完成に見えるため、「これが足りない」というレビューコメントを防ぐ。ベストプラクティスとして推奨されている書き方。
- **なぜ本文を一時ファイルに書いてから `gh` に渡すか** — pr-create と同じ理由。ヒアドキュメントで本文を流すと `gh` の呼び出しが本文込みの長いコマンドになり、承認時に確かめにくい。`.git/PR_BODY.md` に `Write` ツールで書き出してから `--body-file <path>` で渡す。パスを得る `git rev-parse --absolute-git-dir` だけを `allowed-tools` に加え、`Write` は書き込み先を絞れないので事前許可しない。
- **なぜ draft/ready を変えないか** — 公開タイミングはユーザーの判断。`gh pr ready` や `gh stack submit --open` で行う。
