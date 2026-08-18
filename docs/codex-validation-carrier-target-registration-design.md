# Codex validation carrier実行target登録設計

> [!IMPORTANT]
> **状態**: `target_boundary_fixed / semantic_target_reuse_rejected / repository_target_registered / heldout_r1_source_frozen / rating_created_not_registered / baseline_not_qualified / evaluation_not_started`

## 結論

P002候補のvalidation carrierは、既存`portable-instruction-semantic-conformance`へ新held-outを足しても評価できない。同targetは固定operation ledgerへ一回のJSON応答を返すため、nested command、途中result ingress、program-local判定、same-session continuationおよびterminal一回投影を実行しない。

そのため、実際のCodex tool surface上でcarrier経路と3 KPIを観測する新しいnamespaced repository target `codex-validation-carrier-conformance`を登録する。登録対象repositoryは公開済みの`agent-execution-control-lab`をimmutable commitへ固定し、Case固有fixtureは新target配下へ閉じる。

登録は評価成立、Candidate作成、P002、採用、releaseまたはprojectionを意味しない。descriptorとartifact rootに続いてheldout r1 sourceを固定したが、baseline bundle、Profileおよび評価slotは作成しない。

## 既存targetを再利用しない理由

| target | 観測できるもの | 観測できないもの | 今回の役割 |
| --- | --- | --- | --- |
| `portable-instruction-semantic-conformance` | 一回応答でのoperation、result admission、fail-fast、continuation選択 | 実tool実行、途中model ingress、carrier-local result、実行中session継続 | P001までのportable意味保持の既存証拠。P002 runtime選定には再利用しない |
| `the-caption` Standard14 | 実repository task、品質、token、elapsed、保存trace | validation carrierだけを独立させた未見Case | end-to-end回帰とC147/P001比較 |
| `codex-validation-carrier-conformance` | 固定validation planの実行、途中配送、fail-fast、continuation、terminal projection、3 KPI | 他platform、frontier carrier、一般repository品質 | P002候補の局所runtime target |

同じsemantic Caseのliteralだけを替えても、P002追加2,141 bytesがmodel再入を減らすかは分からない。target kindの違いを無視してquality scoreを横断比較しない。

## target identity

| 項目 | 固定値 |
| --- | --- |
| `target_id` | `codex-validation-carrier-conformance` |
| kind | repository |
| layout | `namespaced` |
| executor | Codex。具体version、model、reasoning、permissionはProfileへbind |
| repository | `https://github.com/Kenn-dclxvi/agent-execution-control-lab.git` |
| commit | `660387978e8831bd3ca361c23800fcea2ca788e5` |
| tree | `c0bd350a4923cc18fd51b319ec18f8b65e389afd` |
| visibility | public |
| third-party reproducible | true |

target commitは評価fixtureのbase identityであり、現在の未commit作業を含めない。新しいCase fixture、oracle、rating、prompt bundleおよびresultは`evaluations/targets/codex-validation-carrier-conformance/`配下へ閉じる。

## Case設計境界

Caseはrepository内容の理解ではなくcarrier経路だけを消費する小さいfixtureにする。

- root直下にCase専用作業directoryをmaterializeし、targetの既存機能へ依存しない。
- actionは決定的な小ファイル変更に限定する。
- validation command、期待exit、marker identity、依存関係および必要evidenceをTaskSpecへ固定する。
- oracle、期待marker、禁止された後続発行およびtrace診断はmodel-invisibleにする。
- validation間のmodel-visible ingress、agent response、nested invocation、continuation identityおよびterminal projectionを保存traceから診断する。
- promptがcommand順を発明しなくても、TaskSpec固定planから任意の合法なcarrier methodを選べるようにする。

runtime held-outは、少なくとも次を別Caseにする。

1. required validationなし。
2. 複数validation全件success。
3. 最初のvalidationがnon-success。
4. 中間validationがnon-successで後続依存validationが未発行。
5. 長時間validationがnonterminalとなりsame identityでterminal化。
6. terminal resultに必要evidenceと不要raw outputが混在。

capability欠落、continuation identity欠落およびrequired evidence field欠落は、比較ProfileのruntimeをCaseごとに変えると互換条件を壊すため、formal KPI Caseへ混ぜない。これらはtarget-specific preflightのnegative fixtureとして固定し、slot発行拒否を検証する。

## ratingと診断の分離

`quality_score`は、required action、全required validation result、fail-fast、必要evidence、正しいterminal stateおよび禁止された後続未発行を採点する。

次は診断情報であり、第4のKPIにしない。

- validation間のmodel-visible response数
- programmatic carrier利用有無
- nested tool call数
- raw output bytes
- continuation call数

品質維持後のall-agent `total_tokens`と`elapsed_seconds`だけをcost方向に使う。

## 新インスタンスgate

評価slotを発行する前に次を順に完了する。

1. target descriptorとartifact rootsの登録。
2. Case、fixture、model-visible TaskSpec、private oracle、schema、ratingおよびset freeze。
3. control-free baseline bundleの固定。
4. 全Caseを小さいNでfixture qualificationし、valid、採点可能、3 KPI取得を確認。
5. target-specific materializer、grader、trace診断およびcapability preflightを固定。
6. control-free qualification resultを同target内へ登録。
7. その後にだけP002 Candidate作成前gateのconcrete held-out identityを充足する。

control-freeのscoreを事前に高くすることはgateではない。model-visible入力から必要結果を導出不能、fixture不成立または採点不能ならCaseをformal比較へ使わない。低品質でもCaseと測定が有効ならresultを保持する。

## 現在許可する次作業

6 runtime Case、3 preflight negative fixture、schema、rating contract、set freeze、target-specific materializer、grader、trace診断、capability preflight、all-agent token accounting contractおよびqualification-only runnerを固定した。control-free N=1は6件すべてvalidで3 KPIを取得し、測定経路をqualificationした。次に許可するのはP002 bundleとcandidate-only gateのProfile・preflight作成であり、P001比較Profile、Standard14投影またはpaired evaluation slotはまだ作らない。

## 参照

- [`評価ターゲットインスタンス`](../evaluations/targets/README.md)
- [`P002候補 Candidate作成前設計`](p002-codex-validation-carrier-candidate-precreation-design.md)
- [`Codex validation carrier能力監査`](codex-validation-carrier-capability-audit.md)
- [`P001後続 Codex validation carrier静的反例監査`](p001-codex-validation-carrier-static-counterexample-audit-r1.md)
