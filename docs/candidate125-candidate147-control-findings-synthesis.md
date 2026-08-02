# Candidate125からCandidate147までのprompt制御知見

## 結論

Candidate125からCandidate147までで得た中心知見は、evidence取得やresult待機を一律に制限するのではなく、各resultが状態を変え得るoperation classだけを停止対象にすることである。

Candidate125は、一つのeditable targetに対するcriterion-complete continuationにより、Standard14 N=5で品質、変更前closure、costを同時に満たした。しかし、後続のN=100追試はcase別30件のregistered poolまで拡張した時点でF04のscore `2`を5件観測し、停止した。Candidate126からCandidate142は、この低頻度failureをEvidence coverage、Effect state、Change construction、Closure / recoveryへ分解した。局所gateの追加では部分変更とfalse stopのtradeoffを解消できなかったため、Candidate143はCandidate118へ戻り、required outcome全体のimplementation bindから再構築した。Candidate147は、その安全境界を保持したままresultの停止効果をoperation classへ限定し、Standard14 N=100の1,400 / 1,400件でscore `4`を記録した。現在は採用・release・runtime projectionまで完了している。

したがって、この系列は次の因果順序で読む。

1. Candidate125で、evidence completionを取得量ではなく未解決criterionの充足へbindした。
2. Candidate126からCandidate142で、evidence、effect、change、recoveryを一つのglobal readinessへ統合できないことを確認した。
3. Candidate143で、下流gateの追加を止め、required outcome全体のimplementation identityを上流で完成させた。
4. Candidate145で、consumerのないevidence取得を閉じた。
5. Candidate147で、安全性を緩めず、result待機の適用範囲だけを必要なoperation classへ狭めた。

## 用語

- `required effect`: TaskSpecが要求する、利用者または検証から観測可能な成果状態。
- `Evidence coverage`: required effectの状態を判断するために必要なcurrent contentをmodelが受領済みであること。
- `Effect state`: required effectが開始状態から充足済み、未充足、未観測のいずれであるか。
- `false stop`: TaskSpecとrepository authorityから成果を完成できるのに、制御が保守側へ倒れて停止すること。
- `mechanism gate`: Candidateが意図した制御変化が保存trace上の実挙動として成立したかを判定するgate。
- `N`: 各caseの反復数。Standard14 N=5は14 case × 5件、N=100は14 case × 100件を意味する。

## 系譜

Candidate番号は一本道の継承順ではない。主な系譜は次のとおりである。

```text
C122 -> C125 -> C126 / C127 / C128 -> C129 ... C142
                         |
                         +-- 局所gateの積み増しを停止

C118 -> C143 -> C144 -> C145 -> C146（mechanism不成立で停止）
                                 |
                                 +-> C147（採用・投影済み）
```

Candidate143はCandidate142の直接childではない。Candidate122以降を継承せず、成立していたCandidate118のimplementation-bind terminal closureへ戻った。この巻き戻しは、失敗規則を蓄積せず、最後に成立した設計境界から一軸ずつ再構築するという重要な判断である。

## 1. Candidate125: N=5で成立した局所最適

Candidate125はCandidate122を直接親とし、停止したCandidate123とCandidate124を継承していない。一つのeditable targetが全未解決変更criterionを所有する場合だけ、同じtargetに対するcriterion-complete continuationを一度許可した。

保存結果は次のとおりである。

- Standard14 N=5は70 / 70件がscore `4`。
- token中央値は`1,401,225`。
- elapsed中央値は`846.377秒`。
- A02 N=20は20 / 20件がscore `4`。
- implementation bind後、最初のartifact変更前のcommand再入は0 / 20件。
- F04 false stopは0 / 5、F02 content waveは5 / 5。

Candidate125が確立したのは、「一回」「特定行数」「特定bytes」のような量ではなく、consumer predicateが必要とするcriterionを観測済みかによってevidence operationを閉じる原則である。Candidate125は2026-07-31の明示判断で採用され、内容同一releaseが当時のTHE-CAPTIONへ投影された。

一方、後続のN=100追試はcase別30件のregistered poolまで進んだ時点で、F04のscore `2`を5件観測した。正式なN=30 selection resultは作成しておらず、N=50 partial batchも正式結果へ含めない。この追試により、Candidate125はN=5の品質・cost gateを通過したが、低頻度安定性は未達だったと再解釈する。

## 2. Candidate126からCandidate132: 六点への責務分離

Candidate126からCandidate132は、Candidate125のF04失敗を単一原因として扱わず、次の六点へ分解した。

1. Authority: 何を成果として要求し、実装方法をどこから解決するか。
2. Evidence coverage: 判断に必要なcurrent contentを受領済みか。
3. Effect state: 各required effectが充足済み、未充足、未観測のいずれか。
4. Dependency: 複数effectの関係がTaskSpecの成果条件に含まれるか。
5. Change construction: 変更が最新の観測済みcurrent contentから構成されているか。
6. Closure / recovery: 変更result後も全required effectを保持し、validation、rework、停止を選べるか。

| Candidate | 変更軸 | 保存結果 | 判定 |
| --- | --- | --- | --- |
| C126 | 変更単位を未充足criterionと観測済みoperandへbind | F04 N=5、score `4 / 2 = 3 / 2` | stale hunkは閉じたがfalse stopが増え、停止 |
| C127 | 失敗hunkを捨て、独立した必要変更だけを一回救済 | Standard14 N=5は70 / 70 score `4`。F02 N=29でscore `2`が2件 | hunk単位ではrequired effectが脱落するため停止 |
| C128 | `required_effects_closed` | F02 / F04 / F07各N=5、15 / 15 score `4` | required effect集合を失敗後も保持する基準として成立 |
| C129 | 観測済み未充足effectだけを初回変更へadmit | F04 N=5、false stop 3 / 5 | 未観測effectが観測済み未充足effectの変更まで止めた |
| C130 | bind済みsymbolのfocused continuationを優先 | F04 N=5、focused continuation 0 / 5、false stop 3 / 5 | 抽象的symbol分類では取得経路を固定できず停止 |
| C131 | criterionごとのexact anchorを全一致箇所へbind | N=5通過後、N=29でscore `2` 1件 | anchorがあってもglobal readinessがfalse側へ倒れ、停止 |
| C132 | 変更preimageだけを最新観測exact valueへbind | stale preimage 0 / 5、score `2` 1件 | 独立global preimage gateがvalidation false stopを生み、停止 |

この段階で、六点を一つのglobal predicateへまとめないことを確定した。変更前の未観測と、変更後の未充足を同じfalseへ潰すと、必要な変更まで止めるか、未証明effectを脱落させる。Change constructionはEvidence coverageへ従属させ、独立した全域gateにしない。

## 3. Candidate133からCandidate142: 下流gate追加の限界

Candidate133からCandidate142は、anchor、lexeme、effect-local admission、pending validation、複数target relationを順に厳密化した。

| Candidate | 変更軸 | 主な観測 | 判定 |
| --- | --- | --- | --- |
| C133 | anchorをcontinuation resultの先頭へ置く | F04 5 / 5 score `4`、anchor-first 4 / 5 | 品質は通過したがmechanism不成立で停止 |
| C134 | criterionからcode-shaped lexemeを構文抽出 | direct lexeme 5 / 5、full fallback 3 / 5、score `3` 1件 | 直接取得だけでは上流definition coverageを保証できず停止 |
| C135 | 検索語authorityを明示criterion spanへ限定 | criterion外lexeme 0 / 5、all-lexeme-first 3 / 5、score `2` 1件 | request authorityだけでは変更failureを閉じられず停止 |
| C136 | effectを三値bindし、未充足だけを変更へadmit | effect-local admission成立、criterion member脱落1件 | effect単位だけではrelation memberを保持できず停止 |
| C137 | 未観測effectをrequired validationへ保留 | N=5通過後、N=53でscore `2` 1件 | 対象runが前段gateで停止し、追加した経路へ到達せず停止 |
| C138 | continuation後の未充足effectを変更へhandoff | F04 N=29は29 / 29 score `4`。F02 / F04 / F07ではscore `2` 2件 | 複数target admission leakにより停止 |
| C139 | handoffへsingle-target条件を追加 | score `2` 4 / 15 | target集合の動的縮退により部分変更が残った |
| C140 | relationの全memberと接続をsatisfaction witnessにする | score `2` 2 / 15 | witnessが見えても一部targetだけを変更するrunが残った |
| C141 | target content量をrelation coverageへ置換 | score `2` 1 / 15 | 限定取得は改善したが、全体取得runで部分変更が残った |
| C142 | joint owner domainでは全effect観測後だけ初回変更を許可 | F02部分変更0 / 5、score `2` 3 / 15 | 部分変更は閉じたが、過大取得後の無変更停止へ転化した |

この系列では、部分変更を閉じる下流gateを厳しくするほどfalse stopが増える構造が確認された。問題は変更直前のadmissionだけではなく、required outcome全体のimplementation identityが前段で完成していないことだった。

## 4. Candidate143からCandidate145: 安全境界の上流再構築

### Candidate143

Candidate143はCandidate118を直接親とし、変更前evidence operationのterminal resultを、TaskSpec上の全change effectとartifact間relationを含むrequired outcome全体のimplementation bindへ置換した。

- F02 / F04 / F07 N=100は300 / 300件がscore `4`。
- Standard14 N=5は70 / 70件がscore `4`。
- Candidate125比でtoken中央値`+24.98%`、elapsed中央値`+17.30%`。

安全性と対象stabilityは成立したが、costが増加した。ここで、mechanism、quality、stability、costを別gateとして扱う必要が再確認された。

### Candidate144

Candidate144はrequired outcome bindを維持し、TaskSpecが要求するvalidation predicateと、具体的なcommandというexecution methodを分離した。

- 6 case N=5は30 / 30件がscore `4`。
- A02 token中央値はCandidate143比`-23.50%`。
- 変更前再入1 / 5、変更後method探索1 / 5が残った。

品質と局所costは改善したが、狙ったclosureが完全ではないためmechanism gateで停止した。

### Candidate145

Candidate145はrepository evidenceを、未観測required predicateと欠けた観測値を結び付けられるconsumerが存在する場合だけ許可した。

- 6 case N=5は30 / 30件がscore `4`。
- A02の変更前再入は0 / 5。
- consumerのないevidence再入は0 / 30。
- Standard14 N=5は70 / 70件がscore `4`。
- Candidate125比でtoken中央値`+13.74%`、elapsed中央値`+31.04%`。

`evidence_consumer_ready`はread回数制限ではない。未観測effectの判定に必要なread、TaskSpec-requiredな変更後source確認、無断変更判定のためのdiff / statusは許可する。一方、念のための再読、method選択だけの探索、成立済み判断の再確認、報告だけのreadは閉じる。

保存traceを`agent_message`境界で再集計すると、Candidate125とCandidate145のF01 / F02 / F03はいずれもsource / testを15 / 15件で同じmodel stepから共同発行していた。主な差は開始identityだった。Candidate125は13 / 15件でidentityとcontentを同じstepから発行したのに対し、Candidate145は15 / 15件でidentity result後にcontentを別stepから発行した。この追加stepがcached input増加と整合する。

## 5. Candidate146: mechanism gateの優先

Candidate146は、同じrequired predicateへ入る相互非依存の既知観測をconsumer closureの共同resultへbindした。

- F01 / F02 / F03各N=5は15 / 15件がscore `4`。
- Candidate145比でtoken中央値`-4.50%`、elapsed中央値`-5.61%`。

しかし、再監査ではCandidate145とCandidate146の両方がsource / testを15 / 15件で既に共同発行していた。Candidate146で変更前model stepの削減は確認できず、狙った増分mechanismは成立していない。品質と集約KPIが良くても、差分を狙った制御へ帰属できないため停止した。

この結果は、quality gateやcost gateがmechanism gateを代替しないことを示す。Candidateの採否は、aggregateが良いかだけでなく、変更したpredicateが保存trace上の実挙動を変えたかで判断する。

## 6. Candidate147: resultの停止効果をoperation classへ限定

Candidate147はCandidate145を直接親とし、`DECISION_BOUNDARY`の一軸だけを`result_effect_scope`へ置換した。

```text
result_effect_scope :=
  resultがtarget、permission、method、stop conditionを
  実際に変え得る未発行operation classの集合
```

開始identity resultはartifact変更とrequired validationを止め得る。一方、TaskSpecで既に許可されたreadは止めない。そのためidentity確認と許可済みreadを同じmodel stepから発行し、共同resultを受領して正常と判定するまで、artifact変更とrequired validationだけを閉じる。

保存結果は次のとおりである。

- F01 / F02 / F03各N=5で、開始identityと初回許可readの共同発行15 / 15。
- 同じ共同resultを受領する前のartifact変更とrequired validationは0 / 15。
- Standard14 N=100は1,400 / 1,400件がscore `4`。
- score `3`以下、excluded attempt、controller error、command protocol violationは各0件。
- N=29、53、77、100の各waveで停止条件なし。
- Candidate145比でtoken中央値`-9.17%`、elapsed中央値`-23.13%`。
- N=100のtoken中央値は`1,394,412.5`、elapsed中央値は`831.914秒`。

Candidate125 N=5の中央値に対して記述上はtoken`-0.49%`、elapsed`-1.71%`だが、Nが異なるため統計的にCandidate147が低costとは主張しない。採用理由は、Candidate145との互換比較で安全境界追加後のcostを回収し、Candidate125付近のcost水準でStandard14 N=100の安定性を得たことである。

Candidate147は2026-08-03の明示判断で採用された。内容同一releaseは公開版`the-caption`へ投影済みであり、release status、approval、runtime projectionはいずれも`projected / approved / projected`である。本番運用checkoutの更新とは別状態である。

残存riskはF06のauthority追加read 21 / 100件である。発生群のtoken中央値`160,327`は非発生群`104,230`より`53.82%`高い。一方、F06全体は100 / 100件がscore `4`で、token中央値もN=29以降約`105k`で安定した。このため品質failureではなく、受容済みの高token裾riskとして保持する。

## 7. 統合した設計原則

### 7.1 完了を量の代理値で判定しない

bytes、行数、read回数、target数、invocation数、result round数はevidence completionの代理値である。完了は、consumer predicateが必要とするcriterionを観測済みかで判定する。

### 7.2 Evidence coverageとEffect stateを分ける

未観測と未充足を同じfalseへ潰さない。未観測effectは証拠不足、観測済み未充足effectは変更対象であり、異なる次遷移を持つ。

### 7.3 required outcome全体をimplementationへbindする

複数targetやrelationを持つtaskでは、個別effectのchange admissionを追加する前に、TaskSpec上のrequired outcome全体をimplementation choice、target、保持constraint、変更predicateへbindする。

### 7.4 resultの停止効果をtask全体へ広げない

result待機は、そのresultがtarget、permission、method、stop conditionを変え得るoperation classだけへ適用する。安全性と無関係な許可済みreadまで止めると、model stepとcached inputを増やす。

### 7.5 mechanism、quality、cost、stability、adoptionを別gateにする

局所mechanism通過は全体cost改善ではない。N=5成功はtail stabilityではない。高品質・低costでもmechanism不成立なら採用根拠にならない。評価済みであることは、採用、release作成、projectionを意味しない。

### 7.6 失敗Candidateを直系継承し続けない

失敗したglobal gateを積み増さず、最後に成立した親へ戻り、保存traceで支持された一軸だけを再構築する。Candidate143がCandidate118へ戻り、Candidate147がCandidate145の一軸だけを置換したことが具体例である。

### 7.7 prompt層とexecutor層を分ける

promptが制御できるのは、model-visible resultをどう分類し、次に何を選ぶかである。output置換、byte cap、nonterminal return timing、tool adapter、yield / wait、runtime hookはexecutor側の性質であり、prompt Candidateの解決策へ持ち込まない。

### 7.8 modelを互換条件と採用単位へ含める

この系列の主要結果は`gpt-5.6-sol / medium`条件である。同じpromptでもmodel変更により停止境界、探索量、token、elapsedが変わる。prompt identityだけでなくmodel identityもcompatibility keyと採用単位へ含める。

## 結論表

| 段階 | 到達点 | 成立した知見 | 残った問題または最終状態 |
| --- | --- | --- | --- |
| C125 | criterion-complete single-target continuation | evidenceを量ではなくcriterion充足で閉じる | N=5通過後、N拡張でF04低頻度failure |
| C126〜C132 | evidence / effect / change / recovery分離 | 六点を一つのglobal predicateへ統合しない | stale changeを閉じるほどfalse stopが増加 |
| C133〜C142 | anchor、pending effect、relation、joint admission | 下流gate追加だけでは部分変更とfalse stopを両立解消できない | C142で部分変更が無変更停止へ転化 |
| C143 | required outcome implementation bind | required outcome全体を上流で完成させる | N=100対象stability通過、cost増加 |
| C144〜C145 | validation method分離とconsumer evidence gate | consumerのない探索・再読を閉じる | 品質通過、Candidate125比cost増加 |
| C146 | consumer closure | qualityとKPIだけではmechanism成立を証明しない | 増分mechanism不成立で停止 |
| C147 | result effect scope | 安全性を維持し、待つoperation classだけを限定する | Standard14 N=100 1,400 / 1,400 score `4`、採用・投影済み |

## 現在状態

- Candidate147は`standard14_n100_evaluated / adopted / release_projected / runtime_projected`である。
- Candidate125は過去の採用・投影履歴として保持する。後続N=100追試の停止結果は過去のN=5評価と投影事実を遡及変更しない。
- Candidate126からCandidate142およびCandidate144、Candidate146の停止結果は削除せず、失敗mechanismと再開条件の証拠として保持する。
- Candidate147のF06 authority追加readを残存cost riskとして保持する。
- 他model、他reasoning、他targetへの一般化は別の互換条件であり、現在の採用状態に含めない。

## 一次参照

- [Candidate125設計](candidate125-criterion-complete-single-target-continuation-design.md)
- [Candidate125採用判断](candidate125-adoption-decision.md)
- [Candidate125 N=100追試停止結果](../evaluations/results/candidate125-criterion-complete-single-target-continuation-v14-medium-standard14-atomic-reuse-n100-stopped-at-pool-n30-cli0146_2026-08-01.md)
- [Candidate125からCandidate132 六点control統合](candidate125-candidate132-six-point-control-synthesis.md)
- [Candidate143 F02 / F04 / F07 N=100](../evaluations/results/candidate143-required-outcome-implementation-bind-v14-medium-f02-f04-f07-atomic-reuse-n100-cli0146_2026-08-02.md)
- [Candidate145 lifecycle consumer gate](candidate145-lifecycle-consumer-evidence-admission-design.md)
- [Candidate145 cost原因分析](candidate145-f01-f02-f03-cost-causal-analysis.md)
- [Candidate146 model step境界監査](candidate146-model-step-boundary-audit.md)
- [Candidate147設計](candidate147-result-effect-scope-design.md)
- [Candidate147 Standard14 N=100](../evaluations/results/candidate147-result-effect-scope-v14-medium-standard14-atomic-reuse-n100-cli0146_2026-08-02.md)
- [Candidate147採用判断](candidate147-adoption-decision.md)
- [Candidate147 release](../prompts/releases/the-caption-3ce91a4-result-effect-scope-release-r1/README.md)
