# Candidate202 Standard14全14ケースN=5実行準備監査

> **結果**: `execution_preparation_passed / comparison_preflight_ready / seventy_slots_authorized / issued_zero`

## 結論

Candidate202のStandard14全14ケース各5件は、Candidate175登録resultと、そのresultを実際に生成した保存Layer 1へbindし、prompt identity以外の互換条件を機械照合して発行直前まで準備できた。comparison preflightは`ready`で、不足70件だけを許可した。監査時点の発行数は0件である。

## 固定identity

- profile SHA-256: `f5c74c6ee4a5e6cf90a416fadacb2c0bbbd12517c9ba8dd5ee8e6dda098d1f1e`
- reference result: `c31b560bce92400293c7b3bc40715246`
- reference result content SHA-256: `1d37fd543ecd273fdb4e282b4774a57ceae6f0e0c357983aebf1949fc4c809ce`
- compatibility key: `cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561`
- Candidate175 reference pool: `ac1eeac565d603e1f7b3662bf3316e59c28ca4346a3eee522b37c0be506cefbd`
- Candidate202 pool: `3a04225ca96ebe43a456d9cb935cb4935d8b3b14aab3ab95a70123f37d96d958`
- dispatch plan file SHA-256: `51316aae5934ad752eb94612810afe020df62d2f89bda54748e478c8b95523dc`
- dispatch plan content SHA-256: `5c7f2884a4b910210b14853b1d484ffc63049a610bb9905deec0e9ede48d7bc7`
- global plan SHA-256: `59c692330112417f8f3a1eee3a775e71747526df361e780fdeffc96a2bab84a5`
- comparison generation receipt file SHA-256: `9bc83a1163b1c908b69caeb54dac8afaeb75dbbde857fb85fb4dd5c22c0966e2`
- comparison generation receipt content SHA-256: `4cf402a8e71a34fe56a0b9ae2908223f329e8ceb7bbb7aa505316dbf78b7db60`
- comparison preflight receipt file SHA-256: `954eb7586ffc79c805b431638838d4e143fb414de8b6e7208894290720eab1d1`
- comparison preflight receipt content SHA-256: `3a6c0aa8e5c4199934600d868aea29156ee6ee4caf3bde9c7a7d59082aa8f7a4`
- preparation root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate202-review-admission-routing-receipt-v14-medium-standard14-n5-cli0146-20260813-r1`

## 不足slot

`seed-pool`はCandidate202の空poolを作成した。`plan-missing --desired-count 5`の結果はStandard14全14ケースのexisting各0、missing各5、合計70件である。各slotは独立sample IDを持ち、global planの設定上の並列上限はM=24である。

## 互換条件

Evaluation set identity `2096d15e9d5d072e09e92313caa296caf8853c5e86f205d4d9f819b576263c33`、全fixture identity、case revision、TaskSpec、rating、model、reasoning、Agent/runtime/CLI、permission、executor、command evidence protocol、token accounting、target commit/treeおよびM=24はreferenceと一致する。異なるのは事前宣言したprompt identity、bundle hashおよびbundle pathだけである。

最初の参照候補はF01 fixture identity不一致のため、2番目は参照Layer 1内の旧receiptとの出力先衝突のため、それぞれpreflight生成中に停止した。いずれもslot発行数は0件である。3回目はCandidate175 resultを実生成したLayer 1の`set.json`、`coverage.json`および`fixtures/`をbyte-preserving copyし、旧receiptだけを除いた参照入力で実施した。`prepare-comparison-layer1`、`preflight-comparison`および`verify-comparison-preflight`はすべて成功した。

`candidate202_existing_0 / candidate202_missing_70 / authorized_70 / issued_0 / comparison_preflight_ready / candidate202_not_evaluated`
