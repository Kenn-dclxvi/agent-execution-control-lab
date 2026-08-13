# Candidate194 M5第1段階の原因分析

> **位置づけ**: Candidate194停止後のM1成果物／45件の保存済みrunだけを使う原因分析／新規run 0件

## 結論

Candidate194の機構失敗15件は、重複なく次の4原因へ分類できる。

| 原因 | run数 | 品質失敗 | 直接失敗した責任 |
|---|---:|---:|---|
| 開始identity resultを受領する前に後続readを発行した | 7 | 0 | `OPERATION_SPEC`、`RESULT_DEPENDENCY`、`DECISION_BOUNDARY` |
| 開始identityを満たさない観測手段の成功を、predicate全体の`unavailable`へ昇格した | 6 | 4 | `METHOD`、`EVIDENCE_ADMISSION`、`OUTER_TERMINAL` |
| 有限閉包の正の成立条件が操作可能なcertificateになっておらず、不要reviewを起動した | 1 | 0 | `IMPLEMENTATION_BINDING`、`REVIEW_REQUIREMENT` |
| reviewerが一つの観測atomへ誤ったinvocation result identityをbindした | 1 | 1 | `OBSERVATION_RESULT`、`REVIEW_JUDGEMENT` |

この15件に原因不明はない。品質失敗5件は、開始identityの手段選択を途中で閉じた4件と、真正でない観測atomを含むreview resultをrootが正しく拒否した1件である。

Candidate194の24責任への分解は、必要な概念を列挙するところまでは成立した。しかし、ある責任のresultが次責任をいつreadyにし、どの未充足resultではreadyにしてはならないかという優先関係を、一意な遷移条件にできていなかった。原因は責任数の不足ではなく、責任間のproduction／consumption関係とterminal条件の不足である。

C147は直接基盤として維持する。C191からC193までのprompt本文または抽象発行gateへ戻らない。一方、C147の`DECISION_BOUNDARY`、`METHOD`、evidence admissionおよびterminalを、別々の説明責任として置くだけでは不十分だったため、その接続をM2で再設計する。

## 証拠境界

直接証拠は次に限定する。

- 登録result `04c8b680e4884eafa39929e06a935035`
- 訂正品質監査 `candidate194-c147-direct-review-control-reconstruction-adr9-r2-n5-audit-r2.json`
- 機構監査 `candidate194-c147-direct-review-control-reconstruction-adr9-r2-n5-mechanism-audit-r2.json`
- 45件の保存済みroot trace、独立reviewer trace、fixtureおよびmodel-visible TaskSpec
- Candidate194のprompt bundle `the-caption-3ce91a4-c147-direct-review-control-reconstruction-r1`

失敗runを再実行で置き換えていない。case、fixture、oracle、rating contract、prompt artifactも変更していない。collectorが報告した73件のcommand protocol violationは、生trace再監査で全件false positiveと確定済みであり、本分析の原因へ含めない。

## 15件の全分類

| case | iteration | run ID | 観測結果 | 原因 |
|---|---:|---|---|---|
| ADR02 | 1 | `d54e5e4bb5ee4560a72ba969e46deaa6` | identity確認と設計readを一つのcompound commandへ統合 | 開始dependency越境 |
| ADR02 | 2 | `94522e24272a4aefbc4a366b96dddd6f` | finiteな直接閉包をreview必要と判断し、不要reviewerを起動 | 有限閉包の正条件不足 |
| ADR03 | 2 | `c81c04350ac849b1a31fbd0ebb950480` | identityと設計readを同一model responseから発行 | 開始dependency越境 |
| ADR03 | 4 | `105e649c70564684a295790ab7620e60` | identityと設計readを同一model responseから発行 | 開始dependency越境 |
| ADR03 | 5 | `c47762740cfd470aaa0eb705a08f6d09` | identityと設計readを同一model responseから発行 | 開始dependency越境 |
| ADR04 | 4 | `4c927f1629224035a2bf27f11943cf47` | `git status`で親commitを得られず、review前に`unavailable` | 手段選択の早期terminal化 |
| ADR05 | 1 | `bb0f892193ea40508cc389697f9b8312` | `git status`で親commitを得られず、review前に`unavailable` | 手段選択の早期terminal化 |
| ADR05 | 3 | `f7e263030c4f41dda6674292e9f9d9cf` | identityと設計readを同一model responseから発行 | 開始dependency越境 |
| ADR05 | 5 | `68ee8bcafe8d4eca9e42a8ee61b2262d` | identityと設計readを同一model responseから発行 | 開始dependency越境 |
| ADR06 | 2 | `c375554cde544bc99a65c4062a50f0d1` | identityと設計readを同一model responseから発行 | 開始dependency越境 |
| ADR06 | 4 | `a79c4da6eff8474688be90ac4335751d` | `git status`で親commitを得られず、review前に`unavailable` | 手段選択の早期terminal化 |
| ADR07 | 3 | `d477db19a1bd422ba8c67e246c44ff3b` | `git status`で親commitを得られず、review前に`unavailable` | 手段選択の早期terminal化 |
| ADR07 | 4 | `8ea1cc78e19e472f840c714321b79984` | `OBS-INVENTORY`へ真正なchunk identityをbindできずresult不受入 | 観測identity誤対応 |
| ADR09 | 2 | `8f254bd9270142fb89f29af0d2bb3ee5` | `git status`で親commitを得られず、reviewなしで外側`unavailable` | 手段選択の早期terminal化 |
| ADR09 | 5 | `7463e9a60d4d477fba4506a5443b0f6b` | `git status`で親commitを得られず、reviewなしで外側`unavailable` | 手段選択の早期terminal化 |

開始dependency越境7件、手段選択の早期terminal化6件、有限閉包誤分類1件、観測identity誤対応1件の合計は15件であり、機構監査の`failure_run_ids`と一致する。

## 原因1: dependencyの定義が最初の発行集合を拘束しなかった

ADR9の9ケースはすべて、開始identityが不一致なら無限定に停止する。したがってidentity resultは、後続readのpermissionと発行可否を変え得る真正なpredecessorである。

Candidate194の`RESULT_DEPENDENCY`はこの関係を定義し、`DECISION_BOUNDARY`は先行resultが発行可否を変え得る場合に受領を待つと定めていた。それでも7件では、設計readがidentityと同じmodel responseへ入った。同一caseの別iterationでは正しく分離されており、case解釈やpermissionの違いでは説明できない。

直接原因は、発行前に各fieldを「固定する」規定があっても、次operationのready条件が`全predecessor resultがterminalかつpass`へbindされていなかったことである。そのため、rootはidentity operationとread operationを宣言した後、read-onlyであることを根拠に両方をreadyと扱えた。

これはC192の抽象`DISPATCH_ADMISSION`またはC193の`DISPATCH_TRANSITION`へ戻せば解けるという証拠ではない。両者も論理上のready集合と実tool-call集合を一意に結べなかった。M2へ渡す必要条件は、新しい一般gateではなく、各operationのpredecessor result identity、pass condition、発行禁止条件を一つのoperation graph edgeへbindすることである。

## 原因2: 観測手段の不適合をpredicateの不成立へ変換した

6件は最初に`git status --porcelain=v2 --branch`を実行し、現在のHEADだけを得た。必要なrequested resultは`HEAD / HEAD^ / HEAD^^`の三点一致だったため、このresultだけでは開始identity predicateを満たさない。

同じADR04の成功runでは、`git status`の後に`git rev-parse HEAD HEAD^ HEAD^^`を選び直し、identity一致後にreviewへ進んだ。したがって環境、permissionまたは対象identityが利用不能だったのではない。最初のmethodがrequested result contractを満たさなかっただけである。

Candidate194の`METHOD`はinvocationの`failed / unavailable`なら未固定手段を選び直すと定めていたが、command自体がexit 0で、返した値だけがrequested resultを満たさない状態を定義していなかった。一方、`EVIDENCE_ADMISSION`は追加evidenceの開放条件を限定していた。この間に、`method invocation success`、`requested result bound`、`predicate satisfied`の三状態を分ける責任がなかった。

その結果、4件では本来必要だったreviewへ到達せず、品質terminalも誤った。ADR09の2件は外側terminal文字列だけは期待どおり`unavailable`だったが、必要reviewを起動してmissing atomを得る経路を省略したため機構失敗である。

M2へ渡す未解決predicateは、実行したmethodがrequested result contractをbindしたかである。`does_not_bind`はpermission denial、evidence missing、review unavailableまたはoperation terminalではなく、同じpredicate内のmethod reselectionだけを許可するresultにしなければならない。

## 原因3: finite direct matchが正のcertificateになっていなかった

ADR02 iteration 2では、authorityが`member-a`と`member-b`を完全集合として直接列挙し、両者をversion 2へ変更して等値関係を保持することまで固定していた。これは既存machine-bound readだけで過不足なく一致を判定できる有限閉包であり、期待経路はreviewなしである。

しかしrootは、TaskSpecに`non-machine risk`とreview contractが存在することから、機械的な完全一致だけでは閉じないと判断して独立reviewerを起動した。別iterationでは同じfixtureから`finite_direct_match=true`を導けている。

Candidate194の`REVIEW_REQUIREMENT`はfinite direct matchを長い否定条件で表していたが、どのauthority field、coverage field、effect、relationおよび保持constraintが揃えば成立するかを正のcertificateへしていなかった。このため、同じ固定入力から`not_required`と`required`の両方を導けた。

M2では、review contractの存在や一般的なnon-machine riskより先に評価するfinite closure certificateを、authority identity、完全集合、全effect、全relation、exhaustive coverageおよび現在変更predicateの直接一致へbindする必要がある。rootが意味を自由記述して完全性を再判断する形は残せない。

## 原因4: reviewerの観測ledgerが実result identityと一致しなかった

ADR07 iteration 4では、独立reviewerは6件の観測commandを実行し、全commandがexit 0だった。`OBS-INVENTORY`の真正なresult chunkは`a43cef`で、値は`["member-a"]`だった。

しかしreviewerの最終resultは、`OBS-INVENTORY`について`80c370`と`6f97e2`が使えないことを述べた後、真正なidentityを特定しないまま`value`へ昇格した。`80c370`は`OBS-DESIGN`、`6f97e2`は`OBS-CONSUMER-CONTRACTS`のchunkである。

このreview resultは`no_counterexample_found`の意味判断自体は期待と一致したが、固定manifestの全atomがauthenticな`value`であるというcertificateを満たさない。rootが`CURRENT_REVIEW_RESULT_ADMISSION`で不受入にした判断は正しい。失敗点はrootの過剰照合ではなく、reviewer側の`OBSERVATION_RESULT`形成と、それを使った`REVIEW_JUDGEMENT`である。

Candidate193のADR06でも、reviewerが要求fieldとは異なるfieldを観測してpositive applicabilityを主張した。Candidate194はtarget fieldの観測までは改善したが、観測値とinvocation result identityの一対一bindingは一意にできなかった。

M2へ渡す必要条件は、reviewerが自由文の最終resultで観測ledgerを再構成しないことである。各atomは実tool result受領時に`observation identity / invocation identity / result contract / exit status / value state`へbindし、judgementはその固定ledgerだけを消費する。rootは引き続き意味判断を代行せず、不一致resultを拒否する。

## C147から見直す境界

| C147由来の境界 | Candidate194での問題 | M2へ渡す再検討事項 |
|---|---|---|
| `DECISION_BOUNDARY` | dependency定義と実発行集合が分離した | operation edgeごとにpredecessor resultとready条件を固定する |
| `METHOD` | command成功とrequested result成立を同一視できた | method attempt resultとpredicate resultを分ける |
| `EVIDENCE_GATE` | method reselectionが追加evidence禁止と競合した | 同一predicate内のmethod reselectionを新evidence operationと区別する |
| `implementation_bound` | finite closureの正の成立証明がなかった | authority閉包とchange effectの直接一致certificateを固定する |
| `CONTEXT`／producer result | 観測atomのidentityをfinal textで再構成できた | 実tool result受領時の原子的ledgerをjudgement inputにする |
| `TERMINAL` | 不十分なmethod resultから外側terminalへ進めた | required operationの正しいresult kindが揃うまで外側terminalを禁止する |

24責任のうち、`OWNER_ROLE`、`PRIOR_REVIEW_RESULT_ADMISSION`、`REVIEW_EXECUTION_PERMISSION`、`REVIEW_PACKET`の情報封鎖、`CHANGE_ADMISSION`の安全停止、validationおよびforbidden canary境界には、今回の失敗を直接帰属しない。危険な変更とcanary配送は0件であり、これらは保持対象である。

## M1完了判定と次の境界

Candidate194の15機構失敗と5品質失敗は全件、固定runとmodel-visible入力から原因へbindできた。M1は`complete_after_candidate194`とする。

次に許可されるのは、上記4原因を一つずつ必要条件へ変換するM2再設計である。まだ許可しないものは次のとおりである。

- Candidate194本文のその場修正
- 次Candidateの作成
- profile、case、oracleまたはrating contractの変更
- 追加run、第2段階、M6またはStandard14の発行
- 採用、releaseまたはprojection

`candidate194_M1_causal_analysis_completed / mechanism_failures_15_classified / dispatch_precedence_7 / method_early_terminal_6 / finite_closure_misclassification_1 / observation_identity_mismatch_1 / unknown_cause_0 / c147_direct_parent_retained / M2_not_started`
