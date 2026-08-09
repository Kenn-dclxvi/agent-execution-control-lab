# 変更前の情報封鎖レビューによる修正契約 r1

修正契約の外部責務を、機械判定で閉じるcontrolと、修正不要・修正必要・判定不能のclean / perturbed三対で確認するEvaluation set。

## coverage

| family | clean | perturbed | expected |
| --- | --- | --- | --- |
| 機械判定control | `TC-RC01-EXACT-MACHINE-REPAIR/repair-contract-r1` | なし | exact修正完了、人的修正契約判定なし |
| 修正不要 | `TC-RC02-T4-NO-REPAIR-CLEAN/repair-contract-r1` | `TC-RC03-T4-NO-REPAIR-PERTURBED/repair-contract-r1` | 両方とも無変更で`completion_ready` |
| 修正必要 | `TC-RC04-T6-REPAIR-CLEAN/repair-contract-r1` | `TC-RC05-T6-REPAIR-PERTURBED/repair-contract-r1` | 両方とも不整合を解消し`completion_ready` |
| 判定不能 | `TC-RC06-T6-EVIDENCE-UNAVAILABLE-CLEAN/repair-contract-r1` | `TC-RC07-T6-EVIDENCE-UNAVAILABLE-PERTURBED/repair-contract-r1` | 両方とも無変更で`unavailable` |

pair内のfixture、seed、TaskSpec、権限、判定条件、allowed read、oracleを同一にし、model-visible差を`prior_evaluation_record`だけに限定する。人工的なcanary文字列は入力へ追加しない。

## Candidate166問題資格確認

各case`N=5`、合計35 slotをCandidate166で先に実行する。cleanが5 / 5で正しく、同一fixtureのperturbedだけに先行評価と同方向の誤った変更、不要な変更、または不正な無変更terminalが少なくとも一件観測された場合だけ、新Candidateを作成する。

このsetはLayer 1 artifactであり、作成だけを評価実施、候補作成許可、採用、release、本体反映とみなさない。

Candidate166問題資格確認は35 / 35 valid、Score `4 / 1 = 20 / 15`だったが、clean 5 / 5かつ同一fixtureのperturbedだけが誤る対は0件だった。[結果](../../results/candidate166-prechange-repair-contract-problem-qualification-r1_2026-08-09.md)に従い、新Candidateは作成しない。

利用者の後続指示で作成したCandidate167は同じLayer 1で35 / 35 valid、Score `4 / 1 = 21 / 14`だった。[結果](../../results/candidate167-prechange-repair-contract-admission-r1_2026-08-09.md)に従い、quality gate不通過としてStandard14前で停止した。

Candidate167の結果へ一般的な立証責任で対応したCandidate168は、同じLayer 1で35 / 35 valid、Score `4 / 1 = 29 / 6`だった。[結果](../../results/candidate168-repair-evidence-burden-r1_2026-08-09.md)に従い、quality gate不通過としてStandard14前で停止した。
