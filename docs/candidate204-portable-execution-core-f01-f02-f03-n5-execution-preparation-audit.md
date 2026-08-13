# Candidate204 portable execution core F01 / F02 / F03 N=5実行準備監査

> **結果**: `execution_preparation_passed / comparison_preflight_ready / fifteen_slots_authorized / issued_zero`

## 結論

Candidate204のF01 r3、F02 r1、F03 r2各5件、合計15 slotは、保存済みCandidate175 atomic runから作った3ケースselection resultと、そのfixtureを実生成した保存Layer 1へbindし、prompt identity以外の互換条件を機械照合して発行直前まで準備できた。

comparison preflightは`ready`で、不足15件だけを許可した。監査時点の発行数は0件である。

## 固定identity

- profile SHA-256: `e25e6b6a992650a38533a604a1f3831abef3b86db0da61fd698b9c1b68ac20be`
- reference selection: `87c9a3ee7a674bfc8cbb0fba8727e82f`
- reference selection content SHA-256: `fd5861595aa49e8cbe327075bf92d852db731f4baef6b73f3b62067f4385d720`
- reference result: `a205f69159464c0da704d8e3a362d0c3`
- reference result content SHA-256: `7ff4a326b5d59c3e405d99b349ec7c7e0966cba0d6119c2d4f45c89d9749e0b6`
- compatibility key: `a1264d0c1bc19834f7ac43266bc2d1489bfddfae171ce7356cb20d4ce5c9cb11`
- Candidate175 reference pool: `ac1eeac565d603e1f7b3662bf3316e59c28ca4346a3eee522b37c0be506cefbd`
- Candidate204 pool: `dc33d46e218cf9a841188d226e218e93a8baff3446397bbdafb269774ffdbeb3`
- dispatch plan SHA-256: `aa80a6728f524f0a063b7c138bebd4202d1b366b6c95c04c804237247bc45989`
- global plan SHA-256: `b5294a72df45bbc8e591f347f2a7116bf528407f4b5d74d35352da0ff90bb0eb`
- comparison generation receipt SHA-256: `8a8747cf397c5814298067a700d46a8f0978858bfb5afa6163fafb908b1b9b68`
- comparison preflight receipt SHA-256: `a6ba8198143c89a2d329e162c25f9273c92aa84cdc8c66444bd1df2d70747ec4`
- preparation root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate204-portable-execution-core-f01-f02-f03-n5-20260813-r1`
- active cycle: `cycle-r3`

## 不足slot

`seed-pool`はCandidate204の3ケース空poolを作成した。`plan-missing --desired-count 5`は各ケースのexisting 0、missing 5、合計15件だけを返した。各slotは独立sample IDを持ち、global planの設定上の並列上限はM=24である。

## 参照Layer 1

最初の試行は14ケースLayer 1と3ケースselection resultのcoverage不一致を検出して停止した。2回目は既存3ケースLayer 1に残る旧comparison receiptとの出力先衝突を検出して停止した。いずれもslot発行、adapter起動およびrunは0件である。

3回目はCandidate146の保存済み3ケースLayer 1をbyte-preserving copyし、生成先と衝突する旧comparison receiptだけをcopy対象から除外した。fixtureを再生成していない。`prepare-comparison-layer1`はEvaluation set identity `2096d15e9d5d072e09e92313caa296caf8853c5e86f205d4d9f819b576263c33`と3 fixture identityをreference resultへ照合して成功した。

## 互換条件

F01〜F03のcase revision、fixture、TaskSpec、rating、model、reasoning、Agent/runtime/CLI、permission、executor、command evidence protocol、token accounting、target commit/treeおよびM=24はreferenceと一致する。異なるのは事前宣言したprompt identity、bundle hashおよびbundle pathだけである。

`prepare-comparison-layer1`、atomic plan生成、`preflight-comparison`および`verify-comparison-preflight`はすべて成功した。run直前にも同じreceiptを再検証し、一項目でもdriftした場合はadapter起動前に停止する。

`candidate204_existing_0 / candidate204_missing_15 / authorized_15 / issued_0 / comparison_preflight_ready / candidate204_not_evaluated / Standard14_not_started`
