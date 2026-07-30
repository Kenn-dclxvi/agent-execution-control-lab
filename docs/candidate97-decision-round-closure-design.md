# Candidate97 decision round closure設計

## 結論

Candidate97はCandidate81を直接親とし、`DECISION_BOUNDARY`一規則だけを置換する。単一operationで既知のinspectionとcompletion invocationをresultごとに追加せず、発行前に必要十分なwaveへbindする。

TaskSpec、repository authority、required validation、評価条件、executor、success stdout配送は変更しない。reasoning tokenまたはcommand数の上限も設けない。

## Identityと状態

- candidate number: Candidate97
- prompt identity: `the-caption-3ce91a4-decision-round-closure-r1`
- direct parent: `the-caption-3ce91a4-validation-wrapper-precedence-r1`
- changed target: root `AGENTS.md`
- changed rule: `DECISION_BOUNDARY`
- evaluation status: `not_evaluated`
- release: `not_created`
- runtime projection: `not_projected`

## 作成前gate

1. 基準prompt setはCandidate81、bundle SHA-256 `919e2d4c53a487efde9d87ab182ea9b576c082c29ac81eb46fb7a442fb837220`とする。
2. 基準状態の最短正常経路は、既知のidentity、authority、source、test readを一つのinspection waveから発行し、変更判断を一度行い、既知のdiff、status、required validationをcompletion closureから発行してterminalを判断する経路とする。
3. 保存済みC81 Standard14 B20のF02 100 runは全件score `4`だったが、`runner_elapsed_seconds`は`76.474`秒から`139.676`秒まで分布した。elapsed下位25件と上位25件では、command output bytesの中央値がほぼ同じなのに、output tokenは`3,008`対`3,991`、reasoning tokenは`636`対`1,118`だった。
4. C81の現行`DECISION_BOUNDARY`は既知の相互非依存invocationを同一model stepへ束縛する。ただしwaveへ含めるinvocation集合の閉包条件と、追加readを許すevidence gapを固定しない。このため、同じTaskSpecとrepository authorityでもread resultごとに別readを追加するrouteが残る。
5. 変更predicateは、現在phaseで既知のinvocation集合を閉じ、追加invocationへ明示的な根拠を要求する`DECISION_BOUNDARY`一つとする。
6. 消す判断点は、既知readの各result後に次readの要否を再判断する点、completion evidenceをvalidation後に追加する点、terminal resultがある同一invocationを理由なく再発行する点である。
7. 新たに増える判断点は、受領resultが未発行invocationの`target / permission / method / stop condition`を変えたか、bind済みpredicateに必要な未取得evidenceを特定したか、という一分岐である。
8. 品質確認はF02 r1、Rating v14、Medium、CLI `0.146.0`、candidate-only `N=5`とする。
9. 5 / 5 score `4`、required command evidence 5 / 5、full gate一回 5 / 5、理由なし追加read 0 / 5、final required validation後の追加read 0 / 5を要求する。一つでも満たさなければmechanism gate不通過として停止する。

## 保存traceから固定した観測

C81 F02 100 runでは次を観測した。

- agent message 5件以下: 9 run、elapsed中央値`88.312`秒、8 / 9がelapsed下位25%
- agent message 6件: 76 run、elapsed中央値`99.723`秒
- agent message 7件以上: 15 run、elapsed中央値`109.360`秒、elapsed下位25%は0 / 15
- full gate 1回: 95 run、elapsed中央値`99.417`秒
- full gate 2回: 5 run、elapsed中央値`126.322`秒
- read command 4件以下: 29 run、elapsed中央値`95.782`秒
- read command 8件以上: 15 run、elapsed中央値`104.321`秒

input / output / reasoning tokenによるdiagnostic modelはelapsed分散の`65.6%`を説明した。OS負荷、dispatch順、平均同時実行数だけのmodelは`2.4%`だった。したがって、Mを下げるのではなくmodel decision roundを閉じる。

## Prompt変更

Candidate81の`DECISION_BOUNDARY`を次の意味へ置換する。

- operation開始前とartifact変更完了時に、その時点で既知のinvocationを次waveへ完全にbindする。
- 先行resultがtarget、permission、method、stop conditionを変えない相互非依存invocationは、同一model stepから個別発行する。
- inspectionでは既知のidentity、authority、source、test readをresultごとに追加しない。
- completionでは既知のdiff、status、required validationをresultごとに追加しない。validationのorderとfail-stopは`VALIDATION_CLOSURE`へ従う。
- wave後の追加invocationは、4値の変更またはbind済みpredicateに必要な未取得evidenceを特定できる場合だけ、その理由を先にbindして許可する。
- terminal resultがbind済みの同一invocationは、TaskSpec追加要求、result失効、または`RECOVERY`なしに再発行しない。

## 非目標

- TaskSpecまたはrepository authorityの変更
- required validationのidentity、command、order、pass / stop conditionの変更
- stdout / stderrのprojectionまたはexecutor adapter変更
- command数、output token、reasoning tokenの直接上限
- shell compound commandへの統合
- 評価済み、採用済み、release済み、本体反映済みという主張

## 評価順序

1. bundle構造、C81からの一規則差分、profile互換条件を検証する。
2. Candidate97だけをF02 r1 `N=5`、`M=5`で実行する。
3. qualityとmechanism gateを保存traceで判定する。
4. gate通過時だけ、保存済みC81 resultとのKPI比較を行う。
5. Standard14 B20が必要な場合、保存済みC81 B20を再利用し、不足するCandidate97側だけを最大24並列で実行する。

## r1停止記録

F02 N=5のexecution開始後、resultが一件もterminalになる前に停止した。理由は、置換した`DECISION_BOUNDARY`が設計目的に対して長く、追加した列挙自体がmodel decision量を増やす可能性が高いと判断したためである。result registryへの登録は0件であり、r1を評価結果または品質証拠として扱わない。本文をin-placeで短縮せず、短いr2を別bundleとして作成する。
