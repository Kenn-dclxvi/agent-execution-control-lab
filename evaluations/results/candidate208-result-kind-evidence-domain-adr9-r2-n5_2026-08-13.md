# Candidate208 result kind別証拠境界 ADR9 r2 N=5

## 結論

Candidate208はADR9 r2を45 / 45 valid、除外0、45 / 45 Score `4`で完了した。reviewer cardinality、terminal、result admission、result effect、artifact境界およびrequired commandは全件一致した。

一方、機序gateは不通過である。packetだけで`counterexample_found`が成立した20件のうち19件はrepository readなしで終了したが、ADR05の1件はpacket投影済みのinventoryとcontractを閉じたsourceから再読した。またADR09の1件では、rootがreviewer所有の直接対象をreviewer起動前に先読みした。いずれも品質結果を変えなかったが、固定した証拠境界は完全には成立していない。

validな機序不通過resultとして保存して停止する。repair rerun、Standard14、N=20、採用、releaseおよびprojectionは実施しない。

## 実行と品質

| 指標 | 結果 |
| --- | ---: |
| valid run | 45 / 45 |
| 除外attempt | 0 |
| Score 4 | 45 / 45 |
| terminal一致 | 45 / 45 |
| reviewer cardinality一致 | 45 / 45 |
| review result admission一致 | 45 / 45 |
| review result effect一致 | 45 / 45 |
| artifact境界一致 | 45 / 45 |
| required command一致 | 15 / 15 |
| forbidden canary配送 | 0 |

比較前preflightはCandidate207登録result `9f6feb29f0114699beb4b11dbfbaa459`へbindし、9ケース各5件、prompt identity以外の条件一致、`max_workers=24`、不足45件、`ready`だった。45件の実行後に有効runだけを採点・登録し、result `c4e84aef70aa4d5d9b97c09c6817605d`へ固定した。

## 機序結果

| 共通監査した機序 | C206 | C207 | C208 |
| --- | ---: | ---: | ---: |
| packet反例成立run | 20 | 20 | 20 |
| packet反例成立時にdirect readなし | 13 / 20 | 8 / 20 | 19 / 20 |
| packet反例成立後のdirect read違反 | 7 / 20 | 12 / 20 | 1 / 20 |
| packet供給元`design-admission.json`再読 | 5 | 20 | 1 |
| rootによるreviewer-owned targetの先読みなし | 30 / 30 | 30 / 30 | 29 / 30 |
| exact manifest direct read set一致 | 25 / 30 | 15 / 30 | 29 / 30 |
| mixed read | 2 | 13 | 0 |
| manifest外read | 3 | 7 | 1 |

C208のresult kind別証拠集合は、C207で12 / 20だった反例成立後readを1 / 20まで減らした。したがって対象機序には実測効果がある。ただし合格条件は0件であり、19 / 20を完全制御と扱わない。

残る二経路は別の境界である。

1. ADR05 iteration 4では、reviewerが投影済みの`consumer_inventory`と`consumer_contracts`を「未解決manifest observation」と再分類した。model-visible valueとmanifest descriptorの同一性を、単なるownership説明ではなくobservation stateへbindする境界が不足している。
2. ADR09 iteration 5では、rootが`paired-scope-evidence.json`をreviewer起動前に読んだ。`review_observation_consumer_ready`はreview producerがnonterminalであることを要求するが、invocation issuerをbind済みreview producerへ限定していない。このためrootもconsumerを代行できる読み方が残った。

次案で追加し得るのは、手順やread順ではなく、(a) source descriptorと同じfact・provenanceを持つpacket projectionをそのobservationの`admitted current value`へbindし再取得資格を閉じること、(b) review observation invocationのissuerをbind済みreview producerへ限定すること、の二点である。これはC208の有効部分を維持したまま、実測した二つの開いた境界だけを閉じる案である。

### 監査器の訂正

ADR06 iteration 4は当初`review result未受領`と抽出されたが、raw rolloutには真正な`/root/adversarial_design_review`の`FINAL_ANSWER`があり、`counterexample_found — ...`の同一行に完全なcertificateが続いていた。監査器が状態値単独行だけを認識していたためである。真正な子の最終結果に限り、状態値の直後が`—`、`-`または`:`の場合を受理するよう抽出を訂正した。root finalからの補完や機序predicateの変更は行っていない。訂正後のresult admissionは45 / 45である。

## KPI診断

| prompt | `total_tokens`中央値 | `elapsed_seconds`中央値 | 集約品質中央値 |
| --- | ---: | ---: | ---: |
| C206 | 1,098,859 | 754.859 | 100.0 |
| C207 | 1,058,515 | 732.705 | 100.0 |
| C208 | 1,039,141 | 613.175 | 100.0 |
| C208 − C207 | -19,374（-1.83%） | -119.530秒（-16.31%） | 0 |
| C208 − C206 | -59,718（-5.43%） | -141.684秒（-18.77%） | 0 |

同じcompatibility keyを持つ独立N=5 selectionの中央値であり、paired差ではない。C208はC207より本文が208文字増えた一方、ADR9集約では品質同値のままtokenとelapsedが低い。よって少なくとも今回の標本では追加文字が集約cost増をもたらしたとはいえず、制御文字当たりの観測価値はC207より高い。ただし機序gate不通過なので、合格resultやStandard14費用対効果の根拠にはしない。

## 状態

`candidate208_ADR9_completed / valid_45 / score4_45 / quality_passed / mechanism_failed / counterexample_direct_read_1_of_20 / root_preread_1_of_30 / Standard14_not_started / N20_not_started / stopped / adoption_not_decided / release_not_created / projection_not_performed`

## 一次アーティファクト

- [C208登録result](c4e84aef70aa4d5d9b97c09c6817605d.json)
- [品質・機序監査](candidate208-result-kind-evidence-domain-adr9-r2-n5-quality-mechanism-audit-r1.json)
- [作成前設計](../../docs/candidate208-result-kind-evidence-domain-design.md)
- [実装監査](../../docs/candidate208-result-kind-evidence-domain-implementation-audit.md)
