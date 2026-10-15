# stack-rebase スキル

`/murnana-github:stack-rebase` — `gh stack rebase`（または `gh stack sync`）でスタック全体をカスケード rebase し、コンフリクトを解決して push する。

## 使い方

- 起動は**明示的なスラッシュコマンドのみ**（`disable-model-invocation: true`）。
- `$ARGUMENTS` にモードを渡せる: `--upstack`（現在の層より上だけ）/ `--downstack`（trunk〜現在の層）/ `--no-trunk`（trunk を取り込まない）/ `sync`（マージ済み PR やリモート側の変更を取り込む）。省略時は状態から選ぶ。

| Step | やること |
|---|---|
| 1 | 前提確認（スタック内か、作業ツリーがクリーンか、rebase 進行中でないか） |
| 2 | モード選択（`rebase` / `--upstack` / `--downstack` / `--no-trunk` / `sync`） |
| 3 | 実行。コンフリクト（終了コード 3）なら解決→`git add`→`--continue` のループ |
| 4 | `needsRebase` が全層 false か検証、手動解決があればチェック実行 |
| 5 | **承認後**に `gh stack push` |

コンフリクト対応の詳細 → [`references/conflict-resolution.md`](../../../plugins/murnana-github/skills/stack-rebase/references/conflict-resolution.md)。

## 設計判断とその理由

- **なぜ `git rebase` / `git push --force` を直接使わないか** — gh-stack はジャーナルと層ごとのメタデータを持ち、マージ済み層は `--onto` で処理する。素の git 操作はこれと食い違い、`--abort` での一括復元も効かなくなる。
- **なぜ push 前に承認を取るか** — リモートの履歴を書き換え、全 PR の CI を再実行させる。`sync` は内部で push するので、実行前に承認を取る。
- **なぜ意味的なコンフリクトはユーザーに聞くか** — 下位層の意図を優先するのが原則だが、挙動が分かれる衝突は推測で解決すると上位層のレビュー済み内容を壊しうる。機械的な衝突（隣接編集、import 順など）だけを自動で解決する。
- **なぜ `--prune` を既定にしないか** — マージ済みのローカルブランチ削除は不可逆な操作のため、明示された場合のみ。
- **GitHub の Rebase stack ボタンとの使い分け** — コンフリクトが起きない見込みならサーバー側の **Rebase stack** ボタンで十分。コンフリクトが予想されるときにローカルで解決するためのスキル。
