# C147 transition contract r4校正結果

> [!IMPORTANT]
> **状態**: `completed / valid_14_of_14 / score4_14_of_14 / mechanism_14_of_14 / reference_contract_qualified / portable_prompt_unchanged / independent_heldout_not_yet_frozen`

## 結論

C147 referenceによるtransition contract r4校正は、14 / 14 valid、14 / 14 Score 4、14 / 14 mechanism passedで通過した。r1の失敗をportable promptの不足として扱わず、model-visible response projectionの時間境界、failed actionの失効、authority不足recoveryの`unavailable`、許可済みenvironment recoveryの開始triggerをTaskSpec側へ分離できた。

この結果は既知PIC-H01〜H14に対する契約校正であり、portable Candidateの品質証拠ではない。次はr4 TaskSpecを変更せず、別identityと別依存構造を持つ独立heldoutを凍結し、C147を先に発行する。C147がその未使用setでも14 / 14を通過した場合だけportable Candidateを発行する。

## 計測結果

- valid: 14 / 14
- schema valid: 14 / 14
- Score 4: 14 / 14
- mechanism passed: 14 / 14
- token: min 15,446 / median 15,732 / max 15,977
- elapsed: min 8.881秒 / median 10.834秒 / max 11.861秒

## 成立した境界

- response配列は入力snapshotの再掲ではなく、今回のdeltaだけを返す。
- failed resultの明示scopeは通常actionの既存bindingだけを失効させる。
- authorityまたはallowanceがない唯一のrequired recoveryは`unavailable`へ閉じる。
- bound authorityを持つenvironment recoveryはfailed resultを合法な開始triggerとして受け取り、同時に失効しない。
- denied decoy、scope外operation、すでにterminalのoperationおよび単なるfail-fast後続を追加状態へ誤分類しない。

## 次段のゲート

- 既知14 Caseをportable held-outへ再利用しない。
- 独立heldoutのCase、oracle、response schema、set membershipおよび登録revisionをC147発行前に固定する。
- r4 TaskSpec、C147 bundleおよびportable bundleをheldout結果に応じて変更しない。
- 独立heldoutでC147が14 / 14 Score 4を外した場合、portableを一件も発行しない。
