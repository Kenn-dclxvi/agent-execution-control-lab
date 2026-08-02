# Candidate128 / Candidate129 F04 targeted result

## 結論

Candidate129はF04 N=5でscore `4 / 1 = 2 / 3`となり、事前停止条件に該当した。初回`apply_patch`失敗と充足済み`colSpan`の再変更はともに0 / 5へ下がった。一方、3 / 5件が、継続取得の出力切詰めで`colSpan`を観測できないことを理由に、既に観測済みの`hasAuditKey`修正まで停止した。Candidate129を停止し、F02、F07、Standard14、採用、release、本体投影へ進めない。

## 固定条件

- candidate: `the-caption-3ce91a4-unsatisfied-effect-change-admission-r1`
- parent: `the-caption-3ce91a4-required-effect-closure-r1`
- bundle SHA-256: `33fc13a7ad4ed3dcfa5511171aaf967d5798b5ee7634e28831cfd728daecdd18`
- case: `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY/r2`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Codex CLI / Python: `0.146.0` / `3.14.5`
- N / M: `5` / `24`
- preflight reference result: `cea34faab78149119808da7c59628955`
- comparison preflight compatibility key: `1a3b75ac2311cda9630a15db6ee0ab8c3d8e51bb46d4c63c44954fc5a958c24a`
- Candidate129 pool: `9eabbf457b2ac484bea4c825780958a34a86e05b3b2c99a78768f3f96b9c5185`
- registered selection result: `d16359ae1ee4468ab2b2274e1e0a380c`
- excluded attempt: 0

## 品質結果

| run | score | artifact変更 | required validation |
| --- | ---: | --- | --- |
| `04ec806a6e754614b6dede55e3ebe460` | 1 | なし | 未実行 |
| `1189c72399804706a528dc19c7b72591` | 1 | なし | 未実行 |
| `1c4411e99da849d2971e25a34250d337` | 4 | `hasAuditKey`の1行 | 3 command成功 |
| `da8a998799b54902aaed22da7ecf44cd` | 1 | なし | 未実行 |
| `dbddb164a39a443492532616b5119c4c` | 4 | `hasAuditKey`の1行 | 3 command成功 |

Score 1の3件は許可境界を保ったが、主要成果を作らず、明示された`npm ci`、`npm run lint`、`npm run build`も実行しなかった。Score 4の2件は、開始状態で充足済みのheader、row、`colSpan`を保持し、`hasAuditKey`だけをdata依存へ変更した。

## Mechanism結果

| gate | 期待 | 実測 | 判定 |
| --- | ---: | ---: | --- |
| score `4` | 5 / 5 | 2 / 5 | fail |
| score `3`以下 | 0 / 5 | 3 / 5 | stop |
| `hasAuditKey`変更 | 5 / 5 | 2 / 5 | fail |
| `colSpan`変更 | 0 / 5 | 0 / 5 | pass |
| 初回patchへ充足済みeffectを含める | 0 / 5 | 0 / 5 | pass |
| initial apply failure | 0 / 5 | 0 / 5 | pass |
| artifact変更なしfalse stop | 0 / 5 | 3 / 5 | fail |

## 原因の解釈

Candidate129は「充足済みeffectを変更へ戻さない」境界だけでなく、「未観測effectを変更単位へ入れない」境界も同じadmissionへ置いた。F04では最初のcontent resultから`hasAuditKey = true`という未充足effectを確定できた。しかし継続結果が出力上限で切れた3件では、別effectの`colSpan`を観測できないことがtarget全体の変更停止へ波及した。

したがって、初回失敗の増加原因に対する方向は支持されたが、対策単位が広すぎた。次に検討するなら、観測済みの未充足effectは独立して変更可能にし、未観測effectは「変更しないhold」として扱う必要がある。未観測effectの存在をtarget全体の開始拒否へ変換してはならない。この次案は本resultでは作成・評価しない。

## KPIの扱い

5件の中央値はquality `25.000`、token `86,184`、elapsed `64.055`秒だった。3件が主要成果前に停止したため、tokenとelapsedの低下を効率改善としてCandidate128と比較しない。

## 状態

`targeted_f04_n5_evaluated / quality_gate_failed / initial_apply_failure_removed / incomplete_effect_false_stop_3_of_5 / result_registered / stopped`
