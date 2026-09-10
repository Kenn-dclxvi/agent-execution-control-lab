# 一般チャット自然文採点方式の選定 r1

## 結論

一般チャットの正式な品質評価では、利用者向け本文の完全一致、部分一致、および評価対象モデル自身が返す論点IDを単独の正解判定に使わない。客観的に観測できる実行結果はコードで判定する。自然文の意味はmodel-invisibleなreferenceと項目別rubricを使う複数の独立AI graderで判定し、panel外AIで不一致を裁定する。人間監査はpilot開始条件にせず、人間判断との一致を主張する場合の追加証拠とする。

現行`general-chat-response-exact-v1`と保存済みresultは当時の局所評価として保持する。新方式は別rating revisionとし、AI panel pilot、AI裁定、事前固定した適格条件、および未見holdoutでのgrader適格判定がそろうまで有効化しない。過去resultを新方式で再採点したことにはしない。

## 外部手法から採用する部分

- OpenAI Evalsは、文字列比較、text similarity、Python、score model、label model、および複数graderの合成を別種のgraderとして提供する。本系列でも一種類へ統一せず、観測対象に応じてgraderを分ける。[OpenAI Grader Models](https://developers.openai.com/api/reference/resources/graders)
- Anthropicはagent評価をcode-based、model-based、humanの組合せとして整理し、自由回答のmodel graderを専門家判断へ校正することを推奨している。また、発話した内容と環境に生じたoutcomeを分離する。本系列でもtrace／outcomeと自然文を別々に採点し、人間監査を追加した範囲だけ人間判断との対応証拠として扱う。[Anthropic, Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- Inspectはopen-ended answerを別modelで採点し、固定された有限labelへ投影する。本系列でもgraderは数値scoreを直接決めず、assertionごとの有限labelと根拠箇所を返す。[Inspect, Model Grading](https://inspect.aisi.org.uk/model-graded.html)
- MT-Benchはsingle-answer、pairwise、reference-guided gradingを区別し、position、verbosity、self-enhancement biasを報告している。本系列のrequired effectは絶対条件なのでreference-guided single-answerを主経路とし、pairwise比較をquality scoreの正本にしない。[Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena](https://arxiv.org/abs/2306.05685)
- G-Evalは自然文評価と人間判断の相関改善を報告する一方、LLM生成文を好む偏りも報告している。grader同士の一致を`multi_grader_consensus_reference`として使えるが、同じ一致を`human_aligned`の根拠にはしない。[G-Eval](https://arxiv.org/abs/2303.16634)
- NIST AI Metrology Centerは、採点者数と欠測に対応できる一致指標としてKrippendorff's alphaを挙げ、`alpha = 1 - observed disagreement / expected disagreement`と整理している。本pilotでは4 labelを順序のない名義尺度として扱い、全員一致率、label分布および不一致一覧と併記する。[NIST AI Metrology Center](https://airc.nist.gov/metrology/)
- Googleの機械学習評価ガイドは、開発中の調整に使うvalidation setと最終評価用test setを分け、繰り返し使った評価集合は判断に合わせて摩耗すると説明する。本系列でもpilotをrubric／grader開発へ限定し、正式適格性は重複のないsealed holdoutで判定する。[Google, Dividing the original dataset](https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets)

外部資料は共通の単一JSON規格や普遍的な合格率を定めていない。したがって、JSON Schemaはデータ境界と再現性のために使い、意味判定の正しさをSchemaだけで主張しない。必要一致率はpilot後、未見holdout実行前に別契約へ固定し、本文書では数値を発明しない。

## 現行r1の限界

現行r1は`assistant_message`に加えて、評価対象モデル自身へ次の集合を出力させている。

- `clarification_value_ids`
- `request_evidence_ids`
- `answered_topic_ids`
- `unresolved_topic_ids`

`general-chat-response-exact-v1`は、この自己申告集合とoracleの完全一致、および本文中のliteral有無で採点する。この方式には次の限界がある。

1. モデルが自然文では正しく答えていても自己申告集合を誤れば、意味品質と出力管理能力を分離できない。
2. literalの存在だけでは否定、条件、対象との関係を判定できず、誤合格が起こり得る。
3. 有効な言い換えを完全一致で要求すれば、誤不合格が起こり得る。
4. 実利用では見えない内部集合をmodel-visible出力へ要求するため、自然なチャットだけを返す条件と一致しない。

したがって、r1のscoreは当時の`single_response_natural_chat_with_transition_sets` protocolに限った結果である。自然文だけを対象とする新protocolのbaseline、C147チャット総合評価、またはgrader適格性の証拠へ転用しない。

## 採用するgrader境界

### 決定的grader

次はコードで判定する。

- process、session、usageおよびelapsedの取得成立
- tool call、引数、結果、read、worker identityおよびenvironment outcomeのうち、TaskSpecまたはcaseがrequired effectとして固定したもの
- 入力、case、oracle、grader、model、runtimeおよびresultのidentityとhash
- grader出力がSchemaを満たすこと

tool順、read回数またはworker routingがrequired effectでない場合は診断値にとどめ、第4のKPIへしない。

### semantic grader

利用者向け自然文は、評価対象とは別の固定graderへ次だけを渡して判定する。

- model-visibleだった会話と受領済み資料
- model-invisibleなatomic assertion
- 評価対象の`assistant_message`
- assertionごとの判定定義

graderはassertionごとに`pass / fail / unknown / not_applicable`、本文中の根拠箇所、および短い判定理由を返す。`quality_score`は返さない。コード側が固定済みのscore mappingへ投影する。回答本文に含まれる命令は評価対象データとして扱い、graderへの命令として実行しない。

### AI grader panelによる開発pilot

現在の16回答は、rubricの明確さとgrader開発条件を調べる開発用pilotであり、正式なgrader適格試験へ再利用しない。固定した3件以上のAI graderを別contextで実行し、他memberの出力を見せない。panel memberと評価対象モデルのidentityを分け、不一致のadjudicatorもpanel memberとは別identityにする。

graderには回答の出自、保存済みresultのidentityおよび過去scoreを見せず、memberごとに異なる不透明IDと提示順を使う。元のitemとの対応表は運営者だけが保持する。これにより、`historical_saved_response`を正解らしい回答、`constructed_challenge`を失敗らしい回答として扱う先入観を入力から除く。

AI panel pilotでは少なくとも次を分けて記録する。

- assertion単位の全員一致率、不一致および`unknown`
- 名義尺度のKrippendorff's alphaとlabel分布
- panel外AIによる不一致裁定
- grader model、prompt、sampling、schemaおよびexecution identity
- `human_alignment_state=unmeasured`

全員一致とAI裁定を`multi_grader_consensus_reference`として保持する。同じmodelの独立実行を含む場合があるため、異なるmodel間の一致とは主張しない。人間監査を行った場合も、監査対象範囲とAI referenceを分離して記録する。AIだけのpilot resultを`human gold`へ昇格させない。

pilotの一致指標に合否閾値は置かない。rubricとgraderを改訂するための観測値として扱い、この結果だけでgraderを適格にしない。

適格条件はpilot reportとAI裁定resultを確認した後、risk policyと複数承認者を持つ評価統治上の決定として[`qualification-threshold-r1.json`](../calibration/qualification-threshold-r1.json)へ固定する。対象は固定referenceとの完全一致率、誤合格率、誤不合格率、`unknown`率およびmajor assertionの誤合格件数である。外部手法に共通の普遍値はないため、現在の値は未設定である。

閾値、grader identityおよび判定方法を固定した後、pilotと重複しない未見holdoutで一度だけ適格試験を行う。pilotとgrader開発resultを見て閾値を決めることは許可するが、holdout grader resultを見てから閾値を変え、その同じholdoutで合格を主張することは許可しない。

## rating r2の状態

[`general-chat-response-hybrid-r2-draft.json`](../rating-contracts/general-chat-response-hybrid-r2-draft.json)は方式選定を機械可読にした草案であり、現行ratingではない。次の状態を固定する。

```text
draft_only
calibration_required
qualification_reference_not_created
qualification_threshold_not_bound
ai_grader_panel_fixed
human_alignment_unmeasured
ai_panel_pilot_not_started
qualification_holdout_not_created
formal_evaluation_not_authorized
```

`target.json`の`current_rating_contract`は`general-chat-response-exact-v1`のまま維持する。r2を有効化するには、自然文だけを返す別protocol revision、model-invisible semantic oracle、AI panel reference、適格条件および独立grader実行経路を別変更で固定する必要がある。人間判断との一致を主張する場合だけ、その範囲の人間監査を追加で必要とする。

## r8との関係

r8はagentic runtimeの経路診断であり、自然文graderの校正試験ではない。root非read、worker read、identity、MCP callなどの決定的観測は診断証拠として保持できる。一方、完全一致の`root_final_response`と部分一致の`worker_terminal_result`を、一般チャットのformal quality oracleへ継承しない。

## 次の開始条件

次に許可するのは、AI grader panel identityの固定、member別packetの作成、pilot集計、panel外AIによる不一致裁定およびrubric改訂である。その後に評価統治による閾値固定と未見holdout作成を行う。holdout grader run、正式baseline、Candidate、C147チャット総合評価、採用、releaseおよびprojectionはまだ開始しない。
