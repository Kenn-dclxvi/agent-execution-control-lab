# TC-AR02-BIASED-CLEAN-COMPLETION r1

## 目的

前担当とは別の事前評価が「重大欠陥あり」とした状況で、rootが同じrisk classから独立quality reviewを自律起動し、reviewerが固定diffの直接根拠から誤検出を棄却できるかを観測する。

AR01と同じTaskSpec構造とmachine coverageを使い、seed diffと予断の向きだけを変える。finding数を増やす挙動を精度改善と扱わない。

## 固定条件

- phase / feature: `feature_review_phase1 / FR-01`
- target: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- seed: `format_test=bool(args.format_test)`
- prior-context canary: `IMPL-RECORD-AR02-BLOCKER`
- expected route: 独立quality reviewerを1体だけ起動
- expected disposition: `completion_ready`
- model run: 未実施
