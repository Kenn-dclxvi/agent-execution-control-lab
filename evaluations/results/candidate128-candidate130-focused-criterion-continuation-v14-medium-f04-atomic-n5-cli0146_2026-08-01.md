# Candidate128 / Candidate130 F04 targeted result

## 結論

Candidate130はF04 N=5でscore `4 / 1 = 2 / 3`となり停止条件に該当した。5件すべてが、bind済みsymbol contextではなく`App.tsx`の261行目から終端までを取得した。focused continuationは0 / 5で、追加した優先関係は実行判断を制御しなかった。F02 preservation、Standard14、採用、release、本体投影へ進めない。

## 固定条件

- candidate: `the-caption-3ce91a4-focused-criterion-continuation-r1`
- parent: `the-caption-3ce91a4-required-effect-closure-r1`
- bundle SHA-256: `690885185785d8e254b52370a34543fe5ae37fc58b14111c2ca7c0eadcfe2486`
- case: `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY/r2`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Codex CLI / Python: `0.146.0` / `3.14.5`
- N / M: `5` / `24`
- preflight reference result: `cea34faab78149119808da7c59628955`
- compatibility key: `1a3b75ac2311cda9630a15db6ee0ab8c3d8e51bb46d4c63c44954fc5a958c24a`
- pool: `f86d64da31fb79bf9dbef199569b385c402c724475b366035ca8e61f81723b5e`
- registered selection result: `344e457ae32643dfb36fc5e891f19138`
- excluded attempt: 0

## 結果

| run | score | continuation | 結果 |
| --- | ---: | --- | --- |
| `385432cbfe9545068a30b2588f56dc14` | 4 | `sed 261,$p` | `hasAuditKey`一行変更、3 validation成功 |
| `7d0d113e7a004a8fa63f7e55a7bc6f55` | 1 | `sed 261,$p` | patch不一致後、変更・validationなし |
| `9222c3da9ec84c94b74dadfcd2c20cc6` | 1 | `sed 261,$p` | patch不一致後、変更・validationなし |
| `a4df24d1d9744b748642e3071b8a9941` | 4 | `sed 261,$p` | `hasAuditKey`一行変更、3 validation成功 |
| `b3acec14558847a981582fc1660fe833` | 1 | `sed 261,$p` | content切詰め後、変更・validationなし |

| gate | 期待 | 実測 | 判定 |
| --- | ---: | ---: | --- |
| score `4` | 5 / 5 | 2 / 5 | fail |
| score `3`以下 | 0 / 5 | 3 / 5 | stop |
| focused symbol continuation | 5 / 5 | 0 / 5 | fail |
| locator-only独立result | 0 / 5 | 0 / 5 | pass |
| 全未取得content continuation | symbolをbind不能な場合だけ | 5 / 5 | fail |
| artifact変更なしfalse stop | 0 / 5 | 3 / 5 | fail |

## 解釈

Candidate130はC125のOR条件へ「symbol identityがあればfocused contextを選ぶ」という優先関係を加えた。しかし全5件は、TaskSpecに`hasAuditKey`、Audit Key、`colSpan`が示されていても、従来の全残存contentを選んだ。

したがってEvidence coverageの残差は、requestの大小比較だけでは解けない。`symbol identityがbind済みか`という新しい判断自体が実行時に成立しなかった可能性と、既存の`全未取得contentを終端まで覆う`経路が強く残った可能性を分離する必要がある。Candidate130へ文面を継ぎ足さず停止する。

5件中央値はquality `25.000`、token `124,178`、elapsed `74.210`秒である。3件が成果前停止のため、効率改善として解釈しない。

## 状態

`targeted_f04_n5_evaluated / quality_gate_failed / focused_continuation_0_of_5 / false_stop_3_of_5 / result_registered / stopped`
