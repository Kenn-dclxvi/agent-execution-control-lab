# Candidate151 / Free 6 case targeted N=5結果

## 結論

Candidate151は30 / 30件がscore 4だったが、A02の変更後method探索が2 / 5件に残ったためmechanism gateで停止した。読みやすさを欠く研究用語中心の一文を、効果が確認できた読者向けプロンプトとして採用しない。

| gate | 実測 | 判定 |
| --- | ---: | --- |
| valid / rateable / score 4 | 30 / 30 / 30 | quality pass |
| A01 clarification停止 | 5 / 5 | pass |
| A02 canonical成果 | 5 / 5 | pass |
| A02変更後method探索 | 2 / 5 | fail |
| F04 required変更後source確認 | 2件発行、2 / 2でchanged effectへ接続 | preserved |
| 他4 caseのrequired outcomeとvalidation | 20 / 20 | pass |

## 失敗挙動

A02 iteration 1は`run.sh`の変更後に既存testを検索し、test fileを読んでfocused testを選んだ。iteration 3も変更後にtest symbolを検索してからfull testを実行した。どちらも実装内容は変更前に確定済みであり、TaskSpecが要求したvalidation predicateを満たす具体的methodを探す追加repository evidenceだった。

F04 iteration 1と5は変更後に`App.tsx`の`hasAuditKey`、Audit Key列、`colSpan`を読み、TaskSpecが求めるchanged effectを直接確認した。この2件は必要な変更後evidenceとして保持できた。

したがってCandidate151は、必要な変更後readを残した一方、不要なmethod探索を0件へ閉じられなかった。

## 固定条件

- candidate: `the-caption-3ce91a4-evidence-consumer-boundary-readable-r1`
- bundle SHA-256: `65dd4e4496e205d97df6b07e31fa8c1d87093582810b3fe8c7321a9a30c51f80`
- cases: A01 r2 / A02 r2 / F01 r3 / F02 r1 / F04 r2 / F07 dependency r1
- rating / model / reasoning: v14 / `gpt-5.6-sol` / Medium
- CLI / Python / configured M / N: `0.146.0` / `3.14.5` / `24` / 各`5`
- reference: Free result `8aed5c1abaed4390aed2432d28a5523f`
- candidate pool: `54df8e7518659451ab4dbcb07e116a33b7fc98d5e89a384c700d032911e193b4`
- selection: `e36aad98cd6740f3ab528c4f1075c6ca`
- registered result: `1539063412e942f6ad9e0fbfce624a6a`
- compatibility key: `438d2d35fcea9a7300969c308f794f56cd7d8e03f2ce54b894b447acb5eaf95c`
- execution / final archive SHA-256: `c361ddcd48a0c82992d56e01fb48da597075481f2fef27463ee67e84732c4216` / `2d69f6108dada42e4f98ac9c471ce9730b6d00a858a375d3fc429813c85f802c`

## KPI診断

6 case合計中央値はCandidate151が1,196,490 token・489.448秒、Freeが1,611,749 token・540.284秒だった。差はtoken`-415,259`（`-25.76%`）、elapsed`-50.837秒`（`-9.41%`）である。

品質とKPIが良くても、追加した一文が狙った変更後探索を閉じていないため、cost差をそのmechanismの効果として採用しない。Standard14、採用、release、本体反映は未実施である。
