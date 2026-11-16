# THIRD_PARTY_NOTICES

このプラグインに含まれるサードパーティーの資料の出典とライセンスをまとめます。

> 各権利者は、このプラグインを後援・提携していません。

## 出典とライセンス

### Doxygen マニュアル

- 対象: `comment` スキル（`skills/comment/references/doxygen.md`）
- 内容: Doxygen マニュアルのうち、C++ のコメントブロック、コマンド、Markdown、自動リンク、警告設定の仕様を独自の文章で要約したもの。マニュアルの本文と例は複製していない
- 出典: https://www.doxygen.nl/manual/ / https://github.com/doxygen/doxygen/tree/master/doc
- ライセンス: GNU General Public License version 2（マニュアルのソース `doc/*.dox` の冒頭で、ソフトウェアとドキュメントを GPL の条件で利用できると定めている）
- 著作権: Copyright (C) 1997-2015 by Dimitri van Heesch

### 和田卓人（t_wada）氏の投稿

- 対象: `comment` スキル（`skills/comment/references/what-goes-where.md`）
- 内容: 「コードには How、テストコードには What、コミットログには Why、コードコメントには Why not を書こう」という投稿（2017 年 9 月 5 日）の一文を英訳して引用し、補足の返信の趣旨を要約したもの
- 出典: https://x.com/t_wada/status/904916106153828352
- ライセンス: なし（出典を明示した引用として掲載）

### C++ Core Guidelines（命名）

- 対象: `review` スキル（`skills/review/SKILL.md` の命名の表）
- 内容: 命名に関する項目（NL.5、NL.8、NL.9、NL.10、ES.9）が挙げる ISO C++ 標準ライブラリーの命名の書き方を、項目番号とリンクで参照し、独自の文章で短くまとめたもの。本文と例は複製していない
- 出典: https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines / https://github.com/isocpp/CppCoreGuidelines
- ライセンス: 独自のライセンス（リポジトリーの `LICENSE`）。複製・改変・派生物の作成を「個人利用または社内業務利用に限り」認めている。このため本文の複製や翻案は行わず、参照と独自の要約にとどめている
- 著作権: Copyright (c) Standard C++ Foundation and its contributors

### Canon TDD(Kent Beck)と日本語訳「テスト駆動開発の定義」(t_wada)

- 対象: `test-case` スキル(`skills/test-case/SKILL.md`、`skills/test-case/references/test-design.md`)、`test-case-writer` サブエージェント(`agents/test-case-writer.md`)
- 内容: テストリストを書き、1 つずつテストにして進める手順と、避けるべき失敗の考え方を、自分の言葉で要約したもの。原文・訳文の転載はしていない
- 出典: https://newsletter.kentbeck.com/p/canon-tdd (Kent Beck、2023-12-11。旧 URL の tidyfirst.substack.com から転送される) / https://t-wada.hatenablog.jp/entry/canon-tdd-by-kent-beck (和田卓人による日本語訳、2023-12-11)
- ライセンス: 原文のページに利用許諾の表示はなく、ページ末尾に「© 2026 Kent Beck」とある(確認日 2026-11-16)。日本語訳は和田卓人氏が Kent Beck 本人の許可を得て公開したもので、訳ページにもライセンスの表示はない。そのため原文・訳文は転載せず、考え方の要約と出典の明記にとどめている

### 『テスト駆動開発』(Kent Beck 著、和田卓人 訳)

- 対象: `test-case` スキル(`skills/test-case/references/test-design.md`)
- 内容: 仮実装・三角測量・明白な実装という進め方の名前と考え方を、自分の言葉で要約したもの。本文の転載はしていない
- 出典: Kent Beck, "Test-Driven Development: By Example", Addison-Wesley, 2002 / 『テスト駆動開発』オーム社、2017 年
- ライセンス: 書籍(著作権は各権利者に帰属)。考え方の要約と出典の明記にとどめている

## 商標

- Visual Studio は Microsoft Corporation の米国およびその他の国における商標または登録商標です。
- CLion は JetBrains s.r.o. の商標または登録商標です。
- Stack Overflow は Stack Exchange, Inc. の商標または登録商標です。

その他の製品名・会社名は、各社の商標または登録商標です。
