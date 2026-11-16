# THIRD_PARTY_NOTICES

このプラグインに含まれるサードパーティーの資料の出典とライセンスです。

## TSDoc 宣言参照の文法と標準タグ(Microsoft TSDoc)

- 出典: Microsoft TSDoc `tsdoc/src/beta/DeclarationReference.grammarkdown` https://github.com/microsoft/tsdoc/blob/main/tsdoc/src/beta/DeclarationReference.grammarkdown
- ライセンス: MIT License(下記)
- 利用箇所: `skills/comment/references/declaration-reference.md`(要約・翻案)、`skills/comment/scripts/ts_comments.py`(宣言参照の構文チェック)
- 同じリポジトリーの `tsdoc/src/details/StandardTags.ts`(標準タグの一覧)にも基づきます。利用箇所: `skills/comment/references/tsdoc.md`、`skills/comment/scripts/ts_comments.py`(タグ名の一覧)。ライセンスは同じ MIT License です。

```
Copyright (c) Microsoft Corporation. All rights reserved.

MIT License

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```

## コメントの原則(コードには How、テストコードには What、コミットログには Why、コードコメントには Why not)

- 出典: 和田卓人(@t_wada)氏の X への投稿(2017年9月5日) https://x.com/t_wada/status/904916106153828352 と、同じスレッドでの同氏の返信
- ライセンス: 明示なし(判断できず)。投稿の文章は転載せず、考え方を独自の言葉で要約しています。
- 利用箇所: `skills/comment/references/comment-routing.md`、`skills/comment/SKILL.md`

## コメントの原則の補足に使った資料

いずれも文章は転載せず、考え方を独自の言葉で要約しています。

- John Ousterhout『A Philosophy of Software Design』第13章、16.3節
- Ellen Spertus「Best practices for writing code comments」Stack Overflow Blog(2021年12月23日) https://stackoverflow.blog/2021/12/23/best-practices-for-writing-code-comments/
- Joshua Bloch『Effective Java』(公開 API のドキュメンテーションコメント)
- 利用箇所: `skills/comment/references/comment-routing.md`

## Canon TDD(Kent Beck)と日本語訳「テスト駆動開発の定義」(t_wada)

- 対象: `test-case` スキル(`skills/test-case/SKILL.md`、`skills/test-case/references/test-design.md`)、`test-case-writer` サブエージェント(`agents/test-case-writer.md`)
- 内容: テストリストを書き、1 つずつテストにして進める手順と、避けるべき失敗の考え方を、自分の言葉で要約したもの。原文・訳文の転載はしていない
- 出典: https://tidyfirst.substack.com/p/canon-tdd (Kent Beck、2023 年) / https://t-wada.hatenablog.jp/entry/canon-tdd-by-kent-beck (和田卓人による日本語訳)
- ライセンス: 確認できていない(作成時に出典のページを取得できなかったため)。考え方の要約と出典の明記にとどめている

## 『テスト駆動開発』(Kent Beck 著、和田卓人 訳)

- 対象: `test-case` スキル(`skills/test-case/references/test-design.md`)
- 内容: 仮実装・三角測量・明白な実装という進め方の名前と考え方を、自分の言葉で要約したもの。本文の転載はしていない
- 出典: Kent Beck, "Test-Driven Development: By Example", Addison-Wesley, 2002 / 『テスト駆動開発』オーム社、2017 年
- ライセンス: 書籍(著作権は各権利者に帰属)。考え方の要約と出典の明記にとどめている

## 商標

- TypeScript、TSDoc は Microsoft Corporation の商標または登録商標です。
- X は X Corp. の商標です。
