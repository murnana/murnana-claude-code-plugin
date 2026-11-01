# TypeScript

TypeScript(プログラムを書くための言語のひとつ)で書いたプログラムに、読みやすく役に立つ説明書き(コメント)を Claude に書いてもらうためのプラグインです。

> 開発中です。実際のプロジェクトで最後まで通して使うテストはこれからです。

## こんなときに使います

- 自分の書いた TypeScript のプログラムに、説明書き(コメント)を付けたい
- ほかの人が使う部品に、使い方の説明(TSDoc という決まった形の説明)を付けたい
- いまある説明書きが、本当に必要なものか見直したい

## できること

| やりたいこと | 使う機能 | 説明 |
|---|---|---|
| 説明書きを書く・見直す | [TypeScript のコメント作成](comment.md) | 書く内容をふさわしい場所に振り分けて、必要な説明書きだけを書く |

## インストール

```
claude plugin marketplace add murnana/murnana-claude-code-plugin --sparse .claude-plugin
claude plugin install murnana-typescript@murnana-claude-code-plugin
```

## あわせて入れると便利なもの

- **TypeScript のプログラムの中を調べる道具(typescript-language-server)**: Claude Code から使えるようにすると、Claude がファイルを丸ごと読まずに、部品の場所や使われている場所、型を調べられます。そのぶん、読む量が減ります。次の2つを入れてください。

  ```
  npm install -g typescript-language-server typescript
  claude plugin install typescript-lsp@claude-plugins-official
  ```

  入れなくても動きます。そのときは、ファイルを読んだり文字列で検索したりして代わりに調べます。クラウド上の Claude Code では、この道具は動きません。
- **TSDoc の検査の道具(@microsoft/tsdoc)**: プロジェクトに入っていると、書いた説明が決まった形に合っているかを、より細かく確かめます。入っていなくても、このプラグインに付いている検査は行います。

## 知っておいてほしいこと

- **Claude のモデルは Sonnet に固定しています。** この機能を使っている間だけ Sonnet で動き、次にあなたが話しかけると元のモデルに戻ります。組織の設定で Sonnet が使えないときは、元のモデルのまま動きます。
- **プログラムそのものは変えません。** 変えるのはコメントだけです。作業の前後でプログラムが変わっていないことを、自動で確かめます。
- **理由を作り話にはしません。** 「なぜこう書いたのか」が記録からも分からないときは、あなたに質問します。質問できないときは、報告の最後に質問として書きます。

## 出典

- 説明書きの置き場所の考え方は、和田卓人さん(@t_wada)の「コードには How テストコードには What コミットログには Why コードコメントには Why not を書こう」(https://x.com/t_wada/status/904916106153828352)をもとにしています。
- 使い方の説明の書き方と、ほかの部品へのつなぎ方(リンクの書き方)は、Microsoft の TSDoc(https://github.com/microsoft/tsdoc、MIT ライセンス)をもとに、AI(Claude)が要約・翻案したものです。
- TypeScript、TSDoc は Microsoft Corporation の商標または登録商標です。
