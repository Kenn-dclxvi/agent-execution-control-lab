# Candidate202 M5原因分析

## 結論

Candidate202は、C200とC201で崩れたreviewer起動、入力routing、projection receipt、開始identity境界およびresult admissionを回復した。ADR9 r2 N=5は45 / 45 Score 4で、required reviewerも30 / 30起動した。しかし、具体的反例が投影済み観測だけで成立していた20件のうち9件で、reviewerが終端判定前にreviewer-direct targetを読んだため、状態は`quality_passed / mechanism_failed / stopped`である。

直接原因はroutingの失敗ではない。Candidate202は「counterexample certificateを最初に判定する」と宣言したが、reviewer-direct readの発行資格を、certificate判定のterminal resultへ依存させていない。reviewerはmanifest全件を満たそうとする一般的なevidence収集経路を選べたため、結果kindを正しく保ちながら不要readを先に発行した。

## 証拠境界

分析対象は[Candidate202結果](../evaluations/results/candidate202-review-admission-routing-receipt-adr9-r2-n5_2026-08-13.md)、[品質監査r2](../evaluations/results/candidate202-review-admission-routing-receipt-adr9-r2-n5-quality-audit-r2.json)、[機構監査r2](../evaluations/results/candidate202-review-admission-routing-receipt-adr9-r2-n5-mechanism-audit-r2.json)、登録result `0a509a780f0e40ae857ea602f00ff89b`および保存済みroot / reviewer traceである。

C175との比較には[Candidate175結果](../evaluations/results/candidate175-review-operation-admission-closure-adr9-standard14-n5_2026-08-10.md)、登録result `eba0a4bc1d0e4391afa631462b8daccb`および保存済みADR9 r2 traceを用いた。両登録resultのcompatibility keyは`1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`で一致する。

固定済みcase、fixture、private oracle、rating contract、Candidate202 bundleおよび保存済みresultは変更しない。この原因分析時点では追加run、Standard14、新Candidate、releaseおよびprojectionを作成しないとした。その後、利用者の明示的な別実行許可により[Standard14 N=5](../evaluations/results/candidate202-review-admission-routing-receipt-standard14-n5_2026-08-13.md)だけを実施したが、ADR9の品質・機構判定は変更していない。

## C175との結果比較

| 観測 | Candidate175 | Candidate202 | C202 - C175 |
|---|---:|---:|---:|
| valid run | 45 / 45 | 45 / 45 | 0 |
| Score 4 | 45 / 45 | 45 / 45 | 0 |
| required reviewer起動 | 30 / 30 | 30 / 30 | 0 |
| forbidden canary配送 | 0 | 0 | 0 |
| quality中央値 | 100.000 | 100.000 | 0.000 |
| all-agent token中央値 | 1,123,616 | 1,289,669 | +166,053（+14.78%） |
| elapsed中央値 | 733.368秒 | 692.947秒 | -40.421秒（-5.51%） |
| counterexample前のpaired-scope read | 7 / 20 | 9 / 20 | +2 |

C175の当時の固定機構gateはcounterexample成立後にmissingを優先しない結果効果を確認したが、direct repository readの発行順までは固定していない。したがってC175の`7 / 20`は現在の診断predicateによる追加観測であり、保存済みC175判定を遡及変更するものではない。

Candidate202はC175と同じqualityとdispatchを再現したが、順序制御は改善しなかった。token増加とelapsed短縮も、機構gate不通過のため採用上の効率差ではない。

## C200・C201から回復したもの

| 旧failure | C202観測 | 判定 |
|---|---:|---|
| C200 required reviewer欠落14件 | 0 / 30 | 回復 |
| C200 wrong review result 3件 | 0 / 30 | 回復 |
| C201 required reviewer欠落15件 | 0 / 30 | 回復 |
| C201 projection receipt未観測8件 | 0 / 30 | 回復 |
| C201開始identity境界違反3件 | 0 / 45 | 回復 |
| closed source read / mixed read | 0 / 30 | 維持 |
| counterexampleより無関係なreadを先に発行 | 9 / 20 | 未解決 |

決定的routingはowner authority欠落を解消した。root projectionとreviewer-direct targetをmanifest targetの形から一意に分け、reviewerは必要30件すべてで起動した。projection receipt acknowledgementも30 / 30、exact read setも30 / 30である。C202の停止理由をC200のread閉鎖またはC201のowner欠落へ戻さない。

## 9 runの分類

| case | run数 | 観測 |
|---|---:|---|
| ADR03 | 1 | 投影済みmembership反例の成立前にpaired-scopeを読んだ |
| ADR04 | 1 | 投影済みapplicability反例の成立前にpaired-scopeを読んだ |
| ADR05 | 5 | 投影済みownership反例の成立前にmissingまたはreadable paired-scopeを読んだ |
| ADR06 | 2 | 投影済みconsumer反例の成立前にpaired-scopeを読んだ |

全9件で最終結果は`counterexample_found`、外側terminalは`blocked`、artifact変更は0件だった。したがって品質oracleは満たすが、不要readの発行という機構failureは残る。

## 原因

Candidate202本文は、result-kindの意味上の優先順を記述している。

- concrete counterexampleを最初に判定する
- 成立すれば`counterexample_found`をterminalにする
- 後続missingで失効させない

一方、reviewer-direct observationの発行条件は、routing後にexact targetだけを読むことまでしか固定していない。次の依存関係が欠けている。

`reviewer_direct_read_eligible := counterexample_certificateの投影済み入力による判定がterminal ∧ state=not_established ∧ result-kind判定に当該direct observationが必要`

この欠落により、reviewerは許可範囲とread setを守ったまま、certificate判定結果を物質化する前にmanifest completionを進められた。条項中の「最初に」は判断規範としては読めても、repository invocationの発行資格として拘束されなかった。

## 次の再開境界

次に許可するのはM2設計ではなく、まずM1で次の一軸を固定することである。

1. 投影済み入力だけを消費するcounterexample certificate判定を、reviewer-direct readとは別の先行predicateとして固定する。
2. 先行predicateが`established`ならreviewer-direct readを失効し、そのまま`counterexample_found`へ閉じる。
3. `not_established`の場合だけ、result kindを閉じるために必要なexact direct observationを一件発行する。
4. routing、receipt、read閉鎖、明示producer、三result kind、開始identity境界およびC147直接基盤は変更しない。
5. 新Candidateを作る前に、C175とC202の全counterexample traceへこの発行資格を当て、成立時のdirect readが0 / 20になることを静的に反証確認する。

Candidate202を修正して再評価せず、次案を作る場合もC147を直接親とする。C175、C200、C201およびC202は成立traceまたは反例としてだけ使う。
