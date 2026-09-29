# 検証とrender

元の制作環境では、動画プロジェクトの一階層上にHyperFrames CLIがありました。compositionディレクトリから次を実行します。

```sh
cd <project>
mise exec -- ../node_modules/.bin/hyperframes check
```

このリポジトリの単独Exampleは自身のディレクトリに依存をインストールするため、`mise exec -- ./node_modules/.bin/hyperframes check`を使います。

v6の最終時に記録された結果は**Lint: error 0 / warning 9、Runtime: error 0 / warning 0**でした。これは今回の履歴であり、「warningが9件なら常に安全」という基準ではありません。warningの内容を確認し、意図した出力に影響するものは解決します。errorがあれば原則として次へ進みません。

checkの後は、**Studio Preview → 人の目によるVisual QA → Render**の順番です。再生全体に加え、sprite切り替え、Pugの承認、Player Stats、Outroを重点的に見ます。v5は構造上のcheckを通過しても、この視覚確認で問題が見つかりました。緑の結果だけをrenderの判断にはしません。

Render後は設定値を信じるだけでなく、実ファイルを調べます。

```sh
ffprobe -v error \
  -show_entries stream=index,codec_type,codec_name,width,height,r_frame_rate,nb_frames \
  -show_entries format=duration,size \
  -of json <render.mp4>
```

**codec、解像度、fps、フレーム数、尺、音声ストリームの有無、byte数**を確認します。v6 masterの実測値は、H.264、1920×1080、30 fps、600フレーム、20.000秒、14,768,600 bytes、音声なしでした。公開用ファイルは[GitHub向け動画](github-delivery.md)に記録しています。
