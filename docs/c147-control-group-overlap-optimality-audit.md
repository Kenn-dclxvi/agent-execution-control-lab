# Candidate147 制御群・境界重複・最適性監査

> [!IMPORTANT]
> **状態**: `control_groups_13_audited / overlap_relations_classified / optimality_not_evaluated / standard14_n100_result_bound / archived_event_runs_1385_audited / H1_admitted_evidence_state_missing / H2_full_event_reopened / H3_counterfactual_overquality_rejected / quality_preserving_cost_reduction_only / next_candidate_not_authorized`
>
> Candidate147をゴールまたは最適解として固定しない。13条項を現在のまとまりのまま監査し、各制御群が何をまとめて制御するか、境界重複が強化、相互制限、handoff、競合、冗長候補のどれかを判定する。81 primitiveは条項内の意味を照合する補助台帳としてだけ使い、新ownerへの再配置単位にはしない。

## 結論

C147の13条項は、同じ抽象度で相互排他的に分けた13責任ではない。初期のoperation・producer制御へ、model再入、validation closure、validation ticket、evidence admissionの制御を、観測された失敗系列ごとに積み上げた構成である。

そのため条項間には意図的な重なりがある。現時点で確認できる主要な重なりは、単一ownerへ整理すべき競合ではなく、次の四種類である。

1. 同じ誤動作を異なる入口で閉じる防御的強化。
2. 一方の自由度を他方が制限する相互制限。
3. 一つの制御群のterminal resultを次の制御群へ渡すhandoff。
4. 一般制御を特定lifecycleで具体化する局所強化。

一方、重なりの全てが必要、最小または最適だとは評価されていない。Standard14 N=100は固定14ケースにおける品質安定性を示すが、条項や重複を一件ずつ除去・短縮・portable置換した比較ではない。したがって、現在の判断は`optimal`ではなく、証拠に応じて`supported / change_not_justified / optimization_hypothesis / not_evaluated`に分ける。

## 成立経緯から見た構造

C147の条項構成は、次のように形成された。

| 系列 | 主な条項 | 形成された制御 |
|---|---|---|
| C31〜C43 | `SPEC / PRODUCER / TERMINAL / CONTEXT / OWNER_ROLE / ROOT / INDEPENDENCE / METHOD / RECOVERY` | operation identity、producer一意性、terminal result、context、coordinator権限、手段失敗とrecoveryの基本境界 |
| C69 | `DECISION_BOUNDARY`追加 | resultで次の選択が変わらない区間の不要なmodel再入を閉じる |
| C71、C81 | `VALIDATION_CLOSURE`追加・置換 | validation集合の発行、個別判定、全result収集、完了判断をvalidation専用に閉じる |
| C98、C105〜C108 | `VALIDATION_PLAN`追加・置換 | required validationを事前の実行票へ固定し、nonterminal resultを受けた途中再入を閉じる |
| C104 | `EVIDENCE_GATE`追加 | evidenceをconsumerのある未観測predicateだけへ限定する |
| C116、C118、C125、C143〜C145 | `SPEC / EVIDENCE_GATE / METHOD / VALIDATION_PLAN`の境界改訂 | outcomeとimplementation、変更前closure、validation method、追加evidence、全lifecycle consumerを分離する |
| C147 | `DECISION_BOUNDARY`置換 | resultの停止効果を実際に影響するoperation classだけへ限定する |

この履歴から、条項名は現在の責任分類だけではなく、各時点で一つの変更軸として比較した制御単位でもある。後から抽象ownerへ移すと、条項内部で一緒に評価された正の動作、禁止、barrier、handoffを分離することになる。

## 13制御群がまとめて制御するもの

| 制御群 | まとめて制御する対象 | 同じ条項内へ置く意味 | 現在の証拠状態 |
|---|---|---|---|
| `SPEC` | required outcome、operation identity、正当なbinding元、implementation choiceとの区別、未固定時のclarification | 成果値の定義だけでなく、未固定時に何を開始せず、result効果をどこへ局所化するかまで同時に閉じる | outcome / implementation境界はC116以降で`supported`。全記述の最小性は`not_evaluated` |
| `PRODUCER` | producerの事前binding、一意性、owner metadataとの分離、producer変更 | producerを選ぶ条件と、再割当て・旧binding再利用を同じ場所で禁止する | owner語列からの不要起動防止はC41系列で`supported`。`OWNER_ROLE / ROOT`との重複除去は`change_not_justified` |
| `TERMINAL` | operation terminalの必要条件、nonterminal伝播、result補完禁止 | 正の完了条件と、欠落を文章で補う誤経路を同じ判定へ閉じる | operation terminal closureはC31以降`supported`。他条項との表現最小性は`not_evaluated` |
| `CONTEXT` | producerへ渡すpacket、十分性、最小継承、禁止input | packet内容だけでなく、どの条件なら履歴を追加しないかまで閉じる | context削減のcost効果と品質riskは観測済み。現行形の最適性は`not_evaluated` |
| `EVIDENCE_GATE` | evidence eligibility、predicate state、追加取得、変更前closure、artifact変更への遷移、validationへのhandoff | read許可だけでなく、readをいつ閉じて次へ進むかを同じconsumer lifecycleへ結ぶ | C104、C116、C118、C125、C143〜C145で複数境界が`supported`。長さ・重複・F06残差は`optimization_hypothesis` |
| `OWNER_ROLE` | owner metadata、独立producer開始、delegated result provenance、`unavailable`、補完禁止 | 起動条件と、そのexecutionから返ったresultだけを認める条件を分離せず閉じる | C41とC190/C191系の反例から独立境界の維持は`supported`。runtime field表現のportable置換は`not_evaluated` |
| `ROOT` | producerでないcoordinatorの許可行為と禁止行為 | 非producerが何をしてよいかを短い権限制御として局所化する | root代行禁止は関連系列で`supported`。`PRODUCER / OWNER_ROLE / TERMINAL`への統合は`change_not_justified` |
| `INDEPENDENCE` | 先行resultまたはartifactを対象とする別operationのidentity、predicate、owner、producer | 派生operation形成時に、先行operationのproducerやpredicateを流用させない | operation局所性の安全境界として`supported`。`SPEC / PRODUCER`との重複除去は`not_evaluated` |
| `DECISION_BOUNDARY` | result effect scope、dependency、非依存invocation集合、発行、result収集、次判断 | 待つ対象の判定と、待たない対象の正の発行を一つの局所closureへ置く | C147対象15件とStandard14で`supported`。portable wordingと追加cost最適化は`optimization_hypothesis` |
| `VALIDATION_CLOSURE` | validation readiness、全件発行、個別判定、fail-fast、全result収集、一回の完了判断 | validationの開始から結果closureまでを一般発行規則だけへ委ねない | C71/C81系列でstep・tool削減と挙動安定を観測。`VALIDATION_PLAN`との統合は`not_evaluated` |
| `VALIDATION_PLAN` | required validation実行票、method bind、途中success後の継続、nonterminal invocationの専用待機 | 検証集合の固定と、実行途中に新判断を挟まない継続を同じticket identityへ結ぶ | C98、C105〜C108でnonterminal経路が`supported`。runtime wait表現の置換は`not_evaluated` |
| `METHOD` | 明示method、未固定methodの選択、failure時の代替、permission denialとの分離 | 手段失敗をpredicate失敗やpermission否定へ昇格させず、許可された継続だけを残す | C119/C144境界は`supported`。`EVIDENCE_GATE / VALIDATION_PLAN`との記述重複は`change_not_justified` |
| `RECOVERY` | environment-only repair、同じrequired execution再試行、allowance消費、method選択との分離 | method変更とenvironment recoveryを同じretryとして数えない | 概念分離は既存制御として保持。現行3文相当の独立効果と最小性は`not_evaluated` |

## 境界重複の分類

### 防御的強化

同じ誤動作を異なる入口で閉じる。単一owner競合とは扱わない。

| 条項関係 | 各入口 | 重複の効果 | 判定 |
|---|---|---|---|
| `TERMINAL × OWNER_ROLE × ROOT` | 完了判定、delegated result admission、coordinator権限 | producer terminal resultの欠落を、完了宣言、異sender result、root再構成の三経路から補完できなくする | `supported / intentional_reinforcement` |
| `PRODUCER × OWNER_ROLE` | producer binding、owner metadataとdelegated result | owner語列からproducerを推測せず、明示producerを起動した場合だけそのresultを認める | `supported / intentional_reinforcement` |
| `SPEC × INDEPENDENCE` | 初期operation形成、先行resultを使う派生operation形成 | task全体のresult・constraint伝播と、派生operationでのidentity再利用を別時点で閉じる | `change_not_justified` |
| `PRODUCER × INDEPENDENCE` | 同一operation、派生operation | producer再割当てをoperation内とoperation生成時の両方で閉じる | `change_not_justified` |

### 相互制限

一方が許す自由度を他方が限定する。片方へ統合すると境界を失う可能性がある。

| 条項関係 | 相互制限 | 判定 |
|---|---|---|
| `SPEC × EVIDENCE_GATE` | `SPEC`がoutcome未固定時の開始を禁止し、`EVIDENCE_GATE`がrepository evidenceによるoutcome事後補完を禁止する | C116系列から`supported` |
| `EVIDENCE_GATE × METHOD` | method未固定だけではevidenceを開かず、method failureだけではpredicateやpermissionを失効させない | C119/C144系列から`supported` |
| `DECISION_BOUNDARY × EVIDENCE_GATE` | evidenceがeligibleでも、先行resultで可否が変わるなら待つ。dependencyがなくてもconsumerがなければ発行しない | C145/C147の組として`supported` |
| `METHOD × RECOVERY` | 代替method選択はrecovery allowanceを消費せず、environment repairだけをrecoveryとして数える | `change_not_justified`。独立効果量は`not_evaluated` |
| `CONTEXT × OWNER_ROLE` | producer identityが正しくてもforbidden inputを渡せず、packetが正しくても異producer resultをadmitできない | `change_not_justified` |

### handoff

前の制御群がterminal resultを作り、後の制御群へ渡す。重複ではなくlifecycle境界である。

| from | to | handoff | 判定 |
|---|---|---|---|
| `SPEC` | `PRODUCER / EVIDENCE_GATE` | `spec_ready`とoperation identity | `supported` |
| `EVIDENCE_GATE` | artifact変更 | `implementation_bound`と未発行prechange evidenceの失効 | C118/C143系列から`supported` |
| `EVIDENCE_GATE` | `VALIDATION_PLAN` | artifact変更後に確定するvalidation identity | `supported`。逆流禁止を維持 |
| `VALIDATION_PLAN` | `VALIDATION_CLOSURE` | validation set、順序、個別pass condition、method | `supported`。統合最適性は`not_evaluated` |
| `VALIDATION_CLOSURE` | `TERMINAL` | 個別terminal resultが揃ったvalidation operation state | `supported` |

### 一般制御と局所強化

一般条項と、特定lifecycleで同じ境界を具体化する条項の重なりである。

| 一般制御 | 局所強化 | 局所化する理由 | 判定 |
|---|---|---|---|
| `DECISION_BOUNDARY` | `VALIDATION_CLOSURE` | validationは順序、fail-fast、個別exit、全result closureを持ち、一般的な非依存発行だけでは不足する | `supported / intentional_specialization` |
| `TERMINAL` | `VALIDATION_PLAN / VALIDATION_CLOSURE` | validation途中のnonterminalやresult欠落をoperation完了へ昇格させない | C105〜C108から`supported` |
| `EVIDENCE_GATE` | `VALIDATION_PLAN` | evidenceの一般default denyに対し、変更後validation method選択を追加evidenceへ戻さない | `supported / intentional_specialization` |

### 競合・冗長候補

現時点で保存traceへbindできる確定競合は0件である。ただし、次は最適性が未評価のため監査対象として残る。

| 候補 | 疑う理由 | 現在判断 |
|---|---|---|
| `VALIDATION_PLAN × VALIDATION_CLOSURE`の発行・収集記述 | 実行票形成、継続、全result後の一回判断が両条項に現れる | `supported / intentional_handoff_and_specialization`を保持。full Standard14のvalidation後続発行22件は全件が既存closureからの逸脱で、新しいticket集合relationの不足ではなかった |
| `PRODUCER × OWNER_ROLE × ROOT`の非代行記述 | producer一意性とroot補完禁止が複数回現れる | `change_not_justified`。C190系で独立`OWNER_ROLE`を弱めた反例がある |
| `SPEC × EVIDENCE_GATE`のoutcome/implementation記述 | 同じ境界を両側から説明する | `change_not_justified`。片側削除比較は未実施 |
| `TERMINAL × VALIDATION_*`のnonterminal記述 | 一般規則とvalidation局所規則が重なる | `change_not_justified`。対象identityが異なる |
| runtime固有表面語 | portable性を下げ、別runtimeへ一般化しにくい | 表面分類は保持する。F10 monthlyの共同発行19 / 100件は全件Score 4かつ低tokenであり、start barrier追加は現行oracleでは過剰品質として除外 |

## 現時点の最適化探索候補

### H1: F06 authority追加read残差

C147 F06 N=100では旧`authority_lookup`指標が21 / 100件に残り、発生群のtoken中央値は非発生群より高かった。ただし後続の[原因監査](c147-f06-authority-route-causal-audit.md)で、21件はpath-local instruction read 17件、root-only 2件、discovery-only 2件に分かれた。さらにtool発行前inputを照合すると、root C147本文は21 / 21件ですでにmodel-visible、`tests/AGENTS.md`本文は0 / 21件だった。root本文read 6件は重複取得、discovery-only 2件のprobeは`exit 2`かつresult effectなしと確認した。必要なrepository instruction readと、locator探索、root再読、probeを一括して削減対象にはしない。

- 状態: `optimization_hypothesis`
- 変更単位候補: `EVIDENCE_GATE`のeligibilityではなく、admitted evidence identityを失効までcurrent stateとして保持する遷移
- 保持対象: path-local instruction read、outcome / implementation境界、consumer requirement、具体的不足後の限定continuation
- 棄却: authority関連21件の一括削減、repository instructionをallowed readから外す案
- 観測済み誤経路: F06のroot再取得6件と結果未使用probe 2件に加え、Standard14保存eventでroot再取得130 / 1,385件
- ADR9保存trace: 全9ケースでroot本文再取得111 / 450。対応112 taskの112 / 112で再取得前から同じroot本文がmodel-visible
- 未証明: promptで防ぐ純便益、広いlocatorを省いた場合のinstruction見落とし、Standard14非対象経路へのspillover
- 評価境界: H1だけを変えるC147直接childはADR9の既知review品質失敗を解かない。review制御を同時に加えると因果軸を混ぜるため、現行ADR9先行gateでは単独試験を開始しない

### H2: validation二条項の重複cost

`VALIDATION_PLAN`と`VALIDATION_CLOSURE`は、validation set、発行、途中result非消費、全result後の一回判断を両側から制御する。[保存trace原因監査](c147-validation-control-overlap-causal-audit.md)ではrequired-validation 190件、403 command groupを照合した。189 / 190件は全required commandを一wrapperへ閉じ、command再実行は0件だった。nonterminal 52件の79 waitも別toolまたは利用者向けmessageのinterleavingは0件だった。

- 状態: `supported / intentional_handoff_and_specialization / H2a_missing_relation_rejected`
- 固有境界: `VALIDATION_PLAN`はticket set、method、diff / status、nonterminal継続を所有し、`VALIDATION_CLOSURE`はreadiness、個別発行、exit、fail-fast、result admission、terminalを所有する
- full event観測: required-validation 685件でfalse-unavailableによるrequired command再実行1件、最初のvalidation発行後の完了evidence追加22件
- H2a結果: 22 / 22件で完了evidenceはvalidation前に認識済み。11件はnonterminal ticketを待たず、10件はterminal outputの表示済みevidenceを再取得し、1件は既知のticketを分割した
- 現在判断: 二条項統合案には戻らない。H2aへrelationを足す案は同義反復として棄却する。H2bはfull command用JSON exit行が見えない同型60件中59件が正常admissionしており、fail-fast通過を正のresult admissionにするrelationは`candidate_not_ready`とする

### H3: start gate barrier（現行最適化から除外）

runtime表面を[条項別に分類](c147-runtime-surface-portability-audit.md)しただけでは最適化判断にならなかった。[Standard14保存event](c147-standard14-control-insufficiency-audit.md)へ戻ると、F10 monthly 19 / 100件でstart identity resultを消費する前に少なくとも一つのreview対象readを開始していた。しかし19件は全てScore 4で、token中央値75,070はgate先行81件の93,801より低かった。

- 状態: `not_evaluated_counterfactual / rejected_as_current_overquality`
- 追加した場合の機序: start gateが特定operationを開始禁止にしたとき、そのoperation専用evidence invocationも同じoperation classへ所属させ、drift時の早期停止対象にする
- 得られるもの: 現在のclean fixtureでは観測していないdrift時の追加安全性。評価済み成果品質の改善ではない
- 保持対象: drift時にreadを禁止しないF08等の共同発行、C147対象15件の正の共同発行、producer provenance、nonterminal継続
- 棄却: 全readの逐次化、条項順を処理順へ読む構成、runtime語の一括削除
- 現在判断: 合格結果を変えず、tokenを増やす方向（elapsedは約2.7秒短縮）なのでrelationを設計せず、Candidate候補から外す。drift時早期停止をrequired outcomeにした別oracleで失敗が観測された場合だけ再検討する
- 含めないもの: 外部executor、CLI、tool adapter、runtime hookの変更

### H4: producer系三条項の読解cost

`PRODUCER / OWNER_ROLE / ROOT`は別入口を閉じるため現状維持に根拠があるが、重複した禁止表現による読解costが分離測定されていない。

- 状態: `not_evaluated`
- 変更単位候補: なし。fresh traceで具体的costまたは競合を観測するまで設計しない
- 理由: C190系列の反例から、独立境界の安易な削除riskが高い

## 仮説の証拠準備度

| 仮説 | 具体的な現行costまたは目的 | 変更効果を判定できる保存経路 | 現在許可できる次作業 |
|---|---|---|---|
| H1 | root再取得130 / 1,385、F06の失敗probe 2件、ADR9 root再取得111 / 450。未取得path-local instructionは保持 | Standard14保存event、F06 tool前input、ADR9保存trace | admitted evidence identityのstate保持として表現する。H1単独gateを固定できるまでCandidateを作らない |
| H2 | false-unavailable rerun 1 / 685。同型表示省略60件中59件は正常。validation後続発行22 / 685は既存制御への逸脱 | Standard14 event 685件、対象runと同型正常59件、22件の元rollout、C71/C81/C107/C110/C111履歴 | H2aは閉じる。H2bはnet costを判定できるgateがないためCandidateを作らない。二条項統合へ戻らない |
| H3 | F10 monthly共同発行19 / 100は全件Score 4で、token中央値もgate先行群より低い | 未観測drift時の安全性だけが反実仮想の目的 | 現行最適化から除外。別oracleで必要性が観測されるまで設計しない |
| H4 | 具体的cost未観測 | C190の削除退行だけが直接証拠 | fresh costまたは競合を観測するまで進めない |

現時点ではH1とH2bだけを、Standard14で全件合格を保ちながら観測costを減らし得る仮説として扱う。H1はadmitted evidenceのcurrent / invalidated state、H2bはfalse-unavailable再実行のresult admissionである。ただしH1は130 / 1,385件、H2bは1 / 685件で、H2b同型60件の59件は正常だったため、次の分析優先度はH1とする。H2aは不足relationではなく既存制御への逸脱、H3は未観測安全性の追加であり現行oracleでは過剰品質、H4は具体的cost未観測である。

最適化を「表面文言を削ること」へ限定しないが、「足りないrelationを足すこと」自体も目的にしない。Standard14で成立した品質を守り、観測された再取得・再入・再実行costを減らす場合だけstateまたはrelationの変更を検討する。分析順を制御本文の実行順へ読み替えない。

## 最適化候補へ進める判定手順

1. 制御群または重複関係を一つだけ変更単位にする。
2. 変更前に、対象経路、非対象経路、保持する条項内closure、変更する表面または判断点を固定する。
3. C147の保存traceから、変更が消費する具体的なcostまたは誤経路を示す。
4. 品質oracle、mechanism oracle、token、elapsed、model step、tool callを分ける。
5. targeted gateを通過した場合だけStandard14へ進み、Standard14集約値でcase間のcost移動を相殺しない。
6. Standard14通過後も、評価した変更軸についてだけ判断し、C147全体または新構成を`optimal`にしない。

## 現在判断

- C147は`reference_waypoint / quality_supported / known_mechanisms_supported / optimality_not_evaluated`である。
- 13条項のまとまりは分析単位として保持する。
- 81 primitiveは条項内部の欠落確認に使い、別ownerへ再配分しない。
- 確定した境界競合は0件である。
- 意図的強化、相互制限、handoff、局所強化は現行構造の意味として保持する。
- H1はadmitted evidence state、H2は意図的handoffを保持したfull event再監査を、品質維持のcost削減仮説として残す。H3は現行oracleでは過剰品質、H4は具体的cost未観測である。いずれも現時点のCandidate作成許可ではない。

## 参照

- [`Candidate147 release制御本文`](../prompts/releases/the-caption-3ce91a4-result-effect-scope-release-r1/files/AGENTS.md.txt)
- [`Candidate147 result effect scope設計`](candidate147-result-effect-scope-design.md)
- [`Candidate147 機能分解の再分析`](c147-functional-decomposition-reanalysis.md)
- [`Candidate147 runtime固有表面形・意味拘束監査`](c147-runtime-surface-portability-audit.md)
- [`Candidate147 Standard14結果起点の制御不足監査`](c147-standard14-control-insufficiency-audit.md)
- [`prompt制御の検討原則`](prompt-control-design-principles.md)
- [`制御メカニズムの履歴整理`](control-mechanisms.md)
- [`Candidate一覧`](../prompts/candidates/README.md)
- [`Candidate147 F06 N=100結果`](../evaluations/results/candidate147-result-effect-scope-v14-medium-f06-atomic-reuse-n100-cli0146_2026-08-02.md)
