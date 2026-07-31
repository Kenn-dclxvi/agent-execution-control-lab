# Candidate122 / Candidate124 incomplete content continuation Rating v14 Medium A01 / A02 / F01 / F02 / F04 atomic N=5

## 結論

Candidate124は25 / 25件がvalidだったが、score `4 / 2 = 23 / 2`で品質gateを通過しなかった。2件はいずれもF04である。初回`App.tsx`取得後に同じtargetを一度continuationしたが、取得終端を620行にしたため表描画部分をなお観測できず、artifact変更と3つのrequired Node validationを行わず停止した。

さらにF02は、初回content wave後の追加readが2 / 5件へ再発し、token中央値`188,908`で目標`173,000`を`15,908`（`9.20%`）上回った。よって現在状態を`targeted_a01_a02_f01_f02_f04_evaluated / quality_gate_failed / f04_continuation_scope_incomplete / f02_content_wave_regressed / f02_cost_target_failed / result_registered / stopped`とする。Standard14、採用、release、runtime projection、本体反映へ進めない。

## Identityと実行前gate

- Candidate124 prompt: `the-caption-3ce91a4-incomplete-content-continuation-r1`
- bundle SHA-256: `5c5595bb0debfc2358f5c3e2b8f61cc4bffa496df30a209268ebe70d575ac341`
- profile: `candidate124-incomplete-content-continuation-v14-reasoning-medium-a01-a02-f01-f02-f04-global-m24-n5-cli0146-r1`
- Candidate118 5-case reference selection: `a43f7db80cef4948abb55af4e20b282a`
- Candidate118 5-case reference result: `374b32b97f0048e2a39f108cb197a921`
- Candidate124 pool: `97d20d2d42786cbb3581544c6ea9283e8344ac77dd11fb670ce3ae41c85dde12`
- Candidate124 selection: `eb2c8f352d6845509a931aa2c2f3024d`
- Candidate124 analysis: `d1a8ee1098754323a506b364d9ec35e1`
- Candidate124 result: `f6ce573be7c044319ed44c2e16f48cc8`
- execution: 25 / 25 valid、excluded 0、profile上の`M=24`
- execution archive SHA-256: `fb9a56bb5783ee2b3c22decbff7dbeec45b6f6b2447d207b89d82135931ceef1`
- final compact archive SHA-256: `9bd2e5dd25ed78ea82526ac97bc6a95e35c52dc406187a50702e04f04e2d6319`

最初の準備cycleは14-case Candidate118 resultを5-case profileへ直接bindしたため、preflightがcoverage不一致で停止した。評価slotは発行していない。その後、Candidate118の登録済みatomic runから同じ5 case各5件を選んだreference resultを固定し、r2 cycleのpreflightがreadyになってからCandidate124の25 slotだけを発行した。

## Case別結果

| case | score `4` | token中央値 | gate |
|---|---:|---:|---|
| A01 | 5 / 5 | `18,618` | quality pass |
| A02 | 5 / 5 | `150,266` | quality pass |
| F01 | 5 / 5 | `109,784` | quality pass |
| F02 | 5 / 5 | `188,908` | content wave 3 / 5、cost fail |
| F04 | 3 / 5 | `131,294` | false stop 2 / 5、quality fail |

5-case集約中央値はquality`100.000`、token`586,073`、elapsed`296.305秒`である。quality中央値は2件のscore `2`を隠すため、品質通過を意味しない。F04 token中央値も失敗runを含むため、成功costの根拠にしない。

## F04で起きたこと

5件すべてが、開始identityと`App.tsx` 1〜260行などを初回取得した。表描画部分は初回範囲外だったため、全5件が同じ`App.tsx`へ一度だけcontinuationした。

| continuation scope | 件数 | 結果 |
|---|---:|---|
| 261〜760行または260〜760行 | 3 | predicateをbindし、変更と3 validationを完了、score `4` |
| 261〜620行または260〜620行 | 2 | 必要criterionをなお観測できず停止、score `2` |

失敗runは`062da66f89054d40bff63f7cafa2d520`と`6fc70a5265114724abc1321c40646745`である。C124はcontinuationの回数とtargetを制限したが、その一回のscopeが未観測criterionを最後まで覆うことを要求しなかった。したがって「一回許可」だけではfalse stopを閉じない。

## F02で起きたこと

F02は5 / 5 score `4`だったが、初回content取得だけで変更へ進んだのは3件だった。残る2件は同じ4 targetへ追加のrangeまたはsymbol周辺readを発行した。tokenは`125,149 / 144,238 / 188,908 / 192,689 / 231,814`で、中央値は目標を超えた。

C124のcontinuation条件は、単一targetの不足だけでなく、複数targetが共同で一predicateを決めるF02にも適用された。そのためC122で成立していたF02 content wave 5 / 5を3 / 5へ戻した。これは品質を保った追加readでも、C124の保持gateとcost gateには不通過である。

## 次仮説

次候補はC124を微修正せず、C122を直接親とする。次の二条件を同じ`criterion-complete single-target continuation`軸として扱う。

1. `single_change_target_ready`: TaskSpec上、一つのeditable targetだけが全未解決変更criterionを所有する。複数targetが共同でpredicateを決める場合はcontinuationを開かず、C122のinitial content waveを維持する。
2. `continuation_scope_complete`: continuation requestは、未観測criterionへ直接bindしたsymbol周辺、または同じtargetの全未取得contentを覆う。根拠のない次のbounded chunkを一回として消費しない。

初回gateはA01 / A02 / F01 / F02 / F04各`N=5`を維持する。F04 5 / 5 score `4`とfalse stop 0 / 5、F02 content wave 5 / 5とtoken中央値`173,000`以下を同時に要求する。
