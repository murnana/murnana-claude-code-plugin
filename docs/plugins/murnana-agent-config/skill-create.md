# skill-create スキル

`/murnana-agent-config:skill-create` — Claude Code のスキル（`SKILL.md` と補助ファイル）を、公式仕様とベストプラクティスに沿って作成・更新する。あわせて評価（eval）の雛形も作る。

## 使い方

- 起動は**明示的なスラッシュコマンドのみ**（`disable-model-invocation: true`）。
- `$ARGUMENTS` に「何をするスキルか」のヒントを渡せる。
- 作成先は、プロジェクト（`.claude/skills/`）、個人（`~/.claude/skills/`）、プラグイン（`<plugin>/skills/`）から選べる。
- 生成されるスキルの本文は**常に英語**。ヒアリングは会話の言語で行う。
- 評価は**雛形を作るだけで、実行はしない**。実行するとモデル呼び出しの料金がかかるため、実行コマンドを案内するだけにしている。

| Step | やること |
|---|---|
| 1 | 既存のスキルを調べる（同じ名前・似た description・置き場所の慣習） |
| 2 | スキルが適切かを判定する（CLAUDE.md / rule / hook / subagent / MCP / permission の方が適切なら提案する） |
| 3 | ヒアリングする（下の必須項目のうち、わかっていないものだけ聞く） |
| 4 | 名前・フロントマター・ファイル構成・自由度を設計する |
| 5 | 書き方ガイドに沿って下書きする |
| 6 | 評価の雛形を作る（出力のテスト2〜3件。自動起動するスキルなら起動テスト約20件も） |
| 7 | セルフレビューする |
| 8 | 全文を提示して**承認を待つ** → 書き込む |
| 9 | `claude plugin validate` を実行し、確認方法・評価の実行方法・改善のしかたを案内する |

### ヒアリングの必須項目（Step 3）

調査の結果、良いスキルを作るには次の情報が必要だとわかった。会話や `$ARGUMENTS`、リポジトリからわからないものだけを AskUserQuestion で聞く。

| 項目 | 理由 |
|---|---|
| 目的と「スキルがないと Claude が何を間違えるか」 | スキルが存在する理由になる。Claude が既にできるならスキルは要らない |
| 起動すべき言い方と、ニアミス（起動してはいけない依頼） | description の精度が決まる |
| 起動方法（自動 / 明示のみ / 背景知識） | 副作用のある操作は明示起動にする |
| 置き場所 | 共有範囲と優先順位が決まる |
| 入力・出力形式 | 出力形式が厳密なら、雛形を用意すると確実になる |
| 実際の材料（手順、ユーザーが直した点、コマンド、落とし穴） | 一般論だけで作ったスキルは役に立たない（agentskills.io） |
| どこまで厳密か | 自由度の高低を決める（platform best practices） |
| ツール・依存関係・fork の要否 | `allowed-tools` と `context` が決まる |
| 成功の基準 | 検証ループと評価の土台になる |

## リファレンス

中身はこのドキュメントに写さず、リンク先を正とする。

- 形式（置き場所、フロントマターの全フィールド、他の環境で使えるフィールド、起動方法、引数、`!` 埋め込み、fork、読み込まれた後の扱い、トラブルシューティング）→ [`references/skill-format.md`](../../../plugins/murnana-agent-config/skills/skill-create/references/skill-format.md)
- skill と CLAUDE.md / rule / hook / subagent / MCP / permission の使い分け → [`references/skill-vs-alternatives.md`](../../../plugins/murnana-agent-config/skills/skill-create/references/skill-vs-alternatives.md)
- 良いスキルの構成要素、description と本文の書き方、パターン、避けるべき書き方 → [`references/writing-guide.md`](../../../plugins/murnana-agent-config/skills/skill-create/references/writing-guide.md)
- 評価（出力のテスト、起動テスト、`claude plugin eval` の構成、`evals.json`）→ [`references/evals.md`](../../../plugins/murnana-agent-config/skills/skill-create/references/evals.md)

## 調査で得たベストプラクティス（要約）

### 良いスキルの条件

- **description が起動のすべてを担う**。Claude が起動前に見るのは name と description だけ。何をするか＋いつ使うかを書き、主な用途を先頭に置く。三人称か命令形で書き、ユーザーが実際に使う言葉を入れる（platform best practices, agentskills optimizing-descriptions）。
- Claude はスキルを**起動しなさすぎる**傾向がある。description はやや強めに書き、「X と明示されていなくても」のような暗黙のケースも含める（skill-creator, agentskills）。
- **Claude が知らないことだけを書く**。「これがないと Claude は間違えるか？」と1行ずつ確かめる。網羅的に書くより、適度な詳しさの手順と動く例が1つある方がよい（platform, agentskills best-practices）。
- **実際の知見から作る**。実際の作業で使った手順やユーザーが直した点、ランブック、レビューコメントを材料にする。一般論から作ると曖昧になる（agentskills best-practices）。
- 自由度は**壊れやすさに合わせる**。複数のやり方が成り立つところは方針だけを書き、壊れやすい操作は正確なコマンドを指定する（platform）。
- **選択肢を並べず、デフォルトを示す**。**個別の答えではなく手順を書く**。**落とし穴の節**が最も価値が高いことが多い（agentskills）。
- 大文字の MUST を並べるより**理由を書く**（skill-creator, agentskills evaluating）。
- SKILL.md は500行以内にし、references は SKILL.md から1階層まで。「いつ読むか」を明記する。100行を超えるファイルには目次を付ける（platform, Claude Code skills）。
- 読み込まれた内容は会話に残り、再読み込みされない。コンパクション後は先頭の5,000トークンしか残らない場合がある。重要な指示は冒頭に書く（Claude Code skills）。
- 副作用のある操作は `disable-model-invocation: true` にする（Claude Code skills / best-practices）。
- **評価を先に作る**。スキルなしでの失敗を確認し、スキルあり・なしで比較する（platform, agentskills evaluating）。

### 評価

- 出力のテストは2〜3件から始める。言い回しを変え、境界ケースを1つ含める。assertion は客観的に確認できるものだけにする（agentskills evaluating）。
- 起動テストは約20件（起動すべきもの8〜10件、ニアミス8〜10件）。train と validation を 60/40 に分け、各3回実行し、しきい値は 0.5。選ぶのは validation の成績が最も良い description（agentskills optimizing-descriptions）。
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

## 設計判断とその理由

- **なぜ明示起動のみか** — スキルはファイルを作り、プロジェクトの場合はチームに共有される。自動起動で勝手に作られると困るため、rule-create と同じ方針にした（ユーザーの決定）。
- **なぜ本文を英語に固定するか** — トークン効率と遵守率を優先した（ユーザーの決定）。
- **なぜ評価は雛形だけか** — 実行は課金されるため、実行するかどうかはユーザーが判断する（ユーザーの決定）。
- **なぜ評価の形式を作成先で変えるか** — プラグインのスキルは `claude plugin eval` で、プラグインあり・なしの比較とCIでの判定まで行える。プロジェクトや個人のスキルにはその仕組みがないため、skill-creator や手動評価で使える agentskills 形式にする。2つのツールは互いのファイルを読めない。
- **なぜ「スキルが適切か」の判定を入れるか** — hook や rule の方が向いている依頼をスキルにすると、指示が守られなかったり、必要なときに読み込まれなかったりする。代替手段は提案だけにとどめ、作成はスコープ外とする（rule-create と同じ方針）。
- **なぜ公式 skill-creator プラグインと別に作るか** — skill-creator は評価の自動実行に重点がある。このスキルは、このリポジトリの慣習（references 構成、英語本文、承認待ち、docs）に合わせた作成とヒアリングに重点を置く。評価の実行には skill-creator を案内する。

## 出典

- 公式
  - https://code.claude.com/docs/en/skills.md
  - https://code.claude.com/docs/en/best-practices.md
  - https://code.claude.com/docs/en/plugin-evals.md
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md
  - https://agentskills.io/skill-creation/evaluating-skills.md
  - https://agentskills.io/skill-creation/best-practices.md
  - https://agentskills.io/skill-creation/optimizing-descriptions.md
  - https://github.com/anthropics/skills/tree/main/skills/skill-creator
- コミュニティ
  - https://designrevision.com/blog/claude-code-skills-best-practices.md
  - https://dev.classmethod.jp/en/articles/claude-code-skills-for-cloud-bu-consulting-members/
  - https://www.web-developpeur.com/en/blog/skills-claude-code-patterns-officiels
