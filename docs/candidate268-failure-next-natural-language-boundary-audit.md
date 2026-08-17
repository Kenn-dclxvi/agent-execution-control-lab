# Candidate268を次の直接基盤とする自然語境界監査

## 結論

次の自然語改善はCandidate268を直接の基盤にする。Candidate268は追加N、Standard14、採用、releaseおよびprojectionへ進むgateには失敗したが、F10のinstruction result依存を5 / 5件で成立させ、F01・F03の正常経路も各5 / 5件で保持した。この成立分まで捨ててCandidate254から再構成し直すと、同じ関係を再発見するだけになり、Candidate間の差分として知見が蓄積されない。

Candidate268の失敗を正常経路として継承するわけではない。F02共同発行4 / 5件とterminal closure違反13 / 20件は、次案で解消すべき未完了predicateとして保持する。次案はCandidate268との差分としてだけ設計し、C268で成立した関係を保持したまま、この二つの未完了predicateを狭い自然語差分で閉じる。

Candidate269はまだ作成しない。理由はCandidate268を親にできないからではなく、Candidate268に対してどのpermissionまたはdependencyの辺を最小範囲で変えるかが未固定だからである。Candidate268で観測した二つの誤経路は、どちらもCandidate268のpromptがすでに禁止している。

1. F02 run `8e4ed55acc854576b0c880f7adc380c2`は、開始状態がreadの対象・許可を変えないのに、開始確認resultを受け取ってから許可済みreadを発行した。Candidate268の`DECISION_BOUNDARY`は、このresultをreadの開始条件にすることと、readを別model stepへ置くことを明示的に禁止している。
2. 13件のvalidation runはcell IDを伴うnonterminal resultを受けた。Candidate254から同一byteで保持した`VALIDATION_PLAN`は、同じcell IDへの`wait`だけを発行し、terminalになるまで判断、別toolおよび終了へ進まないことを明示している。3件は別`exec`へ進み、10件はtoolを追加せず終了した。

したがって、次案ではCandidate268の既存境界を変更するが、失敗runの処理順を追記したり、同じ禁止を言い換えて重ねたりする変更にはしない。Candidate268を保持したまま、同じ禁止が実効化されなかった配置、依存元またはobservable output境界を特定し、既存文の置換、配置変更または依存関係の再接続として変更する。Candidate作成前gateを満たすまでは、C269を追加条件Candidateとして発行しない。

## 固定する目的と位置づけ

- `task_objective`: Candidate268の自然語F10 dependencyとF01・F03の正常経路を保持し、F02の開始確認result dependencyとnonterminal resultのterminal dependencyに残る未完了predicateを、Candidate268に対する最小の自然語差分で閉じ、品質を維持しながらC147比の正当化不能なKPI差の解消へ近づける。
- 次の直接基盤: Candidate268。
- Candidate268: 成立したF10、F01・F03を保持する実装基盤であり、F02、terminal closureおよびKPI退行を未完了predicateとして持つ。評価失敗は採用しないが、明示された次系列の親として使う。
- Candidate254: Candidate268の直接の親であり、系譜、元本文および診断比較の参照に限る。次案をC254から作り直さない。
- Candidate147: 本文の複写元ではなく、F01・F02・F03で15 / 15件の共同発行が成立した比較・機序基準。
- Candidate264・Candidate267: 形式記法や本文ではなく、それぞれF01〜F03共同発行とF10 instruction result依存が成立し得ることのfeedback evidence。

## C147でできていたこととの比較

Candidate147はF01・F02・F03の15件すべてで、開始確認と許可済みreadを同じAI判断から発行していた。nonterminal resultが返った対象四ケースでは、4 run・6回の外部`wait`を使って完了を待った。外部`wait`のcost自体は課題だが、nonterminal resultをterminalとして扱わず待機した点はC268と異なる。

Candidate268はF01・F02・F03の15件中14件だけが共同発行で、C147の15 / 15へ届かなかった。また13件でnonterminal resultが返ったのに、外部`wait`は0回だった。これはC147より効率化したのではなく、C147が守ったterminal dependencyを失った結果である。

## モデル再入の課題

モデル再入を二種類に分ける。

- 合法な再入: nonterminal resultの同じcellを待つためだけの再入。C147の4 run・6回とC267の10 run・29回が該当する。直接costではあるが、prompt内では必要な同期であり、待機そのものを禁止しない。
- 誤った再入: pending resultをbindせず別のoperationへ進む再入。C268では3件が別`exec`を発行した。これは既存の`VALIDATION_PLAN`が禁止しており、新しい判断条件ではなく既存dependencyの不遵守である。

C268の残る10件は再入せず終了したため、再入削減として数えない。terminal result欠落のまま完了を宣言できる経路であり、より重大なterminal closure違反として扱う。

## 再入以外の課題

- F02の開始確認・read分離は、C268の自然語境界が一件で守られなかった。原因を特定した後に既存境界を変更するが、成功runのtool順を命令へ転記する変更にはしない。
- F02は5 / 5件でtruncationを観測し、外部`wait=0`でもtoken中央値がC147比`+43.97%`だった。モデル再入を除いてもcarrier容量未拘束の課題は残る。
- F10は5 / 5件で必要dependencyを守ったが、token中央値はC147比`+28.52%`だった。C147のF10にはinstruction result前readが3 / 5件含まれるため、C147の低costなF10 tool順を正常経路として複写しない。
- 全体ではC147比token`+28.06%`、elapsed`+10.02%`であり、自然語機序の復元とKPI差解消の両方が未完了である。

## 次に必要な証拠

次Candidateを作るには、次のいずれかを先に特定する必要がある。

1. Candidate268の共同発行成功14件とF02失敗1件の間で、同じ自然語が実効化されるかを分けた配置、依存元または出力境界。
2. C147のterminal待機とC268の未待機の間にあり、Candidate268ではまだ閉じていないpermissionまたはdependency差。
3. 同じ禁止文を守らないrouteを、追加条件や処理手順ではなく、Candidate268の別のowner、carrierまたはobservable output境界への局所差分で実行不能にできること。

未特定のF02については、既存禁止の反復、ticket、自己判定、tool順、待ち時間、特定command構成または成功runの手順を推測で追加しない。原因を特定済みのterminal closureについては、C268から失われた外側carrierを自然語で再接続する変更の検討を先に進める。

## 知見を蓄積するための次Candidate gate

- 直接の親はCandidate268に固定する。
- 機序合格線は[Candidate268・Candidate147機序基準線と原因分析](candidate268-candidate147-mechanism-baseline-causal-analysis.md)に従い、項目ごとのC147実測率へ固定する。一律100%にしない。
- C147が100%だったF01・F02・F03共同発行、F10必要read完遂および観測済みnonterminal resultのterminal dependencyだけ100%を基準線にする。
- C147が2 / 5だったF10 instruction result先行を、C268が5 / 5だったことだけで次Candidateの100% gateへ昇格させない。
- F02 4 / 5とterminal closure違反13 / 20を未完了predicateにし、成立済みとして扱わない。
- 次案の直接比較はCandidate268とし、Candidate147とCandidate254は診断比較に限る。
- allowed deltaは、C268の既存文の置換、配置変更またはdependencyの再接続に限定する。Candidate254への差し戻し、C147本文の複写、成功runのtool順の転記および既存禁止文だけの追加はallowed deltaにしない。
- 一つの局所差分で二つの未完了predicateを閉じられない場合は、一Candidateへ混ぜず、どちらを先に閉じるかを設計記録で固定する。

現在状態は`candidate268_evaluation_stopped / candidate268_next_direct_base / candidate269_not_created_delta_not_fixed / candidate254_ancestry_and_diagnostic_reference_only / candidate147_mechanism_and_kpi_reference_only / f10_dependency_achieved_and_preserved / f01_f03_preserved / f02_joint_issuance_unresolved / terminal_dependency_unresolved / external_wait_cost_not_a_prompt_candidate / carrier_design_deferred_until_boundary_identified / additional_n_not_started / standard14_not_started / adoption_not_approved / release_not_created / projection_not_performed`とする。
