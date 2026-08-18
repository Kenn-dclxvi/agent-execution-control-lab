# P001後続 Codex validation carrier composition draft r2

> [!IMPORTANT]
> **状態**: `management_draft_rendered / semantic_platform_split / static_counterexample_repaired / dependency_closed / primitive_coverage_15_of_15 / one_sheet_verified / candidate_not_created / evaluation_not_started`

## 結論

P001のcost診断で切り出したvalidation blockを、共通意味二つとCodex能力一つへ分離し、自己完結した一枚の`AGENTS.md`へ再構成できる管理用draftを作成した。

- 共通: `validation-plan-semantics-r2`
- 共通: `validation-result-closure-r2`
- Codex固有: `validation-carrier-codex-r2`

manifestは[`full-agent-codex-validation-carrier-draft-r2.composition.json`](../prompts/compositions/c147-portable-kernel-draft-r1/full-agent-codex-validation-carrier-draft-r2.composition.json)である。後続の作成前設計に従い、直接のsource prompt identityはP001 `portable-semantic-c147-portable-full-agent-r1`へbindする。C147は比較参照として分離する。後続の[`静的反例監査`](p001-codex-validation-carrier-static-counterexample-audit-r1.md)でadmission境界3件を修正した現在のrender結果は12,922 bytes、SHA-256 `999d409cd90b83408739d0140ddb5dc4e052f5af40bc603834553df5a6a0ad0b`となり、manifestの依存閉包と期待SHAに一致する。

これはP002、prompt Candidate、評価入力またはreleaseではない。`model_visible=false / evaluation_eligible=false / bundle_binding_eligible=false / output_prompt_identity=null`を維持する。

## 分離した責任

| component | 所有するもの | 所有しないもの |
| --- | --- | --- |
| `validation-plan-semantics-r2` | required validation、順序、個別pass condition、stop dependency、plan terminal条件 | tool名、carrier API、model step |
| `validation-result-closure-r2` | readiness、個別terminal result binding、完了判断、scope closure | 実行surface、途中resultの配送手段 |
| `validation-carrier-codex-r2` | 一つのcarrier identity、個別nested invocation、途中ingress deny、fail-fast、同一continuation identity、terminal一回投影 | validationの追加選択、pass conditionの事後作成、他platformへの一般化 |

Codex固有blockは、成功traceのtool順を推奨手順に転記したものではない。nonterminal planからmodel-visible consumerへ途中resultを渡すpermissionを閉じ、carrier内で許可する操作を固定済みplanの個別実行、判定、同一identity継続およびterminal投影へ限定する。

## 意味保持

既存r1のvalidation primitive 15件は[`validation-carrier-r2-coverage.json`](../prompts/compositions/c147-portable-kernel-draft-r1/validation-carrier-r2-coverage.json)で15 / 15を対応づけた。

- `VP1`〜`VP6`は共通plan semanticsへ保持した。
- `VC1`〜`VC3`、`VC5`、`VC7`〜`VC9`は共通result closureへ保持した。
- 実行順とterminal一回投影に関係する`VC4`と`VC6`は、共通意味を消さずCodex carrier上の到達方法へbindした。
- platform capability文はC147 primitiveを増やしたものとして数えない。

carrierが持たないplatformへCodex blockを入れない。required validationを扱う構成では、同等の7能力を確認したplatform blockを別に用意するか、validation operationを`unavailable`へ閉じる。

## 一枚化の確認

次の管理用renderとcheckが成功した。

```bash
.venv/bin/python scripts/compose_prompt.py render \
  --manifest prompts/compositions/c147-portable-kernel-draft-r1/full-agent-codex-validation-carrier-draft-r2.composition.json \
  --output /tmp/c147-portable-full-agent-codex-validation-carrier-r2-AGENTS.md

.venv/bin/python scripts/compose_prompt.py check \
  --manifest prompts/compositions/c147-portable-kernel-draft-r1/full-agent-codex-validation-carrier-draft-r2.composition.json \
  --against /tmp/c147-portable-full-agent-codex-validation-carrier-r2-AGENTS.md
```

Agentへ三つのcomponent fileを読ませる運用にはしない。Candidate作成前gateを通過した場合も、配送対象は新しいprompt identityへbindした一枚の`AGENTS.md`だけにする。

## 次の判断境界

この一差分の静的反例監査は、初回blocking edge 3件を修正し、9 Caseで残存0件まで完了した。後続の[`P002候補 Candidate作成前設計`](p002-codex-validation-carrier-candidate-precreation-design.md)で直接の親、比較基準、一差分、評価class、KPIおよび停止条件を固定したが、concrete held-out identityが未作成なのでCandidateはまだ作らない。

1. r2の直接の基準、P001の診断証拠としての役割、C147から保持する意味とr2だけの差分を固定する。
2. 静的監査に使った9 Caseと、本文固定後に作る新しい未見Caseを分離する。
3. 品質、途中result ingress、model response数、tokenおよびelapsedを別gateにする。
4. Candidate作成前gateを満たした後だけ、新しいprompt identityとtargeted評価設計を別アーティファクトとして検討する。

P002、Profile、dispatch plan、Standard14またはportable評価はまだ作成・実行しない。
