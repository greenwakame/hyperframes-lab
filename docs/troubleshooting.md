# 実制作のトラブルシューティング

以下は今回実際に起きた問題と、そのとき有効だった対処です。別の環境で同じ文面を見た場合も、原因を確認してから変更してください。

## npx: command not found

この制作環境ではNodeとpnpmをmiseで管理していました。シェルから`npx`は見つかりませんでしたが、project-localのHyperFramesバイナリは存在しました。既存環境を使った確認は次のとおりです。

```sh
mise exec -- pnpm --version
mise exec -- ../node_modules/.bin/hyperframes --version
```

2行目はworkspaceの子に動画プロジェクトを置いた構成です。このリポジトリの単独Exampleでは、`pnpm install`後に`./node_modules/.bin/hyperframes`を使います。今回観測した問題のために別のツールチェーンを追加する必要はありませんでした。

## localhostで`EPERM`

Studio Previewの起動時に`listen EPERM: operation not permitted 127.0.0.1`が出ました。この事例では、原因はCodex Desktop sandboxのlocalhost待受権限でした。composition、dependencies、HyperFrames設定の問題ではありません。**コード・依存・設定を変更せず、localhost bind permissionを許可し、同じコマンドを再実行**しました。

## zshのglob

一致するファイルがないまま`ffmpeg2pass*`のようなglobを使うと、zshがコマンド実行前に`zsh: no matches found`を出すことがあります。まずシェル展開に頼らず確認します。

```sh
find . -maxdepth 1 -type f -name 'ffmpeg2pass*' -print
```

削除が本当に必要な場合も、表示されたパスを確認してから対象を決めます。globのエラーを理由に広範な削除へ進まないでください。

## エラーで止まる

診断は**1コマンド → 結果確認 → 次の1手**で進めました。既存のmiseコマンドや権限の修正で対処できる場合に、agentが勝手にnpm、別CLI、依存パッケージ、設定へ切り替えない運用です。作業環境の正常な状態を保ちながら原因を絞れます。
