# Candidate261 TaskSpec内部状態の出力先閉鎖設計

## 結論

Candidate261はCandidate147を直接の基準にする。Candidate237でF02について成立した`SPEC`の二文だけを逐語移植し、Candidate254でA01の不要な開始状態確認が減った事実を別ケースへ適用する根拠として使う。

Candidate237とCandidate254の自然文全文は継承しない。Candidate237は同じ出力境界をF02で成立させたが、root本文が15,271 bytesで、C147より4,499 bytes長い。Candidate261はCandidate147のoperation class別`result_effect_scope`、証拠取得条件、実行者と結果の対応、検証境界を逐語保持する。これにより、Candidate254 F03で20件中6件再発した開始確認とreadの分離を許した弱い自然文へは移行せず、Candidate147でtargeted 15件中15件成立した結果影響範囲の関係を維持する。

追加する条件は次のとおりとする。

> TaskSpecへの固定と固定した各項目の値は、作業を制御するための内部状態であり、固定した事実も、その内容も、利用者向けの進捗として出力してはいけない。これは、利用者が決める必要のある成果の値を尋ねること、permissionを拒否されたため停止を伝えること、完了したoperationの最終結果を返すことを妨げない。

この変更は、開始状態を読む手順を禁止しない。利用者が選ぶ必要のある値が未固定で、開始状態を後続作業へ使えず、進捗としても出力できない場合に、開始状態resultの受け取り先をなくす。TaskSpecが開始状態の観測自体を要求し、その結果を未完了の判断へ使う場合は、その正常経路を残す。

## Identity

- candidate number: Candidate261
- prompt identity: `the-caption-3ce91a4-spec-output-consumer-closure-r1`
- direct baseline: Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`
- changed target: root `AGENTS.md`
- changed axis: `SPEC`の内部状態を利用者向け進捗へ出力できるpermission
- Candidate237の扱い: F02で成立済みの局所境界と二文の逐語source。親本文または全文継承元にはしない
- Candidate254の扱い: A01の保存traceと別ケースでの対応証拠。親本文または全文継承元にはしない
- evaluation status: `not_evaluated`
- adoption / release / runtime projection: `not_decided / not_created / not_projected`

## Candidate作成前の検討gate

| 項目 | 固定内容 |
| --- | --- |
| 1. 比較の基準と最短正常経路 | Candidate147。利用者が選ぶ必要のある値が未固定なら、その値だけをclarification resultとして返す。開始identity結果がreadを禁止しない場合は、Candidate147の`result_effect_scope`に従い、開始確認と許可済みreadをAIの次判断より前に発行対象へ固定する |
| 2. 保存traceで確認した問題経路 | C147 A01の中央値経路は、開始workspace、branch、HEAD、clean状態を確認し、その内容を進捗として出力した後、未指定modeを質問した。C254 A01は20件中18件でrepository evidenceを発行せず、未指定modeだけを質問し、C147比でtoken `-45.93%`、経過時間`-45.66%`だった。Candidate237 F02は同じ出力境界を適用し、品質5 / 5、TaskSpec固定の事実または内容の進捗出力0 / 5、tokenはC147比`+0.55%`だった |
| 3. 問題を許した辺 | C147の`SPEC`は`spec_ready=false`で未固定値だけをclarification resultにすると定める一方、TaskSpecへ固定した事実または値を別の進捗resultとして出力するpermissionを明示的に閉じていない。TaskSpecは開始状態の観測を許可できるが、その結果の利用者向け出力先までは閉じない |
| 4. 変更する条件 | Candidate237で成立した二文をC147の`SPEC`へ逐語追加する。clarification result、permission拒否、terminal resultは除外して必要な利用者向け出力を残す |
| 5. 実行できなくなる問題経路 | 未固定のrequired outcome valueを質問する前に、後続作業へ使えない開始状態を取得し、その取得事実または値を進捗として返す経路。開始状態を取得しても合法なconsumerが存在しないため、証拠取得条件も成立しない |
| 6. 維持する正常経路 | 未固定値の質問、permission拒否の通知、terminal resultの返却、TaskSpecが開始状態を必要な未完了判断へ直接bindした場合の観測。F01 / F02 / F03ではC147の`DECISION_BOUNDARY`をbyte同一で保持する |
| 7. 新しく増える判断と対象外影響 | 新しいlabel、順序、read回数、command、例外手順は増やさない。出力が進捗、確認、permission拒否またはterminal resultのどれかを区別する必要はあるが、既存のresult種別を使う。進捗へ必要な利用者観測値まで隠さないよう、A01以外の品質を後続Standard14で確認する |
| 8. 評価 | 最初はA01とF03各N=5。品質、A01の開始状態確認、F03の開始確認とreadの分離、all-agent `total_tokens`、`elapsed_seconds`を別々に記録する。比較には同一条件のCandidate147保存resultを使い、新しいC147 runは発行しない |
| 9. 停止条件 | Score `4`未満、必要なclarification欠落、開始result受領前の禁止済み変更またはrequired commandが一件でもあれば停止する。機序成立率は品質再現性との相関100%が確認されていないため、一件の不成立だけでは自動停止しない。tokenまたは経過時間の一方が増えた場合は必要処理との対応を監査し、説明できなければ正式採用へ進めない |

九項目を固定できたため、Candidate bundleを作成した。評価profileと評価slotは、比較前照合を別途完了するまで作成または発行しない。

## Bundle identity

- bundle path: `prompts/candidates/the-caption-3ce91a4-spec-output-consumer-closure-r1`
- bundle SHA-256: `e651154c31525acf346ce42f0dd002e79522ecb0b5cc478fb56d272df763b7ad`
- root `AGENTS.md`: 11,198 bytes
- Candidate147との差: `+426` bytes
- Candidate254との差: `-2,430` bytes
- Candidate237との差: `-4,073` bytes
- changed target: `AGENTS.md`だけ
- root以外の18 target: Candidate147と同一entry

Candidate147との差分は、Candidate237で成立した二文の追加だけである。Candidate147の`DECISION_BOUNDARY`は逐語同一であり、Candidate237またはCandidate254の自然文再構成は含まない。

## C147から変更しないもの

- `DECISION_BOUNDARY`全文。`result_effect_scope`、停止効果の非伝播、相互非依存invocation、開始identityと許可済みreadの関係を逐語保持する。
- `EVIDENCE_GATE`全文。Candidate254からCandidate260までの部分read、回数条件、取得条件の作り直しは継承しない。
- `VALIDATION_CLOSURE`、`VALIDATION_PLAN`、`METHOD`全文。Candidate254の自然文検証境界は別の変更軸なので混ぜない。
- その他のroot `AGENTS.md`条項とroot以外の全target。

## C254から継承しないもの

- 用語説明と全条項の自然文再構成。
- `DECISION_BOUNDARY`の二文への短縮。
- 狭いcontextの再read、正確な行位置の再検索、owner語列、validation方法に関する追加説明。
- 特定のcommand構成、read範囲、待ち時間または成功runの処理順。

## Candidate237から継承しないもの

- 用語説明と13条項の自然文再構成。
- C147より4,499 bytes増えたmodel-visible本文。
- F02で同時に保持されていた担当起動、再取得、検証方法など、今回の二文以外の差分。
- Candidate237のtargeted結果をA01、F03またはStandard14へ一般化した主張。

## 評価判断

初回A01 / F03各N=5では、品質と機序を別に記録する。A01の開始状態確認が減っても品質を満たさなければ失敗である。反対に開始状態確認が一件残っても、それだけで品質失敗と完全に対応しない限り、機序100%を一律の合否条件にはしない。

品質を維持した後に、Candidate147保存resultとの同条件KPIを比較する。tokenと経過時間がともに減ればStandard14へ進む候補にできる。一方だけが増えた場合は、増加が必要な正常処理によるものかを人間が判断できる形へ分解する。Candidate作成、targeted評価、Standard14、正式採用、releaseおよび本体反映を別の状態として扱う。

## 現在状態

`candidate_creation_gate_passed / c147_direct_baseline_fixed / candidate237_spec_boundary_verbatim_reused / spec_output_consumer_closure_only / c147_result_effect_scope_byte_preserved / candidate261_bundle_created / bundle_identity_verified / a01_f03_n5_completed / quality_passed / a01_start_check_1_of_5 / f03_c147_initial_issuance_preserved_1_of_5 / aggregate_token_regressed_6_09_percent / unjustified_cost_regression / additional_n_not_authorized / standard14_not_authorized / adoption_not_approved / release_not_created / projection_not_performed`

評価結果と次のpermission閉鎖候補は、[Candidate261 A01 / F03 N=5結果](../evaluations/results/candidate261-spec-output-consumer-closure-a01-f03-n5_2026-08-16.md)を正本とする。

一次参照は、[`Candidate147設計`](candidate147-result-effect-scope-design.md)、[`Candidate237設計`](candidate237-taskspec-progress-suppression-design.md)、[`Candidate237 F02 N=5結果`](../evaluations/results/candidate237-taskspec-progress-suppression-f02-n5_2026-08-15.md)、[`Candidate254とCandidate147のN=20原因分解`](candidate254-candidate147-standard14-n20-control-group-causal-decomposition.md)、[`Candidate254 Standard14 N=20結果`](../evaluations/results/candidate254-independent-check-same-model-step-standard14-n20_2026-08-16.md)および[`Prompt制御の検討原則`](prompt-control-design-principles.md)とする。
