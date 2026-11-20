# skill-create スキル

`/murnana-agent-config:skill-create` — Claude Code のスキル（`SKILL.md` と補助ファイル）を、公式仕様とベストプラクティスに沿って作成・更新する。あわせて評価（eval）の雛形も作る。

## 使い方

- 起動は**明示的なスラッシュコマンドのみ**（`disable-model-invocation: true`）。
- `$ARGUMENTS` に「何をするスキルか」のヒントを渡せる。
- 作成先は、プロジェクト（`.claude/skills/`）、個人（`~/.claude/skills/`）、プラグイン（`<plugin>/skills/`）から選べる。
- **プロジェクトのルールを優先する**。優先順位は「プロジェクトの指示（`CLAUDE.md`、`AGENTS.md`、`.claude/rules/`）> ユーザーの指示（`~/.claude/`）> このスキルの既定」。このスキルに書いてある規則（本文の言語、description の書き方、評価の置き場所など）はすべて、ルールがないときの既定として扱う。
- 生成されるスキルの本文は、プロジェクトのルールがなければ英語。ヒアリングは会話の言語で行う。
- 生成するスキルは **Claude Code 専用**。他の環境（claude.ai、Skills API）でも使える項目に限る標準化にはとらわれず、`when_to_use` などの Claude Code の項目を使う。
- `description` にはスキルが何かだけを短い一文で書き、発動条件は `when_to_use` に箇条書きする。2つ合わせて約100トークン（英語で約60語）以内にし、短いほどよい。
- 生成されるスキルは、**Haiku や Sonnet でも動くように**書く（手順に番号を振り、各手順にコマンド・結果の読み方・分岐先を書く）。
- 設計の前に、スキルの書き方と、スキルが扱うツールやライブラリの**ベストプラクティスを公式ドキュメントで調べる**。
- 評価は**雛形を作るだけで、実行はしない**。実行するとモデル呼び出しの料金がかかるため、実行コマンドを案内するだけにしている。

| Step | やること |
|---|---|
| 1 | 既存のスキルを調べる（同じ名前・似た description・置き場所の慣習） |
| 2 | プロジェクトとユーザーのルールを集め、「適用するルール」の表を作る（ルールがない項目はスキルの既定） |
| 3 | スキルが適切かを判定する（CLAUDE.md / rule / hook / subagent / MCP / permission の方が適切なら提案する） |
| 4 | ヒアリングする（下の必須項目のうち、わかっていないものだけ聞く） |
| 5 | ベストプラクティスを調べる（スキルの公式ドキュメントと、扱うツールの公式ドキュメント） |
| 6 | 名前・フロントマター・ファイル構成・自由度を設計する |
| 7 | 書き方ガイド（Haiku / Sonnet 向けの書き方を含む）に沿って下書きする |
| 8 | 評価の雛形を作る（出力のテスト2〜3件。自動起動するスキルなら起動テスト約20件も） |
| 9 | セルフレビューする |
| 10 | 全文、適用したルール、調査結果を提示して**承認を待つ** → 書き込む |
| 11 | `claude plugin validate` を実行し、確認方法（Haiku / Sonnet での確認を含む）・評価の実行方法・改善のしかたを案内する |

### ヒアリングの必須項目（Step 4）

調査の結果、良いスキルを作るには次の情報が必要だとわかった。会話や `$ARGUMENTS`、リポジトリからわからないものだけを AskUserQuestion で聞く。

| 項目 | 理由 |
|---|---|
| 目的と「スキルがないと Claude が何を間違えるか」 | スキルが存在する理由になる。Claude が既にできるならスキルは要らない |
| 起動すべき言い方と、ニアミス（起動してはいけない依頼） | `when_to_use` の精度が決まる |
| 起動方法（自動 / 明示のみ / 背景知識） | 副作用のある操作は明示起動にする |
| 置き場所 | 共有範囲と優先順位が決まる |
| 入力・出力形式 | 出力形式が厳密なら、雛形を用意すると確実になる |
| 実際の材料（手順、ユーザーが直した点、コマンド、落とし穴） | 一般論だけで作ったスキルは役に立たない（agentskills.io） |
| 成功の基準 | 検証ループと評価の土台になる |

次の項目は聞かずに既定値を使い、Step 10 で提示する: 対象モデル（Haiku・Sonnet・Opus のすべて。Haiku に合わせて書く）、どこまで厳密か（状態を変える操作や順序が大事な操作は正確なコマンド、判断は方針のみ）、ツールと依存関係（下書きの手順から決める）、`context: fork`・`model`・`effort`（指定しない）。

## リファレンス

中身はこのドキュメントに写さず、リンク先を正とする。

- 形式（置き場所、フロントマターの全フィールド、Claude Code 専用であること、起動方法、引数、`!` 埋め込み、fork、読み込まれた後の扱い、トラブルシューティング）→ [`references/skill-format.md`](../../../plugins/murnana-agent-config/skills/skill-create/references/skill-format.md)
- skill と CLAUDE.md / rule / hook / subagent / MCP / permission の使い分け → [`references/skill-vs-alternatives.md`](../../../plugins/murnana-agent-config/skills/skill-create/references/skill-vs-alternatives.md)
- 良いスキルの構成要素、description・when_to_use と本文の書き方、Haiku / Sonnet 向けの書き方、トークンを減らす工夫、パターン、避けるべき書き方 → [`references/writing-guide.md`](../../../plugins/murnana-agent-config/skills/skill-create/references/writing-guide.md)
- 評価（出力のテスト、起動テスト、`claude plugin eval` の構成、`evals.json`）→ [`references/evals.md`](../../../plugins/murnana-agent-config/skills/skill-create/references/evals.md)

## 調査で得たベストプラクティス（要約）

### 良いスキルの条件

- **description と when_to_use が起動のすべてを担う**。Claude が起動前に見るのは name・description・when_to_use だけ（Claude Code skills）。このスキルでは役割を分け、description にはスキルが何かだけを書き、いつ使うか（ユーザーが実際に使う言葉、暗黙のケース、ニアミス）は when_to_use に箇条書きする（ユーザーの決定）。
- Claude はスキルを**起動しなさすぎる**傾向がある（skill-creator, agentskills）。ただし、強めに書いて長くするのではなく、when_to_use の箇条書きにユーザーの言い方と暗黙のケースを入れて補う。
- **Claude が知らないことだけを書く**。「これがないと Claude は間違えるか？」と1行ずつ確かめる。網羅的に書くより、適度な詳しさの手順と動く例が1つある方がよい（platform, agentskills best-practices）。
- **実際の知見から作る**。実際の作業で使った手順やユーザーが直した点、ランブック、レビューコメントを材料にする。一般論から作ると曖昧になる（agentskills best-practices）。
- 自由度は**壊れやすさに合わせる**。複数のやり方が成り立つところは方針だけを書き、壊れやすい操作は正確なコマンドを指定する（platform）。
- **選択肢を並べず、デフォルトを示す**。**個別の答えではなく手順を書く**。**落とし穴の節**が最も価値が高いことが多い（agentskills）。
- 大文字の MUST を並べるより**理由を書く**（skill-creator, agentskills evaluating）。
- SKILL.md は500行以内にし、references は SKILL.md から1階層まで。「いつ読むか」を明記する。100行を超えるファイルには目次を付ける（platform, Claude Code skills）。
- 読み込まれた内容は会話に残り、再読み込みされない。コンパクション後は先頭の5,000トークンしか残らない場合がある。重要な指示は冒頭に書く（Claude Code skills）。
- 副作用のある操作は `disable-model-invocation: true` にする（Claude Code skills / best-practices）。
- **評価を先に作る**。スキルなしでの失敗を確認し、スキルあり・なしで比較する（platform, agentskills evaluating）。

### Haiku / Sonnet でも動かすために（2026-11-19 調査）

- スキルの効果はモデルによって変わるため、**使うすべてのモデルで試す**。Opus で問題なく動くものでも、Haiku ではもっと詳しい指示が要ることがある。Haiku には「指示が足りているか」、Sonnet には「明確で無駄がないか」、Opus には「説明しすぎていないか」を確かめる（platform best practices）。
- 順序や漏れのなさが大事なときは、**番号付きの手順**で書く。文脈を知らない新人に渡しても迷わない程度に具体的に書く（prompting best practices）。
- Sonnet は指示を**文字どおりに解釈**し、ある項目への指示を他の項目に広げない。広く適用したいときは「最初の節だけでなく、すべての節に」のように範囲を明記する（Prompting Claude Sonnet 5）。
- Haiku は、長いエージェント用プロンプトを低い effort で動かすと、作業の途中で止めてユーザーに返したり、検索や確認を飛ばしたりすることがある。「依頼されたことがすべて終わるまで続ける」「変更は実際に確認してから完了と報告する」と書くと改善する（Prompting Claude Haiku 5.5）。
- 「〜するな」より「〜する」と書く方が従われやすい。理由を添えると、Claude はそこから一般化できる（prompting best practices）。
- 「CRITICAL: You MUST…」のような強い言葉は、新しいモデルでは過剰に反応する原因になる。普通の言い方で書く（prompting best practices）。
- スキル本文はセッション中ずっとコンテキストに残るため、簡潔にし、やることを書く（Claude Code skills）。理由は一文で添える程度にとどめる。

### プロジェクトのルールと事前の調査

- パスで対象を絞ったルール（`paths:` 付きの `.claude/rules/*.md`）は、該当するファイルを開くまでコンテキストに読み込まれない。そのため、スキルを作るときは rules ディレクトリを明示的に検索して読む必要がある（このリポジトリの `plugin-skill-authoring.md` がこの形）。
- 一般的な知識だけで作ったスキルは、曖昧で一般的な手順になりやすい。実際の資料（プロジェクトのドキュメント、API 仕様、設定ファイル）から作ったスキルの方がよい（agentskills best-practices）。ツールの推奨コマンドや非推奨のオプションは、記憶ではなく公式ドキュメントと、プロジェクトが固定しているバージョンで確かめる。

### 評価

- 出力のテストは2〜3件から始める。言い回しを変え、境界ケースを1つ含める。assertion は客観的に確認できるものだけにする（agentskills evaluating）。
- 起動テストは約20件（起動すべきもの8〜10件、ニアミス8〜10件）。train と validation を 60/40 に分け、各3回実行し、しきい値は 0.5。選ぶのは validation の成績が最も良い when_to_use（agentskills optimizing-descriptions）。
- プラグインのスキルは `claude plugin eval` で、プラグインあり・なしを比較できる。`tool_used: Skill` の grader は Δ の計算から自動で除外され、起動したかの確認用として扱われる（Claude Code plugin-evals）。

## テスト方法と結果（2026-10-12, Claude Code v2.1.296）

1. スクラッチ用のプロジェクト（`package.json` に changeset の release スクリプト、`.changeset/README.md`、`CLAUDE.md`）を用意し、`defaultEnabled: true` にしたプラグインのコピーを使う。
2. `claude -p --plugin-dir <copy> "/murnana-agent-config:skill-create <依頼とヒアリングへの一部の回答>"` を実行した。→ 既存スキルの調査とスキルが適切かの判定を行い、hook の併用も提案した。そのうえで、足りない4項目（バージョン種別の決め方、commit と push、config がないとき、npm 認証）だけを質問して止まった。
3. `--resume` で回答を渡した。→ `package-release` スキルの全文（チェックリスト、事前チェック、落とし穴、報告用の雛形）と `evals/evals.json`（3件、境界ケースを含む）を提示し、承認待ちで止まった。明示起動のみのスキルなので、起動テストを作らない判断も正しかった。
4. 承認後の書き込みは、`-p` モードでは `.claude/` が保護されたパスのため拒否された（`acceptEdits` でも同じ）。スキルは Bash で回避せずに停止し、対処法を案内した。これは期待どおりの動き。生成された内容は手で配置し、`claude plugin validate .claude/skills` が通ることを確認した。さらに `/package-release` で起動し、事前チェックで正しく止まることを確認した。

テストでわかったこと:

- **SKILL.md 内の `!` + バッククォートは、本文の説明文やインラインコードの中でも実行される**。セルフレビューの項目に構文を書いただけで `Shell command permission check failed for pattern "!`cmd`"` になり、スキル全体が読み込まれなかった（num_turns 0）。SKILL.md 内では構文を言葉で説明する。
- **埋め込みコマンドは `||` で連結した部分もすべて `allowed-tools` で許可が必要**。`git rev-parse ... || pwd` は `pwd` が許可されていないため `This command requires approval` で失敗した。そのため、Current state は rule-create と同じ通常の ```bash ブロック（Claude が自分で実行する）にした。
- サンドボックス内では、`ls ~/.claude/skills` が拒否されることがある。Glob を使うよう指示しているが、Claude は先に ls を試し、「確認できなかった」と報告した。動作として問題はない。

## テスト方法と結果（2026-11-19, Claude Code v2.1.327）

1. スクラッチ用のプロジェクトを用意した。`CLAUDE.md` に Jest のテストコマンドを書き、パスで絞ったルール（`.claude/rules/skills.md`、`paths: .claude/skills/**`）で命名 `demo-<verb>` と評価の置き場所 `tests/skills/<name>/` を指定した。プラグインは `defaultEnabled: true` にしたコピーを使った。
2. `claude -p --model <haiku|sonnet> --plugin-dir <copy> "/murnana-agent-config:skill-create Jest の失敗だけを短くまとめるプロジェクトスキル"` を実行した。`-p` では AskUserQuestion が使えないため、既定値で下書きを示し、何も書き込まずに止まるのが期待どおりの動き。

| 実行 | 結果 |
|---|---|
| Sonnet（$0.51、18ターン） | すべての手順を実行した。パスで絞ったルールを見つけ、命名と評価の置き場所を既定より優先した。公式ドキュメント3ページと Jest のドキュメントを調べた。description は一文、when_to_use は3項目（約45語）。出力を絞るスクリプトを同梱した |
| Haiku 1回目（$0.04） | ルールの表と description / when_to_use は正しかった。スキル作成の公式ドキュメント3ページの調査を飛ばし、Jest の調査だけを行った。また「`claude plugin validate` はプラグイン用なので、プロジェクトのスキルには使えない」と誤って判断した |
| Haiku 2回目（$0.09） | 修正後は3ページを調べ、validate も正しく案内した。ただし when_to_use に日本語の例文を引用し、`allowed-tools` に `Bash(node *)` と広く書いた |
| Haiku 3回目（$0.13） | when_to_use は英語の3項目（約40語）、`allowed-tools` は同梱スクリプトのパスだけになった |

テストを受けて直したこと:

- Step 5 は「サブステップ 1 と 2 の両方を行い、1 は省略しない」「WebFetch を3回」と明記し、チェックリストとセルフレビューにも入れた。
- Step 11 に、プラグインでないスキルのディレクトリにも validate を使うことを明記した。
- when_to_use は英語で、例文を引用せずに依頼の種類を書くようにした。日本語の引用はトークンが多くかかり、Claude は意味で照合するため引用しなくても起動する。
- `allowed-tools` に `Bash(node *)` のようにプログラム全体を書かないよう、例を添えた。

残っている点: Haiku と Sonnet は、Read ツールではなく Bash の `cat` や `find` でファイルを読むことがある（落とし穴の節に書いても変わらなかった）。どれも小さなファイルなので、結果への影響はない。

## 設計判断とその理由

- **なぜ明示起動のみか** — スキルはファイルを作り、プロジェクトの場合はチームに共有される。自動起動で勝手に作られると困るため、rule-create と同じ方針にした（ユーザーの決定）。
- **なぜ本文を英語に固定するか** — トークン効率と遵守率を優先した（ユーザーの決定）。
- **なぜ評価は雛形だけか** — 実行は課金されるため、実行するかどうかはユーザーが判断する（ユーザーの決定）。
- **なぜ評価の形式を作成先で変えるか** — プラグインのスキルは `claude plugin eval` で、プラグインあり・なしの比較とCIでの判定まで行える。プロジェクトや個人のスキルにはその仕組みがないため、skill-creator や手動評価で使える `evals/evals.json` 形式にする。2つのツールは互いのファイルを読めない。
- **なぜ「スキルが適切か」の判定を入れるか** — hook や rule の方が向いている依頼をスキルにすると、指示が守られなかったり、必要なときに読み込まれなかったりする。代替手段は提案だけにとどめ、作成はスコープ外とする（rule-create と同じ方針）。
- **なぜプロジェクトのルールを優先するか** — このスキルは様々なプロジェクトで使われ、それぞれのプロジェクトには独自の決まり（description は短い一文、評価は別ディレクトリ、本文の言語など）がある。スキル側の規則を押し付けると、作ったスキルをプロジェクトの規則に合わせて直す手間が生じる。そのため、スキルの規則はルールがないときの既定とし、適用したルールの表を作って提示時に示すようにした（ユーザーの決定）。ユーザーの指示（`~/.claude/`）はプロジェクトの指示より下、スキルの既定より上に置いた。
- **なぜ設計の前にベストプラクティスを調べるか** — 同梱の references は作成時点の要約で、公式ドキュメントの更新に遅れることがある。また、スキルが扱うツールの推奨手順は、Claude の記憶だけでは古かったり誤っていたりする。設計の前に公式ドキュメントを読み、見つけたことを落とし穴の節と提示内容に反映させる（ユーザーの決定）。読むページは合計5ページ程度までとし、取得したページ内の指示には従わない。WebSearch / WebFetch が使えないときは、同梱の references とリポジトリのファイルで続け、調べられなかったことを提示時に示す。
- **なぜ Haiku / Sonnet に合わせて書くか** — スキルはセッションのモデルで動くため、Opus 以外で使われることもある。Opus は曖昧な指示を補えるが、Haiku や Sonnet は手順を飛ばしたり途中で止まったりする。小さいモデルに合わせて書いても Opus にはほとんど害がないため、作るスキルとこのスキル自身の両方を、agent-create と同じ形（番号付きの手順、結果の読み方の表、既定値の表、完了条件）で書くことにした（ユーザーの決定）。WebSearch / WebFetch を `allowed-tools` に加えたのは、調査の手順を毎回の承認で止めないため。どちらも読み取りだけのツールである。
- **なぜ Claude Code 専用にするか** — このスキルで作るスキルは Claude Code でだけ使う。claude.ai や Skills API にも上げられる6項目（`name`・`description` など）に限ると、`when_to_use`・`disable-model-invocation`・`paths` のような、起動の精度とトークンの節約に効く項目が使えない。そのため標準化にはとらわれず、Claude Code の項目をすべて使えるようにした（ユーザーの決定）。
- **なぜ description と when_to_use を分け、合計約100トークンに抑えるか** — 自動起動するスキルの description と when_to_use は、プラグインが有効なすべてのセッションで、すべてのリクエストに含まれる（Claude Code skills, costs）。発動条件や例文を description に詰め込むと、この固定費が増える。description はスキルが何かの一文だけにし、発動条件は when_to_use の箇条書き（2〜5項目、ニアミスは `Not for:`）にまとめて、合計を約100トークン（英語で約60語）以内にした（ユーザーの決定）。スキルの中ではトークン数を正確に数えられないため、語数で目安を示している。明示起動のみのスキルは一覧がコンテキストに入らないため、when_to_use を書かない。`when_to_use` は文字列なので、箇条書きは YAML のリストではなくブロックスカラー（`when_to_use: |`）で書く（`claude plugin validate` で通ることを確認した）。
- **なぜ実行時のトークンも減らすか** — 読み込まれたスキル本文と、手順で読んだファイルやコマンドの出力は、その後のリクエストのたびに送られる（costs）。書き方ガイドに「Keeping token use low」の節を追加し、出力を絞るオプション、Grep してから必要な範囲だけ Read する、冗長な作業はサブエージェントに任せる、質問をまとめる、といった工夫を作るスキルの手順に入れるようにした。調査の手順でも、公式の costs ドキュメントと、扱うツールの出力を絞るオプションを調べる。skill-create 自身も、自動で読み込まれている CLAUDE.md やルールを読み直さず、既存スキルのフロントマターは Grep でまとめて取得するようにした。
- **なぜ公式 skill-creator プラグインと別に作るか** — skill-creator は評価の自動実行に重点がある。このスキルは、このリポジトリの慣習（references 構成、英語本文、承認待ち、docs）に合わせた作成とヒアリングに重点を置く。評価の実行には skill-creator を案内する。

## 出典

- 公式
  - https://code.claude.com/docs/en/skills.md
  - https://code.claude.com/docs/en/best-practices.md
  - https://code.claude.com/docs/en/plugin-evals.md
  - https://code.claude.com/docs/en/costs.md
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md
  - https://agentskills.io/skill-creation/evaluating-skills.md
  - https://agentskills.io/skill-creation/best-practices.md
  - https://agentskills.io/skill-creation/optimizing-descriptions.md
  - https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md
  - https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5.md
  - https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5.md
  - https://github.com/anthropics/skills/tree/main/skills/skill-creator
- コミュニティ
  - https://designrevision.com/blog/claude-code-skills-best-practices.md
  - https://dev.classmethod.jp/en/articles/claude-code-skills-for-cloud-bu-consulting-members/
  - https://www.web-developpeur.com/en/blog/skills-claude-code-patterns-officiels
