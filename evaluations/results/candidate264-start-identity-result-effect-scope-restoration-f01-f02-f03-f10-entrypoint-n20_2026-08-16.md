# Candidate264開始確認結果影響範囲の復元 F01・F02・F03・F10 entrypoint N=20

## 結論

N=5で停止済みだったCandidate264を、利用者の明示的な判断により同じ四ケースだけ各N=20へ拡張した。既存20件を再利用し、不足60件だけを発行した。合計80 / 80件がvalidかつ採点可能で、すべてScore `4`だった。この再開は、以前の停止判断を取り消すものでも、Standard14、採用、releaseまたはprojectionを許可するものでもない。

開始確認resultで対象または許可が変わらないreadを同じAI判断から発行する経路は、F01、F02、F03で各20 / 20件成立した。一方、`src/AGENTS.md`のresultによって配下readの対象または許可が変わり得るF10で、result受領後に三つのentrypoint本文を読んだのは2 / 20件だけだった。追加15件は全件で本文readを先行発行した。N=5で観測した正常経路の退行は、N=20で解消せず、むしろ低頻度の揺らぎとして説明できない状態になった。

同じ四ケース各N=20をCandidate147のN=100 poolから固定した比較では、品質は同じ100、Candidate264のall-agent総token中央値は`514,485`でCandidate147の`478,811.5`より`35,673.5`、`7.45%`多かった。経過時間も`305.958`秒でCandidate147の`289.963`秒より`15.994`秒、`5.52%`長かった。両KPIが退行し、追加品質もない。

保存root rolloutの`wait`を、validation wrapperがcell ID付きnonterminal resultを返した後の追加モデル再入として数えた。C147 N=100の同じ四ケースでは60 / 400件、`15.00%`に発生したため、C147側でも再入は起こり得る。Candidate264 N=20では33 / 80件、`41.25%`だった。F01からF03では`wait`ありrunのtoken中央値が`wait`なしrunより約25,566から55,240多く、今回のtoken増加と整合する。この26.25ポイント差は、C147からCandidate264までのprompt全体構造差と無関係な誤差とは扱わない。Candidate264はCandidate254系列の展開本文、validation境界の表現および固定context量を含めてC147と構造が異なる。一方、実行時間とwrapper返却時機も混在するため、差の全量をCandidate264の局所`DECISION_BOUNDARY`変更だけへ帰属しない。

現在状態は`targeted_n20_explicitly_reopened / valid_80_of_80 / score4_80_of_80 / f01_joint_20_of_20 / f02_joint_20_of_20 / f03_joint_20_of_20 / f10_required_dependency_2_of_20_normal_route_regressed / token_regressed_7_45_percent / elapsed_regressed_5_52_percent / unjustified_cost_regression / stopped / standard14_not_started / adoption_not_approved / release_not_created / projection_not_performed`とする。

## 実行と登録

- cases: `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY` r3、`TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` r1、`TC-F03-ATOMIC-CONTEXT-CLEANUP` r2、`TC-F10-ENTRYPOINT-INVENTORY-REVIEW` r1。
- 既存run: 4ケース各5件、計20件。
- 追加発行: 4ケース各15件、計60件。
- 追加batch: 60 / 60 valid、excluded 0、execution error 0、再試行0、実行時間229.723秒。
- N=20全体: 80 / 80 valid、Score `4 = 80`。
- Candidate264 selection: `142850aac9e748019f7a8e7a88338c9d`。
- Candidate264 analysis: `6645694b99a046aaac85d5c1daa791cf`。
- Candidate264登録result: [`92467093897544f98eb526e018757abb`](92467093897544f98eb526e018757abb.json)。
- C147同数selection: `c2102d19ee2340aa81fbc2b1472398e5`。N=100登録result `e6fc6e10dedd47f5a1d59d114e6e0f57`のpoolから、同じ四ケース各20件を固定し、baselineは再実行していない。
- C147同数登録result: [`a1910bf71a474153947dabfc4582991a`](a1910bf71a474153947dabfc4582991a.json)。
- compatibility key: `a5ba602a9e76164d140f739048f86bde0599f10a9514b7f9a9f4fdf6765ffe57`。
- 追加60件の[品質監査](candidate264-start-identity-result-effect-scope-restoration-f01-f02-f03-f10-entrypoint-n20-extension-quality-audit-r1.json)と、既存N=5の品質監査を合わせて80件の個別scoreを確認した。
- [N=20機序・再入監査](candidate264-start-identity-result-effect-scope-restoration-f01-f02-f03-f10-entrypoint-n20-mechanism-audit-r1.json)はC264 80件とC147 N=100の同一四ケース400件の保存rolloutを全件対応付けた。

## ケース別KPI

| ケース | C147 token中央値 | C264 token中央値 | token差 | C147秒 | C264秒 | 秒差 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| F01 domain duplicate asset key | 107,010.5 | 128,100.5 | +21,090 | 62.107 | 70.991 | +8.884 |
| F02 cross-layer history date bound | 134,960 | 169,728 | +34,768 | 79.763 | 89.819 | +10.056 |
| F03 atomic context cleanup | 98,746 | 133,217 | +34,471 | 70.780 | 90.190 | +19.410 |
| F10 entrypoint inventory | 102,345 | 68,529 | -33,816 | 66.849 | 52.618 | -14.230 |
| 四ケース一組の中央値 | 478,811.5 | 514,485 | +35,673.5 | 289.963 | 305.958 | +15.994 |

ケース別中央値の合計と、同じselection iterationで四ケースを一組にした20標本の中央値は集計方法が異なるため一致しない。正式比較値は最下段であり、ケース別値は原因診断に使う。

F10だけtokenと時間が減ったが、必要なinstruction result境界を18 / 20件で通らなかった。正常経路を省いたことによるcost減少を改善とは扱わない。F01からF03の増加は、次の`wait`頻度と対応する。

## validation完了待ちによる追加モデル再入

| ケース | C147 N=100 `wait`発生run | C147発生率 | C264 N=20 `wait`発生run | C264発生率 | C264 `wait`あり／なしtoken中央値 |
| --- | ---: | ---: | ---: | ---: | ---: |
| F01 | 19 / 100 | 19% | 10 / 20 | 50% | 153,285 / 114,271 |
| F02 | 17 / 100 | 17% | 10 / 20 | 50% | 186,219 / 130,979 |
| F03 | 24 / 100 | 24% | 13 / 20 | 65% | 134,486 / 108,920 |
| F10 | 0 / 100 | 0% | 0 / 20 | 0% | 該当なし |
| 合計 | 60 / 400 | 15.00% | 33 / 80 | 41.25% | — |

一つのrunで複数回`wait`した場合があるため、call数はC147が77回、C264が44回である。この表は追加モデル再入がC147でも発生することと、`wait`ありrunのcontext再投入costが大きいことを示す。C264の高い観測頻度はtoken差の主要な説明経路であり、C147とC264のprompt全体構造差による影響を調べる対象である。ただしC147とCandidate254系列では`DECISION_BOUNDARY`以外の本文構造も異なり、validation実行時間も混在するため、この監査だけで局所条項の単独因果へ縮小しない。

## 機序

| gate | C147 N=100 | C264 N=20 | 判断 |
| --- | ---: | ---: | --- |
| F01 開始確認と許可済みreadを同じAI判断から発行 | 99 / 100 | 20 / 20 | 維持 |
| F02 同上 | 100 / 100 | 20 / 20 | 維持 |
| F03 開始確認resultで変わらない必要readを遅延しない | 98 / 100 | 20 / 20 | 対象機序を維持 |
| F10 instruction result後に配下本文readを発行 | 52 / 100 | 2 / 20 | 必要な正常経路を維持できない |

成功runのtool順を次の制御手順へ転記しない。N=20は、F03の局所機序が成立しても、同じ`DECISION_BOUNDARY`で必要なF10依存境界を閉じられていない反例を強めた。Candidate264へ条件を追加して継続する根拠にはしない。

## 判断

品質結果、F01からF03の共同発行およびC147側にも`wait`再入があるという観測は保持する。しかし、F10の必要な正常経路は追加15件で一度も成立せず、品質同値のC147 N=20に対してtokenと経過時間がともに退行した。増加分を必要な品質または正常経路へ対応づけられないため、Candidate264は引き続き停止する。

この結果からStandard14、採用、releaseまたはprojectionへ進めない。完了待ち頻度を下げるためのwrapper、runtimeまたはexecutor変更も、このCandidateのprompt制御案として提案しない。
