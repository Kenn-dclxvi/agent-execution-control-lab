# Candidate206 review制御コスト・記述構造分析

> **状態**: `analysis_completed / existing_results_only / no_new_run / candidate206_n20_stopped / review_function_needed / current_expression_not_justified_as_optimal / new_candidate_not_created`

## 結論

review機能そのものは過剰品質ではない。Candidate147はStandard14 N=100を1,400 / 1,400 Score 4で通過した一方、ADR9 r2 N=50では161 / 450 Score 4に留まり、review要否、独立review result形成および変更前admissionを持たないことが反復失敗へ対応していた。Candidate173はreview制御を加え、同じADR9 r2 N=50を446 / 450 Score 4まで改善した。したがって、C147へ何らかのreview制御を加える便益は実測されている。

しかし、C206の現在本文が、C147へreview便益を加えるための適切な制御量・記述方法であるとは立証されていない。root `AGENTS.md`はC147の7,090文字からC206の12,776文字へ5,686文字、80.20%増えた。増加分の85.28%を、一行4,849文字、11個の`:=`定義を持つ`DESIGN_ADMISSION`が占める。

C147はすでに、`SPEC`、`PRODUCER`、`TERMINAL`、`CONTEXT`、`EVIDENCE_GATE`、`OWNER_ROLE`、`ROOT`、`INDEPENDENCE`、`DECISION_BOUNDARY`等へ制御を分けている。各条項は同じ抽象度の排他的責務ではなく、意図的な強化、相互制限、handoffおよび局所強化を持つ制御群である。したがって問題は、review責務が未分割であることでも、これから条項を細分化すべきことでもない。C206が、既存制御群がすでに所有するproducer、packet、evidence、terminal、result effectおよび変更許可を`DESIGN_ADMISSION`内部へもう一つの完結したlifecycleとして記載し、既存制御との接続・優先関係を不明瞭にしたことである。

同じStandard14互換条件のN=5では、reviewerを一件も起動しない70件にもかかわらず、all-agent token中央値はC147の1,447,626に対してC206が1,560,614で7.81%高く、elapsedも6.13%高かった。ケース別token中央値もC206はC147より12 / 14ケースで高かった。この差を長いprompt本文だけの単独因果値にはできないが、review非適用経路へ常時負担が流入していないとは判断できない。C173とC175の値は後段で差分形成過程を診断する補助値にだけ使う。

したがって現在判断は、`review_function_needed / C206_minus_C147_contains_procedural_execution_control / current_C206_expression_not_cost_justified / C206_N20_not_ready`である。中断したC206 N=20を再開せず、C147の正常経路を保持したまま、C147へ追加された境界制御と実行制御を分ける。

## 分析境界

新しい評価run、保存resultの再採点、Candidate本文の変更、releaseまたはprojectionは行っていない。次の固定済み一次証拠だけを用いた。

- C147、C173、C175、C206の固定prompt本文
- C147 Standard14 N=5およびN=100
- C147 ADR9 r2 N=50の訂正済み機序判定
- C173 ADR9 r2 N=50およびStandard14 N=5
- C175 ADR9 r2・Standard14 N=5
- C206 ADR9 r2・Standard14 N=5
- C175とC202の保存済みcounterexample read順再監査
- review制御再構成の反復原因分析

制御本文と費用対効果の比較基準はC147に固定する。C206からC147を引いた差分を、C147へ追加された制御の全件集合として扱う。C173とC175はC206へ至る記載の由来および同じ記載が生んだ保存挙動を確認する診断証拠であり、比較基準、親または目標構造として扱わない。

C147、C173、C175、C206のStandard14 N=5はcompatibility key `cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561`で一致する。このうちC147対C206を主比較とし、C173・C175は差分内のどの段階でcostまたは挙動が現れたかを切り分ける補助値に限定する。N=5の差を安定性または一般的効果へ外挿せず、現在の構造を追試へ進める資格の判断に限定する。

静的prompt量は既存のCandidate191複雑性監査と同じく、UTF-8 decoded文字数、raw byte数、top-level条項数、backtick内の`:=`定義数で測った。現在環境には対象modelの互換tokenizerがないため、prompt本文そのもののtoken数を推定値で補わない。実行コストは保存済みall-agent `total_tokens`だけを使う。

## 第一判定: 境界制御か、実行手順化か

制御量の妥当性を判断する前に、C147以後の追加が何を制御しているかを分類する。

- **境界制御**: 誰が何を生成できるか、どの入力・resultを受け入れるか、permission denial、resultの失効範囲およびartifact変更を開く条件を定める。
- **実行制御**: どの中間表現を作るか、何を先に処理するか、どの順で分類・配送・判定するか、改訂時にどのworkflowを再実行するかを定める。
- **混合記述**: readinessやadmissionの境界と、その成立までの作成・分類・発行手順を同じ文へ置く。

promptから実際のtool発行を制御すること自体を禁止する分類ではない。問題は、必要なpermission、consumer、result effectの境界ではなく、一つの標準workflowを手順として固定しているか、その手順が実行時の発行境界として本当に機能したかである。

### C147に対するC206の追加・変更

C147とC206のroot `AGENTS.md`を直接比較すると、差分は次の四箇所である。

1. `PRODUCER`の明示producer execution条件の精密化
2. `OWNER_ROLE`を同じ明示条件へ接続する変更
3. `DESIGN_ADMISSION`一節の追加
4. `EVIDENCE_GATE`への`admitted_evidence_current`追加

C175は1〜3と同じ記載を持つが、ここではC206とC147の差分として分類する。C147から追加・拡張された文を役割別に読むと次のようになる。番号はC206 root `AGENTS.md`の`DESIGN_ADMISSION`を句点単位に分けた文番号である。

| 追加記載 | 文番号 | 分類 | 判定 |
|---|---:|---|---|
| producer execution identityをowner語列と分け、operation identityへ直接・一意にbindする | `PRODUCER`追加、`OWNER_ROLE`参照 | 境界制御 | C147のproducer境界をreview用に精密化する局所強化 |
| `design_contract_ready`、`general_design_ready`とfalse時の非開始・非変更 | 1〜3 | 混合 | readiness境界は必要だが、全boundary decisionの台帳記録までready条件へ含める |
| general design identityと全boundary decisionを台帳へ固定し、各境界へ7項目を結び付ける | 4、5 | 実行制御 | review要否を判断する前の中間artifactと作成方法を共通手順として要求する |
| 全境界を分類し、0件・1件以上・分類不能を三状態へ写す | 6、7 | 混合 | review適用境界を定める一方、全境界分類という事前処理も要求する |
| permission、review operation identity、専用producer、有限manifestを初回review predicate前に構成する | 8〜11 | 混合 | permission・producer境界に加え、operation仕様の作成時点と必要中間表現を固定する |
| 許可fieldだけからpacketを新規構築し、元sourceを配送しない | 12、13 | 混合 | forbidden input遮断は境界制御。packetの新規構築とsource routingは実行方法まで指定する |
| admission closure不成立なら事前停止、成立時だけoperationを一件作り同一packetを一producerへ配送する | 14〜17 | 混合 | dispatch permissionとcardinalityは境界。operation作成・packet配送・観測担当を一連の手順としても記載する |
| counterexampleの成立・不成立条件 | 19、20 | 境界制御 | admissible judgementの意味境界 |
| reviewerが投影済み情報からcounterexampleを先に判定し、成立時はterminal、不成立時だけmissingまたは全successを判定する | 21、22 | 実行制御として記載されたdependency | result kindごとの必要evidence集合ではなく、reviewerが行う判定順として表現する |
| sender、packet、receipt、result kind別certificateを照合して受け入れる | 23、24 | 境界制御 | result admissionとroot補完禁止 |
| admissible result後だけ変更を許可する | 25 | 境界制御 | review resultから既存`implementation_bound`へのchange permission境界 |
| 改訂時は新design identityで台帳とreview要否を再判定する | 26 | 実行制御 | revision lifecycleと再実行手順を固定する |

強く実行手順へ寄っているのは、少なくとも次の四群である。

1. **中間artifact作成手順**: 境界台帳を作り、全境界へ固定fieldを結び付ける。
2. **全域分類手順**: review前に全boundaryを分類して三状態へ写す。
3. **dispatch手順**: operation identity、manifest、packetを作り、一producerへ配送する。
4. **judgement手順**: counterexampleを先に判定し、その後にmissingまたは全successを判定する。

このうち4は、必要な境界を手順で表したことによる具体的な不一致がある。C206に含まれる同一記載を先に使ったC175の保存済みcounterexample対象20件では、7件が投影済み情報だけでcounterexampleが成立する前にpaired-scope readを発行した。これはC175を比較基準にするものではなく、C147からC206へ追加された同一文が実際にどう解釈されたかを示す診断証拠である。最終resultは正しくても、文章上の処理順はrepository invocationの発行資格にならなかった。

必要だった境界は次である。

```text
review_direct_read_consumer_ready(entry) :=
  projected counterexample certificateが未成立
  ∧ entryのresultが現在未解決のjudgement result kindを変え得る
```

これは「最初に判定してから読む」というworkflowではなく、counterexample certificateが成立済みならdirect readにconsumerがなく、発行資格を持たないという境界である。C175/C206はこの形へなっていない。

### C147に対して追加された`admitted_evidence_current`

`admitted_evidence_current`は二つの性質を持つ。

- model-visible inputまたはadmission済みterminal resultだけをcurrentへ入れ、値を変えるresultで失効する部分はevidence availabilityの境界制御である。
- currentな同一identityを取得するrepository invocationを発行しない部分は、read回数へ直接作用する実行制御である。

この実行制御が同一記載を持つcarrier上でroot instruction本文再取得を7件から0件へ変えたため、挙動への作用は確認できた。一方、主比較であるC147対C206では、C147のStandard14保存event 1,385件中root本文再取得130件に対し、C206 N=5は0 / 70だったが、all-agent token中央値はC206がC147より7.81%高く、elapsedも6.13%高かった。C147とC206でreview制御一式も同時に異なるため、再取得差の単独因果値にはできず、共通promptへ常時置く実行制御としての費用対効果も通過していない。

### 第一判定の結論

C147に対するC206の追加は、境界制御だけではない。必要なreview permission、producer、forbidden input、result admissionおよびchange permissionの境界に加え、設計台帳、全域分類、operation準備、packet配送、judgement順序、revision loopおよび同一evidence再取得禁止を実行制御として含む。

したがって、制御tokenの妥当性を判断する前に次を分ける必要がある。

1. ADR9の結果を成立させるために必要だった境界制御。
2. その境界を実装する一方法として書かれた中間artifact・分類・順序。
3. 保存traceで実際の発行を変えた実行制御。
4. 手順として書かれたが、意図した発行境界にならなかった記載。

現時点では、C147からC206へ増えた5,686文字、特に`DESIGN_ADMISSION`の4,849文字をreview境界の必要costとして一括正当化できない。

## 静的制御量

| prompt | 文字数 | UTF-8 bytes | top-level条項 | `:=`定義 | C147比文字数 |
|---|---:|---:|---:|---:|---:|
| C147 | 7,090 | 10,772 | 13 | 9 | 基準 |
| C173 | 10,163 | 15,853 | 14 | 14 | +3,073（+43.34%） |
| C175 | 12,244 | 18,608 | 14 | 21 | +5,154（+72.69%） |
| C206 | 12,776 | 19,382 | 14 | 22 | +5,686（+80.20%） |

C147からC206までの主要な増加は次の三群である。

| 増加群 | C206本文量 | C147から加わった責務 | 現在の証拠状態 |
|---|---:|---|---|
| producer明示条件 | `PRODUCER` 579文字、`OWNER_ROLE` 704文字 | owner語列とproducer execution指定を分け、operation identityへの直接・一意bindingを要求 | Standard14の不要producer抑止に必要。ただしC147にも禁止条件があり、C175は肯定条件を局所強化したもの |
| `DESIGN_ADMISSION` | 4,849文字、11定義 | review適用からartifact変更許可まで | review機能の中心だが、複数責務を一labelへ圧縮し、C206全体の37.95%、C147比増分の85.28%を占める |
| `admitted_evidence_current` | `EVIDENCE_GATE`へ532文字、1定義追加 | 取得済みevidenceを失効まで再利用 | root本文再取得を0件へ減らす機序は成立。支配的KPI改善は不成立 |

条項が13から14へ一つしか増えていないことは単純さを意味しない。`DESIGN_ADMISSION`内部の定義数と責務数が増え、top-level構造へ現れない複雑性になっている。

## Standard14へ流入した常時負担

### 集約中央値

C147対C206を主比較とする。C173とC175は、C147からC206までの記載形成過程のどこでcostが現れたかを見る診断列である。

| prompt | quality中央値 | all-agent token中央値 | C147比 | elapsed中央値 | C147比 | reviewer起動 |
|---|---:|---:|---:|---:|---:|---:|
| C147 | 100 | 1,447,626 | 基準 | 852.543秒 | 基準 | Standard14の正常root経路 |
| C173 | 100 | 1,593,673 | +146,047（+10.09%） | 859.790秒 | +7.247秒（+0.85%） | 0 / 70 |
| C175 | 100 | 1,692,063 | +244,437（+16.89%） | 804.940秒 | -47.603秒（-5.58%） | 0 / 70 |
| C206 | 100 | 1,560,614 | +112,988（+7.81%） | 904.776秒 | +52.233秒（+6.13%） | 0 / 70 |

reviewer起動0件でもtoken差が残るため、review制御のcostを「reviewerを起動した時だけ支払うcost」とは扱えない。少なくとも、review非適用の判定、長い共通instructionの再投入、またはそれに伴う実行routeの差が通常経路へ流入している。

C175とC206の直接比較ではC206のtoken中央値が131,449、7.77%低い一方、elapsedは99.836秒、12.40%高い。`admitted_evidence_current`がroot instruction本文再取得を7件から0件へ減らした機序は成立したが、これをreview制御全体のcost正当化には使えない。むしろ再取得抑止後のC206でもC147比tokenが7.81%高いため、review carrierの常時負担が残る。

### ケース別分布

C147とC206のcase別token中央値では、C206が低いのはF06とF08の2ケースだけだった。A01を含む残り12ケースはC147より高い。

| 代表ケース | C147 | C206 | 差 |
|---|---:|---:|---:|
| A01 clarification | 19,195 | 19,475 | +1.5% |
| A02 repository routing | 129,085 | 171,074 | +32.5% |
| F02 cross-layer | 128,236 | 162,914 | +27.0% |
| F03 cleanup | 104,320 | 137,555 | +31.9% |
| F04 audit | 151,170 | 200,743 | +32.8% |
| F10 inventory | 87,934 | 110,938 | +26.2% |
| F10 monthly | 93,096 | 97,221 | +4.4% |
| F06 snapshot | 151,542 | 106,166 | -29.9% |
| F08 CLI sync | 113,067 | 106,373 | -5.9% |

14ケースのcase中央値合計はC147の1,349,243に対しC175が1,635,826、C206が1,536,637で、C206はC147比13.89%高い。この合計は正式なiteration集約KPIではなく、増加が一部caseだけに閉じていないことを確認する診断値である。

## ADR9で得られた便益と未閉鎖部分

### review機能自体は必要

C147 ADR9 r2 N=50は161 / 450 Score 4だった。review要否と独立review result形成を持たないため、不要review、required review未起動、過剰`unavailable`が反復した。

C173は`DESIGN_ADMISSION`系のreview制御を追加し、ADR9 r2 N=50を446 / 450 Score 4まで改善した。ADR01〜04、ADR08、ADR09は各50 / 50を通過した。この差は、変更前review機能全体を「Standard14で使わないから不要」と扱えない直接証拠である。

### C175/C206本文の完全性は未証明

C173 N=50には次の4件が残った。

- ADR05 2件: 成立済み反例より無関係manifest missingを優先
- ADR06 1件: 禁止canaryをreviewerへ配送
- ADR07 1件: 有効なreview resultを汚染扱いして`unavailable`

C175はreview operation仕様、専用producer、semantic projectionを追加しN=5を45 / 45で通過した。ただし、C173の低頻度失敗のうち、operation仕様とprojectionへ直接対応する部分を改善した証拠であり、反例certificateと無関係missingのdependencyをN>5で閉じた証拠ではない。C206もC175のreview制御を変更せずN=5だけを通過したため、この不足を閉じていない。

後続の保存trace再判定では、投影済み情報だけでcounterexampleが成立する20件のうち、C175は7件でpaired-scope readを先に発行した。最終resultは正しくても、「counterexampleを先に判定する」という意味上の順序がrepository invocationの発行資格になっていなかった。C206の`admitted_evidence_current`はroot instruction再取得を扱う関係であり、このreview内の発行順序を変更しない。

## 責務別の費用対効果

| review責務 | 得られた結果 | 現在判断 |
|---|---|---|
| review適用・非適用 | C147のADR9失敗を大幅に改善し、ADR01・02の不要reviewとADR08 permission否定を閉じた | 必要 |
| permission-before-dispatch | ADR08でreviewer 0、変更0を成立 | 必要 |
| owner metadataとproducer指定の分離 | Standard14で不要reviewer 0。後続C190で削除した際に8件退行 | 独立境界として必要 |
| review operation identityと専用producer | required reviewのproducer routeを成立 | 必要。ただし一般`PRODUCER`との重なり方を整理する |
| allow-list packet projection | C173 ADR06のcanary配送反例へ対応し、C175 N=5では0件 | 必要性は支持。低頻度安定性は未確認 |
| counterexample / no-counterexample / unavailable | ADR9の三つの成果を区別する | 必要 |
| counterexample certificate dependency | C173 N=50 ADR05、C175保存traceの先読みが残る | 現在表現では未閉鎖 |
| result admissionとartifact変更許可 | unsafe changeを止める | 必要。新ownerへ移さず、`TERMINAL`、`EVIDENCE_GATE`、`ROOT`が持つ既存境界のどこをreview固有条件が強化するかを固定する |
| `admitted_evidence_current` | root本文再取得を0件へ減らした | 機序知見は保持。一律追加はKPI非優位 |

必要なreview条件が複数あることと、それらを既存制御群から独立した一つの巨大lifecycleとして再記述する必要があることは同義ではない。また、文字数を減らすためにC147の既存制御群を統合・削除することもできない。Candidate190で`OWNER_ROLE`を統合後削除した結果、Standard14の8件でowner metadataが不要review operationへ昇格した反例がある。

## 記述構造の評価

### 現在のまとまりが持つ意味

`DESIGN_ADMISSION`というまとまり自体には、「一般設計のartifact変更を開く前に、一つのprechange review operationを閉じる」という意味がある。このまとまりを無条件に解体するのは適切でない。review非適用、permission否定、review実行、result受入および変更許可は、同じ外側operationの成果へ接続している。

問題は、reviewという外側のまとまりではない。C147で既に分かれている制御群を利用・局所強化するのではなく、まとまりの内部へ同じ境界を一つの長い論理列として再実装した記述方法である。

### 現在方針との不一致

1. **既存の細分化を接続に使っていない**
   C147にはproducer、packet、evidence、terminal、result effectの制御群が既にある。`DESIGN_ADMISSION`はそれらへreview固有predicateを渡す形ではなく、適用からchange effectまでを内部で再度閉じている。
2. **意図的重複と二重ownerの境界が示されない**
   C147にも条項間の重複はあり、それ自体は防御的強化、相互制限、handoffまたは局所強化として意味を持つ。C175/C206では、producer、packet、evidence、terminal、発行効果の再記述がどの種類の重複で、既存条項と`DESIGN_ADMISSION`のどちらが実際のtool発行・result受入を決めるかが固定されていない。
3. **文章順序がdependencyの代用になっている**
   「先に判定」「成立すれば後続を失効」と書いても、C175の7 / 20ではdirect readを先に発行できた。意味上の優先順位とtool発行資格が別だからである。
4. **完全性条件が異なるresult kindへ流入しやすい**
   `counterexample_found`は一つのwitnessで閉じる一方、`no_counterexample_found`だけが固定scope全件のsuccessを必要とする。一条項内のmanifest完全性が両方へ流入すると、C173 ADR05型の誤`unavailable`を生む。
5. **非review経路にも読解負担がある**
   Standard14でreviewer 0件でも全runが同じ4,849文字の条項を受け取る。適用しないことを判断するための最小条件と、適用後だけ必要な詳細が分離されていない。

### 既存制御群への接続が分析対象である

次に行うのは新しい細分化ではない。C147の既存制御群とその意図的重複を維持し、review固有の不足だけをどこへ接続するかを決めることである。

- review適用条件は、外側review operationを作るかだけを決める。
- producerの一意性とowner metadata非権限化は、既存`PRODUCER / OWNER_ROLE`を使い、review固有の明示条件だけを局所強化する。
- packet membershipとforbidden inputは、既存`CONTEXT / ROOT`へsemantic projection条件を接続する。
- observationの取得資格と失効は、既存`EVIDENCE_GATE`へreview result-kindごとのconsumerを接続する。
- terminal resultの欠落・root補完禁止は、既存`TERMINAL / ROOT`を使う。
- 先行resultがread発行を待たせるかは、既存`DECISION_BOUNDARY`のresult effectで決め、review operationの文中順序で決めない。
- artifact変更許可は、既存`implementation_bound`へadmissible review resultを追加dependencyとして渡す。
- `counterexample_found`、`no_counterexample_found`、`unavailable`は必要evidence集合が異なるため、review固有のjudgement certificateとして分ける。

Candidate191の退行は「条項を細分化したから起きた」とは扱わない。C191は外側admission、観測、変更を別operation identityへ置いた際、C147の`DECISION_BOUNDARY`が持つ相互非依存invocationの正の共同発行を、各operationの逐次開始より優先できなかった。これは既存の細分化が不適切だった証拠ではなく、再構成時に既存制御群の優先関係と正の発行closureを保持しなかった証拠である。

## 現在判断と再開条件

### 現在判断

- review機能の必要性: `supported`
- C147比のC206追加記述量の妥当性: `not_demonstrated`
- C147比のC206追加記述: `contains_procedural_execution_control`
- C206固有`admitted_evidence_current`: `mechanism_supported / optimization_failed`
- C206 N=20: `stopped / not_ready_to_resume`
- 新Candidate: `not_created`
- adoption / release / projection: `not_authorized / not_created / not_projected`

中断前に完了したC206 ADR9の3 atomic runは集約・登録・品質判定へ使用しない。Standard14 N=20は未発行である。

### 次に必要な分析

1. C147からC206へ追加・変更された全文を`境界制御 / 実行制御 / 混合記述`へ分類する。
2. 実行制御ごとに、消した保存済み誤経路、実際に変えた発行routeおよび非対象経路への常時costを対応づける。
3. 手順として書かれたが実行境界にならなかった記載を、permission、consumer、result effect、result admissionまたはinvalidationの境界へ変換できるか判定する。
4. C147の正常な非review経路を固定し、review非適用時に追加する判断を一つに限定する。
5. ADR9の各失敗を、C147のどの既存制御群と、追加が必要なreview固有predicateの組が消費するか一対一に対応づける。
6. C206とC147の差分各文を`既存C147制御で成立済み / 既存制御のreview局所強化 / review固有の新境界 / 根拠のある実行制御 / 結果根拠なし`へ分類する。
7. 同じ外側review operationを保ちながら、既存制御群間のhandoffと優先関係を維持し、追加dependencyを文章順ではなくresult effectで表す構造を作る。
8. 保存済みC147正常trace、C173低頻度失敗、C175成立trace・先読みtraceへ新構造を当て、追加run前に反証する。
9. 構造が閉じた場合だけ、C147直接基盤の新identityとしてADR9 N=5を先に評価する。通過後も低頻度riskを持つcaseだけをN=20へ延長し、その後にStandard14全14ケースを実施する。

C206をそのままN=20へ伸ばすことは、現在の記述構造を固定したまま標本数だけを増やすため、この再開条件を満たさない。

## 一次証拠

- [C147 Standard14 N=5](../evaluations/results/candidate125-candidate145-candidate147-result-effect-scope-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-08-02.md)
- [C147 Standard14 N=100](../evaluations/results/candidate147-result-effect-scope-v14-medium-standard14-atomic-reuse-n100-cli0146_2026-08-02.md)
- [C173 ADR9 r2 N=50](../evaluations/results/candidate173-concrete-counterexample-adjudication-adr9-r2-n50_2026-08-10.md)
- [C173 Standard14 N=5](../evaluations/results/candidate173-concrete-counterexample-adjudication-v14-medium-standard14-atomic-n5-cli0146_2026-08-10.md)
- [C175 ADR9・Standard14 N=5](../evaluations/results/candidate175-review-operation-admission-closure-adr9-standard14-n5_2026-08-10.md)
- [C206 ADR9・Standard14 N=5](../evaluations/results/candidate206-admitted-evidence-current-adr9-standard14-n5_2026-08-13.md)
- [C206機序監査](../evaluations/results/candidate206-admitted-evidence-current-mechanism-audit-r1.json)
- [C202 M5原因分析](candidate202-m5-causal-analysis.md)
- [review制御再構成原因分析](review-control-reconstruction-causal-analysis.md)
- [prompt制御設計原則](prompt-control-design-principles.md)
