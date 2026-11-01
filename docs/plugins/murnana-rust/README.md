# Rust

プログラミング言語 Rust で書いたプログラムに、Claude がコメント(プログラムの中に書く説明文)を書いたり整理したりするためのプラグインです。

> 開発中です。実際のプロジェクトで最後まで通して使うテストはこれからです。

## こんなときに使います

- 自分の書いた Rust のプログラムに、ほかの人が使うための説明を付けたい
- プログラムの中の、古くなったり意味の重なったりしているコメントを整理したい

## できること

| やりたいこと | 使う機能 | 説明 |
|---|---|---|
| コメントを書く・整理する | [Rust のコメント作成](comment.md) | 書くべき内容を決まった場所に振り分けて、コメントと説明文を書く |

## インストール

```
claude plugin marketplace add murnana/murnana-claude-code-plugin --sparse .claude-plugin
claude plugin install murnana-rust@murnana-claude-code-plugin
```

## あわせて入れると便利なもの

Rust のプログラムの中を調べる道具(rust-analyzer)を Claude Code から使えるようにすると、Claude がファイルを丸ごと読まずに、部品の場所や使われている場所を探せます。次の2つを入れてください。

```
rustup component add rust-analyzer
claude plugin install rust-analyzer-lsp@claude-plugins-official
```

入れなくても動きます。そのときは、文字列の検索で代わりに探します。

## 知っておいてほしいこと

- **Claude のモデルは Sonnet に固定しています。** この機能を使っている間だけ Sonnet で動き、次にあなたが話しかけると元のモデルに戻ります。組織の設定で Sonnet が使えないときは、元のモデルのまま動きます。

- **理由を作り話にはしません。** 「なぜこう書いたのか」が記録からも分からないときは、あなたに質問します。
- **書いた説明文の中の例は、実際に動かして確かめます。** 確かめられなかったときは、そう報告します。

## 出典

- コメントに何を書くかの考え方は、和田卓人さん(@t_wada)の投稿「コードには How テストコードには What コミットログには Why コードコメントには Why not を書こう」(https://x.com/t_wada/status/904916106153828352)にもとづきます。その行を読むのに欠かせない理由はコメントにも残す、という補足は、John Ousterhout『A Philosophy of Software Design』などの考え方を参考にしています。
- 説明文の書き方は、Rust by Example「Documentation」(https://doc.rust-lang.org/rust-by-example/meta/doc.html、MIT License)の一部を抜粋・加工したものと、RFC 1574(https://rust-lang.github.io/rfcs/1574-more-api-documentation-conventions.html)の要約にもとづきます。

Rust、Cargo は Rust Foundation の商標または登録商標です。
