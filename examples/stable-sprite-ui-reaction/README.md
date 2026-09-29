# 安定spriteと遅れて反応するUI

[greenwakame Profile PV](../../case-studies/greenwakame-profile-pv/README.md)で有効だった二つの考え方を、6秒の最小HyperFrames compositionで示します。

1. **見た目の同一性:** 一つの幾何学キャラクターを保ったまま、身体全体を動かし、squash、jump、settleを行います。画像の切り替えはありません。
2. **原因と結果:** キャラクターは3.15秒にpanelへleanし、status panelが3.27秒に反応します。差は120 msです。

キャラクターはCSS図形だけで作成しました。greenwakame、Pug、プロフィール由来画像は使いません。音声もありません。完成PVの6シーンや画面を再現するのではなく、動きの原則を示します。画面内の英語ラベルはExampleの表示テキストであり、解説はこの文書にまとめています。

## 実行方法

[mise](https://mise.jdx.dev/getting-started.html)を用意し、このディレクトリで実行します。

```sh
mise install
mise exec -- pnpm install
mise exec -- ./node_modules/.bin/hyperframes --version
mise exec -- ./node_modules/.bin/hyperframes check
mise exec -- ./node_modules/.bin/hyperframes preview
```

`package.json`でHyperFrames 0.8.80を固定し、`mise.toml`にNode 24.18.0とpnpm 11.28.0を記録しています。`pnpm-workspace.yaml`では、このCLIに必要な`esbuild`のbuild処理だけを明示的に許可します。sandbox環境でPreviewを起動する場合、localhostへの待受権限が必要なことがあります。GSAP 3.14.2はCDNから参照するため、checkとPreviewでは到達できる必要があります。HyperFramesとGSAPのソースはこのリポジトリへコピーしていません。[権利とクレジット](../../RIGHTS-AND-CREDITS.md)。

## タイムラインの読み方

- 0.50–1.30秒：同じ身体の小さなidle motion。
- 1.60–2.38秒：予備動作、ジャンプ、着地時の圧縮、settle。
- 3.15秒：panelへlean。
- 3.27秒：panelの枠とstatusが反応。

一つのpaused GSAP timelineをcomposition rootと同じIDで登録しているため、HyperFramesは任意のフレームへ決定的にseekできます。
