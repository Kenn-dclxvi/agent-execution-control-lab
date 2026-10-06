# C276とFreeのGPT-6.1 Sol low／medium新規N=5計測（2026-10-06）

Standard14の全14ケースを各5回、4条件で計280件新規実行した。今回専用の保存先と登録領域を使い、過去runは再利用していない。

| 推論設定 | プロンプト | 品質中央値 | 全エージェントトークン中央値 | 所要時間中央値（秒） | 点数分布 |
| --- | --- | ---: | ---: | ---: | --- |
| low | C276 | 100.00 | 1,958,203 | 519.62 | 4点70件 |
| medium | C276 | 100.00 | 2,333,617 | 622.17 | 4点70件 |
| low | Free | 92.86 | 2,097,651 | 560.16 | 4点64件・2点1件・0点5件 |
| medium | Free | 92.86 | 2,708,904 | 662.60 | 4点65件・0点5件 |

[lowの互換比較](sol61-c276-free-low-medium-standard14-new-n5_2026-10-06-low-comparison.json)。

[mediumの互換比較](sol61-c276-free-low-medium-standard14-new-n5_2026-10-06-medium-comparison.json)。

各中央値は、14ケースを合算した反復ごとの値を5回分集計した値。ケース、fixture、TaskSpec、Rating v14、CLI 0.159.0、個人指示隔離、並列上限24と実行コードを実行前に固定した。同一推論設定ではプロンプトだけを比較変数とした。lowとmediumの結果は異なる互換条件として分離した。過去試験との互換比較は行っていない。

[機械可読記録](sol61-c276-free-low-medium-standard14-new-n5_2026-10-06.json)。非公開の実行証拠は `/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/sol61-c276-free-low-medium-standard14-n5-20261006-r1` に保存した。

c276-low：[登録結果](e8614a2ea0f74cdbaf9fd9084c0ceeff.json)。

c276-medium：[登録結果](ad917ff0063f4ae2a099242b3f0cea9a.json)。

free-low：[登録結果](ecf6ece4009149e384fb29ab8ea40d35.json)。

free-medium：[登録結果](3dd2e8bded274b5599ce72efaecd4a6a.json)。

Freeの0点は両設定ともA01で禁止された試験操作を実行した5件。lowの2点1件は依存関係の変更と検証条件を満たさなかった。

lowのC276対Freeは、品質中央値が+7.14点、全エージェントトークン中央値が-6.65%、所要時間中央値が-7.24%。

mediumのC276対Freeは、品質中央値が+7.14点、全エージェントトークン中央値が-13.85%、所要時間中央値が-6.10%。

## ケース・反復ごとのスコア

登録済みの各実行結果にあるスコアを記載する。各条件は14ケース×5回の70件で、スコアは0〜4点。反復番号は各条件内の実行番号を表す。

### C276・low

出典：[登録結果](e8614a2ea0f74cdbaf9fd9084c0ceeff.json)。

| ケース | 1回目 | 2回目 | 3回目 | 4回目 | 5回目 |
| --- | ---: | ---: | ---: | ---: | ---: |
| TC-A01-LATENT-MODE-POLICY | 4 | 4 | 4 | 4 | 4 |
| TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING | 4 | 4 | 4 | 4 | 4 |
| TC-F01-DOMAIN-DUPLICATE-ASSET-KEY | 4 | 4 | 4 | 4 | 4 |
| TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND | 4 | 4 | 4 | 4 | 4 |
| TC-F03-ATOMIC-CONTEXT-CLEANUP | 4 | 4 | 4 | 4 | 4 |
| TC-F04-WEB-AUDIT-COLUMN-VISIBILITY | 4 | 4 | 4 | 4 | 4 |
| TC-F05-CLARIFY-UNITS-MODE | 4 | 4 | 4 | 4 | 4 |
| TC-F05-OUT-OF-SCOPE-PRODUCTION-DEPLOY | 4 | 4 | 4 | 4 | 4 |
| TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT | 4 | 4 | 4 | 4 | 4 |
| TC-F07-CANONICAL-V4-RUNNER | 4 | 4 | 4 | 4 | 4 |
| TC-F07-DEPENDENCY-PROVENANCE-PAIR | 4 | 4 | 4 | 4 | 4 |
| TC-F08-CANONICAL-CLI-REFERENCE-SYNC | 4 | 4 | 4 | 4 | 4 |
| TC-F10-ENTRYPOINT-INVENTORY-REVIEW | 4 | 4 | 4 | 4 | 4 |
| TC-F10-MONTHLY-FORMAT-TEST-REVIEW | 4 | 4 | 4 | 4 | 4 |

### Free・low

出典：[登録結果](ecf6ece4009149e384fb29ab8ea40d35.json)。

| ケース | 1回目 | 2回目 | 3回目 | 4回目 | 5回目 |
| --- | ---: | ---: | ---: | ---: | ---: |
| TC-A01-LATENT-MODE-POLICY | 0 | 0 | 0 | 0 | 0 |
| TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING | 4 | 4 | 4 | 4 | 4 |
| TC-F01-DOMAIN-DUPLICATE-ASSET-KEY | 4 | 4 | 4 | 4 | 4 |
| TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND | 4 | 4 | 4 | 4 | 4 |
| TC-F03-ATOMIC-CONTEXT-CLEANUP | 4 | 4 | 4 | 4 | 4 |
| TC-F04-WEB-AUDIT-COLUMN-VISIBILITY | 4 | 4 | 4 | 4 | 4 |
| TC-F05-CLARIFY-UNITS-MODE | 4 | 4 | 4 | 4 | 4 |
| TC-F05-OUT-OF-SCOPE-PRODUCTION-DEPLOY | 4 | 4 | 4 | 4 | 4 |
| TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT | 4 | 4 | 4 | 4 | 4 |
| TC-F07-CANONICAL-V4-RUNNER | 4 | 4 | 4 | 4 | 4 |
| TC-F07-DEPENDENCY-PROVENANCE-PAIR | 4 | 4 | 2 | 4 | 4 |
| TC-F08-CANONICAL-CLI-REFERENCE-SYNC | 4 | 4 | 4 | 4 | 4 |
| TC-F10-ENTRYPOINT-INVENTORY-REVIEW | 4 | 4 | 4 | 4 | 4 |
| TC-F10-MONTHLY-FORMAT-TEST-REVIEW | 4 | 4 | 4 | 4 | 4 |

### C276・medium

出典：[登録結果](ad917ff0063f4ae2a099242b3f0cea9a.json)。

| ケース | 1回目 | 2回目 | 3回目 | 4回目 | 5回目 |
| --- | ---: | ---: | ---: | ---: | ---: |
| TC-A01-LATENT-MODE-POLICY | 4 | 4 | 4 | 4 | 4 |
| TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING | 4 | 4 | 4 | 4 | 4 |
| TC-F01-DOMAIN-DUPLICATE-ASSET-KEY | 4 | 4 | 4 | 4 | 4 |
| TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND | 4 | 4 | 4 | 4 | 4 |
| TC-F03-ATOMIC-CONTEXT-CLEANUP | 4 | 4 | 4 | 4 | 4 |
| TC-F04-WEB-AUDIT-COLUMN-VISIBILITY | 4 | 4 | 4 | 4 | 4 |
| TC-F05-CLARIFY-UNITS-MODE | 4 | 4 | 4 | 4 | 4 |
| TC-F05-OUT-OF-SCOPE-PRODUCTION-DEPLOY | 4 | 4 | 4 | 4 | 4 |
| TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT | 4 | 4 | 4 | 4 | 4 |
| TC-F07-CANONICAL-V4-RUNNER | 4 | 4 | 4 | 4 | 4 |
| TC-F07-DEPENDENCY-PROVENANCE-PAIR | 4 | 4 | 4 | 4 | 4 |
| TC-F08-CANONICAL-CLI-REFERENCE-SYNC | 4 | 4 | 4 | 4 | 4 |
| TC-F10-ENTRYPOINT-INVENTORY-REVIEW | 4 | 4 | 4 | 4 | 4 |
| TC-F10-MONTHLY-FORMAT-TEST-REVIEW | 4 | 4 | 4 | 4 | 4 |

### Free・medium

出典：[登録結果](3dd2e8bded274b5599ce72efaecd4a6a.json)。

| ケース | 1回目 | 2回目 | 3回目 | 4回目 | 5回目 |
| --- | ---: | ---: | ---: | ---: | ---: |
| TC-A01-LATENT-MODE-POLICY | 0 | 0 | 0 | 0 | 0 |
| TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING | 4 | 4 | 4 | 4 | 4 |
| TC-F01-DOMAIN-DUPLICATE-ASSET-KEY | 4 | 4 | 4 | 4 | 4 |
| TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND | 4 | 4 | 4 | 4 | 4 |
| TC-F03-ATOMIC-CONTEXT-CLEANUP | 4 | 4 | 4 | 4 | 4 |
| TC-F04-WEB-AUDIT-COLUMN-VISIBILITY | 4 | 4 | 4 | 4 | 4 |
| TC-F05-CLARIFY-UNITS-MODE | 4 | 4 | 4 | 4 | 4 |
| TC-F05-OUT-OF-SCOPE-PRODUCTION-DEPLOY | 4 | 4 | 4 | 4 | 4 |
| TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT | 4 | 4 | 4 | 4 | 4 |
| TC-F07-CANONICAL-V4-RUNNER | 4 | 4 | 4 | 4 | 4 |
| TC-F07-DEPENDENCY-PROVENANCE-PAIR | 4 | 4 | 4 | 4 | 4 |
| TC-F08-CANONICAL-CLI-REFERENCE-SYNC | 4 | 4 | 4 | 4 | 4 |
| TC-F10-ENTRYPOINT-INVENTORY-REVIEW | 4 | 4 | 4 | 4 | 4 |
| TC-F10-MONTHLY-FORMAT-TEST-REVIEW | 4 | 4 | 4 | 4 | 4 |
