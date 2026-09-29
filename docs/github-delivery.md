# GitHub向け動画：masterとdeliveryを分ける

制作masterは作業用プロジェクトに残し、リポジトリ掲載用には別ファイルをencodeしました。masterを上書きせず、掲載のためだけに大きな制作ファイルを持ち込まないためです。

| 出力 | codec | 尺 | 解像度 | fps | フレーム数 | サイズ | 音声 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| master | H.264 | 20.000秒 | 1920×1080 | 30 | 600 | 14,768,600 bytes | なし |
| delivery | H.264 | 20.000秒 | 1920×1080 | 30 | 600 | 8,100,111 bytes | なし |

今回のdeliveryはmasterより約45%小さくなりました。これは20秒の本作における実測値であり、どの動画にも同じbitrateを勧めるものではありません。

masterのあるディレクトリで使用した2-pass H.264の設定は以下です。

```sh
ffmpeg -y \
  -i greenwakame-profile-pv-v6.mp4 \
  -c:v libx264 \
  -b:v 3300k \
  -preset slow \
  -pix_fmt yuv420p \
  -pass 1 \
  -an \
  -f null /dev/null

ffmpeg -y \
  -i greenwakame-profile-pv-v6.mp4 \
  -c:v libx264 \
  -b:v 3300k \
  -preset slow \
  -pix_fmt yuv420p \
  -movflags +faststart \
  -pass 2 \
  -an \
  greenwakame-profile-pv-v6-github.mp4
```

`3300k`は今回の設定値です。次の動画では画面の細かさ、動き、尺、目標容量に合わせて決めます。コピー後のdeliveryもFFprobeで再確認します。2-passログや一時ファイルはリポジトリに置かず、事例の`media/`にはdelivery MP4だけを入れます。
