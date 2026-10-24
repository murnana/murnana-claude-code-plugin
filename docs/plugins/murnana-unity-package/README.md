# murnana-unity-package

Unity Package Manager (UPM) パッケージの保守を支援するプラグイン。

## インストール

```
claude plugin marketplace add murnana/murnana-claude-code-plugin --sparse .claude-plugin
claude plugin install murnana-unity-package@murnana-claude-code-plugin
```

`plugin.json` の `defaultEnabled` が `false` なので、インストール後に別途有効化が必要（`/plugin` コマンドから対象プラグインを有効化する）。

## 収録スキル

| スキル | 起動 | 概要 |
|---|---|---|
| [changelog-write](changelog-write.md) | `/murnana-unity-package:changelog-write`、または「Unity パッケージの CHANGELOG を更新して」などの依頼で自動起動 | UPM パッケージの CHANGELOG.md を Keep a Changelog と Unity のバージョニング規則に沿って作成・追記し、依頼されたときはバージョンを切って `package.json` の `version` も更新する |

## ファイル構成

```
plugins/murnana-unity-package/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── changelog-write/
        ├── SKILL.md
        └── references/
            ├── unity-package.md
            ├── keep-a-changelog.md
            ├── entry-writing.md
            ├── release.md
            └── project-rules.md
```

## 今後

現時点のスキルは `changelog-write` の 1 つのみ。今後、`package.json` の編集、サンプルやテストの追加など、UPM パッケージ開発の作業を支援するスキルを同じプラグインに追加していく想定。追加時はこのディレクトリに `<スキル名>.md` を並べる。

## 商標

Unity は Unity Technologies またはその関連会社の米国およびその他の国における商標または登録商標です。
このプラグインは、Unity Technologies およびその関連会社が後援・提携するものではありません。
