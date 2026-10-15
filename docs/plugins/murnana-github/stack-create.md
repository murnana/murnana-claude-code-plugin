# stack-create スキル

`/murnana-github:stack-create` — 変更を小さな層に分割し、GitHub の Stacked pull requests として PR のスタックを作成する。

## 使い方

- 起動は**明示的なスラッシュコマンドのみ**（`disable-model-invocation: true`）。
- `$ARGUMENTS` に「ログイン機能を model / api / ui に分けて」のような意図や、既存ブランチ名（下から上の順）を渡せる。
- 前提: `gh` 認証済み、`gh stack` 拡張インストール済み（未導入なら確認のうえ導入）、対象リポジトリで Stacked PR が有効。

| Step | やること |
|---|---|
| 1 | `gh` / `gh-stack` が使えるか確認（リモートが複数あれば `--remote` を決める） |
| 2 | プロジェクト規約の発見（pr-create と共通の `project-rules.md`） |
| 3 | 入力パターンの判定（未コミット変更の分割 / 既存ブランチの採用 / jj 等のブランチを `link`） |
| 4 | 層の設計表を提示し**承認待ち** |
| 5 | `gh stack init` → 層ごとに `git add <paths>` → `git commit` → `gh stack add` |
| 6 | PR作成前チェック（失敗したら停止） |
| 7 | `gh stack submit --auto` で draft PR を作成 |
| 8 | `gh stack view --json` で確認し、`stack-pr-message` へ案内 |

層の分割ルール → [`references/layer-design.md`](../../../plugins/murnana-github/skills/stack-create/references/layer-design.md)、コマンドと終了コード → [`references/command-reference.md`](../../../plugins/murnana-github/skills/stack-create/references/command-reference.md)。

## 設計判断とその理由

- **なぜ常に明示的な引数を渡すか** — `gh stack` は引数が足りないと TUI やプロンプトを開き、Claude の Bash 実行がブロックする。公式 gh-stack スキルの非対話ルール（`init <branch>`、`add <branch>`、`submit --auto`、`view --json`、`modify` / `switch` 禁止）に従う。
- **なぜ層設計で承認を取るか** — ブランチ作成後の並び替えは `gh stack modify`（TUI 専用）が必要で Claude からは実行できない。レビュー開始後の構成変更はレビュワーの手戻りにもなるため、最初に確定させる。
- **なぜ `gh stack add -Am` を使わないか** — 日付ベースのブランチ名が自動生成され、全ファイルがステージされて後続層のファイルが混入する。層ごとにパスを明示して `git add` する。
- **なぜ draft で作るか** — `submit --auto` の既定。自動生成のタイトルは仮のものなので、`stack-pr-message` で整えてから ready にする流れを想定している。`--open` はユーザーが求めたときだけ。
- **なぜ 1 ブランチ上の既存コミットの分割は対象外か** — 履歴の書き換えが必要で、失敗時の影響が大きい。停止して相談する。
- **公式 `gh skill install github/gh-stack` との関係** — 公式スキルは自動発火するコマンドリファレンス。本スキルは明示起動の手順書で、層設計・承認・プロジェクト規約の適用を担う。併用しても役割は重複しない。
