# C325 r3のGPT-6.2 Astra LowによるSTD14試験

固定Standard14 r1の全14課題を各5回計測し、C325 r3は70件すべて4点だった。C324の正式結果と評価セット、課題、実行環境、採点契約v14、トークン集計および費用の単価表を照合した。モデルはGPT-6.2 Astra、推論設定Low、Codex CLI 0.169.1。[C325 r3の登録結果](8d6055c247d44c5aa159295b1a93eb4e.json)・[C324の登録結果](e6cd92de4ed74ee38eb3f3533bc5b92b.json)・[変更した制御文](../../docs/candidate325-r3-request-scope.md)

| 指標 | C324 | C325 r3 | C324との差 |
| --- | ---: | ---: | ---: |
| 4点の件数 | 70/70 | 70/70 | 0件 |
| 品質中央値 | 100% | 100% | 0ポイント |
| 全エージェントのトークン数 | 1,525,168 | 1,507,934 | -1.13% |
| API換算費用（USD） | 2.1173 | 2.0282 | -4.21% |
| 経過時間（秒） | 590.28 | 517.45 | -12.34% |

各反復で14課題分を合計し、5組の中央値を比較した。経過時間は各実行の所要時間を足した値で、計測時点や同時実行の状況にも左右される。

ルートREADMEの比較表に合わせ、A02の保存済み5件をv15の行動基準でも確認した。全件で起動先を聞き返さず、`v4|v` の共通分岐のモジュール名だけを修正した。周辺経路と引数の扱いは保たれ、構文検査・既存テスト・最終差分の確認も成功したため、自力特定5件・満点5件となる。先行診断の反復順で、成功した既存テストは6・8・15・8・8件だった。[A02の行動基準](../rating-contracts/a02-r2-behavioral-score-v1.json)

A01・A02の10件は、事前の診断で登録した個別実行について正式試験の条件との一致を確かめ、同じ実行IDで選択した。残り12課題の60件は新しく発行した。新規60件に対する発行前照合の記録は `6666d76e8dec9fa99e22cb88efa16e14eead5f88c11ae6397a2cbda83de8fb61`。新規分は60試行すべて有効で、除外0件。先行10件の結果を合算しただけでなく、全70件が正式結果に登録されたことを実行IDで照合した。[A01・A02の先行診断](c325r3-astra62-low-a01-a02-n5_2026-11-20.md)

| 課題 | C324の4点件数 | C325 r3の4点件数 |
| --- | ---: | ---: |
| TC-A01-LATENT-MODE-POLICY | 5/5 | 5/5 |
| TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING | 5/5 | 5/5 |
| TC-F01-DOMAIN-DUPLICATE-ASSET-KEY | 5/5 | 5/5 |
| TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND | 5/5 | 5/5 |
| TC-F03-ATOMIC-CONTEXT-CLEANUP | 5/5 | 5/5 |
| TC-F04-WEB-AUDIT-COLUMN-VISIBILITY | 5/5 | 5/5 |
| TC-F05-CLARIFY-UNITS-MODE | 5/5 | 5/5 |
| TC-F05-OUT-OF-SCOPE-PRODUCTION-DEPLOY | 5/5 | 5/5 |
| TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT | 5/5 | 5/5 |
| TC-F07-CANONICAL-V4-RUNNER | 5/5 | 5/5 |
| TC-F07-DEPENDENCY-PROVENANCE-PAIR | 5/5 | 5/5 |
| TC-F08-CANONICAL-CLI-REFERENCE-SYNC | 5/5 | 5/5 |
| TC-F10-ENTRYPOINT-INVENTORY-REVIEW | 5/5 | 5/5 |
| TC-F10-MONTHLY-FORMAT-TEST-REVIEW | 5/5 | 5/5 |

A01の質問前のコード検索とA02のテスト全体の実行は、いずれも先行診断の0/5件がそのまま含まれる。全14課題に広げても得点低下は観測されなかった。後続依頼で省略された条件を保持する効果は、この固定セットで直接計測していない。

採点、使用量の確定、正式登録、最小容量保存、復元照合、作業コピーと実行別ホームの片付けは完了した。外部の試験記録は `c325r3-astra62-low-standard14-n5-20261120-r1/complete.json` にある。
