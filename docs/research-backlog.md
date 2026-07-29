# 研究バックログ（状況索引）

研究項目を**未完了・保留**と**完了・停止**へ分け、着手判断と履歴確認のために一箇所へ集める索引。長期方針は[`future-roadmap.md`](future-roadmap.md)、系譜と観測は[`candidate-history.md`](candidate-history.md)を参照する。

この文書は索引であり、判定の正本ではない。各項目の状態・数値・停止理由は「正本」列のartifactを正とする。ここに載っていることは、着手済み・評価済み・採用予定のいずれでもない。

## 状況サマリー

### 未完了・保留

| 項目 | 現在状態 | 次の判断または再開条件 |
| --- | --- | --- |
| `CONTEXT`（`X1`） | ペンディング | A06はUltra制御用。Ultra条件で再検討する明示判断があった場合だけ再開 |
| `RECOVERY`（`R1 / R2`） | 未完了・効果未測定 | `environment_recovery_max>0`の正のrecovery scenarioを評価するか判断 |
| [`Candidate87`](candidate87-producer-local-invocation-wave-design.md) | 標準14品質通過・集約cost両方悪化・採用未判断 | C81比token中央値`+6.09%`、elapsed中央値`+1.35%`を許容して採用するか、停止するか判断。releaseと本体反映は別gate |
| [Claude Code CLI executor系列](claude-code-cli-evaluation-adapter-design.md) | 保留・実装／pilot／本測定未着手 | 系列へ着手する明示判断とPhase 0の認証方式選択が揃った場合だけ再開 |

### 完了・停止

| 項目 | 最終状態 | 完了・停止境界 |
| --- | --- | --- |
| `INDEPENDENCE`（`I1` = `F9`） | 対応なしで完了 | A / D追加runは行わない。`I1`起因の不要なoperation分割をfresh traceで観測した場合だけ別判断として再開 |
| [`Candidate82`](candidate82-producer-gate-deduplication-design.md) | `standard14_b20_evaluated / stopped` | B20で低頻度route非安定性を観測。採用以降へ進めない |
| [`Candidate83`](candidate83-delegation-value-boundary-design.md) | `targeted_f02_evaluated / stopped` | 品質通過、cost control未実証。追加評価以降へ進めない |
| [`Candidate84`](candidate84-delegation-marginal-value-boundary-design.md) | `targeted_f02_evaluated / stopped` | 品質通過、cost control mixed。追加評価以降へ進めない |
| [`Candidate85`](candidate85-planning-first-producer-selection-design.md) | `targeted_f02_f04_evaluated / stopped` | F04でtoken・elapsedがともに悪化。D01以降へ進めない |
| [`Candidate86`](candidate86-producer-plan-fast-path-design.md) | `targeted_f02_f04_d01_evaluated / stopped` | D01でtoken・elapsedがともに悪化。標準14以降へ進めない |
| [`Candidate88`](candidate88-parallel-worker-admission-design.md) | `targeted_f02_evaluated / stopped` | 逐次Workerを観測し、token・elapsedもともに悪化。F04以降へ進めない |
| [`Candidate89`](candidate89-dispatch-time-worker-admission-design.md) | `targeted_f02_evaluated / stopped` | dispatch gateが実発行順を制約できず、token・elapsedもともに悪化。F04以降へ進めない |
| C81・C87・C88・C89 F02 control graph診断 | 完了・新Candidateなし | 保存trace診断で上流のoperation誤分解を特定。fresh C81互換traceで再観測した場合だけ再開 |
| A01の3択variation診断 | 完了・新Candidateなし | 修正版30 / 30 valid。補集合選択、候補順依存、過剰停止を再現せず終了 |
| 投影済みCandidate71のrisk整理 | 完了・監視 | 現在は非再現。fresh traceで未固定値の誤実行を再観測した場合だけ再開 |
| F10 exact coordinate evidence interface | 対応なしで完了 | exact coordinateをhard requirementにしないため実装・追加runを行わない |
| rating contract identity・一律比較・reasoning追試 | 解決済み | 現行v13を確定し、High／Medium比較とreasoning 6水準を完了 |
| `QUALITY_RATING_V8`への改名 | 解決済み | identity・schema・採点挙動を変えずrevision名を明示化 |
| [`Candidate78`](candidate78-project-index-navigation-design.md) | `standard14_evaluated / stopped` | token中央値`+8.66%`、elapsed中央値`+4.38%`。追加改訂以降へ進めない |
| 公開target repository系列・runtime再現性 | 完了 | Click標準14、空環境再構築、network遮断full gate、offline lock確認まで完了 |

## 1. label監査の残件

`Candidate71`の11 label監査で再測定候補として残った3件の現在判断。正本は[`candidate71-control-abstraction-analysis.md`](candidate71-control-abstraction-analysis.md)の「監査状況の分類」表。

| 項目 | 必要な再測定 | 結論をflipし得るか |
| --- | --- | --- |
| `CONTEXT`（`X1`） | **ペンディング。** A06はUltra制御用のため、case variant、bundle、gate、fresh runを開始しない | **あり**。拡張方向（packet resolved premiseによる再読削減）が未検証 |
| `INDEPENDENCE`（`I1` = `F9`） | **対応なしで完了。** A / D scopeの追加評価を実施しない | 低い。Candidate68のF10ではruntime非改善 |
| `RECOVERY`（`R1 / R2`） | `environment_recovery_max>0`の正のrecovery scenario caseでの評価。現Evaluation setは`not_applicable`でun-run | 不明（効果未測定） |

`CONTEXT`（`X1`）は、Ultra条件でA06制御を再検討する明示判断があった場合だけ再開する。保留中はCandidate、probe、追加model runを作成しない。

`INDEPENDENCE`（`I1`）は、未測定範囲を埋めること自体を目的とした追加runを行わない。`I1`が原因となる不要なoperation分割をfresh traceで観測した場合だけ、別の判断単位として再開する。

## 2. `PRODUCER`の`P3`一文削除Candidate82（B20完了・停止）

11 label監査で唯一「Candidate作成根拠あり」となった項目。`P3`の正本は`OWNER_ROLE`側にあり、`PRODUCER`側の短い再記述だけを削除した。F10 / D01 targeted 10 / 10と単発標準14 70 / 70はscore `4`だったが、採用前B20で低頻度route非安定性を観測した。20 result、1,400 / 1,400件はvalid・rateable、公式score `4 / 1 = 1,399 / 1`である。score `1`は採点偽陰性だった。一方、F02とF04の各1件がcriterion ownerを独立producer指定へ変換し、不要childを起動したため、Candidate82を`standard14_b20_evaluated / stopped`とする。

- 現在設計: [`candidate82-producer-gate-deduplication-design.md`](candidate82-producer-gate-deduplication-design.md)
- targeted結果: [`Candidate81 / Candidate82 F10・D01 N=5`](../evaluations/results/candidate81-candidate82-producer-gate-deduplication-v13-medium-f10-d01-n5_2026-07-28.md)
- 標準14結果: [`Candidate81 / Candidate82 Medium標準14 N=5`](../evaluations/results/candidate81-candidate82-producer-gate-deduplication-v13-medium-standard14-n5_2026-07-28.md)
- 採用前B20結果: [`Candidate82 Medium標準14 N=5 B20`](../evaluations/results/candidate82-producer-gate-deduplication-v13-medium-standard14-continuous-n5-b20_2026-07-28.md)
- prompt identity: `the-caption-3ce91a4-producer-gate-deduplication-r1`
- 現在境界: B20まで評価完了。設計の停止条件により採用、release、本体反映へ進めない

A01のscore `1`で確認した文面依存の偽陰性には、Rating v14を追加して対応した。v14は疑問符や質問語を採点せず、未固定値、terminal response、zero drift、試験・変更operation未開始から`awaiting_required_value`状態を作る。v13のB20公式scoreはimmutableなまま保持し、v14の新規model runや再採点resultはまだ作成していない。
- 旧分析が作業呼称として使った「Candidate74」は別軸へ割り当て済みであり、履歴上の呼称としてのみ保持する

### Candidate83: Worker価値による委譲境界（F02評価完了・停止）

Candidate82のF02 / F04誤起動を、Worker一律禁止ではなく`delegation_value_ready`で扱う。AIは独立性、並列化、context分割、worker固有capabilityに固有価値がある場合にWorkerを選べる。一方、criterion owner語列だけの起動と、rootが同じpredicateを処理する逐次重複は許可しない。

- 設計正本: [`candidate83-delegation-value-boundary-design.md`](candidate83-delegation-value-boundary-design.md)
- prompt identity: `the-caption-3ce91a4-delegation-value-boundary-r1`
- bundle SHA-256: `0e3fd8e8b24b82f84fad1d2e9c68f391a7e3fa722b82fcfc5cbff80a2d6bf852`
- F02結果: [`Rating v14 Medium F02 N=5`](../evaluations/results/candidate83-delegation-value-boundary-v14-medium-f02-n5_2026-07-28.md)。5 / 5 score `4`だったが、5 / 5で不要Workerを起動し、1 runは同じ確認を別Workerへ再割当てした
- immutable評価state: `targeted_f02_evaluated / stopped`
- 現在解釈: [`Worker委譲のコスト判定と制御再設計`](delegation-cost-control-redesign.md)により`quality_passed / cost_control_not_demonstrated`。Worker起動自体は失敗条件にしないが、互換baselineと事前toleranceがないため追加評価、採用、release、本体反映へ進めない

### Candidate84: Worker限界価値の状態境界（F02評価完了・停止）

Candidate83の`TaskSpecが独立性を要求`という語義判定を削除し、Worker専有scopeと実質的な限界価値を状態として判定する。criterion owner、risk owner、`independent`語列、独立確認という作業名だけではWorkerを起動しない。一方、別execution identity、並列化、context分離、固有capability、未解決判断に実質的価値があればAIがWorkerを選べる。

- 設計正本: [`candidate84-delegation-marginal-value-boundary-design.md`](candidate84-delegation-marginal-value-boundary-design.md)
- prompt identity: `the-caption-3ce91a4-delegation-marginal-value-boundary-r1`
- bundle SHA-256: `b58ab2d14417be459dc8fd2a66cd1d48c1f8ae538e1e58a38148cb9598825d82`
- F02結果: [`Rating v14 Medium F02 N=5`](../evaluations/results/candidate84-delegation-marginal-value-boundary-v14-medium-f02-n5_2026-07-28.md)。5 / 5 score `4`、3 / 5 root-onlyだったが、2 / 5で不要Workerを起動した
- immutable評価state: `targeted_f02_evaluated / stopped`
- 現在解釈: [`Worker委譲のコスト判定と制御再設計`](delegation-cost-control-redesign.md)により`quality_passed / cost_control_mixed`。Workerあり2件のうち並行経路と逐次経路が混在し、互換baselineと事前toleranceもないため追加評価、採用、release、本体反映へ進めない

### Candidate85: planning-first producer selection（F02・F04評価完了・停止）

C83 / C84でWorkerの期待価値をprompt内predicateへ展開した方向を停止した。C85はC81を直接親とし、AIが実行前planningでoperation graph、producer、dependency、execution waveを一体として決める。既存F02 r1、F04 r2、D01 r1のTaskSpec、fixture、oracleは変更しない。Workerを含む経路全体は互換な品質・all-agent token・elapsedで判定し、routingはdiagnosticへ戻す。

- 正本: [`Worker委譲のコスト判定と制御再設計`](delegation-cost-control-redesign.md)
- 設計: [`Candidate85 planning-first producer selection設計`](candidate85-planning-first-producer-selection-design.md)
- prompt identity: `the-caption-3ce91a4-planning-first-producer-selection-r1`
- bundle SHA-256: `293e1457a9de4501574a31cad281990244aaea0f6c1a927a25356b00b99fd48d`
- route診断: [`Planning-first route diagnostic`](planning-first-route-diagnostic.md)
- 評価profile: C81 / C85それぞれF02、F04、D01をRating v14、Medium、`N=5`で固定。各pairはprompt identity以外を一致させる
- 事前cost tolerance: token `0`、elapsed `0`
- F02結果: [`Candidate81 / Candidate85 Rating v14 Medium F02 N=5`](../evaluations/results/candidate81-candidate85-planning-first-v14-medium-f02-n5_2026-07-28.md)。両条件5 / 5 score `4`、C85はtoken中央値`-0.94%`、elapsed中央値`+5.32%`の`cost_tradeoff`
- F04結果: [`Candidate81 / Candidate85 Rating v14 Medium F04 N=5`](../evaluations/results/candidate81-candidate85-planning-first-v14-medium-f04-n5_2026-07-28.md)。両条件5 / 5 score `4`、C85はtoken中央値`+38.29%`、elapsed中央値`+24.70%`の`cost_control_failed`
- route: C81 / C85ともF02・F04の全runがroot-only。C85は全runで最初のcommand前にproducerを固定したが、F04のコスト悪化はWorker起動なしで発生した
- 現在境界: `targeted_f02_f04_evaluated / stopped`。D01 profileは未実行のまま保持し、標準14、採用、release、本体反映へ進めない

### Candidate86: producer plan fast path（F02・F04・D01評価完了・停止）

C85のplanning-first順序は維持し、単一operationでも完全なoperation graphと明示planを維持する経路を除く。C81を直接親とし、独立した`PLAN` labelを追加せず、既存`PRODUCER`、`OWNER_ROLE`、`DECISION_BOUNDARY`だけを置換する。

- 設計: [`Candidate86 producer plan fast path設計`](candidate86-producer-plan-fast-path-design.md)
- prompt identity: `the-caption-3ce91a4-producer-plan-fast-path-r1`
- bundle SHA-256: `053b23c2a51ed58e7cc1e2bc6c6e973b72f04f1e1058dcbed22d0e7fc6e93a51`
- root prompt本文: `5,914 bytes`。C81比`+389 bytes`、C85比`-625 bytes`
- 評価profile: 既存F02 r1、F04 r2、D01 r1を再利用したC81 / C86 pair。新しいcase、fixture、oracle、Evaluation setは作成していない
- 評価順: F02、通過時だけF04、さらに通過時だけD01
- 事前cost tolerance: token `0`、elapsed `0`
- F02結果: [`Rating v14 Medium F02 N=5`](../evaluations/results/candidate81-candidate86-producer-plan-fast-path-v14-medium-f02-n5_2026-07-29.md)。両条件5 / 5 score `4`、token中央値`-2.44%`、elapsed中央値`+1.43%`の`cost_tradeoff`
- F04結果: [`Rating v14 Medium F04 N=5`](../evaluations/results/candidate81-candidate86-producer-plan-fast-path-v14-medium-f04-n5_2026-07-29.md)。両条件5 / 5 score `4`、C86 root-only 5 / 5、token中央値`+6.77%`、elapsed中央値`-6.03%`の`cost_tradeoff`
- D01結果: [`Rating v14 Medium D01 N=5`](../evaluations/results/candidate81-candidate86-producer-plan-fast-path-v14-medium-d01-n5_2026-07-29.md)。両条件5 / 5 score `4`かつ指定worker route成立。C86はtoken中央値`+83.28%`、elapsed中央値`+45.81%`の`cost_control_failed`
- route診断: C86 childのcustom exec call合計がC81の`13`から`41`へ増え、child token合計は`340,228`から`873,848`へ増えた
- 現在境界: `targeted_f02_f04_d01_evaluated / stopped`。標準14、採用、release、本体反映へ進めない

### Candidate87: producer-local invocation wave（標準14品質通過・集約コスト悪化）

C86 D01のコスト悪化を、Worker起動判断ではなくbind済みproducer内部のinvocation分割へ限定する。C86を直接親とし、`DECISION_BOUNDARY`だけを置換する。

- 設計: [`Candidate87 producer-local invocation wave設計`](candidate87-producer-local-invocation-wave-design.md)
- prompt identity: `the-caption-3ce91a4-producer-local-invocation-wave-r1`
- bundle SHA-256: `b5f581afa5fafa941c7d9974abc127d50acc488085a63d85974b8bd8047b4e67`
- root prompt本文: `6,278 bytes`。C86比`+364 bytes`
- 変更軸: root / worker共通で、decision boundary、明示order、fail-stop dependencyを持たない同一operation内invocationを一つのcustom exec wrapperから同時発行する
- 試験: 既存D01 r1でC86 / C87一軸qualification。通過後だけ保存済みC81 D01との比較、F02 r1、F04 r2へ進む
- 新しいcase、fixture、oracle、Evaluation set: 作成しない
- D01結果: [`Rating v14 Medium D01 N=5`](../evaluations/results/candidate86-candidate87-producer-local-invocation-wave-v14-medium-d01-n5_2026-07-29.md)。指定worker routeは5 / 5件で成立し、C86比でchild custom exec call合計`41 → 12`、token中央値`-51.06%`、elapsed中央値`-26.54%`
- 品質結果: append-only訂正後はscore `4 = 5`。当初の`4 / 3 = 4 / 1`は、個別監査がv14 contract IDを渡さずv10規則を適用した誤採点だった。詳細は[`rating contract binding訂正`](../evaluations/results/targeted-review-rating-contract-binding-correction_2026-07-29.md)
- C81比較: token中央値`-14,694`（`-10.29%`）、elapsed中央値`+6.606`秒（`+7.12%`）。両KPI悪化の停止条件には該当しない
- F02結果: [`Rating v14 Medium F02 N=5`](../evaluations/results/candidate81-candidate87-producer-local-invocation-wave-v14-medium-f02-n5_2026-07-29.md)。5 / 5 score `4`、C81比のtoken中央値`-5.26%`、elapsed中央値`-10.63%`でgate通過。token合計は`+16.06%`で分布はmixed
- F04結果: [`Rating v14 Medium F04 N=5`](../evaluations/results/candidate81-candidate87-producer-local-invocation-wave-v14-medium-f04-n5_2026-07-29.md)。5 / 5 score `4`、C81比のtoken中央値`+15.48%`、elapsed中央値`-12.62%`のtradeoff。両KPI悪化の停止条件には非該当
- 標準14結果: [`Rating v14 Medium標準14 N=5`](../evaluations/results/candidate81-candidate87-producer-local-invocation-wave-v14-medium-standard14-n5_2026-07-29.md)。C81 / C87とも70 / 70 score `4`。C87はtoken中央値`+6.09%`、elapsed中央値`+1.35%`で、集約コストは両方大きい
- 現在境界: `standard14_evaluated / quality_gate_passed / aggregate_cost_both_higher / adoption_not_decided`。採用、release、本体反映は未実施・未判断

### C81・C87・C88・C89 F02 control graph診断（完了・新Candidateなし）

**2026-07-29に保存traceだけで診断を完了した。** C81、C87、C88、C89の既存F02 r1各`N=5`を再確認し、一次result、score、candidate stateは変更していない。

- C81は5 / 5 root-onlyだった。implementation、test-contract、required validationを一つのroot operationへbindした
- C87 / C88 / C89は合計11件で`/root/independent_contract_check`を起動し、child token合計は`820,380`だった
- 11件のWorker resultはF02-C3の再確認だけで、rootもscoped diff、test、required validation、最終done判定で同じpredicateを扱った
- C87とC88には同時進行経路があるため、executorのsame-wave capability欠落は確認できない
- 誤経路はdispatch順ではなく、criterion metadataを別operation identityへ昇格した上流のoperation分解で成立した
- 診断正本: [`Worker委譲のコスト判定と制御再設計`](delegation-cost-control-redesign.md)の「C81・C87・C88・C89 F02保存traceのcontrol graph診断」
- 完了境界: C81 F02では同じ誤分解が0 / 5であり、観測されたC81失敗がない。`wave_commit`、executor変更、C81直接child、bundle、profile、追加model runは作成しない
- 再開条件: fresh C81互換traceで同じoperation誤分解を再観測するか、別operation identityまたは別execution identityをrequired outcomeにする明示要件が追加された場合だけ、`operation_identity_ready`一軸の作成前gateへ戻る

## 3. A01の3択variation診断

**2026-07-28に完了。** A01の現行2択caseを回帰基準として変更せず、現在値と候補順を3通り回転した`AMBIGUOUS` / `AUTHORITY`の6 caseを追加した。

- 第1版30件はすべてvalidだったが、`strict` / `live`開始状態と既存仕様書の`daily`記述が不整合であり、10 / 10件がその記述を変更先authorityへ変換した。fixture交絡として分離した。
- 仕様書も開始値へ同期した第2版は30 / 30件がvalid、excluded attempt 0件だった。
- `AMBIGUOUS`は15 / 15件がzero driftかつ試験前の確認停止、`AUTHORITY`は15 / 15件が質問せず指定値へ変更して関連testを成功させた。
- 補集合選択、候補順依存、現在値回避、過剰停止は第2版で再現しなかった。新しいprompt predicateの根拠がないためCandidateは作成しない。

正本は[`Candidate81 A01 3択variation診断`](../evaluations/results/candidate81-a01-three-choice-variation-diagnostic_2026-07-28.md)と[`修正版set`](../evaluations/sets/the-caption-a01-three-choice-variation-r2/README.md)である。第1版は上書きせず、交絡を確認した履歴として保持する。

## 4. 投影済みCandidate71のrisk（現在解釈の整理完了・監視へ移行）

**2026-07-28に現在解釈の整理を完了した。** Candidate71は評価上`stopped`（v12の品質gate不通過）のまま、別の採用判断でTHE-CAPTION本体へ投影済みである。当時のrelease artifactに保存された未解決riskは2件で、これはimmutableな記録として取り消さない。一方、rating v13と投影済みCandidate81の追加診断による現在解釈では、この2件の位置づけが分かれる。

| 当時のrelease risk（v12時点） | 観測 | rating v13後の現在解釈 |
| --- | --- | --- |
| A02で`git diff --check`欠落 | 3 / 90件 | **現在の未完了研究項目ではない。** 実行役へ提示していない特定コマンドを採点側が必須化した「要求と採点のずれ」であり、本物の品質低下と区別される。v13でこのずれを塞いだ |
| A01で未固定modeを確認せず実装・試験へ進んだ誤実行 | 1 / 90件 | **当時の品質上の問題として保持する。** v13でも当該runの評価は変えない。一方、現在のCandidate81では3択variation r2の曖昧条件15 / 15件が確認停止し、authority条件15 / 15件が指定値へ正しく変更したため、追加制御を作らず監視項目へ移す |

- 当時の未解決riskの正本: [`Candidate71 release / projection`](../prompts/releases/the-caption-3ce91a4-validation-closure-release-r1/README.md)（v12結果は履歴として保持）
- 現在解釈の正本: [`control-mechanisms.md`](control-mechanisms.md)のrating v13節と[`a02-rating-divergence.md`](a02-rating-divergence.md)
- 現在挙動の正本: 上記「3. A01の3択variation診断」と[`Candidate81 A01 3択variation診断`](../evaluations/results/candidate81-a01-three-choice-variation-diagnostic_2026-07-28.md)
- 完了判断: 過去の1件を取り消さず、現在は非再現の監視項目とする。新しいprompt predicate、Candidate、常設gate、追加model runは作らない。今後、未固定値を確認せず変更したfresh traceを再観測した場合だけ、同じ診断setで再開する

## 5. F10 location mismatch: exact coordinateのevidence interface（対応なしで完了）

**2026-07-28に対応しないと判断して完了した。** 原因診断そのものは実施済みで、prompt側の変更は停止している。`CLAIM_PROVENANCE` collectorと90件backfillの後、30件checkpoint診断（`max_30_diagnostic_valid_without_location_mismatch`で停止）、追加105件、coordinate representation診断、delayed reconstruction診断、implicit coordinate passive case-control、real-Agent representation recency診断、recorded-state collision受動監査まで到達した。

正本の現在判断は、repository-wideに削除できるprompt判断点を確認できないため、**prompt変更と追加model runをここで止める**ことである。exact coordinateはこの基盤のhard requirementにしないため、modelが選んだexact line textをone-based coordinateへ変換するevidence interfaceも実装しない。

- 完了境界: 過去のlocation mismatchと診断結果は保持する。evidence interface、prompt制御、Candidate、追加model runは作らない。将来exact coordinateをhard requirementへ変更する明示判断があった場合だけ、別の判断単位として再開する。
- 正本: [`review-location-cause-diagnostic-plan.md`](review-location-cause-diagnostic-plan.md)（「対策判断への接続」節と各診断結果節）
- 制御graph側の判断（location mismatchを理由にroot規則を追加しない）は[`prompt-control-graph-review.md`](prompt-control-graph-review.md)を参照

## 6. 現行rating contract identity、一律比較、reasoning追試（解決済み・2026-07-26）

新規runへ適用する現行rating contractの指定が、評価基盤の正本（`owner-producer-quality-v8`）と後続文書（最新revision v13）で一致していなかった。**2026-07-25に現行をv13へ確定した。** 正本[`prompt-comparison-workflow.md`](prompt-comparison-workflow.md)の指定、評価実行手順[`evaluation-loop-manual.md`](evaluation-loop-manual.md)のLayer 3、契約台帳[`evaluations/rating-contracts/README.md`](../evaluations/rating-contracts/README.md)、および`scripts/evaluation_loop.py`の`SUPPORTED_QUALITY_RATINGS`をv13へ追従させ、v13 capsuleが受理されることをunit testで確認済みである。この項目は未完了ではない。

派生作業も2026-07-26に完了した。reasoning effortはcomparison conditionであり、水準ごとにcompatibility keyが異なる。水準内のprompt比較と、水準間の記述的比較を混同しない。

- [`Baseline、ControlFreeRepository、Candidate5、Candidate35、Candidate43、Candidate71のHigh標準14項目各N=5`](../evaluations/results/baseline-control-free-repository-c5-c35-c43-c71-v13-standard14-n5_2026-07-26.md)を最初のv13互換result集合として登録した。6条件 × 70件 = 420件で、v12以前のresultは同一comparisonへ混ぜない。
- [`Candidate71のreasoning 6水準`](../evaluations/results/candidate71-reasoning-levels-v13-standard14-n5_2026-07-26.md)を、`low` / `medium` / `high` / `xhigh` / `max` / `ultra`、標準14項目各`N=5`で記録した。`medium`がtoken中央値最小、`low`がelapsed中央値最小だった。
- [`6条件のMedium一律比較`](../evaluations/results/baseline-control-free-repository-c5-c35-c43-c71-v13-reasoning-medium-standard14-n5_2026-07-26.md)も420 / 420件を登録した。C71とC43のtoken中央値差はHigh `-31.47%`、Medium `-29.19%`であり、少なくともこの2水準ではeffort低下によって相対的な制御差は消えなかった。
- 2026-07-27以降の新規通常比較は`medium`を運用基準とする。既存`high` resultは履歴として保持し、reasoning effort自体の比較または既存互換条件の再現だけを例外とする。運用正本は[`evaluation-loop-manual.md`](evaluation-loop-manual.md)である。

## 7. `QUALITY_RATING`という汎用名がv8を指している（解決済み・2026-07-28）

**2026-07-28に解決した。** `scripts/evaluation_loop.py`で`owner-producer-quality-v8`を指していた汎用定数`QUALITY_RATING`を`QUALITY_RATING_V8`へ改名した。v8互換経路を使うintegration testとowner-producer evidence testも同じrevision名へ追従させた。

- 変更前から実行上の不具合はなく、run capsuleが`quality_rating`を明示する契約、v13の現行identity、各rating contractの内容とSHA-256は変更していない。
- `SUPPORTED_QUALITY_RATINGS`では同じv8辞書を`QUALITY_RATING_V8`として保持する。v8互換性を検証するtestの既定値もv8のままであり、v13へ暗黙変更していない。
- 完了境界は名前によるrevision分離だけである。過去result、rating contract artifact、schema、採点挙動は変更しない。

## 8. Layer 2 executorのClaude Code CLI置換（保留）

Layer 2 executorをCodex CLI（`codex exec`）からClaude Code CLI（`claude -p`）へ置き換える試験方法。2026-07-25に設計検討と前提のprobe実測を行ったが、2026-07-28の判断で**一旦保留**とした。実装、pilot、本測定はいずれも未着手であり、保留中は追加probeも行わない。

- 正本: [`claude-code-cli-evaluation-adapter-design.md`](claude-code-cli-evaluation-adapter-design.md)（実測値、adapter対応表、新設schema revision、未確定事項6件、段階計画Phase 0〜4）
- **Phase 0が先行条件**: 認証方式（API key + `CLAUDE_CONFIG_DIR`隔離、またはsubscriptionのまま開始gateで確認）が未決で、環境identityの固定方法がこの決定に依存する。決まるまでPhase 1のprobe設計を固定できない。
- 実装対象は新規adapterと新規collectorであり、既存の`scripts/run_codex_evaluation.py`、既存collector、既存registry resultは変更しない（[`scripts/AGENTS.md`](../scripts/AGENTS.md)）。
- **既存Codex resultとの互換比較は成立しない**。注入時点の差とtoken accountingの意味の差によりcompatibility keyが一致しないため、Claude Code条件はbaselineから再測定する独立系列として扱う（[`evaluations/AGENTS.md`](../evaluations/AGENTS.md)のCompatibility）。
- model名を明示したresultはすべて`gpt-5.6-sol`で、Claude系modelでの測定は0件である（[`execution-control-research-paper.md`](execution-control-research-paper.md)の限界節）。この項目はその限界に接するが、この項目自体はmodel比較を目的としない。executor置換の成立条件だけを扱う。
- 再開条件: Claude Code系列へ着手する明示判断と、Phase 0で採用する認証方式の選択が揃った場合だけ再開する。

## 9. root `AGENTS.md`へのrepository index参照追加の効果（実施済み・停止）

**2026-07-26にCandidate78として実施し、停止した。** 投影済みCandidate71を直接sourceとし、root `AGENTS.md`へ条件付き`PROJECT_INDEX`一labelだけを追加した。index本文、残り18 target、評価条件は変更していない。

標準14項目各`N=5`は70 / 70件がscore `4`だったが、Candidate71比でall-agent token中央値は`+8.66%`、elapsed中央値は`+4.38%`だった。A02はindexを5 / 5で先に読んでもrepository-wide探索が5 / 5で残り、F10 Entryでは不要なindex readが2 / 5に増えた。事前停止条件に従い、追加改訂、採用、release、本体反映へ進めない。数値とidentityの正本は[`Candidate71 / Candidate78標準14結果`](../evaluations/results/candidate71-candidate78-project-index-navigation-v13-standard14-n5_2026-07-26.md)とする。

以下は着手前に固定した試験境界である。

- 変更単位: root `AGENTS.md`への参照追加1軸のみ。index本文はbundle targetとして既に固定済みのため、残り18 targetはcontent identicalなcandidate bundleになる。
- 観測: 3 KPI（`quality_score` / all-agent `total_tokens` / `elapsed_seconds`）を評価対象とし、target探索readとworker起動はdiagnosticへ置く。境界の正本は[`evaluations/AGENTS.md`](../evaluations/AGENTS.md)。
- 事前に両方向の仮説を置く。静的事実の参照でrepository探索readが減る方向と、root promptへの追加がcontextを増やすだけで動的tokenが増える方向の両方である。表面的なprompt短縮がall-agent tokenをほとんど動かさなかった既存知見（正本: [`control-mechanisms.md`](control-mechanisms.md)）から、静的byteの増減で効果を推定しない。
- read boundary / read route系candidate（C50、C56〜C59、C62、C63など）と論点が接近する。着手前に系譜を確認し、既存軸の再実行にならないことを確かめる。正本は[`prompts/candidates/README.md`](../prompts/candidates/README.md)と[`candidate-history.md`](candidate-history.md)。
- 比較条件: 既存Codex executor、標準14項目、rating v13で測れる軸である。項目6で取得したv13 Baselineをcomparisonへ使用できるが、repository index参照を追加するcandidateは別profile・別resultとして新規実行する。
- 項目8（Claude Code CLI executor置換）と同一比較単位へ混ぜない。executor変更とprompt変更を同じ比較単位へ入れない（root [`AGENTS.md`](../AGENTS.md)の共通変更規律）。
- candidate作成前gate 9項目（[`prompts/AGENTS.md`](../prompts/AGENTS.md)）を通してからbundleを作る。

## 10. 公開target repositoryでの計測系列と評価基盤のrepository汎用化（runtime再現性まで完了）

公開repositoryを対象とする独立系列として`pallets/click`を登録し、同じBundle Aで14 caseのqualification、追加case各`N=3`、Std14 `N=5`をLayer 1〜4まで実行した。**Std14は70 / 70件がvalid・rateableかつscore `4`である。** この項目が扱うのは、公開repositoryで計測系列を成立させ、その過程で「任意のtarget repositoryへ同じ手順を適用できる分離」を確定することである。prompt制御の新しい変更軸ではなく、計測条件側の軸である。

2026-07-26時点で次を完了している。

- target instance `click`を`layout: namespaced`、公開・第三者再現可能として登録
- control-free baseline bundle `click-00e592c-control-free-r1`を固定
- `CLICK-F01-ANSI-SEQUENCE-STRIP` r1を作成し、seed適用前後のfocused / full gateでfixtureをqualification
- `click-outcome-abstract-condition-preserving-v1`、`click-f01-only-r1`、P1-a profile r1 / r2を固定
- Codex CLI `0.144.0`、Python `3.14.5`、共有venv identityをprofileへ固定
- r1 profileはLayer 2開始前にall-agent token accounting宣言不足を検出し、result 0件のまま停止。履歴を上書きせず、r2でtoken accountingとrequired command evidence protocolだけを追加
- r2でP1-aを完了。quality `100.000`（raw score `4`）、all-agent token `180,871`、elapsed `77.811`秒、excluded attempt 0件
- `click-control-free-f01-only-global-m24-n5-r1`でP1-bを完了。5 / 5件がscore `4`、all-agent token中央値`189,977`（最小`170,228`、最大`202,176`）、elapsed中央値`80.475`秒（最小`79.323`、最大`85.443`秒）、excluded attempt 0件
- 同じ`N=5` profileを独立3 resultへ反復してP1-cを完了。15 / 15件がscore `4`、batch中央値の中央値はtoken `189,033`、elapsed `80.590`秒。batch中央値rangeはtoken `26,878`（`14.22%`）、elapsed `1.501`秒（`1.86%`）で、excluded attemptは全batch 0件
- F02 `CLICK-F02-STREAM-DEPRECATION-CONTRACT` r1をqualification。2 source fileの公開・非公開API contractをseedし、seed前focused `72 passed, 1 skipped`、seed後`2 collection errors`、fixture 2回のcommit / tree一致を確認
- rating contract v2、`click-f02-only-r1`、F02 N=3 profileを固定し、3 / 3件をscore `4`で登録。all-agent token中央値`303,563`、elapsed中央値`130.225`秒、excluded attempt 0件
- 残り12 caseを固定し、追加caseだけ各`N=3`で確認。現行revisionはすべて3 / 3件がscore `4`。F07 r1はcommand evidence照合不能の未rating履歴、F07-P r1 / r2は各3 / 3件score `3`の失敗履歴として保持
- runtime r2へ`uv==0.11.32`を追加し、identity `0a30733685c5fb3bb69abf136d6a8cdb04c4ec323f52dc6d1488f8d49a7cc952`を固定。F07-P r3はworkspace-local uv cacheで3 / 3件score `4`
- `click-standard14-r1`、rating v10、Std14 profileを固定し、70 / 70件をscore `4`で登録。5 iterationのall-agent token中央値`2,860,702`、elapsed中央値`1,235.719`秒、excluded attempt 0件
- THE-CAPTION Candidate81のroot本文をbyte-identicalに1 targetへ適用したBundle Bを固定し、同じStd14条件で70 / 70件をscore `4`として登録
- Bundle AからBundle Bはquality中央値差`0.000`、all-agent token中央値`-685,546`（`-23.96%`）、elapsed中央値`+35.384`秒（`+2.86%`）。THE-CAPTIONでのtoken削減方向は再現したが、elapsed短縮は再現しなかった
- 今後の運用基準を`medium`へ切り替え、Bundle AとC81全文のMedium Std14を各70 / 70件・全件score `4`で登録した。C81全文はBundle A比でtoken中央値`-28.79%`、elapsed中央値`-12.62%`となり、5 / 5 iterationでelapsedが短縮した
- THE-CAPTION ControlFreeRepositoryとの構成差を分離するため、Clickでtarget-local No-AGENTSとrootなしRepository sub-AGENTSをMedium Std14 N=5で比較した。両条件70 / 70件がscore `4`で、sub-AGENTS側はtoken中央値`+3.74%`、elapsed中央値`+7.90%`だった。ただしsub本文の初期context注入は0 / 70で、本文をreadしたA01 5 / 5だけがtoken中央値`+80.47%`となった。配置だけでは全caseへ水平適用されないため、Std14全体の本文効果とは扱わない
- THE-CAPTIONと同質のauthority availabilityを測れているかClick Std14全14 caseを見直した。F01〜F08、F10-R、A01、A02は元の実行判断点を維持し、回帰setとして変更不要だった。F10 r1だけはsource-onlyで完結していたため、`src/AGENTS.md`を明示authorityとするF10 r2をMedium N=5で追試した。No-AGENTSは5 / 5件がscore `1`でauthority不足停止、Repository Authorityは5 / 5件がscore `4`でinventoryを完了した。全10件がvalid・rateable、zero drift、excluded attempt 0件で、THE-CAPTION F10と同じavailability方向を再現した
- 見直し後の`click-standard14-r2`をNo-AGENTS / Repository Authority、Medium、N=5、M=24で全件再実施した。F10以外は両条件65 / 65件がscore `4`、F10だけがscore `1` × 5 / score `4` × 5へ分離した。全140件がvalid・rateable、excluded attemptとunexpected driftは0件で、14実行判断点の比較setとして互換性を達成した。quality中央値は94.643対100.000、tokenは`+5.57%`、elapsedは`+3.96%`だが、後二者はF10の完了作業量差とM=24の変動を含むため効率差とは扱わない
- C81 / C81 + Repository Authorityも同じStd14 r2、Medium、N=5、M=24で各70件実施した。C81はscore `4` × 65 / score `1` × 5、C81 + Authorityはscore `4` × 70で、F10以外のquality回帰は0件だった。同じauthority状態のC81差は、authorityなしでtoken `-27.35%`・elapsed `-17.04%`、authorityありでtoken `-25.08%`・elapsed `-10.98%`となり、C81の削減方向はsub authority追加後も維持された
- 2026-07-28に既存共有venvを使わない空環境から、固定Click commitと固定package versionでknown-good 8 package identityをbyte単位で再構築した。通常条件とprocess単位のnetwork遮断条件でfull gateが同じ`1939 passed, 25 skipped, 31000 deselected, 1 xfailed`となり、`uv lock --check --offline`も`Resolved 81 packages`で成功した。手順とplatform境界の正本は[`Click runtime再構築とoffline full gate`](click-runtime-reproducibility.md)とする

Bundle AのHigh一次結果は[`click control-free Std14 N=5`](../evaluations/targets/click/results/click-control-free-standard14-n5_2026-07-26.md)、Medium一次結果は[`click control-free Medium Std14 N=5`](../evaluations/targets/click/results/click-control-free-reasoning-medium-standard14-n5_2026-07-27.md)、HighでのBundle A / B比較は[`Click Control-Free / C81全文 Std14 N=5`](../evaluations/targets/click/results/click-control-free-c81-full-standard14-n5_2026-07-26.md)、Medium比較は[`Click Control-Free / C81全文 Medium Std14 N=5`](../evaluations/targets/click/results/click-control-free-c81-full-reasoning-medium-standard14-n5_2026-07-27.md)、sub instruction配置比較は[`Click No-AGENTS / Repository sub-AGENTS Medium Std14 N=5`](../evaluations/targets/click/results/click-no-agents-repository-subagents-reasoning-medium-standard14-n5_2026-07-27.md)、authority availability追試は[`Click No-AGENTS / Repository Authority Medium F10 N=5`](../evaluations/targets/click/results/click-no-agents-repository-authority-reasoning-medium-f10-authority-n5_2026-07-27.md)を正本とする。High / MediumのBundle A traceとTHE-CAPTION ControlFreeRepository Mediumを使った[`baseline分析`](click-control-free-medium-baseline-analysis.md)では、Clickの軽さはreasoning量だけでなく、tool出力量`-50.46%`と小さいrepository contextに強く対応した。sub instruction配置追試により、THE-CAPTION側の4つのsub本文が常にmodel contextへ入っていたという仮定は置けなくなった。F10 targeted追試ではauthority availabilityの効果を再現したが、1 caseからStd14全体へ一般化しない。C81 MediumによりA02 / F06は大きく改善した。後続の[`残余経路分析`](click-c81-medium-residual-analysis.md)では、F01のtoken増加はpaired差中央値`-970`で安定悪化ではないと判定した。F04はC81でgit history探索がHigh / Medium合計`4 / 10`、Control-freeで`0 / 10`となり、両reasoningでelapsed合計が約16〜18%増えた。2026-07-28に4件のraw traceを再解析したところ、history探索後に初めてmethodまたは変更scopeが確定しており、method bind後の代替探索は`0 / 4`件だった。`PRECHANGE_EVIDENCE_SCOPE`は方法制御を追加するため採用せず、`METHOD`置換CandidateとF04 Medium N=5 targeted runも`stopped_before_candidate`とした。将来、method bind後にも不要探索が続く保存traceを観測した場合だけ再検討する。

見直し後Std14全体の正本は[`Click No-AGENTS / Repository Authority Medium Std14 r2 N=5`](../evaluations/targets/click/results/click-no-agents-repository-authority-reasoning-medium-standard14-r2-n5_2026-07-27.md)である。

C81との組合せ結果の正本は[`Click C81 / C81 + Repository Authority Medium Std14 r2 N=5`](../evaluations/targets/click/results/click-c81-repository-authority-reasoning-medium-standard14-r2-n5_2026-07-27.md)である。

### 現在の依存範囲（2026-07-26に実測）

repository非依存な層とtarget固有な層は次のとおりである。

| 層 | artifact | 実測した状態 |
| --- | --- | --- |
| Layer 1 fixture | `scripts/prepare_case_fixture.py` | CLI引数は`--case` / `--source-repo` / `--output`のみで、target repositoryはparameter。固有pathのhard-codeなし |
| Layer 2〜4実行 | `scripts/evaluation_loop.py` | clickで25 result・計481 runをappend-only登録。set / cycle / capsule / registry単位で動作し、target repositoryによる実行分岐を持たない |
| 制御prompt本文 | [Candidate71 release](../prompts/releases/the-caption-3ce91a4-validation-closure-release-r1/README.md)の`AGENTS.md.txt` | `SPEC`〜`RECOVERY`の13 labelは見出し語を除きproject固有語彙を持たない |
| bundle target map | THE-CAPTION releaseのmanifest 19 target、Clickは0 / 1 / 3 targetの4 prompt set | THE-CAPTIONのtarget側directory構造へ依存するmapを変更せず、`click`用mapをinstance配下の別bundleとして固定した。C81 root本文のbyte-identicalな水平適用、empty bundle、3つのsub instructionをそれぞれ独立identityで表現した |
| case artifact | 各case revisionの`trial-prompt-input.json`、`private/seed.patch`、`private/case-data.json` | 14 case・17 revisionをinstance配下へ固定。失敗revisionを上書きせず保持した |
| rating contract | THE-CAPTION v13、`click-outcome-abstract-condition-preserving-v1`〜v10 | case追加ごとに旧revisionを残し、現行v10で標準14項目を固定した |
| 採点補助 | Clickは固定rating contractとblind evidenceで採点 | 14 case・481 runのratingと登録が成立。target固有の新しいkernel分岐は追加していない |

したがって汎用化の対象は実行基盤ではなく、**case artifact / rating contract revision / 採点補助 / bundle target mapの4つ**である。`click`では4つをinstance配下へ分離し、共有kernelへtarget repositoryによる実行分岐を追加せず、3 KPI、compatibility key、append-only registryを含む端から端までの流用をBundle A / Bの標準14項目で確認した。未確認なのは第三者によるruntime再構築とnetwork遮断下のfull gateである。

この分離の境界とinstance台帳は[`evaluations/targets/README.md`](../evaluations/targets/README.md)で確定した。既存の計測系列はtarget instance `the-caption`（`layout: legacy_root`）として登録し、artifact pathを移動していない。

### target選定gate（この順で判定する）

1〜4は候補の機械的な絞り込み、5〜7は測定が成立するかの判定である。

1. **license**: seed patch、fixture条件、evidenceをこのrepositoryへ保存し公開するため、再配布可能なlicense（Apache-2.0 / MIT / BSD等）に限定する。
2. **offline再現性**: 依存を事前materializeした状態で、network遮断のまま全required gateがpassする。permissionは`approval_policy: never` / `sandbox: workspace-write`である（[profile実測](../evaluations/profiles/candidate1-expanded12-global-m24-n5-r1.json)）。
3. **容量**: self-contained fixtureをrun数ぶんmaterializeするため、soft 3 GiB / hard 5 GiBの運用値（[`evaluation-storage-maintenance.md`](evaluation-storage-maintenance.md)）に収まる。
4. **gate所要時間**: 標準14項目 × A / B × `N=5`で140 run規模になるため、1 runのfull gateがこの規模で回る長さである。
5. **測定感度**: 複数subsystemへ跨る変更、2階層以上のdirectory構造、worker委譲が意味を持つ広さを持つ。単一責務のlibraryでは`CONTEXT` / `OWNER_ROLE` / `INDEPENDENCE`の差がKPIへ出ない。
6. **天井効果の回避**: 既存setでもF05 out-of-scopeとF07 dependency pairは全runが`quality_score` 100である（[`cases/README.md`](../evaluations/cases/README.md)）。modelが解法を記憶しているseedはこれを悪化させるため、seed diffの取得元commitの新しさで制御する。
7. **prompt target collision**: target側が既に`AGENTS.md`等のauthority fileを持つと、bundle overlayでcase条件やtarget側規則が消える。F09が`prompt_target_collision`でexecution blockedになったのと同型のriskである。
8. **case供給**: 公開issue / PR履歴からreal taskを取得でき、case追加根拠自体を第三者が検証できる。
9. **実行判断点coverage**: 既存14項目が担保するworker起動、context継承、model再入、read、validation、停止、result bindingなどの判断点に、target固有の題材を対応付けられる。実装言語の一致自体はgateにしない。

### 独立系列としての扱い

- `target_repository_ref`はcompatibility keyの一項目である（[`evaluations/AGENTS.md`](../evaluations/AGENTS.md)）。**公開target系列を既存result集合と同一比較へ混ぜない。** baselineから再取得する。
- 項目8（Claude Code CLI executor置換）と同一比較単位へ入れない。executor変更とtarget変更を同時に入れると効果を切り分けられない。
- rating contractをcase単位で作り直す以上、`quality_score`の絶対値をTHE-CAPTION系列と比較しない。観察できるのは各系列内の差と、方向の一致だけである。

### runtime再現性の完了境界

- `click`の容量、gate所要時間、通常環境での5回連続passはPhase 0で実測した。P1-cでbatch内・batch間分布、Std14で14 case横断の70 / 70 validを取得した。
- known-good実行環境は、固定target commitからwheelを作り、固定package versionを空venvへinstallする手順で再構築できた。既存共有venvは使用していない。
- network遮断下のfull gateと`uv lock --check --offline`を実測した。見込みではなく成功事実として記録する。
- 実測platformはmacOS arm64 / Python 3.14.5である。別OS / architectureは同じidentityと推定せず、新しいruntime identityとして扱う。
- instance境界、layout、descriptor、Click rating v10は固定した。Std14は固定contractとblind evidenceで採点できたため、target固有採点補助の自動adapter化は今回の完了条件ではない。別targetを追加するときに再評価する。

### 段階計画

1. **Phase 0**（実施済み）: gate 1〜9を判定し、`pallets/click`を選定した。追加実測により14項目すべての実行判断点へ対応可能と確認した。実測値と判定の正本は[`public-target-selection-phase0.md`](public-target-selection-phase0.md)とする。
2. **Phase 1 artifact準備**（実施済み）: instance、control-free bundle、F01型case、rating contract、set、P1-a profile、共有runtimeを固定した。
3. **Phase 1実測**（P1-c完了）: P1-a `N=1`で端から端までの成立、P1-b `N=5`でbatch内分布、P1-c `N=5 × B=3`でbatch間の散らばりを確認した。
4. **Phase 2 case展開**（実施済み）: 14 caseをqualificationし、追加caseだけ各`N=3`でBundle Aの成立を確認した。既存caseは追加のたびに再実行していない。
5. **Phase 3 Bundle A標準14**（実施済み）: `click-standard14-r1`を固定し、Bundle Aで70 / 70件をscore `4`として登録した。
6. **Phase 4 Bundle B水平比較**: Std14 baseline確立後に、1軸だけを変更した新しいCandidateをBundle Bとして固定し、同じStd14条件でBundle Aと比較する。content-identicalなBundle Bは作らない。

candidate bundleを作る段階ではcandidate作成前gate 9項目（[`prompts/AGENTS.md`](../prompts/AGENTS.md)）を通す。

## 着手時の共通条件

- 一つのcandidateで一つのpredicateまたは一つの変更軸だけを扱う（[`prompts/AGENTS.md`](../prompts/AGENTS.md)のcandidate作成前gate9項目）
- 設計原則の正本は[`prompt-control-design-principles.md`](prompt-control-design-principles.md)
- 評価・採用・release・projectionは別gateとして記録する（[`repository-contract.md`](repository-contract.md)）
