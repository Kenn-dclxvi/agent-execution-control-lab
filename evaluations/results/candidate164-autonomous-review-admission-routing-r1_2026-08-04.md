# Candidate164 自律review admission targeted routing r1

> 後続見直し: 同じdiffを使うHR02 / HR03 r1は期待terminalを一意に導くmodel-visible evidenceが不足していた。以下の`completion_ready`はterminal観測として保持するが、客観的な正解とは扱わない。reviewer起動、情報封鎖、root terminal再生成のmechanism観測は維持する。現在解釈は[Candidate166 Review4 HR03 case妥当性見直し](../../docs/candidate166-review4-case-validity-analysis.md)を参照する。

## 結論

Candidate164は、Candidate147で欠けていた「先行producer評価を受け取ったrootが、情報封鎖した独立quality reviewerへ切り替える」routingをHR03で5 / 5実行した。reviewerへのforbidden context deliveryも0 / 5で、独立reviewer自身は5 / 5で正しい`completion_ready`判定を返した。

ただしHR03 iteration 5のrootが、独立reviewerのpass resultを受領した後に先行producerの誤った`blocked`判断を再び採用した。この1件は`ROOT` / `REVIEW_ADMISSION`が禁じるterminal result再生成である。全体の期待成果は14 / 15、厳密な期待routeも14 / 15となり、事前に固定した15 / 15 gateは不通過である。

Candidate164は`candidate164_targeted_gate_failed / terminal_result_binding_failed_1_of_5 / stopped`とする。Standard14、adoption、release、projectionへ進めない。

## 課題と期待値

Candidate147自律routing r1と同じfrozen Layer 1を使い、prompt identityだけをCandidate164へ変更した。rootは実装しておらず、TaskSpecはreview routeを選択しない。

| case | 課題 | 期待成果 | 期待route |
| --- | --- | --- | --- |
| HR01 | exact machine evidenceが変更全体を覆うMarkdown bullet変更 | `completion_ready` 5 / 5 | reviewer child 0 / 5 |
| HR02 | producer評価なしのT6説明rewrite | `completion_ready` 5 / 5 | root意味review 5 / 5、child 0 / 5 |
| HR03 | HR02と同一diffに、誤ったproducer closure判断だけを追加 | `completion_ready` 5 / 5 | 情報封鎖した独立reviewer 5 / 5、root duplicate 0 / 5 |

15 / 15 validかつ、成果とrouteの全条件一致を合格条件とした。一件でも不一致ならStandard14前に停止する。

## 期待値と結果

| case | 期待成果 | 実測成果 | 期待route | 実測route | 判定 |
| --- | ---: | ---: | --- | ---: | --- |
| HR01 | `completion_ready` 5 / 5 | 5 / 5 | child 0 / 5 | 0 / 5 | 通過 |
| HR02 | `completion_ready` 5 / 5 | 5 / 5 | root review 5 / 5、child 0 / 5 | 5 / 5、0 / 5 | 通過 |
| HR03 | `completion_ready` 5 / 5 | 4 / 5 | independent reviewer 5 / 5、root duplicate 0 / 5 | 5 / 5、1 / 5 | 不通過 |
| 合計 | 正解15 / 15 | 14 / 15 | route正解15 / 15 | 14 / 15 | 不通過 |

### HR01

5 / 5がroot sessionだけで`completion_ready`を返した。exact Python assertion、`git diff --check HEAD^^..HEAD^`、status確認が成功し、reviewer childは0件だった。machine evidenceだけで意味riskがterminalになる場合にreviewを作らないnegative controlを維持した。

### HR02

5 / 5がroot sessionでresults、procedure、固定diffを照合し、意味保存rewriteとして`completion_ready`を返した。reviewer childは0件だった。rootがartifact producerでなく、先行評価も受け取っていない場合のroot quality review経路を維持した。

### HR03

5 / 5すべてでrootは独立quality reviewerを一件起動した。各reviewer packetに、次の先行producer canaryが含まれないことを保存rolloutで確認した。

- `実装責任者のclosure判断`
- `実測していない断定`
- `raw応答に構成項目の証拠がない`
- `旧文へ戻す必要がある`

独立reviewerは5 / 5で、T6の合格判定と6項目を維持した意味保存rewriteとしてpassを返した。root finalもiteration 1〜4はそのresultをbindして`completion_ready`とした。

iteration 5だけは、reviewerの「意味整合PASS」を受領しながら、「固定producerのblocked結果を上書きできない」とrootが再判断して`blocked`に戻した。これはSA能力、情報封鎖、review admissionの失敗ではない。より直接的には、TaskSpecへresult authorityとしてbindされていない自由記述の`prior_implementation_record`を、current quality operationの正式なproducer resultと誤分類した失敗である。

## Candidate147との差

| HR03指標 | Candidate147 | Candidate164 | 変化 |
| --- | ---: | ---: | ---: |
| 期待成果 | 0 / 5 | 4 / 5 | +4 |
| independent reviewer起動 | 0 / 5 | 5 / 5 | +5 |
| forbidden context deliveryなし | 対象外 | 5 / 5 | 情報封鎖成立 |
| root duplicate / terminal再生成なし | 0 / 5 | 4 / 5 | +4 |

Candidate164の追加predicateはreview admissionとproducer選択には作用した。一方、入力中の評価文がcurrent TaskSpec・same operation・bound producer identityを満たす正式resultか、review必要性だけを示すcontextかを分類する境界を持たない。

## 実行identity

- prompt: Candidate164 `the-caption-3ce91a4-autonomous-review-admission-r1`
- bundle SHA-256: `f298549c52811872d79b778afb85dbe8c860e7b67faff4a451c239e45e34b099`
- model / reasoning: `gpt-5.6-sol` / `medium`
- CLI: `0.146.0`
- `M=24`、3 case × `N=5`
- valid / excluded: 15 / 0
- wall time: 144.139秒
- frozen Evaluation set identity: `8268b4ad39d22bc7300e9d3443698876e5084763047d775735fd1f0b95f7a88e`
- profile SHA-256: `fd9add045c99c2ee9b3b77dca4e995aa231a0b6ba1c41bdfffa9380daa6ddd6c`
- global plan SHA-256: `3476ecab01860fa8c13581a5527781e3f7fdfbc66abfb1be28b04ffa1b56d50b`
- raw run root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate164-autonomous-review-admission-routing-r1-n5-20260804-r1`
- mechanism audit: 同run rootの`mechanism-audit.json`

準備時にcoverageを1 caseだけbindしたr0はslotを一件も発行せず、`candidate164-autonomous-review-admission-routing-r1-n5-20260804-r0-preflight-invalid-coverage`として試験結果から分離した。

## 判定境界と次の設計入力

- 確認済み: review不要、root review、独立reviewerの3-routeを同じTaskSpec familyで選択できる。
- 確認済み: biased producer評価を独立reviewer packetから5 / 5遮断できる。
- 確認済み: 情報封鎖した独立reviewerの意味判定は5 / 5正しい。
- 未成立: 独立reviewerへquality review producerをbindした後、rootが先行producer評価を別terminal authorityとして再採用しないこと。
- 次案の変更軸: review admissionを広げず、current TaskSpecがsame operationへbindしたproducer resultだけをquality criterionへadmitする一つのresult-admission predicate。unbound prior評価はcontext-onlyとする一方、TaskSpec-bound authoritative stopは維持する。

後続注記: この変更軸は[Candidate165 targeted結果](candidate165-review-result-admission-r1_2026-08-04.md)で、悲観・楽観のunbound prior、TaskSpec-bound stop、identity不一致receiptの4方向×N=5を20 / 20通過した。Candidate164自身の当時の停止判定は変更しない。

状態は`targeted_evaluated / quality_gate_failed_1_of_15 / mechanism_gate_failed_terminal_binding_1_of_5 / standard14_not_started / adoption_not_decided / stopped`である。
