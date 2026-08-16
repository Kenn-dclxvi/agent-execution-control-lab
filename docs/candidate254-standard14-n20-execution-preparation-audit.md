# Candidate254 Standard14 N=20実行準備監査

## 結論

Candidate254 `the-caption-3ce91a4-independent-check-same-model-step-r1`のStandard14を各ケースN=20へ拡張する。登録済みN=5 result `59117fe7924f4b718df4ff32491551cc`に対応する14ケース各5件、合計70件をatomic poolから再利用し、不足する各15件、合計210件だけを新規発行する。

比較前照合では、Candidate147 Standard14 N=100 result `e6fc6e10dedd47f5a1d59d114e6e0f57`と同じatomic poolに属するN=5 result `f7baeadc5bd44399ac13cc0e0a8aff48`を互換条件の基準へ対応づけた。prompt identity以外の実効互換条件は一致し、比較前receiptは`ready`、承認210件、発行0件である。一項目でも不一致なら一件も発行しない事前停止条件を通過した。

## 発行前固定

- 評価対象: Candidate254 `the-caption-3ce91a4-independent-check-same-model-step-r1`。
- bundle SHA-256: `7cd564be0904efb5cee59ce8d72935971d080282686e5ff7be9e85e62aa0fd52`。
- Evaluation set: `the-caption-standard14-r1` r1、14ケース。
- 累積件数: 各ケース20件、合計280件。
- 再利用: 各ケース5件、合計70件。
- 新規発行: 各ケース15件、合計210件。
- model / reasoning: `gpt-5.6-sol / medium`。
- runtime: Codex CLI 0.146.0、Python 3.14.5。
- target: commit `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`、tree `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`。
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`。
- permission: `workspace-write / never`。
- 設定上の同時実行上限: 24。
- token accounting: all-agent v1。
- pool key: `e71ba5db8f3766df39c9c9af10970888e820ff04761b4f709cd543faa01e8b38`。
- dispatch plan SHA-256: `09a8ad2b403b32b91b2cfe6dfe0f309b384f64d53e27ec82e0b5b2c50b9bdd7d`。
- global plan SHA-256: `f156a8f88026d5288f8776ed5c21b6853f8885bc1f7234efe09ca2214595132f`。
- preflight receipt SHA-256: `02fac0f4230033bd33eb107dfc615dcba0616cb6dd2685c48f73135db9cb8642`。

Nとiteration集合はatomic runの実効互換条件ではなく実行来歴である。比較前照合にはCandidate147の保存済みN=100 poolに属するN=5 resultと完全一致するCandidate254 N=5 profileを使い、N=20 profileとglobal planが不足iteration 6〜20だけを実行来歴へ固定する。この分離は、Candidate176 F02 N=20拡張と同じatomic経路である。

## 判定境界

追加210件について有効性と採点可能性を確認し、既存70件と合わせた280件をN=20 selectionへ固定する。品質は個別Scoreを中央値で相殺せず、Score分布を全件記録する。Candidate147は保存済みN=100 poolから同じ選定規則で各20件を固定し、Candidate254 N=20と品質、token、経過時間を同数比較する。

F02とF03については、完了待ち、開始確認とreadの分離および結果表現の発生件数を診断する。これらは3 KPIへ追加せず、Candidate254の正式採用判断に必要な実行経路の安定性として分離する。

## 実行結果

固定済み計画どおり210件を発行し、210 / 210件がvalid、excluded 0、実行エラー0だった。追加210件はすべてScore `4`で、既存70件と合わせた280 / 280件もすべてScore `4`だった。Candidate147とCandidate254のN=20 selectionを固定して同数比較し、F02とF03の経路診断とともに[Standard14 N=20結果](../evaluations/results/candidate254-independent-check-same-model-step-standard14-n20_2026-08-16.md)へ記録した。

現在状態は`preflight_consumed / issued_210 / valid_210 / selected_280 / result_registered / standard14_n20_completed`とする。
