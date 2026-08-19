# P005 VCC6 elapsed境界監査

> [!IMPORTANT]
> **結論**: `candidate_not_created / carrier_wall_not_primary / model_runtime_intervals_primary / pre_action_projection_is_existing_nonconformance / post_carrier_delta_is_runtime_skew / prompt_only_limit_not_proven`

## 目的

P001・P003・P005のfresh VCC6 N=5 traceから、P005のelapsedを直接観測可能な区間へ分解し、promptで削減できる可能性がある時間と、runtimeまたは必要な正常経路に属する時間を区別する。本監査は保存済み90 runの診断であり、Case、fixture、TaskSpec、oracle、rating、runnerまたは集計方法を変更しない。次Candidateも作成しない。

## 観測区間

各root sessionのtimestampとevaluation observationの`elapsed_seconds`を用い、次の区間へ分けた。

| 区間 | 始点と終点 | 解釈上の限界 |
| --- | --- | --- |
| adapter overhead | adapter計測開始からroot task開始まで、およびroot final後の差分 | promptから直接制御できないprocess・session境界を含む |
| initial to first tool | root task開始から最初のtool callまで | 初回model生成とruntime待機を分離できない |
| non-carrier tool wall | carrier以外のtool callから対応outputまで | required action実行を含む |
| non-carrier inter-tool wait | carrier前のtool outputから次tool callまで | model生成とruntime待機を分離できない |
| action done to carrier | 最後のaction側tool outputからcarrier callまで | carrier code生成を含む次model round |
| carrier wall | outer carrier callからterminal projection outputまで | nested validation、continuationおよびtool transportを含む |
| carrier done to final | terminal projection outputからfinal answerまで | 最終model生成とruntime待機を分離できない |

timestampから純粋なmodel計算時間、queue待ちまたはservice側処理時間を分離することはできない。このため、tool外の区間をそのままpromptで削減可能な時間とは扱わない。

## P003とP005の区間合計

両armは30 / 30件でScore 4かつ対象機序成立のため、同じ正常効果を持つ経路として区間を比較できる。

| 区間 | P003 | P005 | P005 − P003 |
| --- | ---: | ---: | ---: |
| adapter overhead | 144.212秒 | 143.284秒 | −0.928秒 |
| initial to first tool | 340.238秒 | 310.349秒 | −29.889秒 |
| non-carrier tool wall | 6.135秒 | 6.100秒 | −0.035秒 |
| non-carrier inter-tool wait | 45.358秒 | 41.842秒 | −3.516秒 |
| action done to carrier | 409.133秒 | 370.971秒 | −38.162秒 |
| carrier wall | 17.993秒 | 17.782秒 | −0.211秒 |
| carrier done to final | 108.580秒 | 120.006秒 | +11.426秒 |
| elapsed合計 | 1,071.649秒 | 1,010.334秒 | −61.315秒 |

P005の改善はcarrier commandの高速化ではない。主に初回tool発行までとaction完了後のcarrier発行までが短くなった。一方、carrier terminal後のfinal生成区間は11.426秒増えた。

## P005 elapsedの構成

| 区間 | 合計 | P005 elapsed比 |
| --- | ---: | ---: |
| adapter overhead | 143.284秒 | 14.18% |
| initial to first tool | 310.349秒 | 30.72% |
| non-carrier tool wall | 6.100秒 | 0.60% |
| non-carrier inter-tool wait | 41.842秒 | 4.14% |
| action done to carrier | 370.971秒 | 36.72% |
| carrier wall | 17.782秒 | 1.76% |
| carrier done to final | 120.006秒 | 11.88% |

直接のtool wallはnon-carrierとcarrierを合わせても23.882秒、全体の2.36%である。carrier wall 17.782秒を仮にゼロへしても、P001との差156.980秒は解消しない。現在の主な時間境界はtool実行ではなく、初回model生成、action result受領後のcarrier生成、およびterminal projection受領後のfinal生成である。

## 現在観測できる下限

P005各Caseの5 runから最短elapsedを一件ずつ選び、その最短値が5回ずつ再現すると仮定した楽観的lower envelopeは874.641秒である。

- P005実測合計1,010.334秒より13.43%短い。
- P001実測合計853.354秒よりなお2.49%長い。
- P003とP005をまたいで各Caseの最短機序成立runを選ぶ合成envelopeは852.108秒で、P001より0.15%短い。

合成envelopeは一つのprompt identityが実現した結果ではなく、採用可能な比較結果でもない。これは、必要機序を成立させながらP001付近へ到達するtraceがCase単位では存在することだけを示す。P005単独の実測から、prompt-onlyの数学的な下限または到達不能性は証明できない。

## ばらつきと残存余地

P005のrun別elapsedと各区間の相関は、`action done to carrier`が0.842で最大だった。carrier wallとの相関は−0.045である。N=5の小標本で因果を意味しないが、carrier command時間よりcarrierを生成するmodel roundの変動が全体差を説明している。

P003比の改善余地として残るのは、H01とH02、およびcarrier terminal後のfinal生成区間である。ただし、成功runの短いmodel stepやcode生成順を新しい義務として転記してはならない。以下のroute監査でも新しく閉じられるpermissionまたはdependency edgeを特定できなかったため、P006は作成しない。

## H01・H02のaction前projection

`codex-events.jsonl`上で、required actionのfile changeより前にresponse schemaと同形の`agent_message`を出したrunを確認した。

| Case | P003 | P005 | P005で観測した先行状態 |
| --- | ---: | ---: | --- |
| H01 | 1 / 5件 | 5 / 5件 | `action_state=not_required` 2件、`completed` 3件 |
| H02 | 2 / 5件 | 4 / 5件 | validation resultが空の`succeeded` 3件、`unavailable` 1件 |

これらは正常なterminal projectionではない。しかし、P003とP005に共通する`COMPLETION`は、required resultが欠ける間はoperationをnonterminalに保ち、進捗、要約、集約記述またはfinal responseで欠けたresultを補完することをすでに禁止している。H01ではP005の変更対象であるcarrier自体もrequired validation 0件のため開始しない。したがって、この先行projectionはP005が新しく許可した正常routeではなく、既存禁止へのmodel nonconformanceである。既存禁止を別表現で重ねることはpermission edgeの閉鎖にならないため、次Candidateの差分にはしない。

H01のP005はP003比でelapsedが14.195秒、tokensが17,471増えた。ただし増分tokensのほぼ全量はP005 H01 iteration 5の49,663 tokensに集中し、このrunだけがaction前に任意readも追加している。他のP005 H01 4件の平均elapsedは18.302秒で、P003の5件平均17.539秒に近い。先行projectionの件数だけではH01のelapsed増加を説明できない。

## carrier後final生成の再監査

carrierを使うH02からH06までの25件について、最後のcarrier output後に生成されたfinal roundのusageを集計した。

| arm | final input tokens | final output tokens | final reasoning tokens |
| --- | ---: | ---: | ---: |
| P003 | 431,283 | 2,519 | 229 |
| P005 | 427,989 | 2,524 | 232 |

P005のfinal出力量はP003とほぼ同じで、11.426秒の増加と引き換えに追加の結果内容または推論量を得ていない。timestampを秒単位へ丸めた比較では、P005 H03 iteration 2のcarrier後区間だけが11秒であり、通常の3〜6秒からの偏りがP003比増加約12秒のうち8秒を占める。残り24件の差は約4秒である。よって、この増加はterminal projectionの内容増ではなく、主に一runのmodel/runtime待ち時間偏りとして扱う。

carrier terminal resultを受け取る前にfinal responseを生成することはできず、受領後のfinal responseもrequest contractが要求する正常経路である。この二つをpromptで並列化または省略する案は依存関係を壊す。runtime待ち時間をprompt Candidateの解決対象へ置くことも、prompt-only比較の変数境界を越えるため行わない。

## 現時点の判断

1. P005はP003比で、同じ品質と機序を維持しながらelapsedを5.72%減らした。
2. carrier wallは全体の1.76%であり、現在の主因ではない。
3. P001の短いelapsedは対象機序不成立24 / 30件を含むため、full-effect routeの実測下限としては使えない。
4. P005の楽観的envelopeもP001より2.49%長く、P005が固定cost gateを満たす証拠はない。
5. P003・P005をまたぐfull-effect traceにはP001相当のCase別最短値があるため、prompt-only限界へ到達したとも断定できない。
6. H01・H02の先行projectionは既存`COMPLETION`への違反であり、P005のallowed deltaが新しく開いた合法routeではない。禁止文の重複追加は行わない。
7. post-carrier増加はfinal roundのtoken増ではなく、一runのruntime偏りが大半を占める。正常なfinal dependencyは保持する。
8. 現在のprompt-only設計で閉じられる新しい辺は見つかっていない。数学的下限は未証明だが、保存済みtraceから根拠なくP006を作る段階は終了し、`candidate_not_created`を維持する。
