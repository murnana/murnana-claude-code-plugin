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
