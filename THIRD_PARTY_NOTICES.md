# THIRD_PARTY_NOTICES

このリポジトリーの各プラグインが取り込んでいる、または実行時に参照するサードパーティーの資料と、その権利表記をまとめます。

> このリポジトリーは個人利用を目的としており、動作保証は一切ありません。
> 各権利者は、このリポジトリーを後援・提携していません。

## 取り込んでいる資料

### Keep a Changelog

- 対象: `murnana-tech-docs` と `murnana-unity-package` の `changelog-write` スキル
  - `plugins/murnana-tech-docs/skills/changelog-write/references/keep-a-changelog.md`
  - `plugins/murnana-unity-package/skills/changelog-write/references/keep-a-changelog.md`
- 内容: Keep a Changelog 2.0.0 の仕様を要約・翻案したスナップショット
- 出典: https://keepachangelog.com/ / https://github.com/olivierlacan/keep-a-changelog
- ライセンス: MIT License

```
The MIT License (MIT)

Copyright (c) 2014 Olivier Lacan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### Unity Manual

- 対象: `murnana-unity-package` の `changelog-write` スキル（`references/unity-package.md`）
- 内容: UPM パッケージの構成、バージョニング、変更履歴の扱いについて、Unity Manual を自分の言葉で要約したもの。原文は各ページへのリンクで示しています
- 出典: https://docs.unity3d.com/Manual/
- ライセンス: Unity Manual の本文は CC BY-NC-ND 4.0、コードスニペットは Unity Companion License で提供されています。原文の複製や改変は含めていません

## 実行時に参照する資料（取り込んでいない）

次の資料は、スキルの実行中にユーザーの環境から取得して使います。このリポジトリーには含まれていません。

| 資料 | 使うプラグイン | 取得元 |
|---|---|---|
| gitignore テンプレート（github/gitignore のフォーク） | `murnana-git` の `gitignore` | https://github.com/murnana/gitignore |
| Unreal Engine 5 公式ドキュメント | `murnana-unreal-engine` の `ue5-docs` | https://dev.epicgames.com/documentation/ |
| Unity の利用規約・マニュアル・商標ガイドライン | `murnana-unity` の `terms-checker` | https://unity.com/legal ほか |
| Keep a Changelog の最新仕様 | `changelog-write` | https://keepachangelog.com/ |

取得した内容の権利は、それぞれの権利者に帰属します。

## 参照している規格

- [Semantic Versioning 2.0.0](https://semver.org/)（CC BY 3.0）: バージョン番号の付け方の基準として名前とリンクを示しているだけで、本文は含めていません。

## 商標

- Unity は Unity Technologies またはその関連会社の米国およびその他の国における商標または登録商標です。
- Unreal Engine は Epic Games, Inc. の米国およびその他の国における商標または登録商標です。
- GitHub は GitHub, Inc. の商標または登録商標です。
- Claude および Claude Code は Anthropic, PBC の商標です。

その他の製品名・会社名は、各社の商標または登録商標です。
