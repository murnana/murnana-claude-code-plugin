# pr-create スキル

`/murnana-github:pr-create` — プロジェクトの規約に従ってプルリクエストを作成する。

## 使い方

- 起動は**明示的なスラッシュコマンドのみ**。平文で「PRを作って」と頼んでも発火しない（`SKILL.md` の `disable-model-invocation: true`）。
- `$ARGUMENTS` に「ログイン機能だけ」のような意図のヒントを渡せる。

動作フローは次の 7 ステップ。

| Step | やること |
|---|---|
| 1 | `gh` が使えるか確認（不可なら停止して確認） |
| 2 | プロジェクト固有の PR 規約の発見 |
| 3 | PR作成前チェックの実行 |
| 4 | 未pushのコミットをpush（失敗したら完全停止） |
| 5 | PRテンプレートの発見 or 生成 |
| 6 | 提示と**承認待ち** |
| 7 | `gh pr create` で作成 |

## 規約の優先順位

プロジェクト固有の規約が見つかれば、それが唯一の正。見つからないときだけフォールバック規約を使う。

- プロジェクト規約の探索先 → [`references/project-rules.md`](../../../plugins/murnana-github/skills/pr-create/references/project-rules.md)
- テンプレートの探索順（GitHub公式の規約に準拠）→ [`references/pr-template-discovery.md`](../../../plugins/murnana-github/skills/pr-create/references/pr-template-discovery.md)
- フォールバック規約（テンプレートが無い場合、`:emoji:` 付きタイトル + なぜ/影響範囲/デバッグ方法の3セクション）→ [`references/pr-message.md`](../../../plugins/murnana-github/skills/pr-create/references/pr-message.md)
- `gh` が使えない場合のフォールバック手順 → [`references/gh-fallback-mcp.md`](../../../plugins/murnana-github/skills/pr-create/references/gh-fallback-mcp.md)

いずれも中身はこのドキュメントに写さず、リンク先を正とする。

## 設計判断とその理由

- **なぜ明示起動のみか** — PR 作成は GitHub 上で可視化される副作用（通知・CI 起動・レビュワーへの通知）を伴う。`murnana-git` の `commit` スキルと同じ理由で、起動タイミングを人間が握れるようにしている。
- **なぜ push 失敗で完全停止するか** — push できていない状態のブランチに対して PR を作ると、ベースとの差分が不整合になったり、GitHub 側で意図しない挙動になりうる。失敗したら原因を報告し、対応を確認してからやり直す。
- **なぜ pre-PR チェックのランナーを `allowed-tools` に事前許可しないか** — 対象プロジェクトが Node.js とは限らない（Unity、Unreal Engine、Python なども想定される）。特定のランナー（`npm test` など）を先回りで許可すると、他言語・他エンジンのプロジェクトでは的外れになる。実行のたびに通常の Bash 権限プロンプトを経由させることで、プロジェクトを問わず安全に動作させる。
- **なぜ `gh` 不在時に自動インストール/MCP設定をしないか** — CLI ツールのインストールや MCP サーバー設定はこのリポジトリの外側の環境を変更する操作であり、無断で行うべきではない。`AskUserQuestion` で必ず確認を取る。
- **なぜ emoji テーブルを `murnana-git` と別々に持つか** — プラグインは独立にインストール可能で、スキルの `references/` は自プラグインの `${CLAUDE_PLUGIN_ROOT}` 配下にしか解決できない。クロスプラグイン参照は成立しないため、`murnana-git` の `commit-message.md` にある表を意図的に複製している。片方を直すときはもう片方も確認する（両ファイル冒頭にコメントで明記）。
- **なぜ Draft PR をデフォルトにしないか** — `$ARGUMENTS` やユーザーの明示的な指示がない限り通常の PR を作る。毎回 Draft かどうかを聞くと承認フローが増えるだけで、通常運用では不要な確認になる。
- **なぜ assignee が未指定なら `--assignee @me` を付けるか** — テンプレートやユーザー指示にアサイン先の明言がない場合、レビュー依頼の起点が誰もアサインされていない宙に浮いた PR になるのを避けるため、スキルの実行者自身を自動的にアサインする。
