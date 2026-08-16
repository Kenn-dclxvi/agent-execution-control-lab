# Candidate262 Standard14 token退行原因監査

## 結論

Candidate262 Standard14は70 / 70件でScore `4`を維持したが、Candidate147比でall-agent総token中央値が`+5.06%`、経過時間中央値が`-2.65%`だった。時間短縮でtoken増加を相殺せず、token増加が品質または必要成果に使われたかを既存traceで調べた。

主要な増加はA02、F02、F04、F07 canonical runnerの4ケースに集中した。4ケースのケース別token中央値差は合計`+137,457`である。F06の`-47,521`など他ケースの減少で一部が相殺され、14ケースをiteration単位で組にした全体中央値差は`+73,220`となった。

4ケースはいずれもCandidate147と同じScore `4`、同じ必要成果、同じ許可範囲を満たした。Candidate262だけに必要な追加成果または追加検証はない。traceでは、広いrepository検索、大きいsourceやtestの分割読み取り、追加の位置絞り込み、authority探索、最終diff確認の分割がtokenを使っていた。これらの一部は合法で必要な処理だが、Candidate147が同じ品質をより少ない中央値で達成しているため、増加分全体を必要処理の対価とは認めない。

したがって`unjustified_token_regression`とし、Candidate262の正式採用を承認しない。これはCandidate262の一文が4ケースの増加を因果的に発生させたと確定する判断ではない。N=5で観測したCandidate262構成の費用分布が採用条件を満たさないという判断である。

## 全ケース比較

| ケース | C147 token中央値 | C262 token中央値 | token変化 | C147時間 | C262時間 | 時間変化 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A01 | 19,195 | 18,709 | -2.53% | 12.148秒 | 14.746秒 | +21.38% |
| A02 | 129,085 | 160,793 | +24.56% | 73.379秒 | 76.138秒 | +3.76% |
| F01 | 107,202 | 110,258 | +2.85% | 66.424秒 | 55.567秒 | -16.35% |
| F02 | 128,236 | 175,450 | +36.82% | 100.607秒 | 89.866秒 | -10.68% |
| F03 | 104,320 | 100,693 | -3.48% | 70.866秒 | 66.643秒 | -5.96% |
| F04 | 151,170 | 186,096 | +23.10% | 91.431秒 | 80.675秒 | -11.76% |
| F05 clarify | 37,242 | 38,973 | +4.65% | 26.725秒 | 20.522秒 | -23.21% |
| F05 out of scope | 37,366 | 36,611 | -2.02% | 25.291秒 | 20.632秒 | -18.42% |
| F06 | 151,542 | 104,021 | -31.36% | 79.393秒 | 72.884秒 | -8.20% |
| F07 canonical runner | 102,504 | 126,113 | +23.03% | 72.547秒 | 76.913秒 | +6.02% |
| F07 dependency | 87,284 | 84,531 | -3.15% | 54.324秒 | 52.368秒 | -3.60% |
| F08 | 113,067 | 103,556 | -8.41% | 56.343秒 | 60.115秒 | +6.69% |
| F10 entrypoint | 87,934 | 86,360 | -1.79% | 61.546秒 | 62.414秒 | +1.41% |
| F10 monthly | 93,096 | 93,209 | +0.12% | 51.796秒 | 48.740秒 | -5.90% |

## 主要増加ケース

### A02

token中央値は`+31,708`、`+24.56%`だった。Candidate262の5件は128,748から184,235 tokenに分布した。大きいrunでは`run.sh`だけでなく、repository全体のV4 / daily検索、複数README、test authorityを読み、full pytestと複数の最終状態確認を行った。

必要なcanonical routeをrepository authorityから解決する処理は正常経路である。しかしCandidate147は同じ成果とScore `4`を中央値129,085 tokenで達成している。Candidate262で増えた検索範囲と確認分割が追加品質を生んだ証拠はない。

### F02

token中央値は`+47,214`、`+36.82%`で、最大の増加だった。Candidate147は約125,000から128,000 tokenのrunが3件、約257,000から264,000 tokenのrunが2件という二群だった。Candidate262は129,425 tokenが1件、175,020から206,271 tokenが4件だった。このため新しい固有処理が一件だけ現れたのではなく、大きいsource / test読み取りと追加絞り込みを行う中間費用経路の出現頻度が中央値を押し上げた。

Candidate262 traceでは、`v4_engine.py`、`collection_history_updater.py`と二つのtestを別commandで読み、runによっては同じ対象を`rg`や行番号付き表示で追加確認した。必要な実装判断は成立したが、増加分に対応する追加成果はない。

### F04

token中央値は`+34,926`、`+23.10%`だった。5件は126,973から314,927 tokenまで広く分布した。最大runは`App.tsx`を複数範囲に分けて読み、package fileとlock fileも読み足した。別runでも`App.tsx`の大きい範囲を複数回取得した。

必要な列表示条件とtable構造を読むことは正常処理だが、全文に近い複数範囲とlock fileまで読むことが成果品質に必要だったとは確認できない。Candidate147と同じScore `4`であり、追加成果はない。

### F07 canonical runner

token中央値は`+23,609`、`+23.03%`だった。Candidate262は約101,000 tokenが2件、126,000から134,000 tokenが3件だった。大きいrunでは`run.sh`に加えてroot `AGENTS.md`、AGENTS探索、repository top-level identity、複数の最終確認を分けて取得した。

適用中instructionと`run.sh`の確認は合法だが、Candidate147の中央値102,504 tokenより増えた部分を必要処理として裏付ける品質差はない。

## prompt長と因果帰属

Candidate262のroot本文はCandidate147より182 bytes長い。4ケースのtoken中央値増加は各23,609から47,214 tokenであり、本文固定費だけでは大きさを説明できない。主な使用先は実行中に得たrepository出力を次のAI判断へ戻す回数と範囲である。

一方、Candidate262の変更はA01用のpermission境界一件だけで、4ケースに特定の検索、read順、commandまたは確認回数を要求していない。したがって「一文が必ず4ケースの経路を発生させた」という100%の因果帰属は行わない。採用判断では、原因の完全確定より先に、評価した構成が品質同値でtokenを5.06%増やした事実を使う。

## 判断

Candidate262はA01の不要な開始状態読み取りを5 / 5件で閉じ、Standard14の品質も70 / 70件で維持した。しかし全体のtokenと時間を同時に減らす条件は満たさなかった。主要token増加には追加品質または追加成果がなく、必要処理として正当化できない。

このため、追加N、正式採用、releaseおよびtarget本体への反映を承認しない。次の設計へ進む場合は、今回の成功動作やtool順を指示へ転記せず、A01のpermission閉鎖を保持したまま非対象ケースへ全体影響を広げない構造が存在するかを改めて検討する。

`quality_passed / aggregate_token_regressed_5_06_percent / elapsed_improved_2_65_percent / major_regressions_a02_f02_f04_f07 / additional_quality_not_observed / causal_attribution_to_single_clause_not_established / unjustified_token_regression / adoption_not_approved`
