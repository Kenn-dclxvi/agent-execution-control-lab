# Candidate210 review証拠状態閉包 設計

## 結論

Candidate210はCandidate207を直接基盤とし、Candidate208で追加した`TERMINAL / CONTEXT / EVIDENCE_GATE`の責務を、結果種別から必要証拠を逆算する構造ではなく、TaskSpec-fixed manifest descriptorごとの供給経路と観測状態からreview resultを一意に閉じる構造へ再構成する。

Candidate208の三resultの証拠要件、packet提供済みfactの再読抑止、および真正な反例成立後にcertificate外consumerを閉じる効果は保持する。一方、`review_required_evidence(kind)`、`未解決result kind`、`requested resultがその未解決resultをbind可能`および`同じfactとprovenance`という動的判断は継承しない。Candidate209の`certificate_deficit`と排他的依存も継承しない。

新しいreview順序、model-step barrier、result kind別operation、rootによるreview意味判定、case固有分岐またはmanifest固有例外は追加しない。作成前状態は`creation_gate_fixed / candidate_not_created / evaluation_not_started`とする。

## 1. 基準promptと評価状態

- 直接基盤: `the-caption-3ce91a4-c147-review-boundary-recomposition-r1`（Candidate207）
- Candidate207基準result: ADR9 r2 N=5、45 / 45 valid、45 / 45 Score 4、packet反例成立後read 12 / 20件、`quality_passed / mechanism_failed / stopped`
- Candidate208反証: ADR9 r2累積N=50、450 / 450 valid、Score 4は449件、Score 1は1件、packet反例成立後read 10 / 199件、root preread 3 / 300件、reviewer closed-source read 20件、`quality_failed / mechanism_failed / stopped`
- Candidate209反証: ADR9 r2 N=5、45 / 45 valid、Score 4は42件、Score 1は3件。Score 1はすべて`TC-ADR07`の必要direct observation省略、機序不通過は7件、`quality_failed / mechanism_failed / stopped`
- 今回の再構成対象: review inputの供給経路、repository observationのconsumer、三terminal resultの証拠状態を一つの閉包へ接続する境界
- 非対象: review適用、producer identity、packetの禁止入力、root result admission、局所result effect、共同発行、validationおよび評価基盤

Candidate208とCandidate209は失敗系譜の反証であり、その全文を次Candidateの親へしない。Candidate207を直接実装基盤とし、保存traceで有効だった責務だけを再構成する。

## 2. 基準状態で保持する最短正常経路

TaskSpecがartifact変更前の独立reviewを要求した場合、review packetにmanifest observation identityへ明示的にbindされたmodel-visible valueとprovenanceがあれば、そのdescriptorはpacket供給済みとしてreviewerが判定に使用する。同じdescriptorをrepositoryから再取得しない。

packet供給済みまたは許可済みdirect observationの値だけで、具体的instance、固定designとの直接矛盾およびdesignを変えるeffectを含む反例が成立すれば、reviewerは`counterexample_found`をterminal resultとして返す。反例が成立せず、packet供給済みdescriptorとdirect observationを合わせて全manifest descriptorがsuccessなら`no_counterexample_found`を返す。反例が成立せず、未観測のdirect descriptorも残らず、少なくとも一つのdirect descriptorがmissing / unreadable / non-valueなら`review_unavailable`を返す。

rootは真正なreview resultを再構成せず、C207で固定済みの局所result effectだけを適用する。

## 3. 保存traceで確認した誤経路

### 3.1 Candidate208の過剰read

Candidate208は`review_required_evidence(kind)`と`未解決result kind`を導入したが、read前にはresult kindが未確定である。このためreviewerは、packet内で具体的反例を形成できても、別resultへ影響し得るmanifest observationを開けた。累積N=50ではpacket反例成立後readが10 / 199件、reviewer closed-source readが20件発生し、`TC-ADR05` iteration 21ではcertificate外のmissing observationを`unavailable`へ昇格してScore 1となった。

### 3.2 Candidate209の必要read欠落

Candidate209は反例certificateの欠損だけをrepository observation consumerへした。`certificate_deficit(packet)={}`を全manifest observationのconsumer falseへ結び付けたため、具体的反例が存在しない`TC-ADR07`で`no_counterexample_found`を閉じるdirect observationまで3 / 5件で失った。また`TC-ADR09`一件ではdirect targetを観測せず架空のsuccess receiptを構成した。

### 3.3 共通原因

両Candidateは、まだ成立していないresult kindまたはcounterexample certificateの形から、manifest observationの必要性を逆算した。結果を決めるための証拠集合と、証拠を選ぶための予測結果が循環し、C208では過剰read、C209では必要read欠落へ反転した。

## 4. 既存入力だけでは防げない理由

Candidate207の`projected_counterexample_established(packet)=false`は、反例がまだ成立していない全状態を一つにまとめる。`同じrequired factをbindするmodel-visible input`もdescriptor identityではなく意味上の同一性判定を要求するため、packet提供済みmanifest valueをreviewer-owned observationとして再取得する余地が残る。

Candidate208はこの余地をresult kind別必要証拠へ接続したが、result kindの確定前にread permissionを決める循環を増やした。Candidate209は反例certificateの欠損へ縮退させたため、no-counterexample closureの独立した証拠責務を失った。

TaskSpecはmanifest observation identity、target、expected stateおよびsuccess conditionを既に有限集合として固定する。必要なのは新しい情報またはreview手順ではなく、各descriptorの供給経路と観測状態をidentity単位で固定し、その同じ状態をrepository consumerとterminal resultへ使う境界置換である。

## 5. 置換するpredicateと責務境界

### 5.1 `CONTEXT`: descriptor供給経路

各TaskSpec-fixed manifest descriptorをreview producer起動時に次のどちらか一つへbindする。

- `projected`: packetが同じobservation identityへTaskSpec-allowedなmodel-visible value、provenanceおよびdescriptor success conditionの成立を明示的にbindする
- `direct`: 上記bindingがなく、TaskSpec-fixed targetのreviewer-owned observationだけがdescriptor resultを生成できる

意味が似ていること、同じsource artifact由来であること、rootが値を知っていることだけでは`projected`にしない。packet内の明示的なobservation identity bindingを要求する。各descriptorはexactly oneの供給経路を持ち、review開始後に`projected`を`direct`へ戻さない。

この区分はpacket構築とreviewer-owned observationの責務境界であり、rootによるreview predicateの実行またはsuccess receiptの捏造ではない。reviewerはpacket値をreview predicateへ適用し、terminal resultを生成する。

### 5.2 `TERMINAL`: descriptor観測状態とresult閉包

各manifest descriptorのreview evidence stateを次のいずれか一つとする。

- `projected_success`: `projected` descriptorのpacket bindingをreview producerがsuccess conditionへbind済み
- `direct_success`: `direct` descriptorの許可済みobservation resultがsuccess conditionへbind済み
- `direct_nonvalue`: `direct` descriptorの許可済みobservation resultがmissing / unreadable / non-value
- `unobserved_direct`: `direct` descriptorにまだadmission済みresultがない

三resultは未解決result kindからではなく、この状態集合とreview criterionから閉じる。

- `counterexample_found`: admission済みの`projected_success`または`direct_success`の値から、具体的instance、固定designとの直接矛盾およびdesignを変えるeffectを含むcertificateが成立する
- `no_counterexample_found`: 上記certificateが成立せず、全manifest descriptorが`projected_success | direct_success`である
- `review_unavailable`: 上記certificateが成立せず、`unobserved_direct`がなく、一件以上の`direct_nonvalue`がある

真正な`counterexample_found`が成立した時点で、certificate外descriptorのstateはそのterminal dependencyではない。missing observationは反例supportを失効させず、未観測descriptorが残る状態を`review_unavailable`で補完しない。

### 5.3 `EVIDENCE_GATE`: 固定frontier

`review_observation_frontier`を、現在`unobserved_direct`であり、かつadmission済みevidenceから真正な`counterexample_found` certificateがまだ成立していないdescriptorの集合とする。

reviewerのrepository observationは、bind済みreview producerがnonterminalで、対象descriptorが`review_observation_frontier`に属する場合だけconsumerを持つ。`未解決result kind`、`requested resultがその未解決resultをbind可能`、`certificate_deficit`または意味上の`同じfact`をread資格へ使わない。

frontierはread順またはmodel-stepを指定しない。既存`DECISION_BOUNDARY`とexecutor methodを変更せず、どのdescriptorがrepository evidence consumerを持つかだけを定める。

### 5.4 三置換が分離不能な理由

`CONTEXT`だけを変えるとC207の広いallowed disposition consumerが残る。`EVIDENCE_GATE`だけを変えるとterminal resultが別の証拠集合を参照する。`TERMINAL`だけを変えるとpacket提供済みdescriptorをdirectへ戻す余地が残る。

三条項を同じdescriptor identityとstate集合へ接続することで、packet供給済みfactの再読、反例成立後のcertificate外read、no-counterexample closureの必要read欠落、および未観測resultの`unavailable`補完を一つの責務境界で消す。

## 6. Candidate208追加制御の扱い

| Candidate208の追加 | 判定 | Candidate210での扱い |
| --- | --- | --- |
| 三resultごとの異なる証拠要件 | 有効な責務 | descriptor stateによるterminal閉包として再構成 |
| manifestは全result共通の実行義務ではない | 有効な不変条件 | `counterexample_found`成立時のcertificate外dependency除外として保持 |
| packet提供済みfactを再観測へ戻さない | 有効な効果、同一性判定が曖昧 | observation identityによる`projected` bindingへ置換 |
| `review_required_evidence(kind)` | result確定前の循環 | 削除 |
| `未解決result kind`とrequested result可能性 | open-endedな結果予測 | 削除 |
| projected counterexample成立後のconsumer閉鎖 | 有効な効果 | admission済みcertificate成立時のfrontier閉鎖として保持 |

## 7. 消す判断点と増える判断点

| 置換 | 消す判断点・誤経路 | 新たな固定点 |
| --- | --- | --- |
| descriptor供給経路 | packet factとrepository factが意味上同一か、再取得すべきか | packet内observation identity bindingの有無 |
| descriptor state閉包 | どのresult kindが成立しそうか、どの証拠がそのresultに必要か | 各descriptorの四状態 |
| fixed frontier | requested observationが未解決resultを変え得るか | `unobserved_direct` membershipと現在の反例certificate成立状態 |

追加する固定点は既存manifest identityとadmission済みresultの状態を直接表し、新しい探索、参照先、retry、receipt operation、review result kind別operationまたはmodel-stepを増やさない。

## 8. 非目標

- 反例の内容を有限component一覧へ完全形式化すること
- 「packetを判定してからdirect observationへ進む」という逐次review lifecycle
- manifest descriptorの読取り順、tool、command、回数またはwaveの固定
- rootによるreview意味判定、review result再構成または再採点
- Candidate208またはCandidate209全文の継承
- case ID、fixture path、固定observation名または期待resultのprompt本文への埋込み
- root preread、closed-source rereadまたはmixed readを個別禁止文で追加すること
- Standard14、N=20、採用、releaseまたはprojectionの先行実施

## 9. 評価gate

初回gateはADR9 r2 N=5の45件とする。Candidate207保存Layer 1を再利用し、prompt identity以外の実効互換条件を一致させたpreflight receiptが`ready`の場合だけ不足45件を発行する。

品質gate:

- 45 / 45 valid
- 45 / 45 Score 4
- terminal、review result、artifact境界、required commandおよび局所result effectがcase期待と一致

機序gate:

- packet反例成立caseでreviewer repository read 0件
- `TC-ADR07`でdirect observation後に`no_counterexample_found` 5 / 5
- `TC-ADR09`でmissing direct observation後に`review_unavailable` 5 / 5
- root preread、closed-source reread、mixed read、manifest外read、架空receiptなし
- review cardinality、forbidden input、producer result admissionおよび局所result effectに違反なし

停止条件:

- Score 4以外が一件でもある
- packet内で反例certificateが成立するrunにrepository observationが一件でもある
- 必要なdirect observationを省略する
- packet提供済みdescriptorをrepositoryから再取得する
- 未観測direct descriptorが残る状態で`review_unavailable`を返す
- observationなしに`direct_success`を構成する
- review適用、producer、result admission、局所result effectまたはartifact境界が退行する

一件でも停止条件が成立した場合はrepair rerun、Standard14、N=20、採用、releaseおよびprojectionへ進めない。有効な低品質または機序不通過runは保存証拠として保持する。

## 10. 手順化禁止監査

- 「先にpacketを判定し、反例がなければ次にreadする」と記載しない。
- result kindを別operationまたは別model stepへ分けない。
- manifest descriptorを順に読む規則を作らない。
- `review_observation_frontier`はrepository evidence consumerの集合であり、execution planまたはstep sequenceにしない。
- `projected / direct`は供給経路の排他的区分であり、projected観測後にdirect観測へ遷移するstate machineにしない。
- root projectionを新しいreceipt workflowまたはreview predicate実行へ変えない。

作成前判定は`reproduced_bidirectional_failure / c208_three_controls_reaudited / c207_direct_base / three_connected_boundary_replacements / no_procedural_review_lifecycle / creation_allowed`とする。

## 一次参照

- [Candidate207評価結果](../evaluations/results/candidate207-c147-review-boundary-recomposition-adr9-r2-n5_2026-08-13.md)
- [Candidate207本文](../prompts/candidates/the-caption-3ce91a4-c147-review-boundary-recomposition-r1/files/AGENTS.md.txt)
- [Candidate208設計](candidate208-result-kind-evidence-domain-design.md)
- [Candidate208累積N=50結果](../evaluations/results/candidate208-result-kind-evidence-domain-adr9-r2-n50_2026-08-13.md)
- [Candidate209設計](candidate209-named-certificate-deficit-design.md)
- [Candidate209 ADR9 N=5結果](../evaluations/results/candidate209-named-certificate-deficit-adr9-r2-n5_2026-08-13.md)
- [prompt制御設計原則](prompt-control-design-principles.md)
