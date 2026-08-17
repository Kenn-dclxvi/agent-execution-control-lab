# Candidate270の設計方針と結果の一次資料限定再構成

## 結論

Candidate270が対象としたvalidation境界は、Candidate270で初めて考案されたものではない。固定bundleを直接比較すると、Candidate71で全required validationの同一model step発行とresultの一回返却、Candidate80でroot用custom exec wrapper、Candidate81で途中resultをmodelへ返して次commandを別custom tool callにしない優先規則、Candidate108で実行票がterminalになるまで同じcell IDだけを待つ規則が追加されている。Candidate147はこれらを保持し、別の変更軸としてresultの停止効果を関係する後続operationだけへ限定した。

Candidate270の固定本文も、順番のある必須検証を一回の外側validation wrapperへ束ね、個別検証の途中resultをAIへ返さず、対応づけ済みの確定resultをwrapper終了時に一度だけ返す、と定めている。したがって「外側wrapper、途中返却禁止、一回返却を新たに追加する」という改善案は、Candidate147までの既存境界とCandidate270自身の本文を重複させる。

一方、保存済み`codex-events.jsonl`で観測できる`command_execution`の`item.completed`、次の`item.started`、および各itemの`aggregated_output`は、wrapper内で個別commandを逐次実行した場合にも生じる。これらは、途中resultがAIへ返されたことや、AIが再判断して次commandを発行したことを示さない。この観測だけからCandidate270を`mechanism_failed`とした先の判定は誤りである。

`all-agent-usage`が固定したpersisted rolloutを直接監査すると、Candidate270のF01、F02、F03は15 / 15 runで、required validationが一つのouter `exec` callに属し、nonterminal receiptのvalidation outputは0 bytes、継続は同じcell IDへの`wait`だけ、terminal outputは一件だった。Candidate270は20 / 20件でScore `4`であり、対象機序もN=5の15 / 15 runで`passed`とする。この時点でN拡張は実行可能になったが、N=5のKPI差だけで安定性、採用、releaseまたは本体反映を決めない。

この再構成後にStandard14 N=5を実施し、70 / 70件がScore `4`、Candidate147との互換比較はtoken `+18.16%`、elapsed `+9.09%`となった。現在の評価状態は`standard14_evaluated / quality_gate_passed / aggregate_cost_both_higher / adoption_not_decided`である。validation carrier、model再入、共同発行などの経路監査は3 KPI差を説明する診断情報であり、独立した採用gateにはしない。

## 根拠の境界

この再構成では、既存のCandidate270設計文書、実行監査、機序監査、後続分析、README要約を論証、数値または判定の入力に使わない。Candidate bundleのmanifestに残る歴史的な`design_inputs`と`source_interpretation`も、この再構成の解釈authorityにはしない。

使用する資料は次に限定する。

- [`docs/prompt-control-design-principles.md`](prompt-control-design-principles.md)の設計gate
- Candidate71、Candidate80、Candidate81、Candidate108、Candidate147、Candidate269、Candidate270の固定bundle byte
- Candidate番号と固定bundleの直接親・変更範囲を検証するrepository test
- Candidate270の固定Profile [`candidate270-natural-language-predicate-bound-validation-result-v14-reasoning-medium-f01-f02-f03-f10-entrypoint-global-m24-n5-cli0146-r1.json`](../evaluations/profiles/candidate270-natural-language-predicate-bound-validation-result-v14-reasoning-medium-f01-f02-f03-f10-entrypoint-global-m24-n5-cli0146-r1.json)
- Candidate270のwrite-once登録result [`e34f3b5820d745f5912e5af82fede6aa.json`](../evaluations/results/e34f3b5820d745f5912e5af82fede6aa.json)
- 比較対象Candidate269のwrite-once登録result [`2398d22125bd4e658fe5b653679167b5.json`](../evaluations/results/2398d22125bd4e658fe5b653679167b5.json)
- Candidate270実行のsealed `final-evidence.tar.zst`。archive SHA-256は`acaa9126785a8264c12901881cdc9517fa7cb5093414c36ee2ced8ddf68c3895`
- Candidate147実行のsealed一次trace。既存の分析結果や集計判定は使わない
- `all-agent-usage`が固定したCandidate147とCandidate270のlocal persisted rollout、および[`validation carrier再監査`](../evaluations/results/candidate147-candidate270-validation-carrier-rollout-reassessment-r1.json)

## Candidate147までの対応

| Candidate | 直接の固定差分 | この境界で加わったもの |
| --- | --- | --- |
| Candidate71 | Candidate69の`AGENTS.md`へ`VALIDATION_CLOSURE`だけを追加 | 全required validationを個別invocationとして同一model stepから発行し、全resultを一度だけmodelへ返す |
| Candidate80 | Candidate71の`VALIDATION_CLOSURE`だけを置換 | rootは一回のcustom exec wrapper内から個別`exec_command`を発行し、各exit codeをwrapper内で確認する |
| Candidate81 | Candidate71の`VALIDATION_CLOSURE`だけを置換 | 「順に」「1 commandずつ個別」は、途中resultをmodelへ戻して次を別custom tool callにする意味ではない、と固定する |
| Candidate108 | Candidate107の`VALIDATION_PLAN`だけを置換 | cell ID付きnonterminal resultでは、実行票全体がterminalになるまで同じcell IDへのwaitだけを発行する |
| Candidate147 | Candidate145の`DECISION_BOUNDARY`だけを変更 | validation境界は保持し、受領resultの停止効果を、target、permission、method、stop conditionが変わり得る後続operation classだけへ限定する |

Candidate147のvalidation経路は、次の境界を一組として持つ。

1. 検証predicate、順序、個別合格条件、停止条件を実行前にbindする。
2. rootは一回のcustom exec wrapper内でrequired validationを個別`exec_command`として順に実行する。
3. command resultをmodelへ返してから次commandを別custom tool callで発行しない。
4. wrapper内で各exit codeを確認し、失敗または利用不能なら依存する後続を発行しない。
5. 完了済みresultを一度だけmodelへ返す。
6. wrapperがnonterminalなら、同じcell IDへのwait以外を発行しない。
7. resultの停止効果をtask全体へ広げず、関係する未発行operationだけへ適用する。

Candidate147自身が新規に追加したのは7であり、1から6は直接親から保持した境界である。Candidate147をvalidation wrapperの発明元または全差分の直接親として扱わない。

## Candidate270の設計identity

- 直接の実装親: `the-caption-3ce91a4-natural-language-validation-carrier-closure-r1`
- Candidate270: `the-caption-3ce91a4-natural-language-predicate-bound-validation-result-r1`
- bundle SHA-256: `481a035966f1cc6ad8faba7fd05b07baf357d29e0a75dccc563963878547c439`
- 変更対象: root `AGENTS.md`の`VALIDATION_CLOSURE`だけ
- 保持対象: rootのvalidation wrapper、検証ごとの個別実行、途中resultのAI返却禁止、失敗時の依存後続停止、shell compound command禁止、wrapper終了時の一回返却
- 追加対象: 各確定resultを、対応するvalidation、個別合格条件および終了状態へ対応づける関係
- 非目標: TaskSpec、Case、fixture、rating、runtime、他の制御条項、releaseまたは本体反映の変更

Candidate270の直接の実装親はCandidate269である。Candidate147は、同じvalidation permission / dependency境界が先に固定されていることを確認する機序上の基準であり、Candidate270の直接親へ昇格させない。

## Candidate270本文が定める経路

Candidate270は、rootのvalidationについて次を明示している。

```text
全required validationと順序、合格条件、停止条件を固定
  -> 一つの実行票を完了させる一回の外側実行へ束ねる
  -> wrapper内で各validationを個別実行し、終了状態まで確定
  -> 失敗時は依存する後続を発行しない
  -> 個別validationの途中resultはAIへ返さない
  -> 対応づけ済みの確定resultが全部そろった時だけ一度返す
  -> 一度だけ完了を判断
```

これはCandidate147が持つ正常経路と同じpermission / dependency関係を自然な日本語で表したものである。語彙や段落形式は異なるが、固定本文だけから「focused resultをAIへ返してからfull validationを別tool callで発行する経路が合法」とは判定できない。

## 評価条件

Profileは`gpt-5.6-sol`、reasoning `medium`、Codex CLI `0.146.0`、all-agent token accounting v1、`max_workers=24`、各Case N=5を固定した。対象は次の4 Case、計20 runである。

- `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY`
- `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND`
- `TC-F03-ATOMIC-CONTEXT-CLEANUP`
- `TC-F10-ENTRYPOINT-INVENTORY-REVIEW`

Candidate269とCandidate270の登録resultにある`.compatibility`のcanonical JSON SHA-256は、どちらも`f9c46e3cc6f0c5e5ee0f0401aacfd3e4dce42e3389121647006973655c3aebcb`で一致した。比較するprompt identity以外の実効条件に差はない。Candidate270は20 / 20件が`valid`で、excluded attemptは0件だった。

## 品質とKPI

Candidate270の20 / 20件はScore `4`で、5 iterationすべての四ケース合算qualityは`100.0`だった。

| iteration | quality | all-agent `total_tokens` | `elapsed_seconds` |
| ---: | ---: | ---: | ---: |
| 1 | 100.0 | 517,171 | 286.186 |
| 2 | 100.0 | 558,935 | 282.121 |
| 3 | 100.0 | 532,952 | 303.737 |
| 4 | 100.0 | 554,071 | 294.230 |
| 5 | 100.0 | 523,969 | 271.735 |
| 中央値 | 100.0 | 532,952 | 286.186 |

比較対象Candidate269の中央値は`total_tokens=569,253`、`elapsed_seconds=368.193`だった。Candidate270の差はtoken `-36,301`（`-6.38%`）、経過時間`-82.007`秒（`-22.27%`）である。

| Case | Score範囲 | token中央値 | 経過時間中央値 |
| --- | ---: | ---: | ---: |
| F01 | 4–4 | 121,788 | 67.465秒 |
| F02 | 4–4 | 138,017 | 76.976秒 |
| F03 | 4–4 | 128,806 | 70.554秒 |
| F10 | 4–4 | 114,084 | 64.034秒 |

この差はN=5の観測値である。対象機序は直接観測できたが、KPI差の分布安定性と因果の大きさはN=5だけでは固定しない。F10は変更条項を直接消費しないread-only Caseであり、5 / 5件のScore `4`は限定した品質保持の観測にとどまる。

## traceから観測できることとできないこと

F01、F02、F03の15 runでは、focused検証の`item.completed`後にfull検証の`item.started`があり、各`command_execution`に個別の`aggregated_output`が保存されている。この記録だけではAIへの配送境界を判定できないため、同じrunのpersisted rolloutにある`response_item`を追加で監査した。

監査oracleは、profileが固定した全required command groupが同じouter `exec` callの入力に含まれること、そのcallの出力がterminal結果一件、または出力本文を持たないcell ID receiptと同一cellへの`wait`列だけからterminal結果一件へ到達することを要求する。途中receiptへvalidation outputが入った場合は失敗とする。

| 対象 | Case | pass | nonterminal run | nonterminal receipt | 途中validation output |
| --- | --- | ---: | ---: | ---: | ---: |
| Candidate147 | F01 | 4 / 5 | 1 | 1 | 19,775 bytes |
| Candidate147 | F02 | 3 / 5 | 2 | 4 | 56,237 bytes |
| Candidate147 | F03 | 5 / 5 | 1 | 1 | 0 bytes |
| Candidate270 | F01 | 5 / 5 | 2 | 3 | 0 bytes |
| Candidate270 | F02 | 5 / 5 | 2 | 2 | 0 bytes |
| Candidate270 | F03 | 5 / 5 | 1 | 2 | 0 bytes |

Candidate147は15 run中3 runでnonterminal receiptへ合計76,012 bytesのvalidation outputを配送し、12 / 15 passだった。Candidate270はnonterminal receiptを5 run、計7回使ったが、途中validation outputはすべて0 bytesで、継続も同一cellへの`wait`だけだった。このoracleではCandidate270が15 / 15 passである。

この結果は、C147の設計境界が存在したことと、C147の全runで実行機序が成立したことを分離する。また、C270の自然語差分をC147の単純な複写とは扱わない。今回の対象範囲では、C270は同じ正常経路を保持し、C147で残った途中配送を観測上は閉じた。

## 判定と再利用範囲

| 判定軸 | 判定 | 根拠 |
| --- | --- | --- |
| 実行有効性 | passed | 20 / 20 `valid`、excluded 0、比較条件一致 |
| 品質 | passed within N=5 | 20 / 20 Score `4` |
| 経路診断 | validation carrier 15 / 15成立 | F01、F02、F03の全runで単一outer call、wait-only継続、途中validation output 0 bytes、terminal result一件。KPIまたは採用gateにはしない |
| 四ケースKPI | N=5改善方向 | Candidate269比token `-6.38%`、elapsed `-22.27%`。後続Standard14へ一般化しない |
| Standard14 KPI | 評価済み | 70 / 70 Score `4`、Candidate147比token `+18.16%`、elapsed `+9.09%` |
| 採用・release・本体反映 | not decided / not authorized | 評価と別の未実施operation |

Candidate270から再利用できるのは、Candidate147までに固定されたvalidation wrapper境界を自然な日本語で保持し、確定resultとvalidation predicateの対応関係を追加した固定差分である。成功runのtool順は継承しない。外側wrapperとmodel-visible result配送を識別するoracleは、後続評価のKPI差を説明する診断に限定して再利用する。

## 後続Standard14 N=20

後続の[`Standard14 N=20`](../evaluations/results/candidate270-natural-language-predicate-bound-validation-result-standard14-n20_2026-08-17.md)では、登録済みN=5の70件を再利用し、不足210件だけを追加して累積280 / 280件がScore `4`となった。Candidate147の保存済みpoolから同じ規則で各20件を選んだ互換比較は、Candidate270のtoken中央値が`+18.75%`、elapsed中央値が`+7.58%`だった。

required validationを持つ7項目140件のpersisted rollout監査では、単一validation carrierが134件で成立した一方、6件はrequired command群が別outer callへ分離した。N=5の35 / 35成立を累積N=20で再現できなかったため、現在状態は`validation_carrier_mechanism_gate_failed / candidate270_not_adopted / release_not_created / projection_not_performed`である。成功時のcommand順を次の義務へ転記せず、分離を許したpermissionまたはdependencyの辺もこの評価だけでは一意にbindできないため、次Candidateは作成していない。
