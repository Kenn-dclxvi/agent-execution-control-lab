# Candidate81からCandidate125までのprompt制御知見

## 結論

Candidate81からCandidate125までで有効だったのは、agentへ抽象的な注意を増やすことではない。各operationについて、何が確定済みか、どのevidenceがどのpredicateを決めるか、どのresultで次の状態へ進めるかを、modelが実行時に観測できる条件へ閉じることである。

Candidate125は、この系列で別々に確認した次の制御を組み合わせた。

1. Candidate81のrequired validation全体を一つのroot validation waveとして完了させる制御。
2. Candidate104の初期evidenceをTaskSpec由来の範囲へ限定し、追加evidenceをdefault denyにする制御。
3. Candidate116のrequired outcomeとimplementation choiceを別状態として扱う制御。
4. Candidate118のimplementation bind後は変更前evidence operationをterminalにする制御。
5. Candidate119のvalidation predicateとvalidation実行方法を分離する制御。
6. Candidate122のexact target setが同じpredicateを決める場合にcontent evidenceを一つのwaveへ閉じる制御。
7. Candidate125の一つのeditable targetが全変更criterionを所有する場合だけ、criterion-completeな追加取得を一度許可する制御。

SolでのCandidate125はStandard14 N=5の70 / 70件がscore `4`、token中央値`1,401,225`、elapsed中央値`846.377秒`だった。A02 N=20でも20 / 20件がscore `4`で、implementation bind後・最初のartifact変更前のcommand再入は0件だった。

一方、同じCandidate125でもmodelをTerra / Lunaへ変えると品質とcostは維持されなかった。prompt制御はmodel非依存の保証ではない。modelは独立した互換条件として評価し、採用単位へ含める必要がある。

## 系列全体の見取り図

| 段階 | Candidate | 調べた問題 | 残った知見 |
|---|---|---|---|
| validation closure | C81 | 複数required commandの途中でmodelへ戻り、再判断・再実行する | required validationはroot wrapper内の個別invocationとして順序を保ち、全result受領後に一度だけ判断する |
| delegation control | C82〜C89 | Worker admissionやdispatch条件で重複作業を減らせるか | Worker起動条件では、上流のoperation identity誤分解を修復できない |
| output ingress | C90〜C93、C96 | promptでtool output配送量やprojectionを制御できるか | 配送、byte cap、projectionはexecutor側の性質であり、prompt predicateだけでは安定強制できない |
| criterion totality | C94〜C95 | owner、risk、unavailableを一般predicateへできるか | 新しいmeta-judgmentは正規routeの誤停止を増やす。N=5通過だけでtail stabilityを主張できない |
| evidence admission | C98〜C104 | 変更前の広い探索と証拠追加を止める | 説明labelではなく、初期admission集合と追加を開く具体的不足・矛盾を固定する |
| validation reentry | C105〜C111 | nonterminal result後のmodel再入を閉じる | wait-only遷移は有効だが、outer waitやresult配送方法はprompt設計層では完全に強制できない |
| authority boundary | C112〜C118 | outcome未確定、implementation未確定、authority探索を分離する | required outcomeとimplementation choiceを分け、implementation bindを変更前operationのterminal resultにする |
| evidence wave | C119〜C125 | A02 closureを維持しながらF02 costとF04 false stopを解く | exact target set、同一predicate、単一editable owner、criterion-complete continuationを組み合わせる |
| model axis | C125 Sol / Terra / Luna | 同一prompt制御が別modelでも維持されるか | model変更は品質・token・elapsedを変える。prompt adoptionをmodelから独立に扱わない |

## 1. Candidate81で確立した基準

Candidate81の主目的は効率改善ではなくvalidation closureだった。複数required commandを一つのshell compound commandへまとめず、root wrapper内から順序付きの個別invocationとして発行する。wrapperが各exitを確認し、nonzeroまたはunavailableで後続を止め、全resultを一度だけmodelへ返す。

Standard14 N=5は70 / 70件がscore `4`だった。複数required command caseのone-step closureはCandidate71の30 / 35から35 / 35へ改善した。一方、Candidate71比のtokenはほぼ同水準で、elapsedは`+5.78%`だった。したがって、Candidate81から得た知見は「wrapper化すれば安くなる」ではなく、「required validationの発行単位と最終判断点を固定すると経路が安定する」である。

Candidate81は長期stability evidenceも持つ。後続Rating v14 Standard14 B20の1,400 / 1,400件はscore `4`だった。この長期証拠は、Candidate125で未実施のStandard14 B20を代替しないが、Candidate81を安定性の参照点として残す理由になる。

## 2. Candidate82〜Candidate89で分かった委譲制御の限界

この系列は、producer規則の重複削除、Worker価値判定、execution plan、producer内部batching、same-wave admission、dispatch-time admissionを試した。

Candidate87は指定Workerを使うD01でCandidate86比token`-51.06%`、elapsed`-26.54%`を示した。しかしStandard14全体ではCandidate81比token`+6.09%`、elapsed`+1.35%`だった。局所routeの改善を全体cost改善へ一般化できない。

保存traceでは、rootが同じpredicateを処理しているのに独立Workerを起動する重複operationが確認された。Candidate88 / Candidate89がWorker admissionの時刻条件を細かくしても、誤って二つに分けたoperation identity自体は変わらなかった。

ここから残る規則は次のとおりである。

- Worker起動そのものを失敗条件にしない。
- 先にoperation identityとresult consumerを確定する。
- rootとWorkerが同じpredicateを消費するなら、admission条件ではなくoperation分解を疑う。
- targeted routeのcost低下とStandard14集約costを別gateにする。

## 3. Candidate90〜Candidate97で確認したpromptとexecutorの境界

Candidate90〜Candidate93は、raw tool outputをmodel contextへ入れる前のprojection、byte cap、result classをpromptで指定した。しかし狙ったprojectionやcapは安定せず、costも下がらなかった。Candidate96もsuccessful validation resultをidentity、command、exit codeだけへ投影しようとしたが、成功stdoutは全5件でmodelへ返った。

Candidate97はvalidation成功後の追加decision roundを閉じようとした。品質は維持したが、全5件で成功後に別の`git status`を発行し、completion closureは0 / 5だった。

この系列が示したのは、modelが選べる行動と、executorがmodelへ返すeventを混同してはいけないという点である。

- promptで制御できるのは、返されたresultをどう分類し、次に何を選ぶかである。
- output置換、byte cap、nonterminal return timing、tool adapter処理はexecutor側の性質である。
- executor方法を書いたpromptが偶然costを下げても、prompt Candidateの採用根拠にはできない。

## 4. Candidate94〜Candidate104で確立したevidence admission

Candidate94 / Candidate95は、operation criterionを全域化し、ownerをrequired non-machine judgmentへ限定しようとした。Candidate94はA02の正規authority routeを質問へ置換した。Candidate95はN=5を通過したが、Standard14 B20では1,400件中2件でowner clarification経路が再発し、costもCandidate81よりtoken`+4.49%`、elapsed`+5.53%`だった。

これは、risk、owner、judgment必要性を一つのmeta-predicateへまとめると、modelへ新しい判断を増やすことを示す。少数試験で見えないtail failureもある。

Candidate99〜Candidate103は、変更前の広い探索を止めるためにevidence scope、outcome source、追加調査trigger、evidence freeze、receiptを順に追加した。しかし「何を記録するか」を増やすだけでは、modelはauthority、fixture、start gateなどを新しい判断材料として追加できた。

Candidate104で初めて、初期evidenceをTaskSpec、明示開始状態、対象artifact、明示read-only path、適用中instructionへ限定し、追加evidenceをdefault denyにした。追加を開くのは、許可済みresultが具体的な不足または矛盾を示した場合だけである。Standard14は70 / 70 score `4`で、Candidate98比token`-6.48%`、elapsed`-9.77%`だった。

知見は「evidenceを先に宣言する」では不十分で、「初期集合と追加admission条件を閉じる」必要があるということである。

## 5. Candidate105〜Candidate111で分かったvalidation再入の構造

Candidate105 / Candidate106は、validation wrapperがnonterminal resultを返した後の遷移を同じsessionのwaitへ限定した。N=5では良く見えても、Candidate106 F03 B20では100件中1件で対象経路が再発した。

Candidate107はcell ID付きnonterminal result後を同じcell IDへのwait-only遷移にした。F03 B20では中間message 0 / 100、required validation再実行0 / 100、nonterminal後の同一cell wait 6 / 6を達成した。Standard14 N=5も70 / 70 score `4`、token中央値`1,523,137`だった。ただしouter deadlineが内部waitより短い違反が4 / 100件あり、Candidate107自体は採用できなかった。

Candidate108はexecutor時間値をpromptから除き、validation ticket全体のterminal closureへ戻した。品質とtargeted mechanismは通過したが、Standard14 tokenはCandidate107比`+15.75%`だった。Candidate109はouter yield最大値を指定してF03 costを下げたが、executor方法をpromptへ書いたため設計層gateで停止した。Candidate110 / Candidate111の抽象的なdecision / model-return boundaryもterminal前再入を完全には閉じなかった。

この結果から、Candidate107のtoken値は「採用可能なprompt」ではなく、「同じ固定executor条件でprompt差分だけにより到達したcost目標」として使う。一方、outer waitの完全強制はprompt Candidateの責務へ持ち込まない。

## 6. Candidate112〜Candidate118で確立したoutcomeとimplementationの分離

Candidate112〜Candidate115は、evidence scheduling、authority委譲、`spec_ready` phase、authority locationを個別labelで制御した。局所mechanismが通っても別caseの誤停止を起こし、A01とA02を一つのauthority条件で安定分離できなかった。

Candidate116は状態を二つに分けた。

- required outcome: 利用者に観測可能な成果値が確定しているか。
- implementation choice: outcomeを実現する具体的方法がrepository authorityから解決済みか。

この分離により、A01はoutcome未確定のまま変更・試験へ進まず、A02は固定済みoutcomeを実装へ変換できた。Standard14は70 / 70 score `4`、Candidate108比token`-9.26%`、elapsed`+0.25%`だった。

Candidate117はauthority admissionをさらに限定したが、A01 / A02で減った再入以上に他12 caseの再入が増えた。route固有のauthority制御をglobal proseとして適用するとspilloverが起こる。

Candidate118は、implementation choice、target、保持constraint、変更predicateがbindされたresultを変更前evidence operationのterminal resultにした。A02 N=20は20 / 20 score `4`、bind後・変更前再入0 / 20件だった。一方、Standard14 tokenはCandidate116比`+7.44%`だった。機構成立とcost改善は別である。

## 7. Candidate119〜Candidate125でcostとfalse stopを両立した過程

Candidate119は、TaskSpecが要求するvalidation predicateと、exact commandというexecution methodを分けた。変更後のvalidation-method探索は0 / 5へ減ったが、変更前再入が1 / 5残った。これは一つのpredicateで全経路を制御できないことを示す。

Candidate121はevidence requestごとにpredicate、target、result scope、後続判断をbindした。A02変更前再入は0 / 5になったが、F02ではlocator resultとcontent resultが二段階になり、token目標を超えた。result bytes、target数、invocation数のどれか一つを減らすだけではcostを説明できなかった。

Candidate122は、TaskSpec列挙済みのexact target setが同じpredicateを共同で決める場合だけ、content evidenceを一つのwaveへ閉じた。F02 token中央値は`124,719`、Standard14 token中央値は`1,403,840`まで下がった。しかしF04の1件で、初回取得範囲に必要箇所がなかっただけのread可能targetをterminal missingと誤分類した。

Candidate123のresult round数制限は、正常なdetached HEADをidentity未確定と誤分類した。round数は状態の代理値であり、完了predicateではない。

Candidate124は同一targetへの一回の追加readを許可したが、取得範囲がcriterionを覆わずF04 false stopを2件発生させ、F02 one-waveも崩した。「一回」や「620行」のような量的上限では、必要evidenceの完了を定義できない。

Candidate125は、continuationを次の意味条件へbindした。

- 一つのeditable targetが全未解決変更criterionを所有する。
- 他targetはvalidation capabilityまたは保持constraintだけを決める。
- continuationは未観測criterionへ直接bindしたsymbol context全体、または同じtargetの未取得content終端までを覆う。

これによりF04 false stopは0 / 5、F02 one-waveは5 / 5、F02 token中央値は`124,094`となった。Standard14は70 / 70 score `4`、token中央値`1,401,225`でCandidate107目標より`8.00%`低く、A02 terminal closureも維持した。

## 8. Candidate125のmodel-axis試験が追加した知見

Candidate125のprompt、Standard14、fixture、TaskSpec、rating、reasoning、CLI、permission、executor条件を固定し、modelだけを変えたN=5結果は次のとおりである。

| model | score `4` | quality中央値 | token中央値 | elapsed中央値 | Solとの差 |
|---|---:|---:|---:|---:|---|
| Sol | 70 / 70 | `100.000` | `1,401,225` | `846.377秒` | 基準 |
| Terra | 68 / 70 | `100.000` | `1,734,821` | `738.623秒` | token `+23.81%`、elapsed `-12.73%` |
| Luna | 67 / 70 | `92.857` | `3,307,759` | `958.889秒` | quality `-7.143`、token `+136.06%`、elapsed `+13.29%` |

Terraの未達はF07とF04に一件ずつ発生した。Lunaの未達3件はすべてA01 iteration 1〜3で、required valueが未解決のまま試験へ進んだ。LunaではA01の停止境界がmodelによって維持されなかったことが、品質未達と大きいtokenの両方へ現れた。

modelが異なるresultはcompatibility keyも異なる。したがって通常のLayer 4 prompt比較へ混ぜず、modelだけを宣言変更軸にした記述的比較として扱う。現在採用・投影済みのCandidate125はSol条件であり、Terra / Lunaの採用判断は行っていない。

## 統合した設計原則

### 1. 状態遷移を実測可能なresultへbindする

`ready`、`complete`、`owner`のようなlabelだけでは足りない。何を観測すればtrueになるか、どのresultで次状態へ移るか、どの条件で失効するかを定める。

### 2. outcome、implementation、evidence、validationを混ぜない

利用者が求める成果値、repositoryから決める実装方法、変更前に必要な証拠、変更後に必要なvalidationは別predicateである。一つのauthority判定やticketへまとめない。

### 3. evidenceは量ではなくconsumer predicateで閉じる

bytes、行数、target数、invocation数、result round数は完了の代理値にすぎない。どのpredicateが必要とするどのcriterionを観測済みかで完了を決める。

### 4. fast pathは適用条件を狭くする

Candidate122 / Candidate125のone-waveは、exact target set、同一predicate、単一editable ownerが成立する場合だけ有効である。一般read batchとして全caseへ広げない。

### 5. modelへ新しいmeta-judgmentを増やさない

owner必要性、追加調査価値、authority利用可否を新しい抽象判断として重ねると、誤停止または探索拡大を起こす。明示input、repository authority、machine-bound resultへ変換できる条件だけをpredicateにする。

### 6. prompt層とexecutor層を分ける

promptはmodelが観測したresult後の選択を制御できる。tool output変換、return timing、outer wait、adapter atomicityはpromptだけでは保証できない。executor診断結果をprompt Candidateの解決策へ昇格しない。

### 7. mechanism、quality、cost、stability、adoptionを別gateにする

局所mechanism通過は全体cost改善ではない。N=5成功はB20 tail stabilityではない。70 / 70 score `4`は採用、release、projectionを意味しない。Candidate125もStandard14 B20未実施riskを保持する。

### 8. 失敗Candidateを直系継承し続けない

Candidate121、Candidate123、Candidate124の失敗規則を積み重ねず、最後に成立した親へ戻り、成功したpredicateだけを別軸として再検証する。Candidate125がCandidate122を直接親にしたことが具体例である。

### 9. prompt identityだけでなくmodel identityも採用条件にする

同じpromptでもmodel変更により停止境界、探索量、token、elapsedが変わる。model別resultを互換比較へ混ぜず、promptとmodelの組を評価・採用単位にする。

## 現在状態と残るrisk

- Candidate125 Solは`adopted / release_projected / runtime_projected`である。
- Candidate81は直前の投影履歴とStandard14 B20長期stability evidenceとして保持する。
- Candidate125 Standard14 B20は未実施である。Candidate81のB20で代替しない。
- Candidate125 N=100追試は2026-08-01にregistered poolを各case30件まで拡張し、F04 score `2`を5件確認して停止した。N=30 selection resultは未作成で、N=50 partial batchは未採点・未登録である。
- Candidate125 Terra / LunaはN=5評価済みだが未採用である。
- 外部executor対応は、このrepositoryのprompt Candidate、backlog、再開条件へ含めない。

## 一次参照

- [Candidate81 Standard14 N=5](../evaluations/results/candidate71-candidate81-validation-wrapper-precedence-v13-medium-standard14-n5_2026-07-26.md)
- [Candidate81 / Candidate87 Standard14 N=5](../evaluations/results/candidate81-candidate87-producer-local-invocation-wave-v14-medium-standard14-n5_2026-07-29.md)
- [Candidate81 / Candidate95 Standard14 B20](../evaluations/results/candidate81-candidate95-required-judgment-owner-boundary-v14-medium-standard14-continuous-n5-b20-cli0146_2026-07-30.md)
- [Candidate98 / Candidate104 Standard14 N=5](../evaluations/results/candidate98-candidate104-staged-evidence-admission-v14-medium-standard14-n5-cli0146_2026-07-30.md)
- [Candidate106 / Candidate107 Standard14 N=5](../evaluations/results/candidate106-candidate107-validation-wrapper-reentry-closure-v14-medium-standard14-atomic-n5-cli0146_2026-07-31.md)
- [Candidate116 / Candidate118 Standard14 N=5](../evaluations/results/candidate116-candidate118-implementation-bind-terminal-closure-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-07-31.md)
- [Candidate121 F02 evidence route分析](candidate121-f02-evidence-route-analysis.md)
- [Candidate118 / Candidate125 Standard14 N=5](../evaluations/results/candidate118-candidate125-criterion-complete-single-target-continuation-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-07-31.md)
- [Candidate125 Sol / Terra / Luna model-axis N=5](../evaluations/results/candidate125-model-sol-terra-luna-v14-medium-standard14-n5-cli0146_2026-07-31.md)
- [Candidate125採用判断](candidate125-adoption-decision.md)
