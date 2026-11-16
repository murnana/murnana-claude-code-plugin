# C#

C# のプログラムを書くときに、Claude に手伝ってもらうためのプラグインです。

> 開発中です。実際のプロジェクトで最後まで通して使うテストはこれからです。

## できること

| やりたいこと | 使う機能 | 説明 |
|---|---|---|
| コメントを書く・見直す | [コメントの作成と見直し](comment.md) | 本当に必要なことだけをコメントに残し、外から使う人向けの説明も書く |
| テストを書く・見直す | [C# のテストケース作成](test-case.md) | 確かめたい動きを先に書き出してから、1 つずつテストにする |
| テストをまとめて任せる | [test-case-writer](test-case-writer.md) | すでにあるプログラムのテストを別の Claude に書かせて、報告だけを受け取る |

## はじめる前に準備するもの

Claude がプログラムの中身を素早く正確に調べられるように、マイクロソフトが公開している C# の解析用プログラム(Roslyn の言語サーバー)を使います。プラグインを入れる前に、次の2つを入れてください。

1. .NET 10 以降(C# のプログラムを動かすための土台)
2. 解析用プログラム。ターミナル(文字で命令を入力する画面)で次を実行します。

   ```
   dotnet tool install --global roslyn-language-server --prerelease
   ```

   `roslyn-language-server` と入力して動けば準備はできています。

入れていなくてもプラグインは使えますが、Claude がファイルを広く読むことになるので、時間と利用量が増えます。

- Claude Code をブラウザーで使う場合(クラウドで動く場合)は、この解析用プログラムは使われません。
- Anthropic 公式の `csharp-lsp` プラグインも入れていると、どちらか一方しか使われません。このプラグインの解析用プログラムを使うには、`csharp-lsp` を無効にしてください。

## インストール

```
claude plugin marketplace add murnana/murnana-claude-code-plugin --sparse .claude-plugin
claude plugin install murnana-csharp@murnana-claude-code-plugin
```

## 出典

- コメントの考え方は、和田卓人(@t_wada)氏の投稿「コードには How テストコードには What コミットログには Why コードコメントには Why not を書こう」(https://x.com/t_wada/status/904916106153828352)をもとにしています。
- 説明用コメント(XML ドキュメントコメント)の決まりは、Microsoft Learn の「Generate XML API documentation comments」と「Recommended XML tags for C# documentation comments」(© Microsoft Corporation、CC BY 4.0)を、AI(Claude)が要約・加工して作成したものです。原文そのものではなく、Microsoft の見解でもありません。
- テストの書き方は、Kent Beck「Canon TDD」(https://newsletter.kentbeck.com/p/canon-tdd)と、和田卓人さん(@t_wada)による日本語訳「テスト駆動開発の定義」(https://t-wada.hatenablog.jp/entry/canon-tdd-by-kent-beck)の考え方をもとに、AI(Claude)が自分の言葉でまとめたものです。
