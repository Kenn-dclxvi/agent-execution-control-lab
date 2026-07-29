# Candidate81 / Candidate85 planning-first Rating v14 Medium F04 N=5

## 結論

Candidate81とCandidate85はF04で各5 / 5件がvalid・rateable・score `4`だった。Candidate85は5 / 5件で実行前にoperationとproducerを宣言し、全件root-onlyだった。

Candidate85 minus Candidate81の中央値差は、quality `0.000`、all-agent token `+72,126`（`+38.29%`）、elapsed `+24.472`秒（`+24.70%`）である。事前固定した許容幅`0`を両コストKPIで超えたため、`quality_passed / cost_control_failed`とする。設計の停止条件に従いD01、標準14、採用、release、本体反映へ進めない。

## Identity

- evaluation set: `the-caption-planning-first-f04-r1`
- set identity SHA-256: `3c23275eba6eac434413b8dafe8e666bbd3b4b48bcdac2d0ee4e4a5b54018e3d`
- case: `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY/r2`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- repetition: 各`N=5`
- compatibility key: `02d96711c6f3d21deeb082f3752af905bdc7fbe255d133f4a36844a5f2bfeb4f`
- C81 result: `8a52a99a329540f9b07d3ccef0450aa1`
- C85 result: `77ee815cacf84b38abaf3493ea720a27`

試験内容は変更していない。F04 r2のmodel-visible TaskSpec、fixture、oracle、allowed path、required Node validation、adapter-owned teardownを両promptへ同一に適用した。

## 3 KPI

| prompt | score 4 | token中央値 | token合計 | token最大 | elapsed中央値 | elapsed合計 | elapsed最大 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| C81 | 5 / 5 | `188,382` | `960,444` | `222,259` | `99.089`秒 | `481.089`秒 | `107.378`秒 |
| C85 | 5 / 5 | `260,508` | `1,320,681` | `324,099` | `123.561`秒 | `621.414`秒 | `131.404`秒 |
| C85 - C81 | `0` | `+72,126` | `+360,237` | `+101,840` | `+24.472`秒 | `+140.326`秒 | `+24.025`秒 |

iteration別でもC85はtokenが5 / 5件、elapsedが5 / 5件で増えた。token差は`+25,680`から`+135,717`、elapsed差は`+14.721`秒から`+42.867`秒である。

## Route diagnostic

- C81: root-only 5 / 5、child session 0
- C85: root-only 5 / 5、child session 0
- C85は5 / 5件で最初のcommand前に全operationのroot producerを宣言した
- C85の同一operation重複、producer再割当て、Worker待機は0件
- command count中央値はC81 `10`、C85 `11`
- root prompt本文はC81 `5,525 bytes`、C85 `6,539 bytes`で`+1,014 bytes`（`+18.35%`）

したがって今回のコスト悪化をWorker起動へ帰属できない。両条件ともroot-onlyである。planning-first表現の追加とroot内のplanning / execution経路が、F04では一貫したtoken・elapsed増加と共存した。これは原因候補であり、本文byte増だけを単独原因と断定しない。

owner-producer evidenceは両条件の5件すべてでinadmissibleだった。Rating v14ではdiagnostic-onlyであり、成果品質のscoreを変更しない。

## Gate

- quality gate: `passed`
- cost state: `cost_control_failed`
- route state: `planning_observed / root_only`
- Candidate85 state: `targeted_f02_f04_evaluated / stopped`
- D01、標準14、採用、release、THE-CAPTION本体反映: 未実施・未判断

F02の`cost_tradeoff`だけでは停止しなかったが、F04でtokenとelapsedの両方が事前許容幅を超えた。D01 profileは未実行の準備artifactとして保持する。
