# TC-AR03-DIRECT-COVERAGE-NO-REVIEW r2

r1と同じtype-only cleanupとno-review期待を保持し、commit境界だけをprompt overlay後workspaceへ合わせるnegative controlである。

- seed commit: `HEAD^`
- target commit: `HEAD^^`
- source diff: `HEAD^^..HEAD^`
- expected route: quality reviewer 0体
- expected disposition: `completion_ready`
- model run: C147 N=5実施。disposition 5 / 5正解、root-only 5 / 5でnegative control成立
