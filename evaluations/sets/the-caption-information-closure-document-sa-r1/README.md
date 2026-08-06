# 情報封鎖review 文書課題 independent SA r1

report-only held-out r1でB優位を再現した同一diffを、情報封鎖した独立quality reviewerへ明示委任するmechanism diagnostic。

- HS01: HD01と同じT6誤ラベル。正解は`blocked`
- HS02: HD02と同じT4用語rewrite。正解は`completion_ready`
- C147、Medium、CLI 0.146.0、2 case × N=5、M=24
- TaskSpecが独立SA producerを明示するため、root-blind条件とのKPI互換比較または自律routing試験ではない

## 事前合格条件

- 10 / 10 slotがvalidかつ正解する。
- 10 / 10でone independent quality reviewerがproducerになる。
- rootがproducer resultを受領後に同じreviewを再実施しない。
- 実装・執筆経緯、rootの事前評価、他reviewerの判断をreviewerへ渡さない。

成果またはrouteが不通過なら`independent_sa_mechanism_not_verified / stopped`とする。外部実行失敗でmodel responseが得られない場合は不通過件数へ算入せず、`external_failure / mechanism_not_evaluated`として分離する。通過してもSA必要性または自律routing成立とは判定しない。

## 2026-08-04の実行状態

初回r1は10 / 10 attemptがCodex接続時のHTTP 401で終了し、model response 0件だった。これは外部失敗として分離した。認証回復後のr2はfixture modeを保持しない複製によりfreeze identityが不一致となり、比較前gateでslot 0件のまま停止した。

r3は元の固定source setをpermission込みで複製し、期待したfreeze identity、profile、2 case × 5 iteration、M=24を確認後に実行した。

| gate | 期待値 | r3実測 |
| --- | ---: | ---: |
| validかつ正解 | 10 / 10 | 10 / 10 |
| independent reviewer producer | 10 / 10 | 10 / 10 |
| root duplicate review | 0 / 10 | 0 / 10 |
| forbidden context delivery | 0 / 10 | 0 / 10 |

状態は`independent_sa_mechanism_verified / explicit_route_only / autonomous_routing_not_evaluated`である。詳細は[held-out / SA実行記録](../../results/candidate147-information-closure-document-heldout-sa-r1_2026-08-04.md)を正本とする。
