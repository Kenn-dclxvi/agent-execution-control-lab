# semantic grader資格試験 preflight r1 結果

## 結論

seal済みholdoutとreferenceを使う単独資格graderについて、発行前preflightが成功した。状態は`ready_not_issued`、発行数は`0`であり、資格graderはまだ実行していない。

reference labelとorganizer mapは固定sourceとして比較処理へbindしたが、graderのpacket、stdinおよびmodel inputには含めていない。

## receipt

- receipt ID: `general-chat-semantic-qualification-grader-r1-preflight-r1`
- external run root: `/Users/kenn/repos/_verification/general-chat-response-control/semantic-grader-qualification-r1-attempt-r1`
- `preflight.json` file SHA-256: `44dc731e0f9daa668190d24eb420d75396882a7ecc368c1e4e832f3814e2ac44`
- receipt content identity: `b8dc5d646d9701d93c19e177dfae40cbfdcdb2d661379980c3520df4f410ad27`
- issued slot count: `0`

## grader identity

- grader identity: `general-chat-semantic-grader-terra-medium-r1`
- execution ID: `semantic-qualification-terra-r1`
- model: `gpt-5.6-terra`
- reasoning: `medium`
- runtime: `codex-cli 0.148.0`
- run count: `1`

## 測定式

測定式は[`qualification-metric-contract-r1.json`](../calibration/qualification-metric-contract-r1.json)を正本とする。

- exact agreement rate: 全32 reference assertionを分母とする
- false pass rate: referenceが`fail`の13 assertionを分母とする
- false fail rate: referenceが`pass`の19 assertionを分母とする
- unknown rate: 全32 reference assertionを分母とする
- major false pass: rateではなく件数とする

固定thresholdは完全一致`1`、各誤判定の最大値`0`であるため、label不一致が1件でもあれば資格graderを合格にしない。

## 現在の効果

このpreflightは固定receiptから資格grader一件を一度だけ発行できる状態を表す。grader適格性、正式評価、r2有効化、prompt採用、releaseまたはprojectionを意味しない。発行直前に同じreceiptを再検証し、source、material、runtimeまたはreceiptがdriftしていれば実行しない。
