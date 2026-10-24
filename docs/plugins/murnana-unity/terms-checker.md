# terms-checker

Unity 関連のツール、Claude Code プラグインやスキル、UPM パッケージ、Unity プロジェクトが Unity の規約に違反していないかを点検するサブエージェント。ファイルは読むだけで、編集はしない。

## 使い方

「Unity の規約に違反していないか確認して」のように頼むと、Claude が必要に応じてこのエージェントに任せる。明示的に呼ぶときは `@murnana-unity:terms-checker` で指定する。

```
@murnana-unity:terms-checker plugins/murnana-unity を点検して
```

点検対象（パス、ディレクトリ、プラグイン、ツールの説明）を渡す。渡さなければ対象を尋ねる報告を返す。

## 点検する規約

| 文書 | 主な観点 |
|---|---|
| [Unity Terms of Service](https://unity.com/legal/terms-of-service) | 17.2 の利用制限（AI エージェント、MCP、CLI 経由の操作、自動アクセス、複製、AI 学習）、26 の定義（Authorized Agentic Access など） |
| [Unity Editor Software Terms](https://unity.com/legal/editor-terms-of-service/software) | Editor のホスティングやリモート実行の禁止、Editor 内でのパッケージ配布、商標 |
| [Guidelines for Using Unity Trademarks](https://unity.com/legal/branding-trademarks) | 製品名への Unity 商標の使用、商標表示と非提携の免責文 |
| [Unity Package Guiding Principles & Guidelines](https://unity.com/legal/terms-of-service/software/package-guidelines) | Editor 内で配布されるパッケージのみ |
| [Unity Manual Terms of Use](https://docs.unity3d.com/Manual/TermsOfUse.html) | Manual の文章（CC BY-NC-ND 4.0）とコード例（Unity Companion License）の再利用 |

## 報告の形式

次の内容を 1 つの報告にまとめて返す。

- 総合判定と点検日
- 前提条件（呼び出し側が確認したものと、エージェントが仮定したものを区別する）
- 指摘ごとの 2 軸の判定表
  - 当てはまり方: Violation / Gray / Missing requirement / OK / Not applicable
  - 影響の大きさ: High / Medium / Low
- 指摘ごとの該当箇所、条項の短い引用、最小の対処。Gray の指摘には、当てはまるとする読み方と当てはまらないとする読み方を両方書く
- 確認できなかった点と、呼び出し側への質問
- 出典と各文書の更新日
- 法的助言ではない旨

規約の内容に関する記述には、すべて出典タグを付ける。

| タグ | 意味 |
|---|---|
| `[fetched <URL>, updated <date>]` | 今回取得し、引用の照合も通った本文 |
| `[via summary — unverified wording]` | 今回取得したが、文言を照合できなかった |
| `[Unity staff, informal …]` | Unity 社員の非公式な投稿 |
| `[third-party …]` | 第三者のトラッカー、ニュース、ブログなど |
| `[snapshot 2026-10-24 — verify]` | 本文末尾の要点メモだけが根拠 |
| `[target <file:line>]` | 点検対象のファイルの内容 |

## 設計

### 毎回最新の規約を取得する

Unity の規約は頻繁に改定される（2026-06-30 には AI エージェントに関する 17.2(ff) が追加された）。そのため規約は記憶に頼らず、毎回 WebFetch で一次情報を取得する。エージェント本文の末尾には 2026-10-24 時点の要点を載せているが、調べる手がかりとしてだけ使い、取得した本文と違えば本文に従う。

Unity スタッフのフォーラムでの回答は参考として扱い、非公式である旨を明記する。判定は規約の本文で行う。

### 法務チェック用 AI の知見を取り入れた点

Anthropic の [claude-for-legal](https://github.com/anthropics/claude-for-legal) や [knowledge-work-plugins/legal](https://github.com/anthropics/knowledge-work-plugins/tree/main/legal) の設計と、LLM による法務判断の研究を参考にしている。

| 仕組み | 理由 |
|---|---|
| 出典タグを付け、消したり格上げしたりしない。スナップショットや第三者の情報だけが根拠の指摘は Gray 止まり | claude-for-legal の `oss-review` のやり方にならった。汎用の LLM は法律の内容について幻覚が多く、自分の幻覚を予測することも苦手なため（[Dahl ら 2024](https://arxiv.org/abs/2401.01301)） |
| 引用は条文そのものを WebFetch に返させ、別の聞き方でもう一度取得して一致したときだけ使う | WebFetch はページそのものではなく、小さなモデルの回答を返すため。また、出典を付けても内容を支えていない生成文が多いことが示されている（[ALCE、Gao ら 2023](https://arxiv.org/abs/2305.14627)） |
| 最初に前提（Unity との個別契約、プラン、地域、配布形態、実行場所、規約の言語）を確定し、分からないものは仮定として報告に書く | knowledge-work-plugins は、社内のレビュー基準や法域を前提として持たせている。同じツールでも、利用者の契約によって結論が変わるため |
| 判定を「当てはまり方」と「影響の大きさ」の 2 軸に分ける | knowledge-work-plugins の legal-risk-assessment が、重大度と発生可能性を分けて評価しているのにならった。影響は規約に書かれた違反時の扱い（権利の終了など）で決め、Unity が実際に動く可能性の推測では決めない |
| Gray の指摘では両方の読み方を並べ、どちらとも決めない。不明なときは厳しい側に倒す | claude-for-legal は、解釈が分かれる点で「the factors cutting both ways」を示す方針を取っている。公開したツールの判定を甘くすると、後から取り返しがつかないため |
| 呼び出し側の「問題ないよね？」という前提に乗らない。数値の確信度は出さない | LLM はユーザーの誤った前提を受け入れやすく（Dahl ら 2024）、評価役としての確信度も高すぎる傾向がある（[arXiv 2508.06225](https://arxiv.org/abs/2508.06225)） |

### 読み取り専用

ツールは `Read`、`Grep`、`Glob`、`WebFetch`、`WebSearch` に限定している。修正方法は提案するが、ファイルの編集や Unity の実行はしない。

### 既知の注意点

このエージェント自身も unity.com や docs.unity3d.com を WebFetch で読む。利用規約 17.2(l)（自動手段によるアクセスの制限）の解釈によってはこれも対象になり得るため、取得は点検に必要なページに限っている。
