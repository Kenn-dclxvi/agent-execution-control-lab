# Candidate191 ADR05・ADR07・ADR09 N=20拡張実行準備監査

> **位置づけ**: M6実行前監査／既存15件再利用／不足45件承認／発行0件

## 結論

Candidate191のM6は、`TC-ADR05`、`TC-ADR07`、`TC-ADR09`の登録済み各5件を再利用し、累積各20件に必要な不足各15件、合計45件だけを発行できる状態まで準備した。canonical comparison preflightは45 slotを`ready`として承認し、監査時点の発行数は0件である。

M5の登録result `b71bcb211b064977900bce9aa0132cd4`は、訂正機序監査r3と一組でM6への再利用資格を持つ。atomic registryへ登録resultの30 runを不変のままimportし、ADR05、ADR07、ADR09の15 runだけを固定selectionへ選んだ。旧機序監査r2単独の停止判定や、C147・C176の旧collector判定を比較基準へ使用していない。

## 固定identity

- prompt: `the-caption-3ce91a4-explicit-review-operation-applicability-r1`
- bundle SHA-256: `6ff3f31585185ca2f08fd63eb19e4d75156425aecc1e1a6da63753768b24a163`
- M5 source result: `b71bcb211b064977900bce9aa0132cd4`
- M5 corrected mechanism audit: `candidate191-explicit-review-operation-applicability-adr9-r2-n5-mechanism-audit-r3.json`
- reference selection: `540a8cc98b354c269f806b4a2070afc4`
- reference selection content SHA-256: `31975077e64e395d6138f9d397dc4ac753b732f8706a523af7963155455274de`
- reference result: `6276f69f82a3438897b5aed199d41cfc`
- reference result content SHA-256: `d4575ad66ebf6ae603f894e9a8130277da2d70c8aa382b1381c579e73e01f188`
- reference profile: `candidate191-explicit-review-operation-applicability-adr05-adr07-adr09-reference-n5-medium-m24-cli0146`
- cumulative profile: `candidate191-explicit-review-operation-applicability-adr05-adr07-adr09-n20-medium-m24-cli0146`
- pool key: `292840d77723c806003574680837b82136477582c841927dd1b3223865afd42d`
- compatibility key: `155587cce22ef1f34d5366bd6612a0a6e69ed8225160c51cd5abc6fada945b15`
- dispatch plan SHA-256: `93a4c94bd9cebb76e81dbe92d7398d9c2829c86cc3111d72038f2ad50df581bc`
- global plan SHA-256: `e91fa7799a6a4dead4521c82f094d69f00b8ebd27c72640b07a3deb0153b6888`
- comparison receipt content SHA-256: `68735a7e985fb87ca8bd85a4e898f748377ff87e841924a9ae3b447efd0a7cbf`
- max workers: `24`

一次artifactは`/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate191-explicit-review-operation-applicability-adr05-adr07-adr09-n20-20260812-r1`に保存した。実行対象は`atomic-plan-r3/global-plan.json`、comparison preflight正本は`cycle-r3/layer1/comparison-preflight.json`、atomic registry正本は`registry-canonical`である。

## 発行範囲

| case | 既存再利用 | 新規承認 | 累積gate |
| --- | ---: | ---: | ---: |
| `TC-ADR05` | 5 | 15 | 20 |
| `TC-ADR07` | 5 | 15 | 20 |
| `TC-ADR09` | 5 | 15 | 20 |
| 合計 | 15 | 45 | 60 |

`TC-ADR01`〜`TC-ADR04`、`TC-ADR06`、`TC-ADR08`およびTPO系列は追加発行しない。

## 監査結果

1. M5登録resultからimportした30 runのうち、対象3ケースは各5件であり、固定selectionは15件だけを含む。
2. `plan-missing --desired-count 20`は既存各5件を数え、不足各15件だけをdispatchへ含めた。
3. 45 capsuleはCandidate191のprompt identity、固定comparison conditions、個別sample IDおよび3ケースだけへbindされた。
4. templateとcapsuleにはprivate oracle、期待terminal、期待review件数、過去Candidateの結果、quality scoreまたはresult kindの正解値を追加していない。
5. 保存済みLayer 1のfixture identity、Evaluation set、TaskSpec、rating、model、reasoning、runtime、permissionおよびexecutor条件はreference resultと一致した。
6. M=24を不足件数へ合わせて変更せず、`environment_adjustment=none`、`max_attempts=3`を維持した。
7. comparison receiptの`authorized_slots`は45件、`issued_slots`は0件で、`verify-comparison-preflight`も`ready`を返した。

## 準備中に停止した経路

準備診断は削除せず、いずれもslot発行前に停止した。

- M5時点のseed済みpoolは定義だけでrun登録が0件だったため、そのcopyを直接再利用せず、登録resultを新しいcanonical registryへimportした。
- 最初のLayer 1 cloneはfile modeを保持せずfixture digestが不一致になった。条件を緩和せず、mode保持付きcloneを`reference-cycle-n5-r2`へ作成した。
- M5に残っていたtemplateはCandidate190 identityだったため、TaskSpecやmodel-visible payloadを変更せず、prompt identity、bundle hashおよびbundle pathだけをCandidate191固定値へ合わせた。
- 累積N=20 profileをpreflight profileへ直接使うとreference N=5 coverageと一致しなかった。atomic経路の規定どおり、互換性は3ケースN=5 reference profile、45件の不足集合はdispatch planへ分離してcanonical `cycle-r3`を作成した。

## 境界

本監査が証明するのは、比較互換性、入力封鎖、既存run再利用および発行範囲だけである。Candidate191 M6のquality、mechanism、M7全体、採用、releaseまたはprojectionは証明しない。次に許可する操作は、固定global planの45 slotを発行することだけである。

## 状態

`execution_preparation_passed / corrected_m5_result_bound / reference_n5_bound / cumulative_n20_dispatch_fixed / authorized_45 / issued_0 / private_boundary_passed / ready_for_m6_execution`
