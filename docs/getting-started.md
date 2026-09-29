# はじめ方

実行例は[stable sprite + delayed UI reaction](../examples/stable-sprite-ui-reaction/README.md)です。幾何学図形だけを使い、完成PVの画像素材には依存しません。

1. [miseの公式手順](https://mise.jdx.dev/getting-started.html)に従ってmiseを用意し、Exampleの`mise.toml`に記録されたNodeとpnpmをインストールします。
2. Exampleディレクトリで、固定されたproject-localのHyperFrames依存をインストールします。
3. バージョンを確認し、Studio Previewの前に`check`を実行します。

```sh
cd examples/stable-sprite-ui-reaction
mise install
mise exec -- pnpm install
mise exec -- pnpm --version
mise exec -- ./node_modules/.bin/hyperframes --version
mise exec -- ./node_modules/.bin/hyperframes check
```

このディレクトリには`index.html`、`hyperframes.json`、`package.json`、`mise.toml`、`pnpm-workspace.yaml`、lockfileがあります。HyperFramesは`package.json`で0.8.80に固定されています。インストールによって作られる`node_modules/`はGitの対象外です。

元の制作環境では依存パッケージが各動画プロジェクトの一階層上にあったため、`mise exec -- ../node_modules/.bin/hyperframes check`を使いました。CLIの相対パスは、実際に依存を置いた場所に合わせてください。

制作時に`npx: command not found`が発生しました。既存のmise管理環境とproject-local CLIを使うことで解決したため、`npx`を追加することは標準手順に含めません。[詳しい経緯](troubleshooting.md#npx-command-not-found)。

HyperFrames Skillsはこのリポジトリに複製していません。自分の環境に必要なSkillは[公式のSkillsガイド](https://github.com/heygen-com/hyperframes/blob/main/docs/guides/skills.mdx)を参照して導入してください。元の制作環境ではproject-localの`.agents/skills`を使用しましたが、PUBLICには含めていません。
