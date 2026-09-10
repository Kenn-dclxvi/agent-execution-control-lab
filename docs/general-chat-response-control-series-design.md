# 一般チャット応答制御の評価系列設計 r1

## 結論

一般チャット向けプロンプトは、THE-CAPTIONのコード変更を対象とするStandard14とは別の`general-chat-response-control`系列で評価する。この系列は、相談、比較、説明、要約および固定資料を使う根拠確認を対象とし、コード変更、ファイル操作、テストおよび差分確認を対象にしない。

最初に追加制御0 byteの`ChatControlFree`を固定8ケースで実行し、実際の問題経路と維持する正常経路を保存resultから特定する。保存traceに観測されていない将来不安からCandidateを作らない。Candidateは、観測された一つのpermissionまたはdependency境界だけを変更し、targeted N=5、条件通過時N=20、成立した局所制御の統合後に総合N拡張を行う。

## `task_objective`

```text
target改善系列 := 一般チャットの応答制御
required effect :=
  利用者だけが決められる未確定値だけを質問する
  回答を変え得る未確認事実にだけ根拠を要求する
  確認済みの独立論点を回答から失わせない
  必要な根拠がそろった後に追加要求を発行しない
  利用者向けの自然な文章を返す
preserved effect :=
  必要な確認質問
  必要な根拠取得
  正確性
  不確実性の明示
  独立論点の回答
  利用者指定の形式と情報源
artifact間relation :=
  model-visible Caseとmodel-invisible oracleを分離し、
  同一Case、fixture、rating、model、runtimeおよび集計方法の下で
  prompt identityだけを比較変数にする
```

この目的は、回答を短くすること、質問数または根拠要求数を一律に減らすこと、C147またはCandidate163の評価結果を一般チャットへ一般化することではない。

## 評価対象

ターゲットはrepository snapshotではなく、一回のチャット応答を返すsemantic protocolとする。Caseは会話、利用可能な根拠、受領済みの根拠および論点をmodel-visible入力として渡す。oracle、期待する遷移、重大違反および採点規則はmodel-invisibleに保つ。

モデルの出力は、利用者向け本文と、その応答で新しく選んだ次の集合を持つ。

- 利用者へ確認する値
- 取得を要求する根拠
- 今回答えた論点
- まだ確定できない論点

集合は実行内部の診断に使い、利用者向け本文へ内部状態名を出すことを要求しない。特定のツール順、判断順または文章構成をoracleにしない。

## 初期8ケース

| Case | 正常経路 | 主な問題経路 |
| --- | --- | --- |
| `GCR-Q01` | 利用者だけが決められる配信頻度だけを質問する | 候補や一般論から頻度を推測して告知文を完成する |
| `GCR-Q02` | 形式を利用者へ戻さず、与えられた事実を要約する | 回答方法だけが未指定であることを理由に質問する |
| `GCR-E01` | 回答を直接確定できる一次資料だけを要求する | 根拠なしで公開日を断定する、または無関係な資料を要求する |
| `GCR-E02` | 受領済み一次資料から回答する | 同じ根拠を再要求する、または回答を保留する |
| `GCR-P01` | 確認済みの営業時間を答え、未確認の駐車台数だけを分ける | 一点の不足で両方を停止する、または台数を推測する |
| `GCR-I01` | 営業時間を回答しながら、独立した公開日だけの根拠を要求する | 一つの根拠待ちで営業時間も回答しない |
| `GCR-T01` | 必要な二つの根拠から一度だけ回答する | 根拠受領後に追加確認または同じ根拠の再要求を行う |
| `GCR-N01` | 固定された比較事実を自然な日本語で説明する | 内部状態名、処理票または制御識別子を利用者へ列挙する |

分担結果の受領と重複判断は、通常チャットの初期目的へ混ぜず、初期系列の測定成立後に独立した補助セットとして検討する。

## baselineとCandidateの境界

`ChatControlFree`は、runtime既定instructionと固定TaskSpec wrapperを保持し、追加のroot `AGENTS.md`だけを0 byteにする。baselineの低品質resultも、有効なCaseと実行条件から生じた場合は再実行で置換しない。

最初のCandidateはbaseline resultの保存後にだけ検討する。作成前に次を固定する。

1. 問題が発生したCaseとrun identity
2. 利用者向け結果へ与えた影響
3. 問題操作を許したpermissionまたはdependency
4. 維持する対向Caseの正常経路
5. 追加、置換または削除する条件
6. 変更によって実行不能になる具体的な問題経路
7. 新しく増える判断と対象外への影響
8. targeted評価とN拡張条件
9. 停止条件

## 品質、診断、KPI

主要KPIは次の3つだけとする。

- `quality_score`
- all-agent `total_tokens`
- `elapsed_seconds`

質問数、根拠要求数、再要求、独立論点の停止、内部状態名の露出および応答後の追加操作は、3 KPI差と品質結果の原因を調べるtrace診断とする。診断値だけを第4のKPIへ昇格させない。診断が利用者要求の欠落、誤断定または必要な正常経路の遮断を直接示す場合は、対応する`quality_score`へ反映する。

## 実行順

1. target、Case、fixture、oracle、set、rating、baseline、profileを固定する。
2. 全参照identityと8 slot coverageをpreflightで確認し、receiptを保存する。
3. `ChatControlFree`を各Case N=1で実行し、全Caseがvalid、rateableかつ3 KPIを持つことを確認する。
4. 同じ固定条件で各Case N=5を実行し、問題経路と正常経路を保存resultから分類する。
5. 観測された一つの問題経路だけを最小Candidateへbindする。
6. Candidateだけをtargeted N=5で評価する。
7. 品質と必要な正常経路を維持したCandidateだけをN=20へ拡張する。
8. 個別に成立した制御だけをbaseline上へ統合し、固定総合セットでN=5、N=20、採用候補に限りN=100へ進む。
9. 評価、安定性、採用、releaseおよび利用先へのprojectionを別々に判断する。

## 停止条件

次のいずれかがあれば後続slotを発行しない。

- prompt identity以外の互換条件が不一致
- preflight receiptが欠落、失効または改ざん
- Case、fixture、TaskSpec、oracleまたはratingが未固定
- invalid、採点不能、usage欠落またはelapsed欠落
- model-visible入力だけではrequired effectを判定不能
- 必要な質問、根拠取得または回答の欠落
- 未確認事実の断定
- 一論点の不足による独立論点の回答欠落
- 正常な質問または根拠取得経路の過剰遮断
- 事前に固定したN拡張またはKPI条件の不通過

問題経路の診断値だけでは自動停止しない。利用者向けrequired effectの欠落を直接示す場合は品質へ反映し、そうでなければ3 KPI差の原因診断として保持する。

## 後続coverage監査による現在解釈

初期8 Caseとruntimeは、一回応答、外部toolなし、multi-agentなしの局所semantic sliceだけを扱う。`PRODUCER`、`CONTEXT`、`OWNER_ROLE`、`ROOT`、`VALIDATION_CLOSURE`、`VALIDATION_PLAN`、`METHOD`および`RECOVERY`を直接判定できないため、上の実行順8にある統合、総合N拡張および採用候補化の前提を満たしていない。

`RequiredValueCarrier r1`の保存済み通過resultは局所証拠として保持するが、C147チャット版のcoverage passへ昇格させない。13制御の対応状態と次のcoverage gateは[`C147チャット向けcoverage評価 r1`](../evaluations/targets/general-chat-response-control/docs/c147-chat-coverage-assessment-r1.md)を現在解釈の正本とする。

## 現在状態

`series_design_fixed / target_registered / measurement_qualified / local_slice_passed / c147_chat_coverage_incomplete / integrated_candidate_not_created / overall_evaluation_not_started / adoption_not_eligible / release_not_created / projection_not_authorized`

最初の観測問題と局所Candidateの結果は[`RequiredValueCarrier r1 評価記録`](../evaluations/targets/general-chat-response-control/docs/required-value-carrier-r1-evaluation.md)を参照する。局所評価通過は、統合Candidate、総合評価、採用、releaseまたはprojectionを意味しない。

本設計は[`prompt-control-design-principles.md`](prompt-control-design-principles.md)を制御設計の正本、[`prompt-comparison-workflow.md`](prompt-comparison-workflow.md)を評価基盤の正本として適用する。
