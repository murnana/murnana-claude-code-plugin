# Stacked PR message format

The format is pr-create's (project rules → template → `pr-message.md` fallback) plus one **stack section** per PR. This file specifies only what differs for stacks.

## Title

- Same rules as the base format (emoji code prefix in the fallback, or the template's/project's convention).
- Describes **this layer's** change: `:sparkles: ログイン API エンドポイントを追加`, not the whole feature.
- No position markers (`[2/3]`, `Part 2`) — they go stale when the stack is restructured.

## Body

- なぜ (or the template's equivalent): one sentence on the stack's overall goal, then why **this layer** exists.
- 影響範囲: only this layer's diff (`gh pr diff <n> --name-only`).
- デバッグ方法: how to verify **this layer** on its own branch. If it can't be exercised alone (e.g. a model with no caller yet), say so and name the layer where it becomes testable.

## Stack section

Insert directly before the attribution line. Heading and labels stay in Japanese to match the fallback format:

```markdown
## スタック

- 位置: 2 / 3（下: #41 ・ 上: #43）
- この層の役割: ログイン API を追加し、次の層の UI から呼び出せるようにする
- 後の層に回したもの: ログインフォーム（#43）、レートリミット（未着手）
- レビュー: 下の層（#41）から順にレビューしてください
```

| Line | Rule |
|---|---|
| 位置 | `<index> / <count>` counting **open + merged-in-this-stack** layers bottom = 1. Neighbor PRs as `#n` (GitHub autolinks them). Bottom: `下: <trunk>`. Top: omit `上`. |
| この層の役割 | The one-sentence test: "adds ___ so that the next layer can ___". Top layer: what the stack delivers as a whole. |
| 後の層に回したもの | What a reviewer might expect here but is intentionally in a later layer (with `#n`), or not done yet. Write `なし` if nothing. Prevents "this is incomplete" review comments. |
| レビュー | Bottom layer: omit. Others: point to the layer below. |

When a project template is in use, add this section after the template's last section, unless the project's rules forbid extra sections.

## Examples

Bad (describes the whole feature, position in title, full link list):

```markdown
:sparkles: [2/3] ログイン機能

ログイン機能を実装しました。

- #41 モデル
- #42 API
- #43 UI
```

Good (bottom layer of 3, fallback format):

```markdown
:sparkles: ユーザー認証情報モデルを追加

## なぜ (Why)
ログイン機能をスタックで段階的に導入する。この層は、後続の API 層が参照する認証情報モデルとマイグレーションだけを先に入れる。

## 影響範囲 (Scope / Impact)
- `src/models/user.ts`: `passwordHash` / `lastLoginAt` を追加
- `migrations/003_add_credentials.sql`: 既存 `users` テーブルに列追加（NULL 許容、既存行に影響なし）

## デバッグ方法 (How to verify)
`npm run migrate && npm test -- models/user` が通ること。呼び出し元は #42 で追加されるため、この層単体では API から確認できない。

## スタック

- 位置: 1 / 3（下: main ・ 上: #42）
- この層の役割: 認証情報モデルを追加し、次の層の API が認証に使えるようにする
- 後の層に回したもの: ログイン API（#42）、ログインフォーム（#43）

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```
