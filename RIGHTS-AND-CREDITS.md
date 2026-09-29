# 権利とクレジット

この文書はPUBLICリポジトリ内で配布する内容と、適用するライセンスの範囲を示します。法的判断を断定するものではありません。リポジトリ全体に一つのライセンスを適用していません。

## Documentation — CC BY 4.0

リポジトリ用に執筆した`README.md`、`docs/`内の文書、`case-studies/`内のMarkdownと`case.json`の独自記述、`examples/`内のREADME、そしてこの文書の本文には、[Creative Commons Attribution 4.0 International（CC BY 4.0）](LICENSE-DOCS)を適用します。画像・動画など埋め込みメディアには適用しません。ライセンスの条件は[CC公式の法的文書](https://creativecommons.org/licenses/by/4.0/legalcode)を参照してください。

## Example Code — MIT

`examples/stable-sprite-ui-reaction/`のリポジトリ独自の実行コードと設定ファイルには、[MIT License](LICENSE-CODE)を適用します。`examples/`内のREADME本文は上記のCC BY 4.0です。Exampleは幾何学図形を使用し、greenwakame、Pug、プロフィール由来の画像を含みません。依存パッケージ本体やCDNから読み込むコードはMITの対象外です。

## Project-specific Media — publication approved; rights reserved

リポジトリ所有者は、以下の5ファイルを、このCase Studyの一部としてGitHubで一般公開することを承認済みです。公開承認と再利用許諾は別です。これらのファイルにはMITとCC BY 4.0を適用せず、作品固有のメディアに関しては権利を留保し、複製・改変・再配布・再利用のためのライセンスを付与しません。

- `case-studies/greenwakame-profile-pv/media/greenwakame-profile-pv-v6-github.mp4`
- `case-studies/greenwakame-profile-pv/assets/poster.webp`
- `case-studies/greenwakame-profile-pv/assets/screenshots/human-review.webp`
- `case-studies/greenwakame-profile-pv/assets/screenshots/pug-reviewer.webp`
- `case-studies/greenwakame-profile-pv/assets/screenshots/player-stats.webp`

動画と静止画に映るgreenwakame、Pug、プロフィール由来の素材は、この公開承認の対象です。元の画像ファイルは個別に再配布していません。映像内の第三者のロゴ、商標、製品名、その他の要素の権利は各権利者に帰属します。この公開承認は、それら第三者の権利の所有を意味しません。

## Third-party Components — respective rights and licenses

| 項目 | このリポジトリでの扱い |
| --- | --- |
| HyperFrames | 制作時にCLI 0.8.80を使用。ライブラリ本体・ソースは再配布していません。[上流のApache-2.0 LICENSE](https://github.com/heygen-com/hyperframes/blob/main/LICENSE)が適用されます。 |
| HyperFrames Skills | 制作時に参照。Skills本体は再配布していません。[上流のSkillsガイド](https://github.com/heygen-com/hyperframes/blob/main/docs/guides/skills.mdx)を参照してください。 |
| GSAP | 元PVとExampleはCDN経由で使用。GSAP本体は再配布していません。[GSAPのライセンス](https://gsap.com/community/standard-license/)が適用されます。 |
| フォント | フォントバイナリは再配布していません。元PVはシステムフォントとJetBrains MonoをCSSの候補名に指定しています。使用するフォント固有の条件に従ってください。 |
| その他の依存パッケージ | Exampleのmanifestとlockfileには依存関係の情報を記録していますが、package本体は含めていません。各packageのライセンスが適用されます。 |
| ロゴ・商標・製品名など | 各権利者に帰属します。本リポジトリのMIT/CC BY 4.0はそれらへ適用されません。 |

元のPVのHTML/CSS/JS、制作環境のrender master、元のキャラクター画像、個別のicon、第三者の音楽ファイルは再配布していません。delivery動画には音声ストリームがありません。LICENSE-CODEとLICENSE-DOCSは、それぞれ明示したリポジトリ独自の対象にのみ適用されます。
