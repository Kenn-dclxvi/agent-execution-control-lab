# Candidate274 Standard14 N=5の続行

利用者の「いいよ。そのままつづけて」を、初回6ケースのC147比トークン+0.80%を受け入れてStandard14全14ケース各N=5へ続行する指示として固定する。初回のコスト条件不通過という履歴は変更せず、今回の続行根拠を別に記録する。

実行者はroot。成果条件は、既存の30runを再利用して不足8ケース各5回の40runだけを実行・採点・登録し、全70runを同一条件のC147と比較することである。プロンプト・fixture・TaskSpec・採点契約・model・reasoning・CLI・permission・token accountingは初回と同一。configured max_workersは24を保持する。基準resultはC147 Astra Standard14 N=5の`654d171e89a547d9af421ec9ee05ad96`、基準poolは`3f0740c14d3585e9ae07463ab04b2f0251531c094d13215e3f61709653c7e2b0`とする。

新しい全14ケースpoolへ同じC274 prompt identityをbindし、caseごとに既存runを照合する。runが存在する最初の6ケースを再実行しない。元の14ケースLayer 1を比較準備の正規経路で再利用し、不足slot40件と全14ケースcoverageを実行前に照合する。全件の実行・採点・登録までを行い、終了後の値を見て停止基準を遡及変更しない。

未確認・不一致では発行0で停止。invalid・採点不能は品質へ混ぜず、既存profileの外部失敗方針だけを適用する。品質低下は記録して追加Nへ進めない。今回の続行はN=20、N=100、採用、release、本体反映の許可を意味しない。品質とKPI、未評価の範囲を全体N=5結果で報告する。

## 実行前照合済み

不足slotは8ケース各5件の40件だけであり、初回6ケースとの重複は0件。`prepare-comparison-layer1`、`prepare_atomic_plan.py`、`preflight-comparison`、`verify-comparison-preflight`を通過した。

- [全体プロファイル](../evaluations/profiles/candidate274-execution-boundary-core-v14-medium-standard14-astra-m24-n5-cli0153-r1.json)
- 全体pool: `f1c7cf11fd3a7c5638c58fcc1e3fb78e98ff3e1ab6bc942db35a3a70614bb085`
- 証跡保存先: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate274-v14-medium-standard14-astra-n5-cli0153-20260905-r1`


## 完了結果

[Standard14全体N=5結果](../evaluations/results/candidate274-c147-astra-medium-standard14-n5_2026-09-05.md)を登録した。既存30件と追加40件の全70件がScore 4で、C147比トークン0.91%減、経過時間26.52%減。今回の続行範囲を完了した。
