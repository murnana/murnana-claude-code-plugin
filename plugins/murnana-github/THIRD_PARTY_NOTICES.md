# THIRD_PARTY_NOTICES

このプラグインが取り込んでいる、または実行時に利用するサードパーティーの資料と、その権利表記をまとめます。

> 各権利者は、このプラグインを後援・提携していません。

## 取り込んでいる資料

### GitHub Docs（積み重ね PR のコマンドリファレンスなど）

- 対象
  - `skills/stack-create/references/command-reference.md`
  - `skills/stack-rebase/references/conflict-resolution.md`
  - `skills/stack-create/references/layer-design.md`（積み重ね PR に関する GitHub のドキュメントの考え方を参考にしています）
- 内容: GitHub Docs の積み重ね PR のコマンド解説を、要約・翻案したもの。原文から内容を変更しています
- 出典: https://docs.github.com/en/pull-requests/reference/stacked-prs-cli-commands
- 著作権: GitHub, Inc.
- ライセンス: Creative Commons Attribution 4.0 International (CC BY 4.0) https://creativecommons.org/licenses/by/4.0/

### gh-stack のエージェント用スキル

- 対象: `skills/stack-rebase/references/conflict-resolution.md`
- 内容: github/gh-stack リポジトリーの `skills/gh-stack` を要約・翻案したもの
- 出典: https://github.com/github/gh-stack
- ライセンス: MIT License

```
MIT License

Copyright GitHub, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 実行時に利用するツール（取り込んでいない）

次のツールは、利用者の環境にあらかじめ用意して使います。このプラグインには含まれていません。

| ツール | 用途 | 入手先 |
|---|---|---|
| GitHub CLI (`gh`) | PR の作成など | https://cli.github.com/ |
| gh-stack（`gh` の拡張機能） | 積み重ね PR の作成・rebase | https://github.com/github/gh-stack |

## 利用要件の確認

2026-10-28 に GitHub 利用規約（2026-04-27 版）、追加製品の規約（GitHub Actions を含む）、ロゴのポリシーを確認しました。

- 利用者自身のアカウントで `gh` を使うこと自体を禁じる条項は、見つかりませんでした。API の過度な頻度のリクエストと、トークンの共有は禁じられています。
- 名前: GitHub の名前やロゴを自分のものであるかのように使うこと、許可なくロゴを使うことが禁じられています。製品名に GitHub の名前を入れる場合の規定は見つかりませんでした。このプラグインの名前 `murnana-github` は、提携を示唆しない説明的な使用と考えていますが、確実ではありません。

## 商標

- GitHub は GitHub, Inc. の商標または登録商標です。

その他の製品名・会社名は、各社の商標または登録商標です。
