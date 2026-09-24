# C163 4文版 F02 GPT-6 Luna High N=5（2026-09-24）

## 結果

C163の5文目だけを削除した4文版で、F02をGPT-6 Luna High、同一固定Layer 1、同一実効互換条件のまま5回実行した。5 runすべてがScore `4`となった。C163の同じF02 N=5は4件がScore `4`、1件がScore `3`だった。

| 指標 | C163 5文版 | 4文版 | 差 |
| --- | ---: | ---: | ---: |
| Score `4` | 4 / 5 | 5 / 5 | +1 run |
| quality score中央値 | 4 | 4 | 0 |
| all-agent total tokens中央値 | 375,255 | 296,506 | -78,749（-20.98%） |
| 経過時間中央値 | 132.333秒 | 100.899秒 | -31.434秒（-23.75%） |

## 5文目の影響

C163のF02 iteration 4では、focused pytestが初回に`import pytest`欠落で終了コード2となり、修正後の再実行はCSVの改行リテラル誤記で終了コード1となった。5文目の「失敗なら後続を止める」に従ってfull gateは発行されなかった。

4文版のF02 iteration 2も、focused pytestの初回が`import pytest`欠落で終了コード2となった。その後のfocused pytest再実行は終了コード0、`main_verify.sh`も終了コード0で完了した。最終差分は許可された4ファイル内で、必須成果が成立した。

この比較で変わったのは、失敗したfocused testの後の経路である。5文目を削除した条件では修正後の再試験とfull gateまで進み、両方の成功を記録した。初回の`import pytest`記述漏れは両条件で発生しており、5文目の削除によって初回の記述ミス自体が消えたわけではない。C163 iteration 4で続けて出たCSV改行の誤記は、4文版 iteration 2では現れず、focused再試験が通った。

## 条件と証跡

- 変更はC163のroot `AGENTS.md`から5文目をそのまま削除したことだけ。新しい指示への置換はない。
- 共通条件: `gpt-6-luna / high`、Codex CLI `0.156.1`、Standard14固定Layer 1、Rating v14、workspace-write、approval never、`max_workers=24`。比較用compatibility keyは`d72f0ae2d2d945c77bfab3ee51284db2dc8011fbc3072d096ecc3ca041fa304e`。
- 事前照合でprompt identity以外の条件一致を確認し、F02の不足5 runだけを発行した。
- 4文版のiteration 2は、初回pytest exit `2`、同じpytestの再実行exit `0`、full gate exit `0`。ほか4 runもfocused/full両gateがexit `0`。
- 計測・Layer 2証拠・選択・集計: `/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate163-4sentence-f02-luna6-high-20260924-r1`
- 4文版bundle SHA-256: `357f684904979c7703a1d9248d3b88ad9a1704eefa4243affc912ff6921cb5ac`
- 不一致ratingの訂正記録と訂正後集計: `rating-correction-f6ec1150753843669e47bcf3a2e7094f-v2.json`、`candidate-analysis-corrected.json`、`comparison-corrected.json`（上記計測ディレクトリ内）。元のwrite-once ratingとatomic run recordは保持している。

本記録はF02 N=5の観測であり、Standard14全体の結果ではない。
