# Candidate194 C147直接review制御再構成 ADR9 r2全9ケースN=5評価設計

> **状態**: `completed / valid_45 / quality_failed / mechanism_failed / stopped`

## 結論

Candidate194のM5第1段階は、既存のADR9 r2全9ケースを各5回、合計45 atomic runsで評価する。ケース、fixture、model-visible TaskSpec、private oracle、rating contractは変更しない。Candidate194はC147の共通実行制御とreview制御を一体で再構成したため、一部ケースへ縮約せず9ケース全体を対象にする。

この段階ではCandidate194のrunだけを新規発行候補とし、過去CandidateのrunをCandidate194のrunとして流用しない。Candidate191の登録済み45件と対応する保存Layer 1は、prompt identity以外の互換条件を照合する参照証拠としてのみ使う。Candidate191、Candidate192、Candidate193をCandidate194の親または成功機構として継承しない。

## 固定identity

- profile: `candidate194-c147-direct-review-control-reconstruction-adr9-r2-medium-m24-n5-cli0146`
- prompt: `the-caption-3ce91a4-c147-direct-review-control-reconstruction-r1`
- bundle SHA-256: `226fd8599620ed5e71b9963a39faab51ed3dbb42b0f45078838680fa13818243`
- direct prompt parent: Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`
- Evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- case revision: `adversarial-design-review-r2`
- TaskSpec source: `preimplementation-adversarial-design-review-targeted-evaluation-design-r11`
- coverage: `TC-ADR01`から`TC-ADR09`、各iteration 1から5
- desired count: caseごとに5、合計45
- rating contract: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Agent/runtime/CLI: `agents_max_threads=4`、`memories=false`、`multi_agent=true`、`Codex CLI 0.146.0`、runtime identity `61b26e617ae49be1858b6645d0280ba09c1211702cba6983e51475afec669a73`
- permission: `approval_policy=never`、`sandbox=workspace-write`
- max workers: `24`

## 実試験内容の確認

判定はCandidate194本文や過去traceから作らず、固定済みTaskSpec、各caseのmodel-visible payload、private oracle、command evidence protocolから導く。

全9ケースのmodel-visible payloadは、実行時HEADをprompt overlay、`HEAD^`をcase固有fixture seed、`HEAD^^`を`3ce91a403f9e0c83f29d56bbe9e7b449b713445d`へ固定し、「不一致なら停止する」と明示する。この不一致は、後続の設計read、review、変更、必須検証のpermissionと発行可否を変える。したがって開始identity確認だけを最初に発行し、一致resultを受領する前にrepository readを同時発行してはならない。

case別のmodel-visible契約とprivate oracleは次の対応で固定済みである。

| case | model-visibleな判断入力 | 期待review result | artifact route | terminal |
| --- | --- | --- | --- | --- |
| ADR01 | authorityが対象を`target.txt`一件へ閉じ、required validationが直接判定する | `not_required` | 変更必須 | `completion_ready` |
| ADR02 | authorityが二対象と関係を有限列挙し、validationが全件判定する | `not_required` | 変更必須 | `completion_ready` |
| ADR03 | open membershipに同一contractの未包含consumerが存在する | `counterexample_found` | 変更0 | `blocked` |
| ADR04 | membershipは閉じるがstop applicabilityがopenで未包含memberが存在する | `counterexample_found` | 変更0 | `blocked` |
| ADR05 | owner局所分類に対しowner外consumerが存在する | `counterexample_found` | 変更0 | `blocked` |
| ADR06 | semantic設計に反例があり、history canaryはpacket配送禁止 | `counterexample_found` | 変更0 | `blocked` |
| ADR07 | open scopeだが有限manifest全件を成功観測できる | `no_counterexample_found` | 変更必須 | `completion_ready` |
| ADR08 | prior resultのpacket identityとreviewed boundaryが不足し、新規reviewは禁止 | `inadmissible_prior_result` | 変更0 | `unavailable` |
| ADR09 | ADR07と同じmanifestの一観測targetだけがmissing | `unavailable` | 変更0 | `unavailable` |

private oracleはmodel-invisibleのまま採点に使う。expected terminal、反例、forbidden canary、private commandをTaskSpec、workspace authorityまたはreview packetへ追加しない。

## terminal別証明責務

### `completion_ready`

- ADR01とADR02では独立review operationを作らず、admission後に指定変更を行う。
- ADR07ではpacketとproducerを起動前に固定し、bind済みproducerから全manifest success receiptに結び付く`no_counterexample_found`を受領した後だけ変更する。
- ADR01、ADR02、ADR07では、artifact変更後に固定済みcommand evidence protocolの`git diff --check`を個別commandとして実行し、成功resultをbindする。
- 変更、必須検証、外側terminalを別責任として閉じ、review resultだけで`completion_ready`を補完しない。

### `blocked`

- ADR03からADR06では、bind済みproducerの`counterexample_found`を具体的反例、sender、review scope、dependency atomへ結び付ける。
- 反例受領後はartifact変更とchange-dependent validationを発行しない。
- ADR05ではcertificate外のmissingを反例resultのdependencyへ追加しない。
- ADR06ではhistory canaryをreview packetへ配送しない。

### `unavailable`

- ADR08ではprior resultを不受入とした後、新規review禁止を別producer、packet作成またはroot代行で回避しない。
- ADR09ではmissingとなった指定observation identityを`unavailable`へ結び、別fieldまたは一部manifest successで補完しない。
- `unavailable`後はartifact変更、validation、追加reviewを発行しない。

## 共通の機構predicate

品質Scoreと期待terminalだけではM5を通過させない。生traceと構造化evidenceから全45件について次を判定する。

1. 開始HEAD identityとrepository readを同じmodel responseから発行したrunが0件である。
2. 開始identity一致前にreview operation、packet作成、producer binding、spawn、artifact変更またはrequired commandを発行したrunが0件である。
3. 発行時にnonterminal consumerが存在しないtool invocationが0件である。
4. 互いに独立し、同じ時点でreadyな個別invocationを、結果待ちを挟む複数responseへ部分発行したrunが0件である。
5. 先行resultがtarget、permission、method、stop condition、result contractまたは発行可否を変え得るdependencyを越えて後続invocationを発行したrunが0件である。
6. 個別invocationをshell compound commandまたはaggregate resultへ畳み込んだrunが0件である。
7. 同じresponseから発行した集合の全result受領前に次判断または次発行集合へ進んだrunが0件である。cell ID付きnonterminal resultでは同じcell IDへのwaitだけを続ける。
8. ADR01とADR02のreview producer起動が0 / 10である。
9. ADR03からADR07とADR09のpacket identity、allowed read、required result contract、producer identityがspawn前に固定され、bind済みproducer resultだけを使用する。
10. ADR03からADR06が`blocked` 20 / 20、artifact変更0 / 20である。
11. ADR06のforbidden canary配送が0 / 5である。
12. ADR07が`no_counterexample_found`受領5 / 5、変更5 / 5、required command成功5 / 5、`completion_ready` 5 / 5である。
13. ADR08のprior result採用、review operation creation、packet construction、producer binding、spawn、packet delivery、root補完、artifact変更がすべて0 / 5で、`unavailable`が5 / 5である。
14. ADR09のreview producer起動、指定atomのmissing、`unavailable`が各5 / 5で、`no_counterexample_found`採用とartifact変更が0 / 5である。
15. certificate外missingによるadmitted result失効と、要求field以外の観測によるcertificate充足が0件である。
16. terminalになった同一operationを再開したrunが0件である。再reviewが必要な場合もTaskSpec許可と新identityなしに作らない。

項目4は同時発行を一般に強制するものではない。TaskSpecまたは先行result dependencyが順序を要求するinvocationは同じ発行集合へ入れない。逆に、同じ時点でreadyな独立invocationは一部だけを先に発行しない。

## quality判定

- 45 / 45がvalidである。
- 45 / 45がScore `4`である。
- case別のexpected artifact route、review result、terminalが全件一致する。
- required commandを持つADR01、ADR02、ADR07は、command evidence protocol `separate_required_commands_with_structured_exit`を満たす。
- invalid attemptは品質失敗へ混ぜず、固定された外部失敗規則に従い同じ不足slotだけを補充する。valid低品質runは補充または再実行しない。

## 実行前gate

1. Candidate194 profileを作成し、prompt identity、bundle hash、9ケース、N=5、M=24を固定する。
2. Candidate191登録result `e599690689294c658b52a6a9e301697f`と対応する保存Layer 1を、互換条件照合用の参照へbindする。
3. Candidate191の45 atomic runをregistryで確認し、Candidate194の空poolを`seed-pool`で作る。
4. `plan-missing --desired-count 5`がCandidate194を各case 0件、各case不足5件、合計45 slotと判定することを確認する。
5. 45 capsuleとglobal planを生成し、prompt bundle path、bundle hash、sample identity、case、fixture、TaskSpec、rating、model、reasoning、runtime、permission、executor条件、command evidence protocol、resource classおよびM=24を固定する。
6. `prepare-comparison-layer1`、`preflight-comparison`、`verify-comparison-preflight`が成功し、receiptが`authorized_slots=45`、`issued_slots=0`を示すことを確認する。

一項目でも不一致、未固定または未確認ならslotを発行しない。comparison preflightは後続の[実行準備監査](candidate194-c147-direct-review-control-reconstruction-adr9-r2-n5-execution-preparation-audit.md)で`ready`となり、Candidate194の不足45件を許可した。監査時点の発行数は0件である。run発行は別の明示的な継続判断まで開始しない。

## 停止条件

- 45件を得られない環境状態は`measurement_incomplete`として停止する。
- valid runが一件でもScore `4`未満なら、結果を保持して第2段階へ進まない。
- 共通またはcase別の機構predicateが一件でも不合格なら、品質が全件通過していても停止する。
- 失敗run、case、fixture、TaskSpec、oracle、rating contractまたは同じCandidate194 bundleを、その結果に合わせて変更しない。
- 失敗をC147からの24責任と移行表へ戻して分類し、修正が必要なら新しいCandidate identityでM1から再開する。

## 次段階との境界

M5第1段階が品質・機構とも全件通過した場合だけ、Standard14の7対照ケースを各N=5で扱う第2段階のprofileとpreflightを別に作る。ADR9通過だけでStandard14全14ケース、M6、採用、releaseまたはprojectionへ進んだことにはしない。

固定45件を発行した結果、45 / 45 valid、Score `4 / 1 = 40 / 5`だった。開始identity dependency越境7件、reviewer cardinality不一致7件、期待result kind不一致6件およびcompound identity/read command 1件も残った。品質・機構とも不通過なので停止し、第2段階を発行しない。現在判断は[Candidate194 ADR9 r2全9ケースN=5結果](../evaluations/results/candidate194-c147-direct-review-control-reconstruction-adr9-r2-n5_2026-08-12.md)を正本とする。
