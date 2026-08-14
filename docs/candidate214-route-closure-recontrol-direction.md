# Candidate214経路閉鎖の再制御方針

## 状態

- `current_frontier`
- `candidate_not_created`
- `evaluation_not_started`

## 結論

review制御の次の出発点は、Candidate214で成立した経路閉鎖とする。Candidate214の過剰遮断は、「必要な場合だけ読む」という条件付き判断で緩めない。必要値のowner、carrier、read permissionとobservable output境界を実行前に一意化し、閉鎖した誤経路を再開せずに正常経路を成立させる。

Candidate215からCandidate220までは、Candidate214の過剰遮断を解消するための親として扱わない。これらは、必要性、投影状態、operand、ownership、ticketまたはwork itemをモデルが正しく判定することに依存し、誤経路のpermissionが残った反例群として保持する。

## Candidate214で保持する制御

Candidate214 ADR9 r2 N=5では、次の経路が実際に閉じた。

- packet投影元sourceの再readはCandidate213の6回から0回になった。
- rootによるreviewer-owned targetの先読みはCandidate213の1件から0件になった。
- projected source、mixed source、manifest外sourceのreviewer readは0件だった。
- 別containerにあるADR07とADR09の必要paired observationは各5 / 5で残った。

保持するのはCandidate214の文面全体ではない。保持するのは、packetに使ったsourceへの別selector、部分抽出または別commandによる再到達と、rootによるreviewer-owned値の先行消費を、モデルの必要性判断に依存せず発行不能にする境界である。

## 過剰遮断の原因

Candidate214はpacketへ実際に投影した値ではなく、その値を供給したsource container全体を閉じた。そのためADR03の1件、ADR05の2件、ADR06の1件で、packetへ未投影のcurrent inventory membershipまたはconsumer contractに到達できず、期待`blocked`が`unavailable`になった。

これは、不要なreadと必要なreadの判断精度が低かった問題ではない。必要値をどのproducerが観測し、どのcarrierでreviewerへ渡すかが実行前に固定されていないまま、container全体のreadだけを禁止したことが原因である。

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

## 次Candidate作成前の停止gate

次の全件を一次アーティファクトとmodel-visible inputで固定できるまで、Candidate bundle、profileまたは評価slotを作成しない。

1. Candidate214の4品質失敗で必要だった値の正確なownerと合法なcarrier。
2. packet投影元sourceの再readとrootによるreviewer-owned値の先行観測を合法にしている権限辺の全件。
3. 権限辺を削除した後も、ADR03、ADR05およびADR06の必要値が誤経路なしにreviewerへ到達すること。
4. モデルが判断順、必要性分類または自己申告を変えても、対象の失敗invocationがprompt準拠として構成できないこと。
5. 必要値のcarrierを現行prompt境界で強制できない場合に、別条件でread permissionを再開せず`prompt_control_not_demonstrated / candidate_not_created`で停止できること。

現時点では、TaskSpecがCandidate214の4失敗で必要だったcurrent valueのpacket carrierを許すか、またはrootへwhole-container outputを返さずreviewerだけが観測できるexact targetをpromptが発行前に一意化できるかが未固定である。したがって次Candidateは作成しない。

## 参照

- [Prompt制御の検討原則](prompt-control-design-principles.md)
- [Candidate214作成前設計](candidate214-packet-source-container-closure-design.md)
- [Candidate214方向監査](candidate214-packet-source-container-closure-direction-audit.md)
- [Candidate214 ADR9 r2 N=5結果](../evaluations/results/candidate214-packet-source-container-closure-adr9-r2-n5_2026-08-14.md)
- [Candidate216 ADR9 r2 N=5結果](../evaluations/results/candidate216-packet-construction-projection-adr9-r2-n5_2026-08-14.md)
- [Candidate217 ADR9 r2 N=5結果](../evaluations/results/candidate217-review-proposition-operand-closure-adr9-r2-n5_2026-08-14.md)
- [Candidate220 ADR9 r2 N=5結果](../evaluations/results/candidate220-review-observable-output-closure-adr9-r2-n5_2026-08-14.md)
