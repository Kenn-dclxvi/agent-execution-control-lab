# Candidate223 ADR9 r4 N=5 実行準備監査

## 結論

`ready / authorized_45 / issued_0`

Candidate223はTaskSpec r13とcase r4を使う新規development evaluationであり、保存済みr2 resultとの品質比較は行わない。固定fixtureの意味、oracle、期待terminal、rating、model、runtime、permissionおよびexecutor条件をr2から維持し、変更した評価入力はsource外のrequired scope別exact carrierだけである。

## identity

- Candidate: `the-caption-3ce91a4-review-scope-exact-carrier-r1`
- bundle SHA-256: `85473ee6fc8d50c1e9946b2fb4d328fae68a260ade5380e9c32501ed2fbd9320`
- profile: `candidate223-review-scope-exact-carrier-adr9-r4-medium-m24-n5-cli0146-r1`
- profile SHA-256: `aed239bd13d1dbb2426ff78c7c218605149f9524c442c8b3de15bae4ffd05af8`
- Evaluation set: `the-caption-preimplementation-adversarial-design-review-r4`
- Layer 1 identity: `bc5ee573b2e14f6c45f561fe0035ee5c4f0d70a7e8d46ac957e5cf66c4a32f7b`
- frozen set SHA-256: `dffcdeea84016e43ac1fb8cb273b52bfb08931ba27fb5532ba64aef138bd2438`
- coverage SHA-256: `7449c74d6882edad3a1f5e4c45f91fe16b122299bcb91067ce159c9f118923a6`
- global plan SHA-256: `8b7f9e9cb38bc871c7f91f92149203d422a41ffaf24bd5c5dfab2c4985da3839`
- execution root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate223-review-scope-exact-carrier-adr9-r4-n5-20260814-r1`

9ケースのseed patchを固定target commitからmaterializeし、宣言commitと9 / 9件一致した。global planは9ケース各5件、合計45 capsuleで、全capsuleのprompt identity、bundle SHAおよびTaskSpec r13 bindingを照合した。発行済みslotは0件である。

目的は試験成功ではなく、必要reviewがscope外readとroot mixed-owner deliveryなしで完遂されるかを観察することである。一件でも誤配送、scope外read、必要review欠落、必要値欠落、root補完またはresult effect不一致があれば有効runを保持して停止する。
