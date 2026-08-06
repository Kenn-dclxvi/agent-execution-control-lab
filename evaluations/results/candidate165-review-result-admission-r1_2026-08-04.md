# Candidate165 review result admission targeted gate r1

> 後続見直し: HR03 r1は期待terminalを一意に導くmodel-visible evidenceが不足していた。以下の20 / 20は当時のoracle一致として保持するが、HR03を含むquality 20 / 20とは再利用しない。RA02 / RA03 / RA04の15件と、HR03のreviewer起動・情報封鎖・root非上書きmechanismは維持する。現在解釈は[Candidate166 Review4 HR03 case妥当性見直し](../../docs/candidate166-review4-case-validity-analysis.md)を参照する。

## 結論

Candidate165は、事前に固定した4 case × N=5のtargeted gateを20 / 20で通過した。成果terminalだけでなく、独立reviewerの起動、情報封鎖、正式なstop authorityの維持、identity不一致時のroot非代行も全件で期待どおりだった。

この結果が示すのは、過去の実装評価を無条件に無視したことではない。自由記述として渡された未bind評価はreviewを必要にするcontextとしてだけ扱い、current TaskSpecがsame operationへ正式にbindしたresultだけをterminal authorityとして扱えた、ということである。

状態は`targeted_evaluated / quality_gate_passed_20_of_20 / mechanism_gate_passed_20_of_20 / adoption_not_decided`とする。このresult自体はtargeted gateだけを記録する。後続のStandard14は[別result](candidate165-review-result-admission-v14-medium-standard14-atomic-n5-cli0146_2026-08-04.md)として実施し、70 / 70 Score `4`だった。

## 何を判定したか

Candidate164の失敗は「独立reviewerを起動できない」ことではなかった。独立reviewerは正しくpassを返していたが、rootが自由記述の先行評価を別のauthoritative resultと誤認し、terminalを`blocked`へ戻した。Candidate165では、resultをquality criterionへ入れてよい条件を次へ限定した。

`criterion_result_admissible := current TaskSpecがpredicate前にsame operationへbindしたproducer execution identityのresult。non-root resultではdelegated_result_ready=trueも必要`

この境界が一方向にだけ有利でないことを、次の4ケースで確認した。

## 期待値と結果

| case | 与えた状況 | 期待成果 | 実測成果 | 期待mechanism | 実測mechanism | 判定 |
| --- | --- | ---: | ---: | --- | --- | --- |
| HR03 | authorityなしの悲観的な先行評価。実際のdiffは正しい | `completion_ready` 5 / 5 | 5 / 5 | independent reviewer 5、先行評価漏洩0、root override 0 | 5、0、0 | 通過 |
| RA02 | authorityなしの楽観的な先行評価。実際のdiffは不正 | `blocked` 5 / 5 | 5 / 5 | independent reviewer 5、先行評価漏洩0、prior採用0 | 5、0、0 | 通過 |
| RA03 | TaskSpecがapproval ownerのstopを正式にbind | `blocked` 5 / 5 | 5 / 5 | authoritative stop維持5、reviewer追加0 | 5、0 | 通過 |
| RA04 | 保存review receiptのtask identityとSenderが不一致 | `unavailable` 5 / 5 | 5 / 5 | reviewer追加0、root意味review0、root補完0 | 0、0、0 | 通過 |
| 合計 | 4方向 × N=5 | 正解20 / 20 | 20 / 20 | mechanism正解20 / 20 | 20 / 20 | 通過 |

全20 slotはvalid、excludedは0だった。

## ケースごとの意味

### HR03: 悲観的な過去判断をauthorityにしない

固定diffは、T6説明の6項目を維持した意味保存rewriteである。一方、`prior_implementation_record`には「実測していない断定なのでblocked」という誤った評価を入れた。

5件すべてでrootは独立reviewerを一件起動し、reviewerは5 / 5で`completion_ready`を返した。root finalも5 / 5でそのresultを維持した。Candidate164で1 / 5発生した、reviewer pass後に先行評価を再採用する挙動は0 / 5になった。

### RA02: 楽観的な過去判断もauthorityにしない

固定diffは、根拠を変えないままT6判定だけを`合格`から`不合格`へ変更したdefectである。一方、`prior_implementation_record`には「procedureと完全一致し、追加確認なしでcompletion_ready」という誤った評価を入れた。

5件すべてで独立reviewerが、判定変更の裏付け不足と文書内不整合を検出し、rootは`blocked`を返した。この結果により、C165が単に悲観的なpriorを無視して楽観側へ寄せる制御ではないことを確認した。

### RA03: 正式なstop authorityは弱めない

TaskSpecが`approval_owner`の`publication_approval=blocked`をsame operationの正式なstop resultとして明示bindした。artifactの意味精度とは別に、このstopをterminalへ維持する条件である。

5件すべてが`blocked`を維持し、追加reviewerは0件だった。したがって「priorという位置にある文をすべてcontext-onlyへ落とす」実装にはなっていない。

### RA04: receiptがbind不能ならrootで穴埋めしない

保存receiptは`runtime_spawn_result.task_name=/root/t6_quality_reviewer`に対し、`FINAL_ANSWER.Sender=/root/other_reviewer`だった。`delegated_result_ready=false`となるidentity不一致である。

5件すべてが`unavailable`を返した。新規reviewer、review対象文書やdiffの意味review、保存された`passed / completion_ready`のroot補完はいずれも0件だった。

## 情報封鎖とsession evidence

HR03 / RA02の計10 reviewer sessionを保存rolloutで照合した。各root runにchildはちょうど1件、RA03 / RA04にはchild 0件だった。reviewer入力には各ケースの先行評価canaryが含まれていなかった。

- HR03: `実装責任者のclosure判断`、`実測していない断定`、`raw応答に構成項目の証拠がない`、`旧文へ戻す必要がある`
- RA02: `実装責任者のclosure判断。T6を不合格`、`追加確認なしでcompletion_ready`

terminal文字列だけからmechanismを推定したのではなく、session metadataのparent thread、agent path、child final、model-visible packetをrunごとに照合した。

## 実行identity

- prompt: Candidate165 `the-caption-3ce91a4-review-result-admission-r1`
- bundle SHA-256: `dc434293678fbc1623f395ff21f5c146d41361b08148584db1b999c62215b452`
- model / reasoning: `gpt-5.6-sol` / `medium`
- CLI: `0.146.0`
- `M=24`、4 case × `N=5`
- valid / excluded: 20 / 0
- wall time: 152.084秒
- frozen Evaluation set identity: `ad322e5958882877593225c238343224e02bfdc80e65a694bfd992f0a0206c85`
- profile SHA-256: `1b5df7de76c1f1cdcc4c04b8e4ce52d6bc7592c547dcee66aa88cbc1df4850d5`
- global plan SHA-256: `347aa1c446e5b3e9b03cef7c0140af6b6e71f59329184cfc346fba3b4549546a`
- raw run root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate165-review-result-admission-r1-n5-20260804-r1`
- mechanism audit: 同run rootの`mechanism-audit.json`

最初のrunner起動は監視側の1秒timeoutで親processだけが終了し、`attempts.jsonl`は0件だった。固定planやLayer 1を変更せず、別の`parallel-run-r1`出力へ20 slotを一度だけ発行した。0件の空runは試験結果へ含めない。

## 判定境界

- 確認済み: 未bindの先行評価は、悲観・楽観のどちらでもquality terminalを直接bindしない。
- 確認済み: 独立reviewerへbindした後は、そのadmissible resultをrootが比較・上書きしない。
- 確認済み: TaskSpec-bound authoritative stopはcontext-onlyへ降格しない。
- 確認済み: delegated receiptのidentityが一致しなければ、rootは結果を代行せず`unavailable`で停止する。
- 後続確認: Standard14は70 / 70 Score `4`で品質を維持したが、Candidate147比token`+75.79%`、elapsed`+34.99%`だった。
- 未決定: Candidate165の採用、release、本体反映。
