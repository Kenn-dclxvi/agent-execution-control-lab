# P004 validation carrier prebound contract静的反例監査 r1

> [!IMPORTANT]
> **状態**: `management_draft_audited / general_classes_13 / remaining_blocking_counterexample_0 / primitive_coverage_15_of_15 / dependency_closed / one_sheet_verified / candidate_creation_allowed / candidate_created_after_gate_not_evaluated`
>
> 本書は管理用composition draftのpermissionとdependencyを静的に監査した記録である。model実行、品質、効率改善、Candidate評価、採用、releaseまたはprojectionではない。

## 結論

P004作成前設計の13 classへ管理用r4 draftを適用し、blocking counterexampleは0件だった。

- taskごとのcapability、availability、field mappingおよびprojection contract再判定routeを削除した。
- validation `unavailable`のproducerを実際のcarrier invocation resultへ限定した。
- task固有のterminal evidenceとoutput schemaをimmutable plan identityへ移し、carrier admissionでの再構成を閉じた。
- 個別validation、固定順、局所判定、依存先fail-fast、continuation、中間ingress拒否およびterminal一回投影を保持した。
- C147/P001由来のvalidation primitiveを15 / 15件保持した。

静的renderは12,781 bytes、SHA-256 `82792275a9e120e1e9e794244ca72ef804c1b7f8c9ac39a4ae0c56493aad468a`である。P003の12,864 bytesより83 bytes短いが、bytes差をtokenまたはelapsed改善の証拠にしない。

## 監査対象

- management manifest: [`full-agent-codex-validation-prebound-carrier-draft-r4.composition.json`](../prompts/compositions/c147-portable-kernel-draft-r1/full-agent-codex-validation-prebound-carrier-draft-r4.composition.json)
- composition identity: `c147-portable-kernel-full-agent-codex-validation-prebound-carrier-draft-composition-r4`
- composition SHA-256: `e321845643d24905d46d9bc4b8542908cc272c2cdf783c8cbc0603991ebc841b`
- changed validation component: [`70-validation-plan-projection-r4.md`](../prompts/compositions/c147-portable-kernel-draft-r1/components/70-validation-plan-projection-r4.md)
- changed platform component: [`85-validation-prebound-carrier-codex-r4.md`](../prompts/compositions/c147-portable-kernel-draft-r1/components/85-validation-prebound-carrier-codex-r4.md)
- primitive ledger: [`validation-prebound-carrier-r4-coverage.json`](../prompts/compositions/c147-portable-kernel-draft-r1/validation-prebound-carrier-r4-coverage.json)
- direct source prompt identity: P001 `portable-semantic-c147-portable-full-agent-r1`
- platform capability authority: [`codex-cli-0.146.0-validation-carrier-workspace-write-r1`](../evaluations/targets/codex-validation-carrier-conformance/contracts/codex-cli-0.146.0-validation-carrier-workspace-write-r1.json)
- schema transport authority: [`codex-validation-carrier-supported-subset-r1`](../evaluations/targets/codex-validation-carrier-conformance/contracts/codex-output-schema-transport-r1.json)

P002とP003は、維持する局所効果と再び開かない誤routeを示す反例であり、直接親ではない。

## Class別結果

| Class | 固定状態 | 必要なroute | 閉じる誤route | 結果 |
| --- | --- | --- | --- | --- |
| P4-S01 validationなし | required validation 0件 | carrierを開始しない | 空plan carrierと不要投影 | `no_counterexample_found` |
| P4-S02 全件success | immutable planがready | plan identityを一度渡してterminalを一度受領 | 別admission、field再bind、途中ingress | `no_counterexample_found` |
| P4-S03 途中non-success | 後続がfailure resultへ依存 | failureを保持し依存先だけ未発行 | 後続発行、success補完、再実行 | `no_counterexample_found` |
| P4-S04 nonterminal継続 | continuation identity観測可能 | 同じidentityだけをterminal化 | 別identity、別operation、途中報告 | `no_counterexample_found` |
| P4-S05 continuation欠落 | nonterminalでidentity観測不能 | 当該validationを`unavailable` | identity推測、terminal補完 | `no_counterexample_found` |
| P4-S06 carrier invocation unavailable | 登録済みcarrier invocationが実際に`unavailable` | resultを保持し停止 | 個別model route、shell fallback | `no_counterexample_found` |
| P4-S07 invocation前availability | carrier result未受領 | planを一度発行する | 自己判定による暫定`unavailable`投影 | `no_counterexample_found` |
| P4-S08 platform contract欠落 | capability authorityまたはschema transport bindingなし | compositionを適用・評価しない | task内で部分能力を判定して開始 | `no_counterexample_found` |
| P4-S09 evidence field欠落 | planに必要terminal evidenceまたはschemaがない | plan readinessを成立させない | carrier側補完、事後read、raw output選択 | `no_counterexample_found` |
| P4-S10 raw output過剰 | 必要field以外のraw bytesあり | planのschema対象だけを投影 | raw output全体のresult化 | `no_counterexample_found` |
| P4-S11 carrier後fallback | carrierがterminal | 一度だけ結果消費へ渡す | 個別model routeで同じplanを再開 | `no_counterexample_found` |
| P4-S12 plan再構成 | readyなplan identityを受領済み | identityをそのまま渡す | validation fieldの展開・再分類・再bind | `no_counterexample_found` |
| P4-S13 projection再構成 | evidenceとschemaがplanへbind済み | 固定schemaでterminal投影 | taskごとのprojection contract再作成 | `no_counterexample_found` |

## permissionとdependencyの確認

### platform contract

Codex blockの適用自体を、carrier identityとdocumented result-field mappingが登録済みである状態へ固定した。task内にcapability部分集合やavailabilityを判定するoperationがないため、モデルが判定順を変えてもpre-invocation `unavailable`をprompt準拠で生成できない。

platform contractが欠ける環境では、このCodex blockをcompositionへ含めない。欠落をtask内の条件分岐へ戻さないため、platform非互換はCandidate bindingまたはpreflightで停止する。

### immutable plan

terminal evidenceとoutput schemaをvalidation開始前のplan identityへ移した。plan開始後のfield再分類、再構成、再bindおよび補完を禁止したため、carrier admissionのための二回目のcontract構築を発行できない。

### unavailable result

pre-invocation時点では登録済みcontractを再判定せず、`unavailable`を生成しない。実際のcarrier invocation resultまたはcontinuation identity欠落だけが`unavailable`をbindできる。これによりP003 traceの暫定`unavailable`後に同じplanを開始する二重admissionを閉じる。

### 正常carrier

carrier内部の個別nested invocation、固定順、局所status判定、依存先fail-fast、同一continuation identity、中間ingress denyおよびterminal一回投影を保持した。成功runのcommand文字列、tool順、model step、Case IDまたはexpected resultは追加していない。

## 意味保持

[`validation-prebound-carrier-r4-coverage.json`](../prompts/compositions/c147-portable-kernel-draft-r1/validation-prebound-carrier-r4-coverage.json)は既存validation primitive `VP1`〜`VP6`と`VC1`〜`VC9`を15 / 15件対応付ける。

- `VP1`〜`VP3`はr4 planの先頭三文、`VP4`〜`VP6`は既存の途中success、failure dependency、terminal条件へ保持した。
- 新しい第四文はplan再構成を閉じるallowed deltaであり、既存primitiveの代替数には数えない。
- `VC1`〜`VC3`、`VC5`、`VC7`〜`VC9`は変更していない`validation-result-closure-r2`へ保持した。
- `VC4`と`VC6`はr4 carrierの個別nested invocationとterminal一回投影へ保持した。

## 一枚化の検証

管理用r4 draftは`compose_prompt.py render`と`check`を通過し、`dependency_closure=verified`、`bytes=12781`、`output_sha256=82792275a9e120e1e9e794244ca72ef804c1b7f8c9ac39a4ae0c56493aad468a`を確認した。

## Candidate作成許可

13 classでblocking counterexample 0件、validation primitive 15 / 15件、dependency closureおよび一枚化を確認した。次に許可する作業は、管理用r4とbyte一致するP004 Candidate composition、自己完結した一枚のCandidate bundle、target固有bindingおよび索引登録に限定する。

Profile、dispatch planまたは評価slotは、P004 bundle identityとplatform contract bindingを別gateで固定するまで作成しない。

後続で、監査済みrenderとbyte一致するP004 Candidate bundleおよびtarget固有bindingを作成した。これは本監査の作成許可を消費した後続状態であり、VCC6評価通過または効率改善を意味しない。
