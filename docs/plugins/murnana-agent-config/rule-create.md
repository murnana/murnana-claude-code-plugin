# rule-create スキル

`/murnana-agent-config:rule-create` — Claude Code のルールファイル（`.claude/rules/*.md`）を、公式仕様とベストプラクティスに沿って作成・更新する。

## 使い方

- 起動は**明示的なスラッシュコマンドのみ**（`disable-model-invocation: true`）。
- `$ARGUMENTS` に `testing` や `api conventions` のようなトピックのヒントを渡せる。
- 作成先はプロジェクト（`<repo>/.claude/rules/`）とユーザー（`~/.claude/rules/`）のどちらかを選べる。
- 生成されるルールの本文は**常に英語**。

| Step | やること |
|---|---|
| 1 | 既存の rules / CLAUDE.md を確認する（重複・矛盾の検出） |
| 2 | rule が適切かを判定する（skill / hook / permission の方が適切なら提案する） |
| 3 | スコープ・目的・対象ファイル・内容をヒアリングする |
| 4 | ファイル名と `paths` を決め、glob が実在のファイルに一致するか確認する |
| 5 | 目的別チェックリストに沿って下書きする |
| 6 | セルフレビュー（行数、自明な項目、矛盾、フロントマター） |
| 7 | 全文を提示して**承認を待つ** → 書き込む |
| 8 | 読み込まれたかの確認方法を案内する |

## リファレンス

中身はこのドキュメントに写さず、リンク先を正とする。

- ルールファイルの形式（配置、読み込みタイミング、`paths` フロントマター、glob、シンボリックリンク、サイズ、確認方法）→ [`references/rule-format.md`](../../../plugins/murnana-agent-config/skills/rule-create/references/rule-format.md)
- rule と CLAUDE.md / skill / hook / permission の使い分け → [`references/rule-vs-alternatives.md`](../../../plugins/murnana-agent-config/skills/rule-create/references/rule-vs-alternatives.md)
- 目的別に書くべきこと → [`references/rule-content-by-purpose.md`](../../../plugins/murnana-agent-config/skills/rule-create/references/rule-content-by-purpose.md)

## 調査で得たベストプラクティス（要約）

### 公式ドキュメント

- ルールは**参考情報であり、強制力はない**。CLAUDE.md と同様に、Claude が読んで従おうとするだけ。確実に実行・阻止したいものは hook や permission を使う（memory, claude-directory）。
- `paths` のないルールは CLAUDE.md に書くのと**仕組み上まったく同じ**。毎セッション読み込まれるため、範囲を絞れるものは `paths` を付ける（steering 記事）。
- 一部のディレクトリにだけ関係する指示より、**複数の場所にまたがる関心事**（テスト、ハンドラー、マイグレーション）は、ネストした CLAUDE.md よりパス指定のルールに向いている（steering 記事）。
- 「毎回 X のときは Y をする」は hook、「絶対に X しない」は permission や hook、手順は skill に書く（steering 記事, best-practices）。
- 指示は具体的で検証できる形にする（「Use 2-space indentation」は○、「Format code properly」は×）。見出しと箇条書きで整理する。他の指示と矛盾させない（memory）。
- 1行ごとに「消したら Claude が間違えるか？」と問い、間違えないなら削る。長すぎるとルールが埋もれて無視される。IMPORTANT による強調は1か所だけにする（best-practices）。
- 書くもの：推測できないコマンド、既定と異なるスタイル、テストの方法、リポジトリ運用の作法、アーキテクチャ上の決定、環境の癖、落とし穴。書かないもの：コードを読めばわかること、標準的な慣習、詳細な API ドキュメント、頻繁に変わる情報、チュートリアル、ファイルごとの説明、自明なこと（best-practices）。
- 1ファイル200行以内。CLAUDE.md が200行に近づいたらルールに分割する（memory, claude-directory）。
- 制約の理由（why）を書き、例を添えた明示的なプロンプトとして書く（steering 記事）。

### コミュニティ

- **1ファイル1関心事**、内容がわかるファイル名（`api-validation.md` は○、`rules1.md` は×）。`frontend/` や `backend/` のようなサブディレクトリで整理する（claudefa.st）。
- 各ルールは「**命令文 ＋ 守らないと何が起きるか ＋ なぜ代替案だと失敗するか**」の3部構成で書く。例：`Use X, not Y. Without X, <bad thing>. Y causes <problem> because <mechanism>.`（xiaolai/nlpm-for-claude writing-rules）。
- 常時読み込むルールは最小限にする（基本のコーディング規約、譲れない制約、共通の前提）。手順、特定ディレクトリ向けの指示、まだ固まっていない慣習は常時ルールにしない。読み込まれていると思い込まず、実際に確認する（Senior Data Science Lead substack）。
- 範囲を本文の文章で指定するのはヒントにすぎず、`paths` で指定すれば仕組みとして適用される。`globs:` は Cursor の書式（aitraining2u, smithery creating-claude-rules）。
- glob はクォートする（smithery）。

### 注意点

- GitHub issue [#17204](https://github.com/anthropics/claude-code/issues/17204)（2026-01）で、クォート付きや YAML リスト形式の `paths` が読み込まれず、`globs:` なら動くという報告があった。メンテナーは回答しないまま、非アクティブとして close されている。現行の公式ドキュメントは「YAML リストまたはカンマ区切り文字列」と明記しており、`paths` 解析の関連修正（v2.1.207 / v2.1.217）も入っているため、スキルは公式どおり YAML リストを採用する。そのかわり、生成後に**必ず読み込まれたかを確認する**手順を案内する（Step 8）。

## テスト方法と結果（2026-10-12, Claude Code v2.1.296）

1. 小さな TypeScript のプロジェクト（`src/math.ts`、`src/math.test.ts`、`CLAUDE.md`）を作る。`.claude/settings.json` に、`InstructionsLoaded` の入力をファイルに追記する hook を入れておく。
2. `claude -p --plugin-dir <plugin> "/murnana-agent-config:rule-create testing <ヒアリングへの回答>"` を実行する。ヘッドレスでは AskUserQuestion が使えないため、回答はあらかじめ引数に書いておく。→ Step 7 で全文を提示し、承認待ちで止まることを確認した。glob が実在ファイルに一致するかの確認、矛盾チェック、why の付与、hook の提案もされていた。
3. 生成された内容を `.claude/rules/testing.md` に置く。新しいセッションで `src/math.ts` だけを読むとルールは読み込まれず、`src/math.test.ts` を読むと `load_reason: path_glob_match` で読み込まれることを確認した。

テストでわかったこと：

- **`defaultEnabled: false` のプラグインは `--plugin-dir` で指定しても無効のまま**。テストするときは、コピーしたプラグインを `true` に書き換えて使う。
- `disable-model-invocation: true` のスキルは、モデルが参照できるスキル一覧に出てこない（仕様どおり）。スラッシュコマンドからは起動できる。
- サンドボックス内の Bash では `ls ~/.claude/rules` が拒否される。そのため、ユーザールールの列挙は Glob ツールで行うように修正した。
- `claude -p ... --allowedTools Read "prompt"` のように書くと、可変長のフラグがプロンプトまで飲み込んでしまう。`--allowedTools=Read` と書くか、プロンプトを先に置く。
- 当初の名前 `murnana-claude-code` は、`claude plugin validate` で「Anthropic 公式のプラグインに見える」と警告された（検証自体は通る）。このため `murnana-agent-config` に改名した。サードパーティのプラグインは、`claude-` `anthropic-` `anthropics-` `cc-plugin-` で始まる名前や `claude-code` そのものだとエラーになる。名前の途中に `claude` や `anthropic` を含むだけでも警告が出る。

## 設計判断とその理由

- **なぜ明示起動のみか** — ルールは毎セッションのコンテキストに影響し、プロジェクトの場合はチームに共有される。自動起動で勝手に作られると困るため、`commit` や `pr-create` と同じ方針にした。
- **なぜ本文を英語に固定するか** — トークン効率と遵守率を優先した（ユーザーの決定）。ヒアリングは会話の言語で行う。
- **なぜデフォルトでパスを指定するか** — `paths` のないルールは CLAUDE.md と同じコストが毎回かかる。関係ない作業のときはコンテキストに入れない方がよい。
- **なぜ glob が一致するか確認するか** — 何にも一致しない `paths` はエラーにならず、ルールがずっと読み込まれないだけになる。この失敗は気づきにくい。
- **なぜ代替手段を作らないか** — skill / hook / permission が適切な場合も提案だけにとどめる。作成はスコープ外（将来、同じプラグインの別スキルにする想定）。

## 出典

- 公式
  - https://code.claude.com/docs/en/claude-directory.md
  - https://code.claude.com/docs/en/memory.md
  - https://code.claude.com/docs/en/best-practices.md
  - https://claude.com/resources/articles/steering-claude-code-skills-hooks-rules-subagents-and-more
- コミュニティ
  - https://claudefa.st/blog/guide/mechanics/rules-directory
  - https://joseparreogarcia.substack.com/p/how-claude-code-rules-actually-work
  - https://skills.sh/xiaolai/nlpm-for-claude/writing-rules
  - https://smithery.ai/skills/pr-pm/creating-claude-rules
  - https://www.aitraining2u.com/ccar-f/exercises/load-rules-conditionally-with-path-scoped-frontmatter.html
  - https://blogs.novita.ai/claude-code-rules/
  - https://github.com/anthropics/claude-code/issues/17204
