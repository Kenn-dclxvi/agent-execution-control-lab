# P001 Standard14 N=5 機能block別cost診断

> [!IMPORTANT]
> **状態**: `diagnostic_complete / validation_carrier_primary / frontier_carrier_secondary / p001_immutable / candidate_not_created / new_evaluation_not_started`

## 結論

P001のStandard14 N=5で増えたcostは、portable本文全体の長さや機能の詰め込みではなく、主に`validation`の実行結果をmodelへ返す境界がC147から変わったことで生じている。次に分離する対象は、validationの意味ではなく、複数の個別検証を固定順・fail-fastで一つの判断から実行し、完了結果を一度だけmodelへ返す**validation carrier**である。

二番目は`frontier`である。互いに独立したreadやidentity確認を同じ判断から発行し、共同resultが揃うまでmodelへ途中結果を戻さない**frontier carrier**を、意味規則から分ける。

したがって、次の作業はP001全体の短縮やcompact化ではない。共通semantic kernelとplatform capabilityを次のように分け、まずvalidation carrierだけを再設計する。

- 共通semantic kernel: operation、actor、observation admission、dependency frontier、validation readiness、固定順、個別pass condition、fail-fast、completion、method、recoveryの意味
- platform capability: 複数tool invocationを一つのmodel判断から発行できるか、途中result ingressを抑止できるか、nonterminal invocationを同じidentityで継続できるか、multi-actor provenanceを取得できるか
- 配送形: platformごとに必要なcapability blockを選び、最終的には自己完結した一枚の`AGENTS.md`へrenderする

P001正本と評価済み投影bundleは変更しない。本診断からCandidateや追加評価slotも発行しない。

後続のinterface設計では、validation semanticsとplatform carrierを別blockへ分け、carrier能力を持たないplatformで個別resultをmodelへ返すloopを代替正常経路にしない境界を固定した。詳細は[`P001 validation carrier platform分離設計`](p001-validation-carrier-platform-separation-design.md)を正とする。

## 固定した比較

- P001 result: `e8bb0207c8014e5bac8d79ec2cf74bf4`
- C147 reference result: `f7baeadc5bd44399ac13cc0e0a8aff48`
- 互換key: `cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561`
- 比較対象: Standard14、14 Case、各N=5、両方とも70 / 70 Score `4`
- P001対C147: token `+113.73%`、elapsed `+17.04%`

prompt bytesはC147の10,772 bytesに対してP001は10,781 bytesで、差は9 bytesだけである。静的prompt長だけでは、tokenが約2.14倍になった結果を説明できない。

## model再入場の観測

C147 N=5 archiveに同じraw traceが存在する11 Caseでは、P001のCase別model response中央値は次のように変わった。

| Case | C147 | P001 | 増分 | token中央値差 |
| --- | ---: | ---: | ---: | ---: |
| A01 | 1 | 2 | +1 | +16,271 |
| A02 | 4 | 7 | +3 | +311,750 |
| F04 | 5 | 8 | +3 | +192,383 |
| F05 clarify | 2 | 2 | 0 | -873 |
| F05 out-of-scope | 2 | 2 | 0 | +1,734 |
| F06 | 5 | 6 | +1 | +107,145 |
| F07 canonical | 4 | 7 | +3 | +155,824 |
| F07 dependency | 4 | 5 | +1 | +52,084 |
| F08 | 4 | 5 | +1 | +221,933 |
| F10 inventory | 4 | 5 | +1 | +56,764 |
| F10 monthly | 4 | 4 | 0 | -597 |

この11 Caseで、追加model response数とtoken中央値差のPearson相関は0.804だった。これは因果KPIではなく、経路診断である。ただし、model responseが増えないF05の2経路とF10 monthlyではtokenもほぼ横ばいであり、P001本文を常に読む固定costが主因という説明とは整合しない。

A02、F01、F02、F03、F04、F07 canonical、F08のaction前後を分けると、P001 35 runの平均はaction前3.06回、action後4.11回だった。同じC147 identityの互換runを診断用に参照した168 runでは、action前2.25回、action後2.02回だった。response超過の約72%はaction後にある。これはtoken配賦率ではないが、主因をvalidation側へ置く根拠になる。

## block別判定

### 1. validation: 主因

P001は、個別validationを一つの発行判断から固定順で実行し、各resultを個別判定して最初のnon-successで停止し、完了結果を一度だけ返す意味を保持している。一方で、C147が持っていた「一つのcustom exec wrapper内で個別`exec_command`を実行し、command間でmodelへ戻らない」というCodex向けの具体的carrierを一般化した。

traceでは、focused test、full test、`npm` validationなどの各結果が途中でmodelへ返り、そのたびに次commandを新しい判断で発行している。tool数やcommand output量が大幅に増えなくても、蓄積済みinputを次のresponseが再消費するためtokenが増える。F08ではmodel responseが1回増え、cached input中央値が216,576増え、token中央値差は221,933になった。

これはvalidationの意味不足ではなく、意味をplatform上で効率よく運ぶcarrier bindingの消失である。

### 2. frontier: 副因

P001は、開始identityとその結果に依存しない許可済みreadを同じfrontierへ置く意味を持つ。しかしtraceでは、identity結果を一度modelへ返してからauthority、source、testを読む経路がある。

C147は、既知で相互非依存なinvocationを同じmodel stepから発行する具体的な発行境界を持っていた。P001では意味規則は残ったが、model-visibleなcarrierが弱くなり、action前にも平均0.81回のresponse超過が生じた。

### 3. core、actor、observation、execution: 今回の主因ではない

- `core`: F05 clarify、F05 out-of-scope、F10 monthlyのresponse数は変わらず、tokenもほぼ横ばいである。A01はidentity readがC147の2 / 5からP001の3 / 5へ変わった中央値の反転であり、core全般の固定costとは判定しない。
- `actor`: P001 70 runの`collab_tool_call`はF02の`wait` 1件だけで、worker spawnの増加はない。
- `observation`: tool数とoutput量だけでは増加を説明できない。問題は何を読んだかより、途中resultがどこでmodelへ戻ったかにある。
- `execution`: excluded attempt、retry、controller errorはなく、recoveryの増加は観測していない。

## F01、F02、F03のtrace範囲

C147 N=5 archiveには、別campaignからatomic reuseされたF01、F02、F03のraw traceが重複保存されていない。この3 Caseだけは、同じC147 prompt identityと互換条件を持つiteration 6〜29をresponse経路の診断に使用した。正式なN=5 KPI比較や中央値の置換には使用していない。

診断上、P001のmodel response中央値はF01が7、F02とF03が8で、C147互換runはいずれも4だった。command数はP001の方が同等以下であり、増えたのはtool作業量よりmodelへの途中result ingressである。

## 次に固定する設計境界

次案を作る前に、次のpermissionまたはdependency境界を固定する。

1. validation carrierは、個別validation identity、固定順、個別pass condition、fail-fastを保持したまま、途中resultをmodelへ返さず、carrier terminal後にresult集合を一度だけ返す。
2. platformがこのcarrierを提供しない場合、順序や自己判定を追加して代替しない。capabilityを`unavailable`として、そのplatform構成から除外するか、別の合法なcarrierを明示する。
3. validation carrierの境界が固定された後にだけ、frontier carrierを別差分として扱う。同じCandidateへ二つの原因差分を混ぜない。
4. 既知のStandard14は診断・回帰確認用であり、次案の採用証拠にはしない。Candidate本文を固定する前に、未使用の評価境界とstop conditionを別途固定する。

この順序なら、portableの意味を完成させながら、platform固有部分だけを交換可能な機能blockとして保てる。agent向けfull setは必要なcapability blockをすべて組み合わせ、chat向け構成は提供できないcarrierを含めず、どちらも最終配送時には一枚の`AGENTS.md`へ転写する。
