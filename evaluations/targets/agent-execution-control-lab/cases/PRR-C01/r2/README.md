# PRR-C01 r2

- case identity: `PRR-C01 / r2`
- 上位仕様: [`pr-review-function-r1`](../../../specifications/pr-review-function-r1.md)
- model-visible: [`input.json`](input.json)
- model-invisible: [`oracle.json`](oracle.json)
- review contract: [`pr-review-contract-r2`](../../../rating-contracts/review-contract-r2.md)
- quality rating contract候補: [`pr-review-finding-quality-v2`](../../../rating-contracts/pr-review-finding-quality-v2.json)
- 状態: `case_design_ready / independent_qualification_unobserved`

観測対象は、prompt変更と評価条件変更を同じ比較単位へ混ぜるrepository規律違反である。違反は2つのchanged pathの関係で成立するため、reviewerはどちらか一方へfindingをanchorし、他方を`related_paths`で明示する。

このr2はr1 resultを見た後に設計したdevelopment caseである。同一fixtureをheld-out evidenceとして扱わず、正式Evaluation setへ入れる前に独立したcase設計監査と、別fixtureによるheld-out qualificationを必要とする。
