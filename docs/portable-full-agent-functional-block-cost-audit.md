# Portable full-agent機能block cost監査

> [!IMPORTANT]
> **状態**: `static_cost_partitioned / total_bytes_10781 / primitives_81_bound / tuning_q01_q08_bound / removable_blocks_0 / compact_candidate_not_created / new_evaluation_not_started`

> [!NOTE]
> この静的cost分割は履歴診断として有効だが、後続のC147 reference先行資格確認でsemantic held-out r1が不適格となったため、compact化は停止している。portable同等性を資格確認するまで、本書の統合候補からCandidateを作成しない。

> [!NOTE]
> 後続のP001 Standard14 N=5では、静的byte比率ではなくmodelへの途中result ingressを使ってcostを再分割した。主因をvalidation carrier、副因をfrontier carrierへ限定した現行診断は[`p001-standard14-n5-functional-block-cost-diagnostic.md`](p001-standard14-n5-functional-block-cost-diagnostic.md)を正とする。

## 結論

portable full-agent一枚の固定instruction costは一つの巨大条項ではなく、core、actor、observation、frontier、validationおよびexecutionへ分散している。最大のcoreでも20.6%であり、最大blockを一つ削れば解決する構造ではない。

全blockがC147由来primitiveまたはQ01〜Q08の正常経路を消費するため、削除可能なblockは0件と判定する。次に調べるのは機能削除ではなく、block間で重複するresult admission、terminal closure、method bindingおよび「全result受領後に一度だけ次を判断する」表現を、意味と発行形を変えずに共有境界へ統合できるかである。

## 静的cost

| 機能block | components | bytes | 構成比 | 対応primitive | tuning Case |
| --- | --- | ---: | ---: | ---: | --- |
| core | header、vocabulary、outcome、completion | 2,221 | 20.6% | 12 | Q01、Q03、Q04、Q06、Q07 |
| actor | actor-core、actor-input、multi-actor | 2,097 | 19.5% | 19 | Q04 |
| observation | observation | 2,120 | 19.7% | 15 | Q02 |
| frontier | frontier | 1,393 | 12.9% | 11 | Q03、Q05 |
| validation | validation-plan、validation-execution | 1,919 | 17.8% | 15 | Q06、Q07 |
| execution | method-recovery | 1,031 | 9.6% | 9 | Q01、Q08 |
| 合計 | 12 components | 10,781 | 100% | 81 | Q01〜Q08 |

このbyte比率は効率KPIではない。正式N=1で観測したcontrol-freeとの対応token差は全14 Caseで+2,305〜+2,811、中央値+2,565だったが、その差を各blockへtoken単位で配賦する観測はない。byte比率をtoken寄与率または削除優先度へ読み替えない。

## 統合候補となる境界

### actor result admission

`actor-core`はoperation、actor、inputおよびresult kindの一般対応を持ち、`multi-actor`は事前identity、開始identity、送信元を加えた対応を再記述する。一般対応を一箇所に保ち、multi-actorが追加provenanceだけを供給できるかを調べる価値がある。ただしQ04の異actor result拒否とcoordinator非代行を弱める統合は棄却する。

### observationとvalidation plan

依存台帳上、`observation`は`validation.plan`を要求し、`validation-plan`は`observation.admission`を要求する。両方を削れない循環であり、変更前observationを再開しないhandoffと、method未固定だけでobservationを追加しない境界を共通化できるかを調べる。Q02の必要observation開始とQ06のfail-fastを同じ発行手順へ縮退させない。

### frontierとvalidation result consumption

`frontier`と`validation-plan`は、途中resultを次判断へ使わず全result受領後に一度だけ判断する境界を持つ。一方、frontierは独立operationの共同開始、validationは固定順と最初のnon-success後の停止であり、発行形は異なる。共有できるのはresult consumptionの不変条件だけで、同時発行または順次実行のmethodを統合しない。

### terminalとcapability欠落

`completion`の欠落result非補完に加え、multi-actor、frontier、validation-planおよびmethod-recoveryが各domainの能力欠落を`unavailable`へ閉じる。共通terminal原則へ寄せられる記述と、各permission edgeの近くに残す必要がある正のclosureを分ける。局所再記述を文字列重複だけで削除しない。

## 次の作業

1. 上の四境界ごとに、現行statement、供給capability、消費component、Q01〜Q08の正常経路および禁止経路を一対一で並べる。
2. 各境界について、意味を変えない共有statement案と、局所に残すdomain固有statementを作る。
3. 81 primitiveの重複0・欠落0、component dependency closure、Q01〜Q08静的反例0を満たす場合だけ、管理用compact draftをrenderする。
4. compact draftのbyte減少だけではCandidateを作らない。新しいCandidate作成前gateと、本文固定後の別held-out revisionを先に固定する。

この監査ではprompt本文、既存Candidate bundle、Profile、case、oracle、ratingまたはresultを変更しない。C147 reference、N=5、N=20、採用、releaseおよびprojectionも発行しない。
