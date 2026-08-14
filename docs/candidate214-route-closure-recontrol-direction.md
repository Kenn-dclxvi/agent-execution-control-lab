# Candidate214経路閉鎖の再制御方針

## 状態

- `candidate221_evaluated`
- `candidate221_quality_failed`
- `candidate221_mechanism_failed`
- `candidate221_stopped`
- `carrier_bootstrap_audit_completed`
- `candidate222_design_completed`
- `candidate222_quality_failed`
- `candidate222_mechanism_failed`
- `candidate222_stopped`
- `cumulative_route_ledger_fixed`
- `carrier_feasibility_evidence_required`

## 結論

review制御の次の出発点は、Candidate214で成立したpacket構築後のreviewer再read閉鎖と、別containerの必要観測を残した局所境界とする。後続のdelivery境界監査により、Candidate214でもrootはreview開始前にwhole design sourceを受領しており、rootへの初回mixed-owner deliveryは閉じていなかったことを確認した。過剰遮断は「必要な場合だけ読む」という条件付き判断で緩めず、最初のsource取得からroot projectionとreviewer direct observationを別carrierへ固定する。

Candidate215からCandidate220までは、Candidate214の過剰遮断を解消するための親として扱わない。これらは、必要性、投影状態、operand、ownership、ticketまたはwork itemをモデルが正しく判定することに依存し、誤経路のpermissionが残った反例群として保持する。

## Candidate214で保持する制御

Candidate214 ADR9 r2 N=5では、当時固定した監査境界で次の経路が成立した。

- packet投影元sourceの再readはCandidate213の6回から0回になった。
- projected source、mixed source、manifest外sourceのreviewer readは0件だった。
- 別containerにあるADR07とADR09の必要paired observationは各5 / 5で残った。

Candidate214の一次resultにあるroot reviewer-owned preread 0件は、当時の消費・admission定義による歴史的判定として保持する。一方、seal済みrolloutをobservable deliveryで再監査すると、全45 root runが`design-admission.json`全体を取得し、ADR03からADR06の20 / 20 runでもpacket配送禁止のinventoryとcontractsを含むresultをrootが受領していた。したがって、Candidate214がroot whole-source deliveryを発行不能にしたとは扱わない。

保持するのはCandidate214の文面全体ではない。保持するのは、packetに使ったsourceへreviewerが別selector、部分抽出または別commandで再到達する経路を閉じたことと、別containerの必要観測を一律に止めなかった局所境界である。

## 過剰遮断の原因

Candidate214はpacketへ実際に投影した値ではなく、その値を供給したsource container全体を閉じた。そのためADR03の1件、ADR05の2件、ADR06の1件で、packetへ未投影のcurrent inventory membershipまたはconsumer contractに到達できず、期待`blocked`が`unavailable`になった。

これは、不要なreadと必要なreadの判断精度が低かった問題ではない。rootがwhole sourceを受領してpacketの一部だけを投影した後にcontainer全体を閉じたため、packet非配送値はrootへ届いている一方、reviewerへ渡る合法carrierが存在しなかったことが原因である。

## 再制御で解く責務境界

次の設計は、review命題に必要な各値について、repository evidenceを発行する前に次のいずれか一つへ固定できる場合だけ成立する。

| 合法な経路 | 必要な境界 |
|---|---|
| packetで運ぶ | TaskSpecまたはschemaがその値のpacket配送とpacket constructorによる受領を明示的に許し、別owner用の余分な値をrootへ観測させず、必要な投影だけを構築できる |
| reviewerが直接観測する | reviewer-owned targetがevidence発行前に一意で、発行したinvocationのobservable outputがroot-owned値またはpacket投影済み値を含まない |
| 観測せず停止する | 上記2経路のいずれも固定できない場合は広いread、別target、自己分類または推測で補完せず`unavailable`にする |

この分類をモデルがsource内容を読んだ後に選ぶことは禁止する。TaskSpec、schema、repository authorityおよび発行前にmodel-visibleなidentityから一意に固定できない値は、経路を開く判断材料にしない。

ADR9のTaskSpec、case、fixture、schemaおよびoracleは比較条件として固定し、Candidate214の品質失敗を通すために変更しない。既存のmodel-visible inputが合法なcarrierを許さないなら、その事実はpromptの追加条件で補完せず、現行比較境界での未解決を意味する。

## 今後使わない解決パターン

次の記述は言い換えやlabel変更を含め、Candidate作成根拠にしない。

- terminalに必要な場合だけ未投影regionを読む。
- 先にpacket充足、counterexampleまたはmissingを判定し、その後だけ読む。
- source identity、region identity、operand、ownership、ticketまたはwork itemを正しく自己分類した場合だけreadを許す。
- rootがwhole-container resultを受け取った後に、不要な値を消費しないよう求める。
- KPIまたはScore 4の改善を、失敗operationの実行不能性より先に採用根拠にする。

Candidate215からCandidate220までの保存済みresultは、上記パターンを再導入しないための反例として使う。各Candidateの制御文を継承し、その上へ修正条件を追加するために使わない。

## 次Candidate作成前の設計gate

次の全件を一次アーティファクトとmodel-visible inputで固定できるまで、Candidate bundle、profileまたは評価slotを作成しない。

1. Candidate214の4品質失敗で必要だった値の正確なownerと合法なcarrier。
2. packet投影元sourceの再readとrootによるreviewer-owned値の先行観測を合法にしている権限辺の全件。
3. 権限辺を削除した後も、ADR03、ADR05およびADR06の必要値が誤経路なしにreviewerへ到達すること。
4. モデルが判断順、必要性分類または自己申告を変えても、対象の失敗invocationがprompt準拠として構成できないこと。
5. 必要値のcarrierを現行prompt境界で強制できない案は、別条件でread permissionを再開せず`prompt_control_not_demonstrated / candidate_not_created`として棄却し、owner、read対象、packet構築、observable output境界を分解し直した別案の検討へ戻れること。

後続の一次入力監査では、TaskSpecのpacket permission、finite evidence manifest、exact structural targetおよびroot substitution禁止から、packet配送値とpacket非許可のmanifest targetを意味上は区別できると判断した。Candidate221はこのproducer別source authorityだけをCandidate147へ加えたが、後続評価により、発行前に実行可能な別carrierへ分離できたという判断は反証された。

ADR9 r2 N=5の実行では、この分離は成立しなかった。ADR03からADR06の20 / 20 runでrootがreviewer-owned targetを先行取得し、mixed-owner resultを受領した。TaskSpec-declared集合を追加しても、whole design containerをroot operationへ含める自己分類がprompt準拠として残ったためである。Candidate221はC214のroute closureを保持できず、`quality_failed / mechanism_failed / stopped`とした。

現行のmodel-visible inputから必要carrierと禁止targetをpromptだけで実行不能な境界へ固定できることは実証されていない。このため、Candidate221と同じ自己分類条件を継承した次Candidateは作成しない。一方で問題の検討は終了せず、owner、read対象の粒度、packet構築、rootが受け取れるoutputを再分解し、C214のreviewer-side局所境界を維持しながら初回deliveryも閉じる別の構造を設計する。

後続のcarrier bootstrap監査では、C214とC221の両方で、review sourceへの最初のroot readがwhole-container resultを返していたことを確認した。次の設計軸は、reviewer readを後から条件付きで開くことではなく、最初のsource取得からrootへ返せるexact projectionとreviewerが直接観測するexact targetを分ける`source bootstrap projection`である。

現在のTaskSpecはpacket配送可能なvalue classとreviewer observationのexact manifest targetを持つ。Candidate221ではこれらに将来root operation用集合を併置したため、whole sourceをroot operationへ分類できた。Candidate222は評価入力を変更せず、review terminal前のroot source viewから将来root operation用集合を削除し、packet配送許可viewだけを残すprompt-only差分を固定ADR9 r2で検証した。

固定ADR9 r2の結果、Candidate222でもroot whole-source deliveryとmixed-owner admissionはpacket case 20 / 20に残り、必要reviewは29 / 30、必要なreviewer direct observationは12 / 20だった。observation viewという分類を追加してもwhole-source invocation自体を発行不能にできなかったため、`quality_failed / mechanism_failed / stopped`とし、次Candidateは作成しない。

C222は、C221の`root_operation_set`を削除すれば閉じるという仮説を棄却した。現在の未閉鎖辺は、packet構築に必要なliteral値がreviewer専有値と同じcontainerにあり、rootのreadがprojectionとwhole outputの両方を実行できる結合である。C214からC222までの成立境界、棄却仮説、残存辺は[`review carrier bootstrap authority監査`](review-carrier-bootstrap-authority-audit.md)の累積閉鎖台帳を正本とする。

次は新しい制御文を作るのではなく、変更しないADR9 r2入力に、packet literalをsource外から供給するcarrierまたはwhole outputを実行不能にする既存authorityがあるかを監査する。現時点ではいずれも確認できていない。同じread surfaceへ分類名、禁止文または条件を追加する案は作成せず、安全性と必要review完遂を同時に満たす実在routeが見つかった場合だけCandidate作成gateへ戻る。

## 参照

- [Prompt制御の検討原則](prompt-control-design-principles.md)
- [Candidate214作成前設計](candidate214-packet-source-container-closure-design.md)
- [Candidate214方向監査](candidate214-packet-source-container-closure-direction-audit.md)
- [Candidate214 ADR9 r2 N=5結果](../evaluations/results/candidate214-packet-source-container-closure-adr9-r2-n5_2026-08-14.md)
- [Candidate216 ADR9 r2 N=5結果](../evaluations/results/candidate216-packet-construction-projection-adr9-r2-n5_2026-08-14.md)
- [Candidate217 ADR9 r2 N=5結果](../evaluations/results/candidate217-review-proposition-operand-closure-adr9-r2-n5_2026-08-14.md)
- [Candidate220 ADR9 r2 N=5結果](../evaluations/results/candidate220-review-observable-output-closure-adr9-r2-n5_2026-08-14.md)
- [Candidate221 ADR9 r2 N=5結果](../evaluations/results/candidate221-review-source-authority-closure-adr9-r2-n5_2026-08-14.md)
- [Candidate221 source authority closure原因分析](candidate221-source-authority-closure-causal-analysis.md)
- [review carrier bootstrap authority監査](review-carrier-bootstrap-authority-audit.md)
- [Candidate222 ADR9 r2 N=5結果](../evaluations/results/candidate222-review-source-observation-view-adr9-r2-n5_2026-08-14.md)
