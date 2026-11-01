# Swift

Swift(Apple が作ったプログラミング言語)で書いたプログラムに、読みやすく役に立つ説明書き(コメント)を Claude に書いてもらうためのプラグインです。

> 開発中です。実際のプロジェクトで最後まで通して使うテストはこれからです。

## こんなときに使います

- 自分の書いた Swift のプログラムに、説明書き(コメント)を付けたい
- ほかの人が使う機能に、使い方の説明(ドキュメントコメント)を付けたい
- いまある説明書きが、本当に必要なものか見直したい

## できること

| やりたいこと | 使う機能 | 説明 |
|---|---|---|
| 説明書きを書く・見直す | [Swift のコメント作成](comment.md) | 書く内容をふさわしい場所に振り分けて、必要な説明書きだけを書く |

## インストール

```
claude plugin marketplace add murnana/murnana-claude-code-plugin --sparse .claude-plugin
claude plugin install murnana-swift@murnana-claude-code-plugin
```

## あわせて入れると便利なもの

Swift のプログラムの中を調べる道具(SourceKit-LSP)を Claude Code から使えるようにすると、Claude がファイルを丸ごと読まずに、部品の場所や使われている場所、型を調べられます。SourceKit-LSP は Xcode や Swift の開発道具一式に入っています。Claude Code では次のプラグインを入れてください。

```
claude plugin install swift-lsp@claude-plugins-official
```

入れなくても動きます。そのときは、ファイルを読んだり文字列で検索したりして代わりに調べます。

- Xcode のプロジェクト(`Package.swift` がないもの)では、ほかのファイルとのつながりまで正しく調べるには、別の準備(ビルドの設定を SourceKit-LSP に渡す道具)が必要です。準備がないときは、開いているファイルの中だけを調べます。
- クラウド上の Claude Code では、この道具は動きません。

## 知っておいてほしいこと

- **Claude のモデルは Sonnet に固定しています。** この機能を使っている間だけ Sonnet で動き、次にあなたが話しかけると元のモデルに戻ります。組織の設定で Sonnet が使えないときは、元のモデルのまま動きます。
- **プログラムそのものは変えません。** 変えるのはコメントだけです。作業の前後でプログラムが変わっていないことを、自動で確かめます。
- **理由を作り話にはしません。** 「なぜこう書いたのか」が記録からも分からないときは、あなたに質問します。質問できないときは、報告の最後に質問として書きます。

## 出典

- 説明書きの置き場所の考え方は、和田卓人さん(@t_wada)の「コードには How テストコードには What コミットログには Why コードコメントには Why not を書こう」(https://x.com/t_wada/status/904916106153828352)をもとにしています。
- 使い方の説明の書き方は、Swift-DocC のドキュメント(https://www.swift.org/documentation/docc/writing-symbol-documentation-in-your-source-files 、https://www.swift.org/documentation/docc/formatting-your-documentation-content 、Copyright (c) 2021-2026 Apple Inc. and the Swift project authors、Apache License 2.0)を、AI(Claude)が要約・加工して作成したものです。
- Swift、Xcode は Apple Inc. の商標です。
