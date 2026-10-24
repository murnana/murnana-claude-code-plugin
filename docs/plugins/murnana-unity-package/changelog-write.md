# changelog-write スキル

`/murnana-unity-package:changelog-write` — Unity Package Manager (UPM) パッケージの CHANGELOG.md を [Keep a Changelog](https://keepachangelog.com/) と Unity のバージョニング規則に沿って作成・追記する。頼まれたときだけバージョンを切り、`package.json` の `version` も更新する。

[murnana-tech-docs の changelog-write](../murnana-tech-docs/changelog-write.md) を UPM 開発向けに調整したもの。共通の書き方ルールと設計判断はそちらを参照。

## 使い方

- スラッシュコマンドで明示的に起動できるほか、UPM パッケージの CHANGELOG の作成・更新やリリースを頼むと自動で起動する。
- `$ARGUMENTS` に記録したい変更のヒントを渡せる。「release」「バージョンを切って」「1.2.0 にして」のようにバージョンを指定すると、リリース切りと `package.json` の更新まで行う。
- 書き込む前に、必ず追記内容を提示して承認を待つ。コミットやタグ作成はしない。

| Step | やること |
|---|---|
| 1 | 対象パッケージ（逆ドメイン名の `package.json`）を見つけ、その隣の CHANGELOG.md を対象にする |
| 2 | プロジェクト規約・リリースツールを探す（見つかればそれが最優先） |
| 3 | 新規作成のとき: Keep a Changelog の最新版を確認し、言語（既定は会話の言語）とバージョニング方式を決める。`package.json.meta` があれば `CHANGELOG.md.meta` も作る |
| 4 | 既存ファイルのとき: 前文の版・言語・カテゴリ順・リンク形式をそのまま引き継ぐ。最新見出しと `package.json` の版が一致するか確認する |
| 5 | 前回リリースからのパッケージ内の変更と、その元になった Issue / PR を集める。Unity 固有の破壊的変更も探す |
| 6 | 書き方ルールに沿ってエントリを起草する。動作として書けない変更は相談する |
| 7 | 提示して**承認を待つ** → 書き込む |
| 8 | 頼まれたときだけ: Unity の規則で版番号を決め、`[Unreleased]` を `[x.y.z] - YYYY-MM-DD` に移し、リンクと `package.json` の `version` を更新する |

## tech-docs 版との違い

- 対象は UPM パッケージのルート（`package.json` の隣）にある CHANGELOG.md
- エントリに書いてよい名前に、パッケージ利用者が触る public C# API、コンポーネント名、メニューパス、Inspector の項目、Project Settings、サンプル名、define シンボルを加えた
- 破壊的変更の観点に、asmdef の設定（Auto Referenced、defineConstraints、プラットフォーム）、`.meta` の GUID 変更、シリアライズフィールドの改名を加えた
- 版番号は Unity の [Package versioning](https://docs.unity3d.com/6000.6/Documentation/Manual/upm-semver.html) に従う。`unity` / `unityRelease` が変わったら最低でも minor
- リリース時に `package.json` の `version` も更新する
- 新規作成時に `CHANGELOG.md.meta` を作る

## 設計判断とその理由

- **なぜ自動起動を許可したか** — tech-docs 版は汎用なので、無関係な作業中に追記を提案しないよう明示起動のみにした。このプラグインは UPM 開発専用で、有効化するのは UPM パッケージを扱うときに限られる。そこで頼んだだけで起動するようにした。書き込み前の承認待ちは残しているので、自動起動でも勝手に書き換えることはない。
- **なぜ references を tech-docs 版からコピーしたか** — 各プラグインは `git-subdir` で個別に取得されるため、他のプラグインのファイルを参照できない。また、片方だけをインストールしても動く必要がある。二重管理にはなるが、Keep a Changelog の確認手順など共通部分を直すときは両方を直す。
- **なぜ `package.json` の `version` も更新するか** — UPM では `package.json` の `version` がそのまま公開される版になる。CHANGELOG の見出しとずれると、Package Manager に表示される版と変更履歴が食い違う。tech-docs 版は他の規約やスキルと役割が重ならないよう版番号に触れないが、このプラグインでは同じ判断の中で両方を更新する。ただし semantic-release などのツールが版を管理しているときは触らない。
- **なぜ Unity の規則で版番号を決めるか** — Unity の SemVer は、C# の API 以外にも、asmdef の Auto Referenced、アセットの GUID、`unity` フィールドなど、Unity 特有の互換性の境界を定めている。一般的な SemVer の判断だけでは、これらの破壊的変更を見落とす。
- **なぜ `.meta` を作るか** — git URL やレジストリからインストールされたパッケージは不変フォルダになり、`.meta` のないファイルがあると読み込み時に警告が出る。Unity はそこで `.meta` を生成できない。GUID は既存のものと重複すると参照が壊れるため、`uuidgen` で毎回新しく作る。
- **なぜ `[Unreleased]` の扱いをプロジェクトに合わせるか** — Keep a Changelog はリリース後も空の `[Unreleased]` を残すよう勧める。一方、Unity の Package Validation Suite は公開時に `[Unreleased]` があると警告やエラーを出す。どちらを優先するかはプロジェクトの運用次第なので、既定は Keep a Changelog に従い、Validation Suite を使うプロジェクトや過去に空の節を残していないプロジェクトではそれに合わせる。
- **なぜ Unity の最低バージョン引き上げを破壊的変更として扱わないか** — Unity の規則では `unity` / `unityRelease` の変更は「最低でも minor」で、major は求めていない。Package Manager は対応しない Editor に新しい版を表示しないため、古い Editor のプロジェクトが壊れるのではなく、旧版に留まるだけになる。そこで `**Breaking:**` は付けずに Changed に書き、リリースの要約で目立たせる。
- **なぜ自動起動でも UPM パッケージがなければ止まるか** — 自動起動を許可したため、Unity と無関係なリポジトリで CHANGELOG を頼んだときにも起動しうる。そこで npm の `package.json` などに Unity の規則を当てはめないよう、UPM パッケージが見つからなければ何も編集せずに止める。description のトリガー語も Unity・UPM を含むものに絞った。
- **なぜ `-exp` / `-pre` を既定にしないか** — これは Unity 公式レジストリのライフサイクル表記で、サードパーティのパッケージに必須ではない。プロジェクトが既に使っているか、ユーザーが求めたときだけ付ける。

## 参考

- [Package development](https://docs.unity3d.com/6000.6/Documentation/Manual/cus-pkg-development.html)
- [Update the package changelog](https://docs.unity3d.com/6000.6/Documentation/Manual/cus-changelog.html)
- [Package layout](https://docs.unity3d.com/6000.6/Documentation/Manual/cus-layout.html)
- [Package manifest reference](https://docs.unity3d.com/6000.6/Documentation/Manual/upm-manifestPkg.html)
- [Package versioning](https://docs.unity3d.com/6000.6/Documentation/Manual/upm-semver.html)
- [Package states and lifecycle](https://docs.unity3d.com/6000.6/Documentation/Manual/upm-lifecycle.html)
- [Package Validation Suite の CHANGELOG](https://docs.unity3d.com/Packages/com.unity.package-validation-suite@0.80/changelog/CHANGELOG.html)（`[Unreleased]` の警告・エラーを追加したときのエントリがある）
