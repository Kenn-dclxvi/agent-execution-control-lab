# Candidate81 / Candidate86 producer plan fast path Rating v14 Medium F04 N=5

## 結論

Candidate81とCandidate86はF04で各5 / 5件がvalid・rateable・score `4`だった。Candidate86は5 / 5件がroot-onlyだった。

Candidate86 minus Candidate81の中央値差は、quality `0.000`、all-agent token `+12,747`（`+6.77%`）、elapsed `-5.975`秒（`-6.03%`）である。事前固定した許容幅`0`では`quality_passed / cost_tradeoff`とする。Candidate85で観測したtoken・elapsed両方の悪化は再現せず、停止条件には該当しないため既存D01 r1へ進む。

## Identity

- evaluation set: `the-caption-planning-first-f04-r1`
- set identity SHA-256: `3c23275eba6eac434413b8dafe8e666bbd3b4b48bcdac2d0ee4e4a5b54018e3d`
- case: `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY/r2`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- repetition: 各`N=5`
- compatibility key: `02d96711c6f3d21deeb082f3752af905bdc7fbe255d133f4a36844a5f2bfeb4f`
- C81 result: `8a52a99a329540f9b07d3ccef0450aa1`
- C86 result: `0046a61f3fc1499d94c6b595d1acbb4f`

試験内容は変更していない。C85評価で固定済みのF04 r2 Evaluation setを再利用し、model-visible TaskSpec、fixture、oracle、allowed path、required Node validation、adapter-owned teardownをC81 / C86へ同一に適用した。新しいcase、fixture、oracle、Evaluation setは作成していない。

## 3 KPI

| prompt | score 4 | token中央値 | token合計 | token最大 | elapsed中央値 | elapsed合計 | elapsed最大 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| C81 | 5 / 5 | `188,382` | `960,444` | `222,259` | `99.089`秒 | `481.089`秒 | `107.378`秒 |
| C86 | 5 / 5 | `201,129` | `1,024,440` | `248,674` | `93.115`秒 | `451.428`秒 | `98.997`秒 |
| C86 - C81 | `0` | `+12,747` | `+63,996` | `+26,415` | `-5.975`秒 | `-29.661`秒 | `-8.381`秒 |

token合計はC81比`+6.66%`、elapsed合計は`-6.17%`だった。片方のKPIだけが改善しているため、効率改善またはcost controlledとは判断しない。

## Paired diagnostic

| iteration | token差 | elapsed差 |
| ---: | ---: | ---: |
| 1 | `+3,741` | `-8.681`秒 |
| 2 | `-13,157` | `-9.445`秒 |
| 3 | `-12,286` | `-14.600`秒 |
| 4 | `+2,713` | `-7.395`秒 |
| 5 | `+82,985` | `+10.460`秒 |

elapsedは4 / 5件、tokenは2 / 5件でC86が小さかった。iteration 5は両方増えたため、安定した効率改善とは主張しない。

## Route diagnostic

- C81: root-only 5 / 5、child session 0
- C86: root-only 5 / 5、child session 0
- C86のWorker待機、同一operation重複、producer再割当て: 0件
- root prompt本文はC81 `5,525 bytes`、C86 `5,914 bytes`で`+389 bytes`（`+7.04%`）
- Candidate85のroot prompt `6,539 bytes`より`625 bytes`（`9.56%`）小さい

今回のF04では単一operation fast pathが5 / 5件で成立した。owner-producer evidenceは両条件の5件すべてでinadmissibleだった。Rating v14ではdiagnostic-onlyであり、成果品質のscoreを変更しない。

## Gate

- quality gate: `passed`
- cost state: `cost_tradeoff`
- route state: `root_fast_path / root_only`
- Candidate86 state: `targeted_f02_f04_evaluated / proceeding_to_d01`
- D01: 実行可能
- 標準14、採用、release、THE-CAPTION本体反映: 未実施・未判断
