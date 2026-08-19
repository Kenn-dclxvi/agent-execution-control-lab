# P005 Standard14 C147移植損失監査

> [!IMPORTANT]
> **状態**: `diagnostic_complete / validation_carrier_substantially_restored / frontier_carrier_not_transplanted / c147_direct_efficiency_route_not_preserved / f04_not_primary / candidate_not_created / new_evaluation_not_started`

## 結論

P005がP001比でtokenを36.30%減らしてもCandidate147比でtoken `+36.14%`、elapsed `+18.48%`を残した主な移植損失は、validation carrierではなく、action前のfrontier carrierである。

P005はP001で失われたvalidation resultの途中配送境界を大幅に回復した。一方、C147が`decision_boundary=false`の相互非依存invocationを`同一model step`から発行していたplatform上の境界を、P005は共通`FRONTIER`の意味へ一般化しただけで、Codex向けcapability blockへ分離していない。そのため、frontierの一部resultをmodelへ返した後でも、そのresultを次の選択や抑止へ「使っていない」と解釈すれば残りを別model responseから発行できるrouteが残る。

次のprompt改善境界は、共通`FRONTIER`へ条件や手順を追加することではない。P005のvalidation blockと同じ分離原則で、`frontier全対象の発行完了前の個別result -> model-visible consumer`を閉じるCodex向けfrontier carrierを一つのplatform capabilityとして設計する。P005正本、評価済み投影bundle、Standard14、rating、runnerおよび保存resultは変更しない。本監査からP006または新しい評価slotは作成しない。

## 固定した比較

- Candidate147 result: `f7baeadc5bd44399ac13cc0e0a8aff48`
- P001 result: `e8bb0207c8014e5bac8d79ec2cf74bf4`
- P005 result: `28082254ecc6447f8d76d63e85062299`
- compatibility key: `cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561`
- 条件: Standard14 14 Case × N=5、Rating v14、`gpt-5.6-sol / medium`、CLI `0.146.0`、M=24、all-agent token accounting v1
- 正式KPI: quality、token、elapsedは登録済み三resultを正とする
- trace診断: model response、tool wave、action前後およびproducer起動は原因切り分けだけに使い、勝敗または採用判定へ使わない

C147の選択済みN=5 archiveには、別campaignからatomic reuseされたF01、F02、F03のraw traceが重複保存されていない。このため三者の同一選択trace再集計は、raw traceが揃う11 Case、各arm 55 runへ限定した。欠けた3 Caseを別runで正式中央値へ補完していない。

## 11 Caseの発行経路再集計

`codex-events.jsonl`から、利用者向け記述を含む各model response、model response間で連続して開始されたtool invocation群、最初のfile changeより前後のtool waveを同じ方法で数えた。

| arm | run | token合計 | elapsed合計 | model response | tool | tool wave | action前wave | action後wave |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| C147 | 55 | 5,203,193 | 3,122.117秒 | 203 | 433 | 148 | 116 | 32 |
| P001 | 55 | 10,640,779 | 3,563.417秒 | 265 | 421 | 208 | 133 | 75 |
| P005 | 55 | 6,699,743 | 3,620.974秒 | 240 | 463 | 180 | 139 | 41 |

P001からP005へのaction後waveは`75 -> 41`となった。P001がC147より増やした43 waveのうち34 wave、79.1%をP005が回収している。これはP005がvalidation carrier内へ個別validationを収容し、途中resultを外側modelへ返さない効果と整合する。

一方、action前waveは`C147 116 / P001 133 / P005 139`である。P005はC147より23 wave多く、P001からも6 wave増えた。validation blockだけをP001から置換したP005でこの差が残ったため、未回収costをvalidation carrierの再修正へ戻さない。

## C147から失われた境界

C147の`DECISION_BOUNDARY`は、受領resultでtarget、permission、methodまたはstop conditionが変わらない既知の相互非依存invocationを、分割せず`同一model step`から発行すると定めていた。

P005の共通`FRONTIER`は、effect scope外のoperation集合を構成し、途中resultを次の選択または抑止へ使う前に全対象を開始すると定める。これはportableな意味としては対応しているが、次のplatform surfaceを閉じていない。

```text
frontier member Aを開始
  -> A resultをmodel-visible consumerへ返す
  -> A resultを選択・抑止へ使わなかったと自己分類
  -> 同じfrontierのmember Bを別model responseから開始
```

このrouteでは、A resultからBのtarget、permission、methodまたはstop conditionを変えていないため、P005の意味条件に従っていると解釈できる。しかしresult ingressのたびにmodel responseと蓄積inputの再消費が増える。P005には`VALIDATION_CARRIER_CODEX`がある一方、frontier result ingressを所有する対応platform blockがない。

これはC147のtool順を新しい実行手順へ転記する提案ではない。閉じる対象は、frontier全対象の発行完了前に個別resultをmodel-visible consumerへ渡せるpermission edgeである。

既存の[`Candidate147 runtime固有表面形監査`](c147-runtime-surface-portability-audit.md)は、C147の対象15 runすべてで開始identityと許可済みreadを最初の発行対象へcommitしたことを確認している。同じ固定CLIで今回再監査したF08もC147の5 / 5件が開始identityと必要readを最初のmodel responseから発行している。したがって現在runtimeに合法routeがないのではなく、P005のplatform構成がそのrouteをfrontier resultの唯一のcarrierへbindしていない。これは新しいruntime機能の要求ではない。

## Case対照

### F08: 最も明瞭な移植損失

F08はP005の5 / 5 runすべてが、action前3 wave、全4 wave、model response 5件だった。C147は5件すべてaction前2 waveで、4 / 5件が全3 wave、model response 4件だった。C147は開始identity、許可済みinstruction、対象文書および現行entrypointを最初のmodel responseから発行した。P005は開始identity resultをmodelへ返してから、対象readを別model responseから発行した。

F08のP005対C147はtoken `+6.1%`に対してelapsed `+40.4%`である。N=5から一waveの時間を固定値へ一般化しないが、token量だけでは説明しにくいelapsed差と、毎回一つ増えたaction前frontierが同時に観測された代表例である。

### F07 dependencyとF07 canonical: 同じaction前差

F07 dependencyはP005の5 / 5件がaction前3 wave、C147は4 / 5件がaction前2 waveだった。F07 canonicalもP005の4 / 5件でC147よりaction前waveが一つ多い。開始identityと、結果によって対象・permissionが変わらないtarget readを別responseへ分けるrouteが中心である。

P005対C147のelapsedはF07 dependencyが`+0.7%`、F07 canonicalが`+22.4%`であり、wave増加だけからelapsed量を因果推定できない。しかし、同じfrontier closureを同じroute shapeで移植できていないことはKPI差と独立に確認できる。

### A02とF10 entrypoint: 一部result後の追加read

A02ではC147の3 / 5件がaction前2 waveだったのに対し、P005は全件3 wave以上、3 / 5件が4 waveだった。開始identity後にrepository authorityを読み、さらに同じrouting判断の実体確認を別responseへ分けた。

F10 entrypointはP005の5 / 5件がaction前4 waveだった。C147の中央値は3 waveである。TaskSpec上の開始gate後、authorityとentrypoint実体を同一の未解決判断へ使うにもかかわらず、authority resultと各fileのreadを別responseへ分けた。

### F04: 今回の主対象ではない

F04のaction前wave中央値はC147とP005の双方が3で、frontier移植損失の代表ではない。P005のaction後wave中央値は2、C147は1だったが、P005では次が混在した。

- source静的確認のlocator不足または引用エラーによる別waveの再確認: 3 / 5件
- `owner=independent source check`を独立producer要求へ誤昇格したrun: 1 / 5件
- 最初の変更を再修正したrun: 1 / 5件

これらはF04のelapsed `+36.4%`へ影響するが、一つのP005準拠permission edgeへまとめられない。独立producer起動は既存`MULTI_ACTOR`に反するnonconformanceであり、同じ禁止を重ねない。静的確認のmethod失敗とrecoveryもN=5の局所分布からfrontier carrier設計へ混ぜない。

## 過去の失敗を再利用しない境界

Candidate253からCandidate258までは、C147の`同一model step`を自然語で戻し、相互非依存readや部分readのdependencyを閉じようとした。Candidate258でもF04の途中result依存が1 / 5件残り、token中央値はC147比`+23.34%`だった。

したがって、次案で共通`FRONTIER`へ「同じstep」「まとめて」「部分read禁止」などの条件を追加しない。成功runのcommand、read範囲または判断順も転記しない。validation carrierで成立した分離と同じく、共通意味はP005のまま保持し、platform上のresult ingress permissionだけをplatform capabilityへ移す。

## 次の設計前gate

次に検討する対象を仮に`FRONTIER_CARRIER_CODEX`と呼ぶ。ただし、次の全項目を一次資料と既存traceから固定するまでCandidateを作成しない。

1. **入力owner**: 共通`FRONTIER`が、全memberのoperation identity、actor、target、permission、method未固定時の選択範囲およびeffect scope非該当を一つのimmutableなfrontier identityへ固定する。
2. **単一admission**: Codex blockはfrontier identityだけを一回受け取り、memberごとの再分類、capability自己判定または再bindを行わない。
3. **途中ingress deny**: 全memberが開始される前は、個別result、progressまたは部分観測をmodel-visible consumerへ渡せない。
4. **identity保持**: memberを一つのshell compound commandへ潰さず、各invocationとresultのidentityおよびexit状態を保持する。
5. **正常な非frontier経路**: 先行resultでtarget、permission、methodまたはstop conditionが変わり得るoperation、実際のmissing・unreadable・矛盾後の追加observation、明示的にreadも禁止する開始gateをcarrierへ入れない。
6. **platform能力**: 現在の固定Agent/runtime/CLIで上記を提供できる既存surfaceを証拠化する。executor、runner、tool adapterまたはruntimeの変更を解決案にしない。
7. **停止条件**: validation carrier、actor、observation、method、recoveryおよびP005 terminal projectionへ同時差分を加えない。合法carrierを固定できなければ`candidate_not_created`とする。

評価時もStandard14、fixture、TaskSpec、oracle、rating、model、runtime、runner、permission、accountingおよび集計を変更せず、prompt identityだけを変数にする。既知Caseごとのcommandまたはcontentを新しいpromptへ持ち込まない。

## 参照

- [`P005 THE-CAPTION投影 Standard14 N=5評価`](../evaluations/results/p005-the-caption-standard14-projection-n5_2026-08-19.md)
- [`P001 Standard14 N=5 機能block別cost診断`](p001-standard14-n5-functional-block-cost-diagnostic.md)
- [`P001 validation carrier platform分離設計`](p001-validation-carrier-platform-separation-design.md)
- [`Candidate253とC147のF04使用token差監査`](candidate253-c147-f04-token-step-causal-audit.md)
- [`Candidate258 途中result dependency除外`](candidate258-partial-result-continuation-dependency-exclusion-design.md)
- [`C147 portable kernel clause architecture`](c147-portable-kernel-clause-architecture.md)
- [`Candidate147 runtime固有表面形監査`](c147-runtime-surface-portability-audit.md)
