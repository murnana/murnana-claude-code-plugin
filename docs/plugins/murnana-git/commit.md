# commit スキル

`/murnana-git:commit` — 作業ツリーを Why 単位のコミットに分割し、承認を得てからコミットする。

## 使い方

- 起動は**明示的なスラッシュコマンドのみ**。「コミットして」と平文で頼んでも発火しない（`SKILL.md` の `disable-model-invocation: true`）。
- `$ARGUMENTS` に「READMEだけ」のような意図のヒントを渡せる。

動作フローは次の 5 ステップ。

| Step | やること |
|---|---|
| 1 | 差分の把握（path を絞って読む） |
| 2 | プロジェクト規約の発見 |
| 3 | コミット前チェックの実行 |
| 4 | Why 単位に分割し**承認待ち** |
| 5 | 順次コミット |

## 規約の優先順位

プロジェクト固有の規約が見つかれば、それが唯一の正。見つからないときだけフォールバック規約を使う。

- 探索先の一覧 → [`references/project-rules.md`](../../../plugins/murnana-git/skills/commit/references/project-rules.md)
- フォールバック規約（t_wada 氏の「コミットログには Why」原則に基づく、1 コミット = 1 つの Why、emoji 付きタイトル）→ [`references/commit-message.md`](../../../plugins/murnana-git/skills/commit/references/commit-message.md)

どちらも中身はこのドキュメントに写さず、リンク先を正とする。

## 設計判断とその理由

- **なぜ明示起動のみか** — commit のような副作用のある操作には `disable-model-invocation: true` を使うことが公式ドキュメントの推奨。起動タイミングを人間が握れる。スキル自体がスラッシュコマンドになるため、別途 `commands/` を作る必要もない。
- **なぜ `allowed-tools` に `git push` / `git commit --amend` / `git reset` を含めていないか** — 承認プロンプトを安全弁として意図的に残している。
- **なぜ `git add -A` / `git add .` を禁じているか** — 無関係な変更を巻き込まないため。コミットごとに対象パスを明示する。
- **なぜ `--no-verify` を禁じているか** — プロジェクトのコミット前チェックを迂回しないため。
- **なぜ `references/` に規約を分離したか** — progressive disclosure。リンク先は明示的に参照されたときだけ読み込まれるので、常時コンテキストに乗るのは `SKILL.md` 本体だけで済む。
- **なぜコミット前に必ず承認を取るか** — 意図しないコミットを防ぐため。1 コミットで済む場合も分割案を提示する。

## 実装上の落とし穴：動的コンテキスト注入と空リポジトリ

SKILL.md 冒頭の ```` ```! ```` ブロック（動的コンテキスト注入）は、中のコマンドが**非ゼロ終了するとスキル呼び出し全体が失敗する**仕様。

開発初期の注入ブロックはこれを踏んでいた。コミット 0 件のリポジトリ（`git init` 直後）で以下がいずれも `fatal` で exit 128 になり、`/murnana-git:commit` が**起動すらしなかった**。

| コマンド | 挙動 |
|---|---|
| `git diff --stat HEAD` | `fatal: ambiguous argument 'HEAD': unknown revision` |
| `git log --format='%s' -20` | `fatal: ... does not have any commits yet` |

対処は `HEAD` を参照しない形への書き換え（`git diff --stat` / `git diff --cached --stat` に分割）と、落ちうるコマンドを `2>/dev/null || true` でガードすること。

**教訓**: 動的コンテキスト注入に置くコマンドは、異常系（空リポジトリ、対象ファイル不在など）でも終了コードを確かめてから採用する。

## git コマンドの選択と根拠

現在の `SKILL.md` が使っているオプションと、その根拠。いずれも `git diff --help` / `git log --help` を確認した上で、このリポジトリで実測して裏を取っている。

| 用途 | 使うもの | 理由 |
|---|---|---|
| 状態確認 | `git status -sb` | short format + ブランチ/追跡差分が 1 行で得られ、`git branch --show-current` の呼び出しが不要になる |
| 差分サマリ | `git diff --numstat` | man に "more machine friendly" とある通り装飾が無く、パスが省略されない |
| 差分本体 | `git diff -U1 -- <paths>` | コンテキスト行が既定の 3 行から 1 行に減る。必ず path で絞る |
| 履歴（規約推定） | `git log --format='%s' --no-merges -15` | マージコミットの件名は自動生成で手書き規約を反映しない |
| 履歴（結果報告） | `git log --oneline -<N>` | 件数を必ず縛る |

補足:

- `--stat` は man に「Maximum width defaults to terminal width, or **80 columns if not connected to a terminal**」とあり、ツール実行時（非 TTY）は 80 桁分のヒストグラムと桁揃え空白を毎行吐く。さらに長いパスを `...` で切る。実際にこのリポジトリで比較すると、`--stat` は `.../skills/commit/references/commit-message.md` を途中で省略したが、`--numstat` はフルパスのまま出力した。切られたパスは `git add` や `git diff -- <path>` にそのまま渡せないため、これはトークン効率だけでなく**正しさ**にも関わる。
- `--no-merges` の効果もこのリポジトリで実測済み。付けない場合、履歴には `Add murnana-unreal-engine plugin with ue5-docs skill (#4)` のような GitHub 生成の squash マージ件名が 4 件混ざり、`:emoji:` 形式の実際の規約と食い違う。`--no-merges` を付けるとこの 4 件が落ち、`:emoji:` 形式の件名だけが残る。トークン削減と規約推定の精度向上を兼ねる。
