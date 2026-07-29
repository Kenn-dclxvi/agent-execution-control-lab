# Candidate94 operation criterion totality設計記録

## 結論

Candidate94はCandidate81を直接sourceとする。変更軸は、operation-localなcriterion stateを開始前のreadinessからproducer terminal後のfailure resultまで一意に閉じることである。

root `AGENTS.md`の`SPEC`、`TERMINAL`、`OWNER_ROLE`だけを置換する。`spec_ready`をoperation単位へ明示し、`non-machine risk=none`がbind済みのcriterionへ`criterion owner=none`をbindし、bind済みproducerがterminalでもdelegated resultをbindできない場合は`unavailable`をterminal failure resultとしてbindする。

## Candidate作成前gate

1. 基準prompt setは`the-caption-3ce91a4-validation-wrapper-precedence-r1`（Candidate81）とする。最短正常経路は、各operationのrequired valueだけをbindし、machine-only criterionではowner clarificationを追加せずroot producerへ進み、明示worker operationではruntime identityとfinal resultをcriterionへbindしてterminalを判断する経路である。
2. 2026-07-30のread-only semantic auditでは、現在本文から`spec_ready`をTaskSpec全体へ伝播する解釈、machine-only criterionでもowner未固定として全predicateを開始不能にする解釈、producer terminal後の`unavailable`をresult欠落として永久にnonterminalへ残す解釈が出力された。この監査応答を保存済み解釈traceとし、非公開の会話全文はrepositoryへ取り込まない。
3. 既存TaskSpec、repository authority、repository stateだけでは、`spec_ready`の式にoperation引数がなく、`non-machine risk=none`時のowner値と`unavailable`のterminal性も本文にないため、三つの解釈を一意に排除できない。
4. 置換する一つの変更軸は`operation criterion totality`である。各operationのreadinessを別operationから分離し、riskがないcriterionにもowner値を全域化し、bind済みproducerのterminal後はdelegated criterionもterminal resultへ全域化する。
5. この変更軸が消す判断点は、別operationの未固定値を伝播させるか、machine-only criterionへowner clarificationを要求するか、回復不能なdelegated result欠落をnonterminalへ残すか、というcriterion stateの三つの未定義分岐である。
6. 新たに増える判断点はない。既存の`non-machine risk`、producer terminal、`delegated_result_ready`だけを使う。`unavailable`をterminal failureへ分類するため、別producerへの再割当て、root補完、retryは追加しない。
7. targeted評価は、machine-only root operation、明示workerの正常result、Senderまたはtask identity不一致、producer terminal後のresult欠落を同一TaskSpec・fixture・runtime条件で確認する。candidateは各case `N=5`で全件valid・rateable・score `4`、正常worker route 5 / 5、`owner=none` route 5 / 5、`unavailable` terminal failure route 5 / 5を必須とする。
8. token、tool call、model step、worker数は診断として記録する。主判定は不要clarification 0件、正常worker route回帰0件、回復不能nonterminal 0件であり、cost改善はcandidate成功条件にしない。
9. `owner=none`がmachine-only criterionで5 / 5成立しない、正常worker resultを`unavailable`へ誤分類する、`unavailable`後にroot補完または別producer再割当てを行う、operation failureを別operationまたはtask全体へ伝播させる、score `4`未満、required result欠落、許可外driftのいずれかがあれば停止する。targeted通過前に標準14、採用、release、本体反映へ進めない。

九項目を固定済みであるため、Candidate94のfull bundleと構造testを作成できる。評価case、rating revision、profileは別artifactとして固定し、candidate作成と同じ比較単位へ混ぜない。

## 変更境界

- direct source: Candidate81
- 変更target: root `AGENTS.md`一つ
- 置換label: `SPEC`、`TERMINAL`、`OWNER_ROLE`
- 非変更: `PRODUCER`、`CONTEXT`、`ROOT`、`INDEPENDENCE`、`DECISION_BOUNDARY`、`VALIDATION_CLOSURE`、`METHOD`、`RECOVERY`と残り18 target
- 非目標: TaskSpec schema変更、worker起動条件変更、retry追加、root補完、評価条件変更、採用、release、runtime projection

## Candidate状態

- candidate number: Candidate94
- prompt identity: `the-caption-3ce91a4-operation-criterion-totality-r1`
- evaluation status: `not_evaluated`
- state: `draft`
- release: `not_created`
- runtime projection: `not_projected`

## 後続評価状態

2026-07-30のユーザー明示依頼により、targeted gateより先に[`Rating v14 Medium標準14 N=5`](../evaluations/results/candidate81-candidate94-operation-criterion-totality-v14-medium-standard14-n5-cli0146_2026-07-30.md)を実行した。Candidate94は70 / 70 valid・rateableだったが、score分布は`4 / 1 = 69 / 1`だった。A02 iteration 5の成果未達により事前停止条件へ該当したため、後続状態を`standard14_evaluated / quality_gate_failed / stopped`とする。上記の構築時状態とmanifestは履歴として変更しない。

## Evidence

- [Candidate81 bundle](../prompts/candidates/the-caption-3ce91a4-validation-wrapper-precedence-r1/manifest.json)
- [Prompt制御の検討原則](prompt-control-design-principles.md)
- [Candidate34 owner result state separation result](../evaluations/results/candidate34-owner-result-state-separation-owner-producer-v5-targeted2-expanded12-n5_2026-07-18.md)
- [Candidate31 operation terminal closure result](../evaluations/results/candidate31-operation-terminal-closure-owner-producer-v5-expanded12-global-m24-n5_2026-07-18.md)
