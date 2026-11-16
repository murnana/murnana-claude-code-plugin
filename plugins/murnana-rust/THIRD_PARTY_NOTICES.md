# THIRD_PARTY_NOTICES

このプラグインに含まれるサードパーティーの資料の出典とライセンス、関わる商標です。

## Rust by Example「Documentation」

- 出典: Rust by Example, "Documentation" https://doc.rust-lang.org/rust-by-example/meta/doc.html (ソース: https://github.com/rust-lang/rust-by-example の `src/meta/doc.md`)
- ライセンス: MIT License または Apache License 2.0 のいずれか(このプラグインでは MIT License を選択)
- 利用箇所: `skills/comment/references/rustdoc.md`(コード例と説明を抜粋・加工)
- ライセンス本文:

```
Copyright (c) 2014 Jorge Aparicio

Permission is hereby granted, free of charge, to any
person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the
Software without restriction, including without
limitation the rights to use, copy, modify, merge,
publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice
shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF
ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
```

## RFC 1574「More API Documentation Conventions」

- 出典: https://rust-lang.github.io/rfcs/1574-more-api-documentation-conventions.html (ソース: https://github.com/rust-lang/rfcs の `text/1574-more-api-documentation-conventions.md`)
- ライセンス: MIT License または Apache License 2.0 のいずれか(rust-lang/rfcs リポジトリーの README による)
- 利用箇所: `skills/comment/references/rustdoc.md`(規約を英語で要約)

## t_wada「コードには How …」

- 出典: Takuto Wada (@t_wada) の X への投稿(2017年9月5日) https://x.com/t_wada/status/904916106153828352
- ライセンス: 不明(投稿にライセンスの表示がありません)。1文を出典を明示して引用し、それ以外はこのスキル独自の解説として書いています。
- 利用箇所: `skills/comment/references/comment-placement.md`、`skills/comment/SKILL.md`

## Rust API Guidelines「Naming」

- 対象: `review` スキル（`skills/review/SKILL.md` の命名の表）
- 内容: 命名の章（C-CASE、C-CONV、C-GETTER、C-ITER など）を、独自の文章と表で要約したもの。本文は複製していない。例の識別子は標準ライブラリーの名前を一部使っている
- 出典: https://rust-lang.github.io/api-guidelines/naming.html （ソース: https://github.com/rust-lang/api-guidelines ）
- ライセンス: MIT License または Apache License 2.0 のデュアルライセンス（リポジトリーの `README.md`、`LICENSE-MIT`、`LICENSE-APACHE`）
- 著作権: Copyright (c) The Rust Project Developers

## Canon TDD(Kent Beck)と日本語訳「テスト駆動開発の定義」(t_wada)

- 対象: `test-case` スキル(`skills/test-case/SKILL.md`、`skills/test-case/references/test-design.md`)、`test-case-writer` サブエージェント(`agents/test-case-writer.md`)
- 内容: テストリストを書き、1 つずつテストにして進める手順と、避けるべき失敗の考え方を、自分の言葉で要約したもの。原文・訳文の転載はしていない
- 出典: https://newsletter.kentbeck.com/p/canon-tdd (Kent Beck、2023-12-11。旧 URL の tidyfirst.substack.com から転送される) / https://t-wada.hatenablog.jp/entry/canon-tdd-by-kent-beck (和田卓人による日本語訳、2023-12-11)
- ライセンス: 原文のページに利用許諾の表示はなく、ページ末尾に「© 2026 Kent Beck」とある(確認日 2026-11-16)。日本語訳は和田卓人氏が Kent Beck 本人の許可を得て公開したもので、訳ページにもライセンスの表示はない。そのため原文・訳文は転載せず、考え方の要約と出典の明記にとどめている

## 『テスト駆動開発』(Kent Beck 著、和田卓人 訳)

- 対象: `test-case` スキル(`skills/test-case/references/test-design.md`)
- 内容: 仮実装・三角測量・明白な実装という進め方の名前と考え方を、自分の言葉で要約したもの。本文の転載はしていない
- 出典: Kent Beck, "Test-Driven Development: By Example", Addison-Wesley, 2002 / 『テスト駆動開発』オーム社、2017 年
- ライセンス: 書籍(著作権は各権利者に帰属)。考え方の要約と出典の明記にとどめている

## 商標

- Rust、Cargo は Rust Foundation の商標または登録商標です。
- X は X Corp. の商標または登録商標です。

その他の製品名・会社名は、各社の商標または登録商標です。各権利者は、このプラグインを後援・提携していません。
