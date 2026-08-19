# P006 frontier carrier結果後因果再監査

> [!IMPORTANT]
> **状態**: `causal_reassessment_complete / p006_delta_not_unique_route_closure / observed_route_is_prompt_nonconformance / independent_mechanism_gate_retracted / p007_not_created / p006_n20_eligible_not_started`

## 結論

P006 Standard14 N=5でF08の5 / 5件に残った開始identity後のread分割は、P006がprompt準拠で許した経路ではない。P005から保持した共通`FRONTIER`は、drift時にもreadが禁止されずtargetとpermissionが変わらない場合、identity observationと許可済みobservationを同じfrontierへ入れることをすでに要求している。F08のTaskSpecはdriftまたはdirty stateで編集を禁止するが、readを禁止していない。このため、identity resultを受領してからreadを別responseで発行した5件は、既存条項へのnonconformanceである。

P006で追加した`FRONTIER_CARRIER_CODEX`は、このpermission edgeを初めて閉じた差分ではなかった。共通`FRONTIER`が正しい複数member集合を構成済みであることを前提に、その集合を`Codex dispatch group`へbindすると再記述したが、frontier identityをmodel判断から独立してmaterializeする既存のprogrammatic carrierは固定していない。したがって、P006の追加1,763 bytesと、N=5で観測したcost改善またはA02のresponse減少との因果対応は確立していない。

この結果から同じ禁止、`同じmodel step`、開始gate後readまたはCase固有の順序を追加するP007は作成しない。観測経路は3 KPI差を説明する診断情報として保持し、独立したmechanism gateにはしない。P006は品質100を維持してP005比token `-10.57%`、elapsed `-3.90%`だったため、効率の安定性を確認するN=20へ進める資格はある。ただし本再監査から評価slotは発行しない。

## 固定した目的と一次資料

- 改善系列: C147を機種非依存の共通意味とplatform capabilityへ分離するPortable full-agent系列。
- required effect: 成果品質を保ち、同一条件でall-agent tokenとelapsedを減らす。
- preserved effect: P005のvalidation terminal projection、個別invocation identity、真正dependency、fail-fast、actor provenanceおよび一枚配送。
- 比較基準: P005 result `28082254ecc6447f8d76d63e85062299`、副基準C147 result `f7baeadc5bd44399ac13cc0e0a8aff48`。
- P006 result: `684cb3c380bc4b28a65680f415ecb8e6`。
- prompt差: P005全文をbyte保持し、`FRONTIER_CARRIER_CODEX` 1,763 bytesだけを追加。
- trace範囲: P005とP006の選択済みStandard14 N=5、F08各5件、およびfrontier対象として事前に挙げたA02、F07 canonical、F07 dependency、F10 entrypoint各5件。

評価ケース、fixture、TaskSpec、oracle、Rating v14、model、reasoning、CLI、permission、runner、M=24、token accountingおよび集計は変更していない。

## F08のpermissionとdependency

F08のTaskSpecは次を別々に固定している。

- 最初の編集またはrequired command前にcheckout identityを記録し、clean statusを確認する。
- start-identity gate failureまたはdirty stateなら**編集せず**停止する。
- repository、適用中`AGENTS.md`、指定文書、weekly / monthly entrypointのreadを許可する。
- read-only対象は`src/app/entrypoints/weekly_main.py`、`monthly_main.py`および`src/AGENTS.md`である。

drift resultが変えるのはactionとrequired executionのpermissionまたはstop conditionである。read自体、そのtargetおよびread permissionは変わらない。したがって、readはidentity resultのeffect scope外にある。

P005とP006が共有する`FRONTIER`も、この関係を直接定めている。

1. 開始identity resultは、drift時に禁止されるoperation classだけをeffect scopeへ入れる。
2. drift時にもobservationが禁止されずtargetとpermissionが変わらなければ、identity observationと許可済みobservationを同じfrontierへ入れる。
3. 共同result受領まではactionとrequired executionだけを保留する。
4. observation自体が禁止されるか、targetまたはpermissionが変わる場合だけ後続frontierへ分ける。

よって、F08の分割は「resultを選択や抑止へ使わなければ後続発行してよい」という合法routeではない。identity resultをread開始資格として使い、既存のeffect scopeをreadへ広げたnonconformanceである。

## 保存traceの対応

P006 F08の5件はすべて、第一responseでcheckout identityとclean statusだけを発行した。第一result後のresponseは例外なく「ゲート通過」「両方が成立した場合のみ」「次にreadする」と述べ、対象文書、authorityおよびentrypointを第二responseから発行した。

frontier対象として事前に挙げた5 Caseのmodel response中央値は次のとおりである。

| Case | P005 | P006 | P006の第一responseでidentityと対象readを共同発行 |
| --- | ---: | ---: | ---: |
| `TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING` | 7 | 5 | 1 / 5 |
| `TC-F07-CANONICAL-V4-RUNNER` | 5 | 5 | 1 / 5 |
| `TC-F07-DEPENDENCY-PROVENANCE-PAIR` | 5 | 5 | 0 / 5 |
| `TC-F08-CANONICAL-CLI-REFERENCE-SYNC` | 5 | 5 | 0 / 5 |
| `TC-F10-ENTRYPOINT-INVENTORY-REVIEW` | 5 | 5 | 0 / 5 |

A02ではresponse中央値が減ったが、共同発行は1 / 5件に限られる。F08、F07 dependencyおよびF10 entrypointでは追加blockが意図した第一frontierの共同発行を観測していない。P006全体の11 Caseでmodel responseが240件から224件へ減った事実は維持するが、その減少をfrontier carrierの一貫した適用効果とは扱わない。

## P006差分が閉鎖を追加しなかった理由

P006の追加blockは、`共通FRONTIERが構成してmemberを固定したfrontier identity`を入力前提にしている。しかしP005の共通条項もP006の追加blockも、modelが最初のtool outputを作る前に、そのfrontier identityを別の実行主体またはprogramへmaterializeする経路を持たない。

`VALIDATION_CARRIER_CODEX`では、一つのprogrammatic carrier executionが固定planを受け取り、nested resultをcarrier-localに保持する実在のsurfaceを能力probeで確認していた。これに対し`FRONTIER_CARRIER_CODEX`の`Codex dispatch group`は、通常のmodel outputに複数tool callを置くというmodel挙動へ名前を付けたもので、独立したcarrier executionではない。

プロンプトはoperationのpermissionとdependencyを定められるが、tool resultの配送やmodel outputの不可分性をruntime機能として強制できない。P006は、すでに禁止済みの分割を別labelで再記述したにとどまり、P005から新しく削除したprompt準拠permission edgeを示せない。

静的反例監査の14 classは、追加block単体の自己整合性を確認したが、次を確認していなかった。

- 親P005に同じroute closureがすでに存在し、P006差分がpermissionを追加で狭めていないこと。
- carrier入力であるfrontier identityが、model自身の正しい分類を前提にせずmaterializeされること。
- `Codex dispatch group`が、通常のmodel outputとは別の既存programmatic carrier surfaceであること。

したがって、静的監査の`blocking_counterexamples_0 / candidate_creation_allowed`は作成時点の記録として保持するが、P006差分の一意な機序成立根拠には使わない。

## 判定修正

N=5直後は`frontier_mechanism_gate_failed`を独立状態として記録した。しかし正本の設計原則では、model response、tool waveおよび経路成立率は3 KPI差の診断情報であり、品質再現性との100%対応が確認されない限り独立した合否gateにしない。

F08の分割5件はすべてScore `4`であり、P006全体も70 / 70件がScore `4`だった。機序nonconformanceと品質不成立の100%対応はない。よって現在解釈を次へ修正する。

```text
standard14_n5_completed
quality_gate_passed
p005_cost_both_lower
c147_cost_regression_persists
frontier_nonconformance_observed
p006_delta_causal_attribution_not_established
independent_mechanism_gate_retracted
n20_eligible_not_started
adoption_not_decided
```

登録result、Score、3 KPI、traceおよび当初判定は変更しない。この修正は採用、releaseまたはruntime projectionを意味しない。

## 次のoperation

同じpermission禁止を重ねるP007、成功したC147またはA02のtool順転記、F08固有のcommand・path・read順追加は行わない。P007は`candidate_not_created`とする。

効率を判断する次の測定は、同一Standard14条件でP005とP006をN=20へ拡張する比較である。現在のatomic poolは両armとも各Case 5件を持つため、N=20にはそれぞれ各Case15件、合計210 slotが不足する。Candidate147は保存済みN=20以上を再利用できる。発行前にはP005 resultを直接基準にprompt identity以外を再度preflightし、P005とP006の不足slotを別cycleのまま同じM=24 global queueへ固定する。

本再監査はN=20の設計資格だけを確認する。評価profile、dispatch plan、preflight receiptおよびslotは作成していない。

## 参照

- [`P006 THE-CAPTION投影 Standard14 N=5評価`](../evaluations/results/p006-the-caption-standard14-projection-n5_2026-08-19.md)
- [`P006 Codex frontier carrier作成前設計`](p006-frontier-carrier-codex-precreation-design.md)
- [`P006 Codex frontier carrier静的反例監査 r1`](p006-frontier-carrier-codex-static-counterexample-audit-r1.md)
- [`P005 Standard14 C147移植損失監査`](p005-standard14-c147-transplant-loss-audit.md)
- [`Prompt制御の検討原則`](prompt-control-design-principles.md)
