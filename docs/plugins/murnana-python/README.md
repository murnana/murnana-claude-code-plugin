# Python

Python(プログラムを書くための言語のひとつ)で書いたプログラムに、読みやすく役に立つ説明書き(コメント)を Claude に書いてもらうためのプラグインです。

> 開発中です。実際のプロジェクトで最後まで通して使うテストはこれからです。

## こんなときに使います

- 自分の書いた Python のプログラムに、説明書き(コメント)を付けたい
- ほかの人が使う部品に、使い方の説明(docstring という決まった形の説明)を付けたい
- いまある説明書きが、本当に必要なものか見直したい

## できること

| やりたいこと | 使う機能 | 説明 |
|---|---|---|
| 説明書きを書く・見直す | [Python のコメント作成](comment.md) | 書く内容をふさわしい場所に振り分けて、必要な説明書きだけを書く |

## インストール

```
claude plugin marketplace add murnana/murnana-claude-code-plugin --sparse .claude-plugin
claude plugin install murnana-python@murnana-claude-code-plugin
```

インストールしただけでは使えるようになりません。`/plugin` と入力して開く画面で、このプラグインを有効にしてください。

## あわせて入れると便利なもの

- **Python のプログラムの中を調べる道具(pyright)**: Claude Code から使えるようにすると、Claude がファイルを丸ごと読まずに、部品が使われている場所を調べられます。そのぶん、読む量が減ります。

  ```
  npm install -g pyright
  claude plugin install pyright-lsp@claude-plugins-official
  ```

  入れなくても動きます。そのときは、文字列で検索して代わりに調べます。クラウド上の Claude Code では、この道具は動きません。
- **書き方の検査の道具(Ruff)**: 入っていると、書いた使い方の説明(docstring)が決まった形に合っているかを確かめます。入っていなくても、Claude が読み直して確かめます。Claude が勝手に入れることはありません。

## 知っておいてほしいこと

- **Claude のモデルは Sonnet に固定しています。** この機能を使っている間だけ Sonnet で動き、次にあなたが話しかけると元のモデルに戻ります。組織の設定で Sonnet が使えないときは、元のモデルのまま動きます。
- **プログラムそのものは変えません。** 変えるのはコメントと使い方の説明(docstring)だけです。
- **理由を作り話にはしません。** 「なぜこう書いたのか」が記録からも分からないときは、あなたに質問します。質問できないときは、その場所にはコメントを書かず、報告にまとめます。

## 出典

- 説明書きの置き場所の考え方は、和田卓人さん(@t_wada)の「コードには How テストコードには What コミットログには Why コードコメントには Why not を書こう」(https://x.com/t_wada/status/904916106153828352)をもとにしています。
- 使い方の説明(docstring)の書き方は、PEP 257(https://peps.python.org/pep-0257/、パブリックドメイン)をもとに、AI(Claude)が要約・翻案したものです。
- Python は Python Software Foundation の登録商標です。
