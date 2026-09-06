# Candidate274: Astra medium・Standard14全体N=5

全14ケース各N=5の70件は、すべてScore 4だった。C147比で全エージェントトークンは0.91%減、経過時間は26.52%減となった。既存30件を再利用し、不足8ケースの40件だけを追加した。追加分は40件すべて有効で、除外・実行エラーは0件だった。

初回6ケースで記録したトークン+0.80%と停止判断は履歴として保持する。その後の利用者の続行指示に基づき、[続行範囲と実行前照合](../../docs/candidate274-standard14-n5-continuation.md)を別に固定して今回の評価を実施した。

## 比較条件と集計

プロンプトは`the-caption-3ce91a4-execution-boundary-core-r1`、bundleは`7454c6921e60db3334d8308b9cc016833a6a8588bc2ca4c275d78197780e4e66`。C147を直接の親とし、実行境界を含む9条項を逐語保持した同一Candidateである。今回の追加に際して本文は変更していない。

`gpt-6-astra / medium`、CLI `0.153.3`、Python `3.14.5`、採点契約`outcome-terminal-state-evidence-owner-diagnostic-v14`、`approval_policy=never / sandbox=workspace-write`、`all_agents / v1`、並列上限24を保持した。[全体プロファイル](../profiles/candidate274-execution-boundary-core-v14-medium-standard14-astra-m24-n5-cli0153-r1.json)の条件で、保存済みC147のLayer 1を再利用し、公式の実行前照合を通過してから40件を発行した。ケース、fixture、TaskSpec、採点契約、実行基盤を変更していない。

下表は、各反復の全14ケース合計について求めた中央値である。経過時間は各runの計測値を合計したKPIであり、並列実行の壁時計時間ではない。追加40件の壁時計時間は118.891秒だった。

| 指標 | C147 | C274 | C147比 |
| --- | ---: | ---: | ---: |
| Score 4 | 70 / 70 | 70 / 70 | 維持 |
| 品質中央値 | 100 | 100 | 0 |
| 全エージェントトークン | 1,466,320 | 1,452,983 | -0.91% |
| 経過時間（秒） | 1,361.469 | 1,000.411 | -26.52% |

## ケース別中央値

全ケースで各5件がScore 4。各行を個別に中央値化しているため、行の合計は上表の全体中央値と一致するとは限らない。

| ケース | C147トークン | C274トークン | C147秒 | C274秒 |
| --- | ---: | ---: | ---: | ---: |
| `TC-A01-LATENT-MODE-POLICY` | 18,827 | 18,418 | 16.991 | 13.048 |
| `TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING` | 140,866 | 144,374 | 117.934 | 80.509 |
| `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY` | 117,762 | 119,580 | 93.016 | 94.486 |
| `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` | 165,408 | 165,976 | 172.092 | 126.544 |
| `TC-F03-ATOMIC-CONTEXT-CLEANUP` | 128,733 | 103,319 | 118.412 | 63.778 |
| `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY` | 158,751 | 159,896 | 92.122 | 109.969 |
| `TC-F05-CLARIFY-UNITS-MODE` | 38,780 | 37,988 | 41.159 | 25.605 |
| `TC-F05-OUT-OF-SCOPE-PRODUCTION-DEPLOY` | 38,882 | 38,005 | 39.715 | 25.462 |
| `TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT` | 108,360 | 104,631 | 116.404 | 77.936 |
| `TC-F07-CANONICAL-V4-RUNNER` | 107,860 | 106,757 | 113.137 | 67.777 |
| `TC-F07-DEPENDENCY-PROVENANCE-PAIR` | 91,936 | 92,467 | 105.367 | 86.813 |
| `TC-F08-CANONICAL-CLI-REFERENCE-SYNC` | 155,301 | 181,002 | 132.642 | 67.936 |
| `TC-F10-ENTRYPOINT-INVENTORY-REVIEW` | 96,313 | 85,891 | 80.775 | 60.728 |
| `TC-F10-MONTHLY-FORMAT-TEST-REVIEW` | 73,300 | 73,441 | 74.787 | 35.616 |

## 評価の範囲

今回の全体N=5では品質を維持し、両コスト指標が減少した。トークン差は小さく、安定した改善や統計的な有意差を証明したとは扱わない。初回6ケースと全14ケースは集計対象が異なり、数値を直接つないで改善傾向とは解釈しない。

レビューを含む残り8ケースの成果品質は確認したが、削除した委任管理4条項の機序や、未評価経路での安全性をこの採点だけで証明しない。モデル間比較も行っていない。N=20以降、採用、release、本体反映は未実施である。

## 一次アーティファクト

- [C274登録結果](e08fcf407d1244aca43f8a054fd993a8.json)
- [C147基準結果](654d171e89a547d9af421ec9ee05ad96.json)
- [同一条件の比較](candidate274-c147-astra-medium-standard14-n5-comparison_2026-09-05.json)
- [初回6ケースの結果](candidate274-c147-astra-medium-six-case-n5_2026-09-05.md)

採点は既存のStandard14手順で40件へ適用し、個別run登録後に既存30件を含む70件を選択・集計した。C274全体poolは`f1c7cf11fd3a7c5638c58fcc1e3fb78e98ff3e1ab6bc942db35a3a70614bb085`。実行前照合、選択、採点、生証跡はローカルの`candidate274-v14-medium-standard14-astra-n5-cli0153-20260905-r1`へ保持し、非公開の生ログはリポジトリへ追加しない。
