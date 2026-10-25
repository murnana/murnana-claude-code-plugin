# launch

Unity プロジェクトを Unity Editor で起動するスキル。

## 使い方

```
/murnana-unity:launch android
/murnana-unity:launch ios ~/Projects/MyGame
/murnana-unity:launch
```

汎用プラグインのため `disable-model-invocation: true` を指定しており、Claude が会話の流れから自動で起動することはない。スラッシュコマンドで明示的に呼んだときだけ動く。

プラットフォームを省略すると、プロジェクトに保存された既定のプラットフォームで起動する。保存がなければ尋ねる。

## 設計

### 2 つの CLI の使い分け

| 役割 | 使うもの |
|---|---|
| Editor の検索・インストール、モジュール追加 | [Unity CLI](https://docs.unity.com/en-us/unity-cli/unity-cli-reference)（`unity editors`、`unity install`、`unity install-modules`） |
| プラットフォームを指定した起動 | `unity open --build-target`。CLI が無いときは Editor 本体のコマンドライン引数（[Unity 6.3 の例](https://docs.unity3d.com/6000.3/Documentation/Manual/EditorCommandLineArguments.html)）の `-projectPath` と `-buildTarget` |

`unity open` は `--build-target`（Editor の `-buildTarget` として渡される）と `--args`（その他の Editor 引数）を持つため、Unity CLI があればそれで起動する（1.0.0-beta.14 の `--help` で確認）。公開リファレンスにはこれらのオプションが載っていない。Unity CLI が未導入なら、Hub の既定パスから Editor の実行ファイルを探し、`-projectPath` と `-buildTarget` を付けて直接起動する。

### 既定プラットフォーム

最初に指定されたプラットフォームを `<プロジェクト>/.claude/unity-launch.local.md` の frontmatter（`platform:`）に保存する。以後は指定がなければそれを使う。別のプラットフォームを指定したときはその回だけ上書きし、既定は「今後はこれをデフォルトに」と言われたときだけ書き換える。

既定はプロジェクト単位。プロジェクトごとに必要なモジュールや対象が違うため。

### 安全側の判断

- Editor やモジュールのインストールは容量が大きいので、実行前に必ず確認する。
- すでに開いているプロジェクトを `unity close` で閉じない（保存されないため）。
- `-batchmode`、`-quit`、`-nographics` は付けない。Editor が対話できなくなる、または終了するため。

### Editor ログ

起動のたびに `-logFile` で `<プロジェクト>/Logs/Editor_<yyyyMMdd_HHmmss>.log`（プロジェクトから見て `./Logs/Editor_日時.log`）を指定する。日時は起動の直前に別コマンドの `date` で取得し、結果をリテラルとして起動コマンドに埋め込む（`$(date …)` を起動コマンドに入れると許可プロンプトが毎回出るため）。複数の Unity を起動してもログが混ざらず、いつの起動のログか分かる。Editor は相対パスの `-logFile` を自身の作業ディレクトリから解決するため、プロジェクトルートから組み立てた絶対パスを渡す。`unity open --args` が文字列をどう分割するかは `--help` に書かれていないため、プロジェクトパスに空白があるときは CLI を使わず Editor 本体を直接起動する。ユーザーが別の `-logFile`（`-` でコンソール出力など）を求めたときはそちらを優先する。

### 起動完了の待機（MCP 接続テスト）

`unity open` は Editor のプロセスを起動した時点で戻るため、その直後は Unity MCP や `unity command` がまだ応答しない。そこで起動後に `unity status --until-ready --project-path <プロジェクト>` で Editor が応答するまで待ち、その後に作業を始める。Unity MCP も CLI も、プロジェクトの `com.unity.pipeline` パッケージ経由で Editor に接続するため、先に `Packages/manifest.json` にこのパッケージがあるかを確かめる。無ければ待っても ready にならないので、待たずに `unity pipeline install` を案内する。

- タイムアウトは `unity status --timeout`（秒、既定 300）で指定し、Bash の `timeout` はそれより長くする。初回のプラットフォーム切り替えは再インポートで長引くため延ばす。
- Safe Mode（C# のコンパイルエラー）やモーダルダイアログ（利用規約、プロジェクトのアップグレード）で止まっているときは、待ち続けずに原因をユーザーに伝える。
- MCP の登録確認は `unity mcp configure --list`。登録（`unity mcp configure claude-code`）は設定ファイルを書き換えるため、ユーザーが求めたときだけ行う。
- Unity CLI が無いときは待機も接続テストもできないので、行っていないと報告する。

### 公式スキルとの関係

[Unity-Technologies/skills](https://github.com/Unity-Technologies/skills) の `unity-cli` スキルを読み、`unity status --until-ready` という待機手段の存在を知るために参照した。文面や構成は転記せず、手順は本プラグイン独自の言葉で書いている。公式リポジトリの `LICENSE.md` は Unity Companion License（Unity に依存するプロジェクト向け）を指しており、その本文と Unity 利用規約は実行環境からは取得できず未確認。配布前に terms-checker エージェントで確認すること。

Windows の Editor を直接起動するときの許可パターンは、Hub の既定パス（`C:\Program Files\Unity\Hub\Editor\<version>\Editor\Unity.exe`）を `/` 区切りで書いている。インストール先を変えている場合は一致せず、許可プロンプトが出る。

起動テンプレートは実行ファイルのパスを引用符で囲む（`"<editor executable>" -projectPath …`）ため、コマンド文字列は `"` で始まる。許可パターンは引用符なしと引用符つきの両方を持つ。ただし、パターンが引用符つきのコマンドに一致するかは実機で未確認。許可パターンの対象は Bash ツールで、PowerShell ツールや `C:\` のバックスラッシュ形式は含まない。
