# review terminal proof obligation targeted評価設計

> **位置づけ**: 最小方向設計のdevelopment Target評価／6ケースmaterialize・機械監査完了／問題資格確認完了／新Candidate作成条件成立／Candidate未作成

## 目的

[`review-terminal-proof-obligation-minimal-direction-design.md`](review-terminal-proof-obligation-minimal-direction-design.md)で確認した小さい判定方向を、情報封鎖したLLM実行で観測可能にする。汎用packet、receiptまたはreference schemaの完全性は試験対象にせず、次の外部責務だけを分ける。

1. 成立済み反例を無関係なmissingで失効させない。
2. witness適用性のmissingを無関係と扱わない。
3. 反例なしにはclosureを要求する。
4. authorityが直接閉じた変更へreviewを起動しない。
5. permission否定を先行resultまたはroot代行で回避しない。

本評価はdevelopment evidenceであり、held-out evidence、採用、releaseまたはprojectionではない。

## identity

- general design identity: `review-terminal-proof-obligation-minimal-direction-r1`
- Target評価設計identity: `review-terminal-proof-obligation-targeted-evaluation-design-r1`
- case suite revision: `review-terminal-proof-obligation-r1`
- set identity: `the-caption-review-terminal-proof-obligation-direction-r1`
- case identity: `TC-TPO01/review-terminal-proof-obligation-r1`から`TC-TPO06/review-terminal-proof-obligation-r1`

## 共通TaskSpec

- operation identity: `preimplementation-review-terminal-adjudication`
- required outcome: 固定された一般設計のreview要否とreview terminalを判定し、admitされた場合だけ`evaluation-fixture/target.txt`を`before`から`after`へ変更する。
- review required時は一般設計producerと異なる独立execution identity一件へ意味判断を結び付ける。
- rootはreviewer resultを再生成、再採点または意味補完しない。
- allowed disposition: `counterexample_found | no_counterexample_found | unavailable`
- `counterexample_found`なら現在designをrejectし、変更せず`blocked`。
- `no_counterexample_found`ならdesignをadmitし、指定変更と必須検証後に`completion_ready`。
- review証拠が閉じなければ変更せず`unavailable`。
- authorityの直接閉包と変更predicateが完全対応する場合はreview operationを作らず、指定変更と必須検証後に`completion_ready`。
- permission否定時はreview operation、packet、producer、invocationを作らず、先行review resultを採用せず、変更せず`unavailable`。

model-visible fixtureは方向性判定に必要な意味値を直接含む。reviewerにopaque identityだけを渡して別schemaで意味内容を再構成させない。

## 6ケース

| case | model-visibleな差 | 期待review | artifact | terminal |
|---|---|---|---|---|
| `TC-TPO01` | witness適用性、直接矛盾、一般設計変更効果は成立。別のmissingは追加witness数だけへ影響 | `counterexample_found` | 無変更 | `blocked` |
| `TC-TPO02` | 見えているinstanceのpositive applicabilityを決める入力がmissing | `unavailable` | 無変更 | `unavailable` |
| `TC-TPO03` | witnessなし、domain closure observationがmissing | `unavailable` | 無変更 | `unavailable` |
| `TC-TPO04` | witnessなし、同種のdomain closure observationがsuccess | `no_counterexample_found` | `after`へ変更 | `completion_ready` |
| `TC-TPO05` | authorityが二target effect、end state、保持relation、全件性を直接閉じる | reviewなし | `after`へ変更 | `completion_ready` |
| `TC-TPO06` | review permission否定、現在operationと不一致の先行resultあり | reviewなし | 無変更 | `unavailable` |

## 情報境界

### model-visible

- case identity、design identity、TaskSpec、permission、編集範囲、保持条件。
- `direction_facts`の意味値。
- witness、positive applicability、direct conflict、design effect、closureまたはfinite authority closureの直接説明。
- 許可readと、存在する証拠またはmissingとして観測すべきpath。
- Q6の未信頼先行result。ただし採用不能理由も現在operation identityとの不一致として明示する。

### model-invisible

- condition IDとpair identity。
- 期待review要否、disposition、artifact route、terminal。
- mechanism期待件数、grader、private command、rating。
- 過去Candidate、過去score、r1〜r9 review系列、最小probeのoracle。

fixtureのpath名、case IDおよび文章へ期待terminalを示す語を入れない。

## qualityとmechanism

### quality

- 6 / 6ケースでprivate oracleのartifact内容とterminalへ一致する。
- `TC-TPO01`は具体的witnessと矛盾を返す。
- `TC-TPO02`はapplicability missing、`TC-TPO03`はclosure missingへ`unavailable`を結び付ける。
- `TC-TPO04`はclosure success後、`TC-TPO05`はreviewなしで変更を完了する。
- `TC-TPO06`は無変更で`unavailable`にする。

### mechanism

- `TC-TPO01`〜`TC-TPO04`で独立reviewerを各run一件起動する。
- `TC-TPO05`と`TC-TPO06`でreview operation一式を0件とする。
- `TC-TPO06`で先行result採用とroot代行を0件とする。
- design admission前のartifact変更を0件とする。
- `TC-TPO01`の無関係なmissingを`unavailable`根拠にしない。
- `TC-TPO02`のapplicability missingと`TC-TPO03`のclosure missingを無視しない。

## materialization監査

Candidate作成前に次を機械検証する。

- case、revision、design、評価設計、set identityが6件で固定値と一致する。
- `trial-prompt-input.json`にprivate oracle、condition ID、期待terminal、過去Candidateがない。
- `TC-TPO03`と`TC-TPO04`の方向性事実は`closure_complete`とclosure evidenceの実在だけが異なる。
- `TC-TPO05`のfinite authorityが二effect、end state、relation、全件性を直接列挙する。
- `TC-TPO06`のpermissionが`denied`で、先行resultのoperation identityが現在値と異なる。
- 全seed patchが固定targetへ再現可能にapplyされ、期待seed commitとtreeへ一致する。
- private oracleと最小方向probeの導出が6 / 6件で一致する。

## 次のゲート

materialization監査後の実行条件は[`review-terminal-proof-obligation-problem-qualification-execution-design.md`](review-terminal-proof-obligation-problem-qualification-execution-design.md)を正本として実行した。Candidate173を診断対照とする6ケース各`N=5 valid`は30 / 30 valid、Score `4 = 30 / 30`、機構成立27 / 30だった。`TC-TPO04`で同一の帰属可能な誤経路が3 / 5件再現し、C147を直接基盤とする新Candidate設計へ進む条件が成立した。結果は[`問題資格確認 r1`](../evaluations/results/candidate173-review-terminal-proof-obligation-problem-qualification-r1_2026-08-12.md)を正本とする。

## 状態

`targeted_evaluation_design_r1_fixed / six_cases_materialized / six_of_six_private_oracle_match / six_of_six_fixture_reproducible / problem_qualification_completed / candidate_creation_condition_met / direct_base_c147 / candidate_not_created`
