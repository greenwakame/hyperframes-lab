# 制作フロー

**Design → Codexによる実装 → HyperFrames Check → Studio Preview → 人の目によるVisual QA → 修正 → Final Render → FFprobe → Delivery**

| 段階 | 行うこと | 残す根拠 |
| --- | --- | --- |
| Design | 目的、シーン順、時間、素材の制約、動きの意図を決める。 | Brief、storyboard、motion notes。 |
| Codexによる実装 | 一度に変更する範囲を確認し、動作する版を残す。 | Compositionと変更履歴。 |
| HyperFrames Check | lintとruntime・layoutなどを確認する。errorで止まり、warningの内容を読む。 | `check`の結果。 |
| Studio Preview | 完成したタイムラインを通常速度で通して見る。 | 気づいた視覚上の問題。 |
| Human Visual QA | キャラクターの連続性、可読性、テンポ、行動とUI反応の因果関係を判断する。 | 採用・修正の判断。 |
| 修正 | 見つかった問題を直し、checkとPreviewを繰り返す。 | 修正後の挙動。 |
| Final Render | Previewの結果を受け入れた後にmasterを出力する。 | masterファイル。 |
| FFprobe | codec、解像度、fps、フレーム数、尺、音声、容量を実測する。 | メディアの測定結果。 |
| Delivery | masterとは別に公開用ファイルを用意する。 | deliveryファイルと仕様。 |

**技術的なvalidationと視覚的な品質は別です。** v5は記録上、lintとruntimeのerrorが0件でした。しかし、個別生成した多数のposeを切り替えると、顔・等身・輪郭・重心がフレーム間で変わり、同じキャラクターに見えませんでした。Studio Previewで人が発見した問題です。v6ではvalidatorを回避するのでなく、アニメーションの設計を変えました。[v5からv6への経緯](../case-studies/greenwakame-profile-pv/ITERATIONS.md#v5-more-sprites-less-continuity)。

環境エラーを調べるときも、まず1コマンドを実行し、結果を見てから次の1手を選びます。権限やシェルの問題を、依存パッケージや設定の無断変更で片付けないことが重要でした。[トラブルシューティング](troubleshooting.md)。
