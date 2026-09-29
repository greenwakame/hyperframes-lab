# 実制作の環境

以下はgreenwakame Profile PVの制作時に使用した環境の記録です。今後のすべてのHyperFrames制作で、同じバージョンを必須とするものではありません。

| 項目 | 記録された値 |
| --- | --- |
| マシン | Apple Silicon MacBook Air、arm64 |
| macOS | 26.5.2 |
| mise | 2026.7.18 |
| Node.js | 24.18.0 |
| pnpm | 11.28.0 |
| HyperFrames CLI | 0.8.80 |
| FFmpeg / FFprobe | 9.0.2 |
| ブラウザ | Google Chrome |

Nodeとpnpmはmiseで管理しました。制作workspaceにはproject-localのHyperFramesがあり、各動画プロジェクトはその子ディレクトリに置かれていました。この構成でのバージョン確認は次のとおりです。

```sh
cd <workspace>
mise exec -- pnpm --version
cd <project>
mise exec -- ../node_modules/.bin/hyperframes --version
```

ローカルのCLIを明示することで、グローバルインストールや`npx`の有無に左右されず、使用したバージョンを追えます。このリポジトリの単独Exampleは自身のディレクトリに依存パッケージを持つため、CLIのパスは`./node_modules/.bin/hyperframes`です。[はじめ方](getting-started.md)を参照してください。
