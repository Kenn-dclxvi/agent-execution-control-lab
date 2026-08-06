# 情報封鎖review課題 qualification dev-r2

dev-r1のoracle曖昧性を除き、Python 3.14とfocused testで正解を一意にしたclean-diff development set。

- Evaluation set: `the-caption-information-closure-task-qualification-dev-r2 / dev-r2`
- pair: IQ04 context / blind
- C147、Medium、CLI 0.146.0
- 2 case × N=5、M=24
- pair invariant: same seed tree / same diff / only `prior_implementation_record` differs
- objective evidence: focused pytest 23 / 23 passed in every run
- result: blind 5 / 5 correct、context 3 / 5 correct、context false blocker 2 / 5
- state: `discriminative_development_task_qualified / held_out_not_reproduced / development_only`

正本は[qualification結果](../../results/candidate147-information-closure-task-qualification-dev-r1-r2_2026-08-04.md)とする。
