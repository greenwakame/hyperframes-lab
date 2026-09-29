# デザインと動きの設計

## Visual direction

20秒のGitHubプロフィールをゲーム画面として扱いました。暗いRPG風パネル、緑・mintのaccent、pixel artのニュアンス、status表示、quest card、party-completeのOutroを使います。UIが情報を整理し、greenwakameの動きが視線の順路を作ります。Pug Reviewerはレビューから承認までの分かりやすい節目を担います。

元の制作ではプロフィール由来の画像を背景とデータ表示に使用しました。キャラクターspriteは前面の独立レイヤーとし、パネルとは別の時刻に動かせるようにしました。[権利状況](../../RIGHTS-AND-CREDITS.md)。

## 6シーンの時間設計

| 時間 | シーン | キャラクターとUIの関係 |
| --- | --- | --- |
| 0–3秒 | Player Enters | greenwakameが歩いて入り、プロフィール情報が続く。 |
| 3–7秒 | How I Build | プレイヤーが開発工程を進み、Human Reviewで一拍置く。 |
| 7–11秒 | Pug Status | reviewing → pendingの保持 → approvedと小さなジャンプ。 |
| 11–15秒 | Current Quest | greenwakameがquestと技術スタックを見る。 |
| 15–18秒 | Player Stats | プレイヤーがStatsとLanguagesへ近づき、それぞれのUIが後から反応する。 |
| 18–20秒 | Outro | 2人がプロフィールURLを囲み、落ち着いた完成画面になる。 |

## 動きの語彙

最終版ではpose変更を物語上のstateに限定しました。greenwakameは`idle`、`walk-a`、`walk-b`、`review`、`success`、Pugは`reviewing`、`pending`、`approved`を使用します。歩行中は既存の2枚を各5フレームで交互に表示し、身体全体に約3 pxの上下動と約1°の傾きを付けます。これは一貫して描かれた小さな歩行サイクルであり、独立生成した大量の画像を順に替える方法とは異なります。

着地では同じ画像を保持し、身体を約3 px沈め、約10 px上げ、短く圧縮（`scaleX`約1.04、`scaleY`約0.96）して中立へ戻します。Pugも控えめな呼吸、予備動作、小ジャンプ、着地で演技します。これらは本作の設定値であり、一般的な必須値ではありません。

## Player Statsの因果関係

15–18秒の場面でgreenwakameはStatsへ到着・着地し、**15.62秒**にleanを開始します。Stats UIは**15.74秒**に反応します。Languages側へ移動・着地した後、**16.75秒**にleanし、Languages UIは**16.87秒**に反応します。二つとも120 msの差を設け、プレイヤーがカードを作動させたように見せました。反応後には読める長さの保持時間を取ります。

時刻は一つのpaused GSAP timelineで管理しました。外側のcharacter nodeが移動を、内側のbody-motion nodeが小さな身体変形を担当します。これにより位置と演技を別々に調整できます。ただし最終判断はStudio Previewで行います。技術的に正しい動きでも、視覚的には不連続になり得るためです。

[改善履歴](ITERATIONS.md) · [アニメーション設計のナレッジ](../../docs/animation-design.md)
