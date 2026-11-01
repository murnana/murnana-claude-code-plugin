# Kotlin

Kotlin(プログラミング言語の一つ)で書いたプログラムに、Claude が説明書き(コメント)を付けたり、いらない説明書きを整理したりするためのプラグインです。

> 開発中です。実際のプロジェクトで最後まで通して使うテストはこれからです。

## こんなときに使います

- 他の人が使う部分に、使い方の説明を付けたい
- 説明書きが多すぎたり古くなったりしていて、整理したい
- 「なぜこう書いたのか」を、あとから読む人に残したい

## できること

| やりたいこと | 使う機能 | 説明 |
|---|---|---|
| 説明書きを付ける・整理する | [コメントの作成](comment.md) | 書くべき場所にだけ説明を付け、いらない説明は消すか、ほかの場所に移すよう提案する |

## インストール

```
claude plugin marketplace add murnana/murnana-claude-code-plugin --sparse .claude-plugin
claude plugin install murnana-kotlin@murnana-claude-code-plugin
```

## あると便利なもの

Kotlin LSP(プログラムの中の名前や型を正確に調べる道具)を入れておくと、調べる精度が上がります。入れ方は[コメントの作成](comment.md#もっと正確にしたいときなくても使えます)を見てください。なくても使えます。

## 出典

- 説明書きの書き方は、Kotlin の公式ドキュメント「Document Kotlin code: KDoc」(https://kotlinlang.org/docs/kotlin-doc.html)と「Coding conventions」(https://kotlinlang.org/docs/coding-conventions.html)をもとに、AI(Claude)が要約・加工したものです(Apache License 2.0)。
- 「どこに何を書くか」の考え方は、和田卓人さん(@t_wada)の投稿「コードには How テストコードには What コミットログには Why コードコメントには Why not を書こうという話をした」(https://x.com/t_wada/status/904916106153828352)をもとにしています。
- Kotlin は Kotlin Foundation により保護された商標です。
