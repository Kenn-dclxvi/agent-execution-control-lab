# Candidate192 Standard14共同発行対象9ケース・F04対照 N=5実行準備監査

> **位置づけ**: Candidate192初回targeted gate実行前監査／C191既存50件を基準へ再利用／C192不足50件承認

## 結論

Candidate192の10ケース各5件は、Candidate191の保存済みatomic runから同じ10ケースだけを選んだreference resultへbindし、comparison preflightが`ready`となった。prompt identity以外の互換条件、固定Layer 1、50 capsule、dispatch planおよびM=24を機械照合した。preflight前に評価slotは発行していない。

## 固定値

- reference result: `4b3fcabe4a004d9a945f6d1bcbdecfdc`
- reference result SHA-256: `ea313bb918f0bd844342195485ba501f47aa2e3e3b960be6e3cb3794fd7de348`
- compatibility key: `58c8563e60f397402b8b6d07f6636273f1836ddc88e0e51ad9df900b8f2719b3`
- Candidate192 pool key: `889fc29433dc0c13a64aef3f724b5ec76ee04ba9de6a4e0dba46784ef58b5a0d`
- evaluation set identity SHA-256: `2096d15e9d5d072e09e92313caa296caf8853c5e86f205d4d9f819b576263c33`
- Candidate192 profile SHA-256: `1e0766e4a9c82e7a30c13acccb9fd02a7985a7b275189505ced3702dc4505398`
- dispatch plan SHA-256: `1ae878f1a69b7b6208c3664f5db15b0addb4461f93a37ad63c34b943448588b8`
- global plan SHA-256: `4fd43ff52617703e50de7f5cc27e86207b87e10cefbeef5375fea2cb1ad7a567`
- preflight receipt SHA-256: `509bcd376164cd2452e16c0a274ed5821cd09e00777dcf116a37c2a767d8b010`
- reference slots: `50`
- authorized Candidate192 slots: `50`
- max workers: `24`

一次artifactは`/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate192-consumer-bound-coissuance-standard14-affected9-f04-n5-20260812-r1`に保存した。固定global planは`atomic-plan/global-plan.json`、comparison preflight正本は`cycle/layer1/comparison-preflight.json`である。

## 停止した準備経路

最初のコピー元に既存comparison receiptが含まれ、write-onceの`comparison-generation.json`と衝突したためslot発行前に停止した。次に14ケースreference resultをそのまま使う経路は、10ケースprofileとのcoverage不一致をpreflightが拒否した。どちらも退避して保持し、条件を緩和しなかった。

C191の登録済みpoolから対象10ケース各5件だけを選び、同じprofile条件の不変reference resultを登録した。そのcoverageへ対応するreceipt未付与Layer 1を作り直してpreflightを通した。

## 入力境界

50 capsuleは既存Standard14 templateのprompt identityとbundle locatorだけをCandidate192へ置換した。case、fixture、TaskSpec、rating、model、reasoning、runtime、permission、executor parameters、token accountingおよびM=24はreferenceと一致する。private oracle、期待terminal、過去findingまたは修正後の正解値をmodel-visible inputへ追加していない。

## 状態

`execution_preparation_passed / comparison_preflight_ready / reference_50_reused / candidate192_authorized_50 / issued_50`

この文書は実行前receiptとして保持する。実行後の品質・機序判定は[`Candidate192 Standard14対象9ケース・F04対照 N=5`](../evaluations/results/candidate192-consumer-bound-coissuance-standard14-targeted-n5_2026-08-12.md)を正本とする。
