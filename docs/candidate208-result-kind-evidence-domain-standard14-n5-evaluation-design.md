# Candidate208 Standard14 N=5 評価設計

## 判断

Candidate208のADR9 r2は品質45/45件でscore 4だったが、制御機序は`mechanism_failed`のままとする。ログ再調査では、ADR05-i4はreviewerがmodel-visible inventoryと契約を再読した明確な制御漏れ、ADR09-i5は必要なpaired-scope readをrootが先に実施したproducer ownershipの逸脱と判定した。利用者の明示的な判断を受け、これらを見落とさず受容したうえでStandard14 N=5へ進む。

この測定はCandidate208の通常経路における品質、全agent token、経過時間を測る独立評価である。ADR9の機序不通過を取り消さず、採用、releaseまたはruntime projectionを決めない。

## 比較境界

- Evaluation setは`the-caption-standard14-r1`の14ケース、各N=5に固定する。
- 比較基準は保存済みCandidate206 result `0aba77ffad0848e5be7e635f96293070`と、それを生成した保存Layer 1に固定する。
- Candidate208のprompt identity以外は、case revision、fixture、TaskSpec、rating contract、model、reasoning、Agent/runtime/CLI、permission、executor、token accounting、target commit/tree、M=24を一致させる。
- Candidate208 poolは空から始め、`plan-missing --desired-count 5`が不足70件だけを固定する。
- `prepare-comparison-layer1`、`preflight-comparison`、`verify-comparison-preflight`が成功し、発行済みslotが0件でなければ一件も発行しない。

## 判定

品質は固定済みrating contractで14ケース×5件を採点する。KPIは同一条件のCandidate206 resultに対する品質通過率、全agent token中央値、経過時間中央値を比較する。

Standard14ログは通常経路の診断材料として、開始時の共同発行、required command、結果経路、review対象ケースのproducer ownershipを確認する。ただし、Standard14の品質合格をADR9の機序合格へ読み替えず、追試後に評価基準を追加しない。

## 停止条件

- preflightの互換条件に不一致、未固定または未確認がある。
- 70件以外のslotが発行対象になる。
- valid runが各ケース5件に達しない。
- 品質採点またはKPIの一次証拠をresultへbindできない。
