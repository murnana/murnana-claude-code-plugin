# large-file-guard スキル

`/murnana-github:large-file-guard` — GitHub に push できない大きさの非 LFS ファイルを `git commit` の前に止める Hook を、現在のリポジトリに設定する。

## 使い方

- 起動は**明示的なスラッシュコマンドのみ**（`SKILL.md` の `disable-model-invocation: true`）。リポジトリに `.claude/` のファイルと設定を書き込むため。
- 一度設定すれば、以降は Hook が自動で働く。スキルを毎回呼ぶ必要はない。
- `$ARGUMENTS` に設定先や閾値を渡すと、その質問を省く。

| Step | やること |
|---|---|
| 1 | git リポジトリか確認する |
| 2 | `jq` があるか確認する（無ければ停止） |
| 3 | 既存の `.claude/settings.json` / `settings.local.json` を読み、登録済みか調べる |
| 4 | 設定先と閾値を `AskUserQuestion` で 1 回にまとめて確認する |
| 5 | `scripts/check-git-file-size.sh` を `.claude/hooks/` にコピーする |
| 6〜7 | 設定ファイルへ `PreToolUse` の Hook を既存の設定を壊さずに追記する |
| 8 | `jq empty` で JSON を検証する |
| 9 | 結果と Hook が見られない範囲を報告する |

## Hook の動作

| ファイルサイズ（非 LFS） | 動作 |
|---|---|
| 50 MiB 未満 | そのままコミットする |
| 50 MiB 以上 | コミットは通し、Claude にユーザーへ警告させる |
| 100 MiB 以上 | コミットをブロックし（exit 2）、Claude が LFS 化・除外・分割のどれにするかをユーザーに確認する |

閾値は環境変数 `GIT_FILE_SIZE_WARN_MIB` / `GIT_FILE_SIZE_BLOCK_MIB` で変えられる。GitHub の制限値と測り方は [`references/github-limits.md`](../../../plugins/murnana-github/skills/large-file-guard/references/github-limits.md) を正とする。

## 設計判断とその理由

- **なぜ push ではなく commit の前で止めるか** — 100 MiB を超えるファイルが一度コミットされると、push が拒否されたあとも履歴に残り、`git filter-repo` などで履歴を書き換えない限り push できない。コミット前なら `git restore --staged` で取り除くだけで済む。
- **なぜ LFS のファイルを除外する仕組みを別に持たないか** — LFS のファイルはインデックス上では約 130 バイトのポインタになる。ステージ済みの blob サイズ（`git cat-file -s :<path>`）を測れば、LFS を除外する処理なしに自然に通る。LFS の設定があるのに `git-lfs` が入っておらず変換されなかったファイルは大きいまま残るので、正しくブロックされる。
- **なぜ `git commit -a` では別の測り方をするか** — `-a` は未ステージの変更済みファイルも取り込むが、その時点ではまだインデックスにない。ワーキングツリーのサイズを測り、`filter` 属性が `lfs` のパスだけ除外する。
- **なぜプラグインの Hook ではなく、スクリプトをリポジトリへコピーするか** — プラグインを入れた全リポジトリで勝手に有効になるのを避け、必要なリポジトリだけに設定できるようにするため。`.claude/settings.json` に登録すればチームで共有でき、プラグインを入れていないメンバーの環境でも働く。プラグインのキャッシュ先はバージョンごとに変わるので、そのパスを設定に書くこともできない。
- **なぜ Hook 側で `git commit` かを判定するか** — `if: "Bash(git commit *)"` だけだと、`$()` を含むコマンドなど解析できないものでも Hook が走る。スクリプトが標準入力の `.tool_input.command` を読み、`git commit` 以外では何も出さずに終了する（`murnana-git` の `commit` スキルと同じ方針）。
- **なぜ見られない範囲を明記するか** — Bash ツール経由の `git commit` だけが対象で、`git add 大きいファイル && git commit` のように 1 コマンドにつなぐと `git add` の前に判定されて見逃す。ユーザーが誤って安全だと思わないよう、設定後の報告で必ず伝える。
- **なぜ push 全体やリポジトリ全体のサイズは測らないか** — スキルの目的は「個々のファイルが GitHub に拒否される」ことの防止。全体のサイズには推奨値があるだけで、拒否の条件として確実に判定できる値ではない。
- **なぜ `allowed-tools` を狭くしているか** — 書き込みは `.claude/hooks/check-git-file-size.sh` へのコピーと `chmod +x` だけに絞る。設定ファイルの編集は `Edit` / `Write` の承認プロンプトを通す。

## 前提

- `bash`, `git`, `jq`
- 制限値の出典は GitHub Docs。数値が変わったら `references/github-limits.md` とスクリプトの既定値を更新する。
