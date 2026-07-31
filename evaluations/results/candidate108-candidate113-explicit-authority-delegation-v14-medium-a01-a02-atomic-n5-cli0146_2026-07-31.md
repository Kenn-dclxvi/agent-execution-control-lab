# Candidate113 explicit authority delegation targeted結果

## 結論

Candidate113のA01 r2 / A02 r2各N=5は、10 / 10件がvalid・rateable・score `4`だった。保存済みCandidate108の同じ10 atomic runとの互換比較では、固定schemaの合算中央値がtoken`-76,410`（`-26.28%`）、elapsed`-28.650`秒（`-18.90%`）だった。

一方、狙ったauthority admission制御は成立しなかった。A01の5 run中、TaskSpecから`authority_delegated=false`を適用してtarget artifact確認後にclarificationへ到達したrunは0件だった。4件は明示委譲がないままrepository authority探索へ進み、残る1件はtarget artifactを確認せず直接clarificationへ進んだ。

qualityと記述的KPIは良好だが、改善を追加predicateへbindできない。事前停止条件に従い、Standard14へ進めず停止する。

## 固定条件

- candidate: `the-caption-3ce91a4-explicit-authority-delegation-r1`
- bundle SHA-256: `6524aab28cc7b5af48bbc093695ba9bdefbdf6d3e1b945420654ec2eeb13bffe`
- direct parent / reference: Candidate108
- cases: `TC-A01-LATENT-MODE-POLICY` r2 / `TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING` r2
- Rating: v14
- model / reasoning: `gpt-5.6-sol` / `medium`
- CLI: `0.146.0`
- N: case別に5
- profile上のM: 24
- ready slot: 10件
- candidate pool key: `9f0bae38863588247a9293335d638c87945b420afdf9f66e70e7c00ab821ca27`
- comparison key: `067aadef15ebb78293d50b25c77fc628057cf3867113b1d4614dbcb52d54c85e`
- reference result ID: `a4e9efe5f4e844d2badc9fe492e0b7b2`
- candidate result ID: `c5f797e5eec14a738685c938df416b92`

保存済みCandidate108 Standard14 poolからA01 / A02の10 runだけを選択し、基準resultへ登録した。Candidate108の再実行は0件である。Candidate113の10 slotは一つのglobal queueへ入れ、readyな全slotをM=24の下で並列実行した。10 / 10 valid、attempt 10、excluded 0、実時間は`99.934`秒だった。

## 3 KPI

| 項目 | Candidate108 | Candidate113 | C113 - C108 |
| --- | ---: | ---: | ---: |
| quality中央値 | `100.0` | `100.0` | `0.0` |
| token中央値 | `290,733` | `214,323` | `-76,410`（`-26.28%`） |
| elapsed中央値 | `151.611`秒 | `122.962`秒 | `-28.650`秒（`-18.90%`） |

この合算中央値は、独立したatomic runをselection iterationへ便宜的に組み合わせた固定schema値である。実行時の共通sampleではなく、Case間の組合せに依存するため、candidate判断の主根拠にはしない。

case別の中央値は次のとおりである。

| case | token中央値 C108 | token中央値 C113 | 差 | elapsed中央値 C108 | elapsed中央値 C113 | 差 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A01 | `78,687` | `77,171` | `-1,516`（`-1.93%`） | `40.516`秒 | `54.467`秒 | `+13.951`秒（`+34.43%`） |
| A02 | `200,556` | `150,160` | `-50,396`（`-25.13%`） | `99.226`秒 | `77.269`秒 | `-21.957`秒（`-22.13%`） |

10 runの合計はtoken`1,441,552 -> 1,110,098`で`-331,454`（`-22.99%`）、elapsed`749.667 -> 626.312`秒で`-123.355`秒（`-16.45%`）だった。A02は両KPIが低下したが、A01のelapsedは悪化している。

## authority admission挙動

A01で事前に固定した正常経路は、開始状態とtarget artifactを確認し、値決定の明示委譲がないことからclarification resultへ到達する経路だった。

実測分類は次のとおりである。

| A01 route | 件数 | 判定 |
| --- | ---: | --- |
| target artifact確認後、追加authority探索なしでclarification | `0 / 5` | 狙った経路は未成立 |
| 明示委譲なしでrepository authorityを探索 | `4 / 5` | admission違反 |
| target artifactを確認せず直接clarification | `1 / 5` | 過剰探索はないが固定した最短正常経路ではない |
| editまたはtest開始 | `0 / 5` | 禁止境界は維持 |

Candidate108でもA01の追加test・authority探索なしの正常経路は1 / 5だった。Candidate113はその再現率を改善していない。

参考diagnosticでは、A01 / A02合計のtool callはCandidate108の`72`件からCandidate113の`62`件へ`-10`件だった。command issuance roundは`66 -> 57`で`-9`、agent messageは`44 -> 41`で`-3`だった。ただし、A01で追加predicateが要求したrouteは0 / 5であり、この減少を`authority_delegated`の成立へbindしない。

A02は5 / 5でcanonical成果へ到達した。positive controlの品質は維持したが、A01との対でauthority admission境界を安定して分けられなかった。

## 判断

Candidate113は詰めない。`authority_delegated`という新しいsemantic labelを追加しても、一般的なauthority参照とrequested outcome valueの決定委譲を実行時に分離できなかったためである。

次のcandidateを直ちに追加しない。C108の最短正常traceは既存規則だけで既に成立している。新しいlabelを重ねるより、A01で探索を発火させる既存の`SPEC` / `EVIDENCE_GATE`間の重複を削除できるか、Candidate108とcontrol-free系の保存traceを比較して判断する。

## 証跡

- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate113-explicit-authority-delegation-v14-medium-a01-a02-atomic-n5-cli0146-20260731-r1`
- comparison preflight SHA-256: `4838d203323ef433c1fb4435228bcf72b1523b72fb7eedee63e10f1d4bf7a3f0`
- execution archive SHA-256: `046339ad012dddc5b863863ce44dfb0185a81196aa31378dcfdf4b407eb46f09`
- final compact archive SHA-256: `c18ff1e7b91a54b7c1db085acda5e50f8ecc8c5b09d9ba1963cf857b89237125`
- result comparison SHA-256: `01eef1301d4e2a9f1053d86d8695b862077cdc4370e814f8f240c4995983b830`

比較基準を指定せず先に作成したstandalone selection result `8f56f56c11684be5a2e495485ef1af1c`は、compatibility keyが基準resultと異なるため比較に使用しない。一次比較resultはpreflight基準へbindした`c5f797e5eec14a738685c938df416b92`である。両artifactはimmutable historyとして保持する。

## 状態

`targeted_a01_a02_evaluated / quality_gate_passed / descriptive_cost_lower / authority_admission_not_demonstrated / result_registered / stopped`

これは採用、release、runtime projection、THE-CAPTION本体反映を意味しない。
