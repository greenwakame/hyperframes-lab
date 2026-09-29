# 改善履歴：動くUIからキャラクターの演技へ

実験中も旧版の作業ディレクトリを残しました。v5がVisual QAで失敗した際、v4の動作する構成へ戻れたことが重要でした。旧版のMP4はこのリポジトリで配布しません。

| 版 | 変更 | 学んだこと |
| --- | --- | --- |
| v1 | 20秒・1920×1080・30 fpsのRPG風プロフィール構造を作成。 | 6シーンでプロフィールの筋を伝えられる。 |
| v2 | greenwakameとPug Reviewerを追加。 | キャラクターがUIに視点を与える。 |
| v3 | greenwakameのidle/walk/review/successとPugのreviewing/pending/approvedを追加。 | state遷移でUIの物語を補強できる。 |
| v4 | キャラクターが行動し、その後にUIが変わる構成へ変更。 | プレイヤーが物語を進める主体になる。 |
| v5 | 個別生成したposeを多数追加。 | poseの多さとアニメーションの良さは一致しない。 |
| v6 | v4を土台に、安定spriteとtransform中心の動きへ再構築。 | 同じ画像を動かしたほうが連続性を保てた。 |

## v4：因果関係のある構成

初期の版は「動くUIパネルにキャラクターが付いている」ようにも読めました。v4では**キャラクターの行動 → UIの反応**を中心に置きました。Player StatsはStats → greenwakameが移動 → Languagesとなり、各カードを読むための静かな時間も確保しました。6シーン、短い方向性のある受け渡し、控えめなカメラ移動が土台です。

## v5: More Sprites, Less Continuity

もっと動かすため、v5ではgreenwakameの追加10ポーズ（`idle-b`、`walk-c`、`walk-d`、`land`、`point`、typing、nod、左右を見るpose）とPugの追加4ポーズ（`review-b`、`think`、`paw-tap`、`approve-b`）を用意しました。歩行、review、着地、typing、承認の場面で切り替えました。キャンバスの基準は揃えましたが、顔、等身、手足、小物、輪郭、重心までは一致しませんでした。

Studio Previewで高速切り替えを見ると、**同じキャラクターの動きではなく、似た画像への交換**に見えました。Pugが特に顕著でした。記録上、HyperFrames checkは**lint error 0、runtime error 0**でした。compositionの破損やファイル不足ではなく、視覚的な連続性の失敗です。Human Visual QAが発見しました。

## v6：checkへの対症療法ではなく設計変更

v6はv4の安定したシーン構造へ戻り、v5の追加pose群を使わない方法にしました。greenwakameは基本5枚、Pugは物語上の3 stateに限定。移動、少しの回転やlean、scale、squash、小ジャンプ、着地、idleの微動で演技します。`land`画像へ切り替える代わりに、同じ画像をジャンプから着地まで保持します。

動きは**anticipation → action → settle**で組みました。Player StatsのleanからUI反応までは120 msです。v6の記録はlint error 0 / warning 9、runtime error 0 / warning 0でしたが、これらの数値だけで見た目を保証したわけではありません。Previewと人の目で確認する工程を残しました。

一般化できる学びは、生成画像を**1枚ずつでなく連続する列として評価する**ことです。本作ではsprite数より、同一性と因果関係が重要でした。

[制作事例](README.md) · [設計詳細](DESIGN.md) · [アニメーションのナレッジ](../../docs/animation-design.md)
