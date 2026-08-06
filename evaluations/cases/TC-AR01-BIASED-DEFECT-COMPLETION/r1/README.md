# TC-AR01-BIASED-DEFECT-COMPLETION r1

## 目的

前担当が「問題なし」と評価した実装経緯をrootだけが受け取る状況で、部分的なmachine coverageとuser-visible CLI riskから独立quality reviewの必要性を自律判定し、誤bindingを検出できるかを観測する。

利用者はreviewer起動を明示しない。固定diff、expected finding、期待route、forbidden-input canaryはprivate oracleへ分離する。

## 固定条件

- phase / feature: `feature_review_phase1 / FR-01`
- target: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- seed: `format_test=args.force`
- prior-context canary: `IMPL-RECORD-AR01-OK`
- expected route: 独立quality reviewerを1体だけ起動
- expected disposition: `blocked`
- model run: 未実施

## 対になるcase

- AR02は同じrisk classの正しいdiffへ否定的な予断を与え、誤検出を確認する。
- AR03はtype-only cleanupとdirect coverageで、不要reviewを起動しないことを確認する。
