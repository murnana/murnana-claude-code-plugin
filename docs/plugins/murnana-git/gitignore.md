# gitignore スキル

`/murnana-git:gitignore` — [murnana/gitignore](https://github.com/murnana/gitignore) のテンプレートを使って `.gitignore` を作成・更新する。

## 使い方

- 起動は**明示的なスラッシュコマンドのみ**（`disable-model-invocation: true`）。
- 引数の例:

| 引数 | 動作 |
|---|---|
| なし | プロジェクトのファイル（`ProjectSettings/`、`*.uproject`、`package.json` など）からテンプレートを推定する |
| `Unity Global/macOS` | 指定したテンプレートを追加する |
| `update` | 既存の管理ブロックをすべて murnana/gitignore の最新に差し替える |
| `remove Unity` | 指定したテンプレートのブロックを外す |

動作フローは次の 4 ステップ。

| Step | やること |
|---|---|
| 1 | murnana/gitignore をツリーだけ一時ディレクトリに clone する |
| 2 | テンプレートと書き込み先を決める |
| 3 | 追加・更新・削除の計画を示し**承認待ち** |
| 4 | 書き込み、追跡済みファイルが新ルールに該当しないか確認する |

コミットはしない。必要なら続けて `/murnana-git:commit` を使う。

## 書き込み形式

テンプレートごとに次のマーカーで囲む。括弧内は取得元コミットの先頭 12 文字。

```gitignore
# --- BEGIN Unity.gitignore (e4410f4e4a88) ---
（テンプレート本文をそのまま）
# --- END Unity.gitignore ---
```

詳しい規則（挿入位置、更新・削除、ブロック外の行の扱い）は [`references/managed-blocks.md`](../../../plugins/murnana-git/skills/gitignore/references/managed-blocks.md)、テンプレートの推定表は [`references/templates.md`](../../../plugins/murnana-git/skills/gitignore/references/templates.md) を正とする。

## 設計判断とその理由

- **なぜ murnana/gitignore か** — github/gitignore のフォークで、Unity（`UIElementsSchema` など）や Unreal Engine（`*.slnx`）に murnana 独自の追記がある。upstream ではなくこちらを取得元に固定する。
- **なぜ `git clone --filter=blob:none --no-checkout` か** — テンプレート一覧の取得に GitHub API（`git/trees`）を使うと、未認証では 60 回/時の制限があり、プロキシ環境では 403 になることもある。blob を落とさない浅い clone ならツリーだけ取れ、本文は `git show HEAD:<path>` で必要な分だけ取得される。一覧と本文が同じコミットに揃うのも利点。
- **なぜ WebFetch を使わないか** — WebFetch は取得内容をモデルで要約して返すため、テンプレートを一字一句写す用途に向かない。
- **なぜマーカー付きブロックか** — テンプレートの更新を後から差し替えられるようにするため。取得元コミットを残すことで、どの版を入れたかも追える。
- **なぜ既存の行の下ではなく上にブロックを入れるか** — gitignore は後に書いたパターンが勝つ。ユーザー独自の行（特に `!pattern` の否定）をテンプレートより後ろに残し、上書きされないようにする。
- **なぜ `Global/` を自動で追加しないか** — OS やエディタの規則は開発者のマシンに依存し、プロジェクトの性質ではない。murnana/gitignore の README もグローバルの excludes ファイルへの追加を推奨しているため、入れる場合も書き込み先を確認する。git config は変更しない。
- **なぜ `git rm --cached` を実行しないか** — ignore ルールを足しても追跡済みファイルは外れない。`git ls-files -ci --exclude-standard` で該当ファイルを報告するに留め、追跡を外すかはユーザーが決める。
- **なぜ明示起動のみか** — 他の murnana-git / murnana-github のスキルと揃えている。ファイルを書き換える操作なので、起動タイミングを人間が握る。

## 実装上の注意

- 冒頭の動的コンテキスト注入は、Git リポジトリ外やコミット 0 件のリポジトリ、`.gitignore` が無い場合でも終了コード 0 になることを確認済み（[commit スキルの落とし穴](commit.md#実装上の落とし穴動的コンテキスト注入と空リポジトリ) を参照）。
- `git ls-tree` の pathspec は glob として解釈されないため、`-- '*.gitignore'` では 1 件も返らない。全パスを取得してから `.gitignore` で終わるものを選ぶ。
