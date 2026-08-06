# the-caption profile index

`the-caption` target instanceの`legacy_root` execution profileを引くための索引である。profileの作成・revision・互換条件・保存済みrun再利用の規則は[`evaluations/AGENTS.md`](../AGENTS.md)、実行方法は[`docs/evaluation-loop-manual.md`](../../docs/evaluation-loop-manual.md)を正本とする。

各profile JSONがmodel、reasoning、Agent/runtime/CLI、permission、対象set / case、rating contract、repetitionなどの固定条件を持つ。実行結果、score、KPI、停止判断の正本は[`evaluations/results/`](../results/README.md)の各result本体であり、このREADMEへCandidateごとの評価史を複製しない。

## 現行・直近のprofile系列

### Review admission / information closure

Candidate147のinformation closureとCandidate164〜166のreview admission系列で使用したprofileをまとめる。

| 系列 | profile | 用途 | result |
| --- | --- | --- | --- |
| task qualification | [`dev-r1`](candidate147-information-closure-task-qualification-dev-r1-medium-m24-n3-cli0146.json) / [`dev-r2`](candidate147-information-closure-task-qualification-dev-r2-medium-m24-n5-cli0146.json) | implementation record有無をcase pairで確認するdevelopment qualification | [`result`](../results/candidate147-information-closure-task-qualification-dev-r1-r2_2026-08-04.md) |
| document development | [`doc-dev-r1`](candidate147-information-closure-document-task-development-r1-medium-m24-n3-cli0146.json) / [`r2`](candidate147-information-closure-document-task-development-r2-medium-m24-n5-cli0146.json) / [`r3`](candidate147-information-closure-document-task-development-r3-medium-m24-n5-cli0146.json) | 文書課題のdevelopment qualification | [`result`](../results/candidate147-information-closure-document-task-development-r1-r3_2026-08-04.md) |
| document held-out / SA | [`held-out`](candidate147-information-closure-document-heldout-r1-medium-m24-n5-cli0146.json) / [`independent SA`](candidate147-information-closure-document-sa-r1-medium-m24-n5-cli0146.json) | held-out判別と明示的独立reviewer diagnostic | [`result`](../results/candidate147-information-closure-document-heldout-sa-r1_2026-08-04.md) |
| autonomous routing | [`C147`](candidate147-information-closure-autonomous-routing-r1-medium-m24-n5-cli0146.json) / [`C164`](candidate164-autonomous-review-admission-routing-r1-medium-m24-n5-cli0146.json) | review operationの自律routing / admission | [`C147`](../results/candidate147-information-closure-autonomous-routing-r1_2026-08-04.md) / [`C164`](../results/candidate164-autonomous-review-admission-routing-r1_2026-08-04.md) |
| result admission | [`C165 targeted`](candidate165-review-result-admission-r1-medium-m24-n5-cli0146.json) / [`C165 Standard14`](candidate165-review-result-admission-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json) | review result authority gateと既存Standard14 quality確認 | [`targeted`](../results/candidate165-review-result-admission-r1_2026-08-04.md) / [`Standard14`](../results/candidate165-review-result-admission-v14-medium-standard14-atomic-n5-cli0146_2026-08-04.md) |
| prior evaluation admission | [`C166 preservation gate`](candidate166-prior-evaluation-review-admission-r1-medium-m24-n5-cli0146.json) | prior evaluationを含むReview4 preservation | [`result`](../results/candidate166-prior-evaluation-review-admission-r1_2026-08-04.md) |
| held-out generalization | [`C147 held-out`](candidate147-information-closure-heldout-r1-medium-m24-n5-cli0146.json) | development pairを流用しないheld-out確認 | [`result`](../results/candidate147-information-closure-heldout-r1_2026-08-04.md) |

case妥当性や現在解釈はprofile READMEへ上書きせず、対応resultと[`docs/`](../../docs/README.md)の分析文書を参照する。

### Rating v14 Medium Standard14の比較anchor

2026-08-03に単一互換条件へ揃えた比較anchorは次のprofileである。実測値はprofileではなく対応resultを正とする。

| 条件 | profile | result |
| --- | --- | --- |
| Baseline | [`baseline-current-r2-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1`](baseline-current-r2-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json) | [`Baseline / ControlFree / C147`](../results/baseline-control-free-candidate147-v14-medium-standard14-atomic-n5-cli0146_2026-08-03.md) |
| ControlFreeRepository | [`control-free-repository-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1`](control-free-repository-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json) | [`Baseline / ControlFree / C147`](../results/baseline-control-free-candidate147-v14-medium-standard14-atomic-n5-cli0146_2026-08-03.md) |
| Candidate43 | [`candidate43-outcome-authority-boundary-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1`](candidate43-outcome-authority-boundary-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json) | [`C43 / C71 / C147`](../results/candidate43-candidate71-candidate147-v14-medium-standard14-atomic-n5-cli0146_2026-08-03.md) |
| Candidate71 | [`candidate71-validation-closure-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1`](candidate71-validation-closure-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json) | [`C43 / C71 / C147`](../results/candidate43-candidate71-candidate147-v14-medium-standard14-atomic-n5-cli0146_2026-08-03.md) |

Candidate147のprofile identityと実行条件は上記result本体を正とする。READMEから推測して補完しない。

### ControlFree readable系列

ControlFreeRepositoryへ説明可能な小さい制御を段階的に加えた系列は、対象caseごとにprofileを分け、最後にStandard14へ統合している。

| 段階 | profile | result |
| --- | --- | --- |
| 5項目一括の初回 | [`Candidate148 Standard14`](candidate148-five-point-execution-control-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json) | [`result`](../results/candidate148-free-five-point-execution-control-v14-medium-standard14-n5-cli0146_2026-08-03.md) |
| 4判断ルール targeted | [`6 case`](candidate152-four-decision-rules-readable-v14-reasoning-medium-a01-a02-f01-f02-f04-f07-global-m24-n5-cli0146-r1.json) / [`F08`](candidate152-four-decision-rules-readable-v14-reasoning-medium-f08-global-m24-n5-cli0146-r1.json) / [`F03`](candidate152-four-decision-rules-readable-v14-reasoning-medium-f03-global-m24-n5-cli0146-r1.json) | [`result`](../results/candidate152-free-four-decision-rules-readable-v14-medium-targeted-n5-cli0146_2026-08-03.md) |
| 5文一括の再試験 | [`Candidate156 Standard14`](candidate156-five-prompt-conditions-readable-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json) | [`result`](../results/candidate156-free-five-prompt-conditions-readable-v14-medium-standard14-n5-cli0146_2026-08-03.md) |
| 個別確認 | [`C157 F08`](candidate157-focused-prechange-research-readable-v14-reasoning-medium-f08-global-m24-n5-cli0146-r1.json) / [`C158 A01/A02`](candidate158-outcome-method-readable-v14-reasoning-medium-a01-a02-global-m24-n5-cli0146-r1.json) / [`C159 F02`](candidate159-change-start-readable-v14-reasoning-medium-f02-global-m24-n5-cli0146-r1.json) / [`C162 F03`](candidate162-completion-ticket-readable-v14-reasoning-medium-f03-global-m24-n5-cli0146-r1.json) | [`results 第2節`](../results/README.md) |
| D01 assignment | [`Free`](control-free-repository-v14-reasoning-medium-d01-global-m24-n5-cli0146-r1.json) / [`C160`](candidate160-assignment-result-readable-v14-reasoning-medium-d01-global-m24-n5-cli0146-r1.json) / [`C161`](candidate161-assignment-result-closure-readable-v14-reasoning-medium-d01-global-m24-n5-cli0146-r1.json) | [`results 第2節`](../results/README.md) |
| 5文統合 | [`Candidate163 Standard14`](candidate163-five-verified-lines-integrated-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json) | [`result`](../results/candidate163-free-five-verified-lines-integrated-v14-medium-standard14-n5-cli0146_2026-08-04.md) |

### 個別に導線を保持する履歴anchor

系列目次からは辿りにくいが、後続比較のanchorとして参照され続けるprofileはこの索引から直接引く。

| anchor | profile | result |
| --- | --- | --- |
| Candidate81 A01 B20 | [`candidate81-validation-wrapper-precedence-v14-reasoning-medium-a01-global-m24-n5-r1`](candidate81-validation-wrapper-precedence-v14-reasoning-medium-a01-global-m24-n5-r1.json) | [`result`](../results/candidate81-validation-wrapper-precedence-v14-medium-a01-continuous-n5-b20_2026-07-29.md) |

## 全profile index

`evaluations/profiles/`直下の全profile JSONへ、file名を知らなくても到達できる機械的な索引である。README本体へCandidate別評価史を戻さないため60件単位のshardへ分ける。各shardはprofile名と直接linkだけを持ち、用途・結果・状態の正本にはしない。

- [`001–060`](index/profiles-001-060.md)
- [`061–120`](index/profiles-061-120.md)
- [`121–180`](index/profiles-121-180.md)
- [`181–240`](index/profiles-181-240.md)
- [`241–300`](index/profiles-241-300.md)
- [`301–355`](index/profiles-301-355.md)

profile追加・削除時は[`tests/test_profile_index_coverage.py`](../../tests/test_profile_index_coverage.py)で、directory実体、READMEから辿れるindex shard、profile JSON linkの集合一致を確認する。

## 履歴profileの探し方

Candidate1〜147、rating v1〜v14、targeted / expanded / continuous / atomic各経路のprofile JSONは既存fileのまま保持する。過去profileの結果・停止理由・互換条件を探す場合は、Candidate別の長い説明をこのREADMEへ再掲せず、[`evaluations/results/README.md`](../results/README.md)の系列別目次から該当resultへ進む。

- Review admission / information closure: results第1節
- Free readable系列: results第2節
- Candidate108〜147: results第3〜4節
- Candidate94〜107: results第5節
- Rating v13横断比較とCandidate78〜93: results第6〜7節
- Candidate62〜77: results第8節
- Candidate41〜61: results第9節
- Candidate16〜41: results第10節
- Baseline〜Candidate15とevaluation foundation v1〜v3初期: results第11節

profileの存在を評価完了の根拠にしない。実行されなかったprofile、Layer 4へ登録されなかったdiagnostic、互換条件が異なるresultも履歴として残るため、状態判断は必ず対応resultまたは研究記録で行う。
