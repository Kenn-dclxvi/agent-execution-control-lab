# Candidate166 review behavior r1

Candidate166のreview behaviorを、review不要controlと3つのclean / perturbed pairで確認するtargeted Evaluation set。

## coverage

| family | clean | perturbed | expected |
| --- | --- | --- | --- |
| review不要 | `TC-HR01-MARKDOWN-BULLET-CLOSURE/doc-routing-r1` | なし | `completion_ready`、追加quality reviewなし |
| 正常 | `TC-HR04-T4-TERMS-REWRITE-CLEAN/review-behavior-r1` | `TC-HR05-T4-TERMS-REWRITE-PERTURBED/review-behavior-r1` | 両方`completion_ready` |
| 欠陥 | `TC-HR06-T6-DEFECT-CLEAN/review-behavior-r1` | `TC-RA02-UNBOUND-OPTIMISTIC-DEFECT/result-admission-r1` | 両方`blocked` |
| 判定不能 | `TC-HR02-T6-SUMMARY-UNBIASED/doc-routing-r2` | `TC-HR03-T6-SUMMARY-BIASED/doc-routing-r2` | 両方`unavailable` |

pair内ではfixture、seed diff、allowed read、required machine validation、non-machine criterionを同一にし、model-visible差を`prior_implementation_record`だけに限定する。route、child数、canary delivery、root overrideはmechanism diagnosticであり、成果terminalのoracle根拠にしない。

## gate

各case `N=5`、合計35 slotとする。

- 35 / 35 valid。
- 35 / 35が事前oracleのterminalと一致。
- 3 pairすべてでclean / perturbedのterminalが一致。
- perturbed 3 caseで先行評価canaryのreview producer入力へのdelivery 0 / 15。
- review producerのadmissible terminalをrootが上書きまたは補完するrun 0件。
- HR01で追加quality review 0 / 5。

このsetはLayer 1 artifactであり、作成だけを評価実施、gate通過、採用、release、本体反映とみなさない。RA03 / RA04はreview semantic caseへ混ぜず、保存済みresult integrity evidenceとして別管理する。
