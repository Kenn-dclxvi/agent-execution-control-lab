# Candidate207 C147 review境界再構成 ADR9 r2 N=5

## 結論

Candidate207はADR9 r2を45 / 45 valid、除外0、45 / 45 Score `4`で完了した。reviewの要否、producer cardinality、terminal、result effect、artifact境界およびrequired commandは全件一致した。

ただし機序gateは不通過である。投影済みpacketだけで`counterexample_found`が成立した20件のうち、12件でreviewerがterminal判定前にrepository readを発行した。また、reviewerはpacket供給元の`evaluation-fixture/design-admission.json`を20件で再読した。C207本文の`projected_counterexample_established(packet)=false`というread資格は、期待した発行抑止として十分に作用しなかった。

validな低品質機序resultとして保存して停止する。repair rerun、Standard14、N=20延長、採用、releaseおよびprojectionは実施しない。

## 比較前固定

- 比較基準: Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`
- Candidate147保存N=50 poolから各case先頭5件を再選択し、新規baseline slotは0件
- C147 N=5 reference result: `2b3aa86fd9a440d78bc078307fd5fa45`
- C207 result: `9f6feb29f0114699beb4b11dbfbaa459`
- comparison compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- preflight: 9ケース×5件、45 capsule、prompt identity以外の条件一致、`max_workers=24`、`ready`

## 品質結果

| 指標 | 結果 |
| --- | ---: |
| valid run | 45 / 45 |
| 除外attempt | 0 |
| Score 4 | 45 / 45 |
| terminal一致 | 45 / 45 |
| reviewer cardinality一致 | 45 / 45 |
| artifact境界一致 | 45 / 45 |
| required command一致 | 15 / 15 |
| forbidden canary配送 | 0 |

reviewerはADR01、ADR02、ADR08で0、ADR03〜ADR07、ADR09で各run一件だった。ADR03〜ADR06は`blocked`、ADR07は`completion_ready`、ADR09は`unavailable`となり、review resultのadmissionとartifactへの効果も30 / 30一致した。

## 機序結果

| 共通監査した機序 | C206 | C207 | C207 - C206 |
| --- | ---: | ---: | ---: |
| rootによるreviewer-owned targetの先読みなし | 30 / 30 | 30 / 30 | 0 |
| reviewer cardinality一致 | 45 / 45 | 45 / 45 | 0 |
| review result admission一致 | 45 / 45 | 45 / 45 | 0 |
| review result effect一致 | 45 / 45 | 45 / 45 | 0 |
| packet反例成立run | 20 | 20 | 0 |
| packet反例成立時にdirect readなし | 13 / 20 | 8 / 20 | -5 |
| packet反例成立後のdirect read違反 | 7 / 20 | 12 / 20 | +5 |
| packet供給元`design-admission.json`再読 | 5 | 20 | +15 |
| exact manifest direct read set一致 | 25 / 30 | 15 / 30 | -10 |
| mixed read | 2 | 13 | +11 |
| manifest外read | 3 | 7 | +4 |

主失敗は、C207がread eligibilityをpredicateとして定義しても、reviewerがpacket上の反例を宣言した後に「全manifest descriptorへterminalをbindする」ためreadを追加したことである。C206でも同じC207共通gateを後付けすると7 / 20件の違反があったが、C207は12 / 20件へ退行し、source再読とread set逸脱も増えた。したがって、C206の手順記載を除外しただけで境界が同等に保たれたとはいえない。

この比較はC206保存済み45 traceへC207と同じpredicateを適用した再監査であり、新規runは0件である。C206当時の`mechanism_passed`は`admitted_evidence_current`によるroot instruction再取得抑止の成立を指す。その歴史的判定を変更せず、今回のread gateでは`7 / 20 violation`だったという別の診断を追加する。

## KPI診断

ADR9の正式gateは品質と機序であり、Standard14のcost gateではない。参考として、同じcompatibility keyを持つ各promptの独立N=5 selection集約を示す。case・反復数・評価条件は互換だがatomic run自体は別であり、paired差ではない。

| prompt | `total_tokens`中央値 | `elapsed_seconds`中央値 | 集約品質中央値 |
| --- | ---: | ---: | ---: |
| C147 | 1,027,294 | 518.109 | 50.0 |
| C206 | 1,098,859 | 754.859 | 100.0 |
| C207 | 1,058,515 | 732.705 | 100.0 |
| C207 − C206 | -40,344（-3.67%） | -22.154秒（-2.93%） | 0 |
| C207 − C147 | +31,221（+3.04%） | +214.597秒（+41.42%） | +50.0 |
| C206 − C147 | +71,565（+6.97%） | +236.750秒（+45.70%） | +50.0 |

C207はADR9集約上、C206と同じ品質中央値でtokenとelapsedの両方が低い。しかし機序は、反例成立後readがC206の7 / 20からC207の12 / 20へ退行している。したがってC207は「C206より低costで同品質」だけを根拠に優位とは判定できず、費用を正当化する合格resultにもならない。Standard14を発行して通常経路costを測る資格も得ていない。

## 状態

`candidate207_ADR9_completed / valid_45 / score4_45 / quality_passed / mechanism_failed / counterexample_direct_read_12_of_20 / packet_source_reread_20 / Standard14_not_started / N20_not_started / stopped / adoption_not_decided / release_not_created / projection_not_performed`

## 一次アーティファクト

- [C207登録result](9f6feb29f0114699beb4b11dbfbaa459.json)
- [C147 N=5再選択result](2b3aa86fd9a440d78bc078307fd5fa45.json)
- [C206登録result](aee4cdf149ef43de9305b1a3138ebe59.json)
- [品質・機序監査](candidate207-c147-review-boundary-recomposition-adr9-r2-n5-quality-mechanism-audit-r1.json)
- [C206へのC207共通機序監査](candidate206-admitted-evidence-current-adr9-r2-n5-c207-comparable-mechanism-audit-r1.json)
- [実装監査](../../docs/candidate207-c147-review-boundary-recomposition-implementation-audit.md)
