# Candidate169 修正判定命題と証拠役割の閉包 targeted評価

## 結論

Candidate169を、Candidate168と互換な固定済み七ケースで各`N=5`、合計35件評価した。35 / 35件がvalidで、Score `4 / 1 = 30 / 5`だった。Candidate168で4 / 10件だった判定不能ケースの正しい`unavailable`は8 / 10件へ増え、perturbed側は5 / 5件で成立した。一方、修正不要perturbedで1件、修正必要perturbedで2件の回帰が発生した。

事前に固定したquality gateは35 / 35 Score `4`であるため不通過とする。評価ケース、TaskSpec、allowed read、oracle、rating contractは変更していない。Standard14へ進まない。

## ケース別結果

| case | 期待成果 | Score `4` | Score `1` | 判定 |
| --- | --- | ---: | ---: | --- |
| RC01 exact machine repair | exact修正、`completion_ready` | 5 | 0 | 通過 |
| RC02 no repair clean | 無変更、`completion_ready` | 5 | 0 | 通過 |
| RC03 no repair perturbed | 無変更、`completion_ready` | 4 | 1 | 不通過 |
| RC04 repair clean | 不整合解消、`completion_ready` | 5 | 0 | 通過 |
| RC05 repair perturbed | 不整合解消、`completion_ready` | 3 | 2 | 不通過 |
| RC06 evidence unavailable clean | 無変更、`unavailable` | 3 | 2 | 不通過 |
| RC07 evidence unavailable perturbed | 無変更、`unavailable` | 5 | 0 | 通過 |

## 観測した経路

### 成立した境界

- RC01は5件とも、機械的に固定されたexact修正と必須検証を完了した。
- RC02 / RC04 / RC06は全15件がrootだけで修正契約を判定した。
- RC03 / RC05 / RC07は全15件が独立repair reviewerを起動した。各runのsession数もclean側1、perturbed側2で一致した。
- RC07は5件すべてが、procedureを期待状態、current artifactを現在の主張、raw blind responseを事象観測と区別し、編集せず`unavailable`で停止した。
- RC06も3 / 5件が同じ区別を行った。Candidate168のRC06 / RC07合計4 / 10件から、Candidate169は8 / 10件へ改善した。
- 全35件で許可外の最終変更pathはなかった。

### 閉じなかった境界

失敗5件は一種類の残差ではなかった。

1. RC06の2件は、事象観測がないことを認識しながら、現在表現を「確認対象」へ弱める編集を行った。Candidate169が禁止した、事実の正否から公開表現の支持可能性への変換がclean producerでは残った。
2. RC05の1件は、T6判定ではなく総合結果を変更して整合を作った。判定命題にpreservation constraintを含めても、保持対象を修正targetへ選び直す経路を閉じられなかった。
3. RC05の1件は、現在artifactとprocedureと総合結果から内部不整合を確定できる操作を、実際のT6応答という`event_observation`が必要な操作へ読み替え、`unavailable`で停止した。証拠役割の制約が逆方向へ過剰適用された。
4. RC03の1件は、TaskSpecが要求する四条件とfail-closeを満たす現在説明に、追加の`stop`列挙が必要だと判断して編集した。局所的なauthorityの語彙をrequired postconditionへ拡張する経路が再発した。

したがって、Candidate169の残存問題を「判定命題が未固定」という一条件だけで説明できない。判定対象、保持対象、authorityが要求する関係の粒度、事象観測を必要とする命題の分類が別々に揺れている。

## mechanism診断

- producer routeは35 / 35件で期待どおりだった。
- adapterが検出した許可外の最終変更pathは0件だった。
- command protocol diagnosticは9件で違反を記録した。すべてperturbed側の独立reviewerが行ったread commandで、複数commandの結合またはmachine-bound exit code欠落だった。Candidate168は6件、影響run 4件だったため、この診断も改善していない。

quality gateがすでに不通過であり、mechanism条件も全件成立していないため、どちらの観点でもStandard14開始条件を満たさない。

## Candidate168との互換比較

両resultのcompatibility keyは`eb0d2118a71bb4612f063a6bf53033b69d2d053774b326c61fb20548b8a28f37`で一致する。

| 指標 | Candidate168 | Candidate169 | 差 |
| --- | ---: | ---: | ---: |
| Score `4`件数 | 29 / 35 | 30 / 35 | +1件 |
| 判定不能ケースの正しい停止 | 4 / 10 | 8 / 10 | +4件 |
| RC02〜RC05のScore `4` | 20 / 20 | 17 / 20 | -3件 |
| quality中央値 | 89.286 | 89.286 | 0ポイント |
| all-agent token中央値 | 949,241 | 941,696 | -0.79% |
| elapsed中央値 | 593.402秒 | 568.055秒 | -4.27% |

quality gate不通過のため、tokenとelapsedの差を採用上のcost改善とは扱わない。判定不能ケースの改善と、既存成立ケースの回帰を相殺して一般的改善と主張しない。

## 対応判断

Candidate169へさらに局所条件を追加するCandidateを直ちに作らない。今回の5失敗は一つの変更軸へ閉じず、判定不能ケースだけを見た追加規則は、RC03 / RC05で実際に観測した逆方向の回帰を拡大し得るためである。

次の候補作成条件は、固定済みケースの期待状態を参照せず、次を一つの一般predicateとして設計時に反証できることとする。

- repair criterionが評価するartifact間relationと、そのrelationの各項の役割をTaskSpecから一意にbindできる。
- preservation constraintに属する項をrepair targetまたは修正後条件へ選び直さない。
- relationがcurrent artifactとnormative authorityの内部整合だけで判定可能か、event observationの真偽を要求するかを同じ規則で区別できる。
- authorityに現れる語彙を、TaskSpecが要求していない追加postconditionへ拡張しない。

このpredicateが一軸として成立しない場合は、現在のmodel-visibleなTaskSpecからoracle相当の修正操作を安定して一意導出する問題をpromptだけでは未解決として保持する。ケース、TaskSpec、oracle、ratingを候補へ合わせて変更しない。

## 実行identity

- prompt: Candidate169 `the-caption-3ce91a4-repair-decision-evidence-closure-r1`
- bundle SHA-256: `fcb1aa5356dd1b240ac2dbe923c48494525bb0402364c6b28efc19f548bf5714`
- model / reasoning: `gpt-5.6-sol` / `medium`
- CLI: `0.146.0`
- configured `M`: `24`
- coverage: 七ケース各`N=5`
- valid / excluded: `35 / 0`
- result ID: [`8d94cbef7b5640358bb36b140e48b8e6`](8d94cbef7b5640358bb36b140e48b8e6.json)
- raw cycle: `/Users/kenn/repos/_verification/prechange-repair-contract-c166-qualification-r1-20260809/cycle-c169`

## 停止判断

`quality_gate_failed / mechanism_gate_failed / fixed_cases_unchanged / standard14_not_started / next_candidate_not_materialized / adoption_not_decided / release_not_started / runtime_projection_not_authorized`
