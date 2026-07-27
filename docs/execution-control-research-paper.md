# 実行制御としてのprompt設計

## 成果品質を保ったままall-agent tokenを削減する制御メカニズムの実測、および2026年7月のベンダ公式指針との対照

> [!IMPORTANT]
> **位置付け**: この文書は本リポジトリの研究成果を一つの論文形式へまとめた**総説**である。いずれの契約・原則・状態についても正本ではない。数値・件数・status・identityの正本は各節に示す一次artifactとし、この文書は参照と解釈だけを担う。研究状態の記述は**2026-07-26時点**、外部指針の引用は2026-07-25に取得した公開文書に基づく。

---

## 要旨

AIエージェントに与えるprompt（指示書）の設計は、慣習的に「文面の良し悪し」として扱われてきた。本研究は、promptを**実行制御**、すなわちモデルの実行経路上の判断点を規定する不変条件の集合として定義し直し、その変更が成果品質・token消費・所要時間・実行経路へ与える影響を、固定した互換条件のもとで反復測定した。

対象は実在のコードベースTHE-CAPTION（commit `3ce91a4`）であり、baseline 2件から81番までのcandidate（bundle 79件）を派生させ、20 case、11 evaluation set、13 revisionのrating contract、145件の公開評価result文書（READMEを除く）を蓄積した。加えて公開target `pallets/click`で14 case・17 revision、18 set、10 revisionのrating contract、5件の公開result文書を作成し、Layer 4 resultを20件・計131 run登録した。modelとAgentは`gpt-5.6-sol` / Codex CLIに固定し、主要測定はreasoning effort `high`、追試は`low` / `medium` / `xhigh` / `max` / `ultra`を加えた6水準で実施した。

主要な結果は次の3点である。

1. **精緻に書かれたbaseline promptは、実行時tokenの約4倍の超過を生んでいた。** root指示書を0 byteにした対照条件（ControlFreeRepository）は、baselineに対しall-agent token中央値`-74.06%`（`10,826,033 → 2,808,523`）を記録し、品質中央値は同値だった。指示書を書くこと自体が、成果に寄与しない実行経路を誘発していた。

2. **削減対象はprompt文字数ではなく、実行経路上の判断点である。** root promptを`-1.43%`から`-39.12%`まで縮約した8件のcandidateは、実行時tokenを`-2.33%`から`+31.36%`へ動かし、多数が**増加**した。一方、root promptへ**1 labelを追加**した3件（C41・C69・C71）はいずれもtokenを`26%`〜`30%`削減した。C43からC71では、root promptを`3,980 → 4,987 bytes`（`+25.30%`）へ**増やしながら**、2段の測定でtokenを各`-26.21%` / `-26.14%`削減している。

3. **効率改善の効果量は制御の種類で桁が異なり、その順位は「処理量そのものを減らすか」で決まる。** 最大は不要なworker起動の抑制、次にmodel再入と検証の一括化、次にread経路の事前確定、最小はprompt表面の圧縮（有意差なし）だった。

追試では、Rating v13・標準14項目・各`N=5`へBaseline、ControlFreeRepository、C5、C35、C43、C71を揃え、reasoning `high`と`medium`で各420 runを登録した。C71の6水準比較では、`medium`がtoken中央値最小、`low`がelapsed中央値最小で、`xhigh`以上は`high`よりtokenとelapsedがともに増えた。reasoningを`medium`へ下げてもC71とC43のtoken中央値差は`-29.19%`であり、制御差は消えなかった。

repository汎用化の追試では、公開target `pallets/click`にcontrol-free Bundle AとC81全文のBundle Bを固定し、14 caseのStd14を各`N=5`で実行した。両条件とも70 / 70件がscore `4`で、Bundle BはBundle A比でall-agent token中央値`-23.96%`、elapsed中央値`+2.86%`だった。trace診断ではmodel stepが`-32.27%`、shell commandが`+12.15%`で、input token削減量の`97.98%`をcached inputが占めた。すなわちtoken削減はcommand削減ではなくmodel再入とcontext再計上の削減に整合した。一方、確認系のelapsed `-283.485`秒を実装系の`+324.899`秒が相殺し、安定した時間短縮は実証できなかった。これは公開target上でC81全文のtoken削減方向を再現した結果であり、個別predicateの因果効果や採用を示さない。

これらは、2026年7月に公開されたOpenAI GPT-5.6 Sol指針（lean system promptがelaborate scaffoldingを上回る、outcome-first、停止条件の明示）およびAnthropic Claude Opus 5指針（検証指示を削除せよ、subagent起動を抑制せよ、既に行う再確認を指示するな）と**同方向の独立観測**である。同時に本研究は、両指針が「lean」「trim」「remove」という語で混在させている**byte削減と判断点削減の区別**を、実測で分離する。両指針は減らす方向を示すが、減らし切った下限（0 byte条件）の測定と、削除では閉じない残余品質欠陥の存在を示していない。本研究では、最良のcandidateは0 byte条件を効率で上回るのではなく、**0 byte条件の効率を維持したまま残余欠陥1件を閉じる**ことで得られた。

重要な限界として、本研究のmodelは`gpt-5.6-sol`、AgentはCodex CLIの単一条件であり、Claude Opus 5上での再測定は0件である。reasoning effortは6水準へ広げたが、Opus 5指針との一致は同方向の独立観測にとどまり、別model / 別CLIでの再現は未確認である。

---

## 1. 背景と問題設定

### 1.1 対象

THE-CAPTIONは別リポジトリで運用される本体システムであり、その実行はroot `AGENTS.md`とpath別のrepository instructionによって制御される。本リポジトリはそのpromptを設計・比較・評価し、反映可能な単位へ固定する専用の実験基盤である。本体のruntime変更は通常作業範囲に含めず、本体への反映は明示的な別作業として扱う（正本: [`repository-contract.md`](repository-contract.md)）。

### 1.2 問題

promptの改善は通常、出力文の読みやすさや網羅性で評価される。しかしエージェント実行では、指示書の1文がモデルの分岐を1つ増減させ、下位セッションの起動を1体増減させる。下位セッション1体の使用量は総量へ丸ごと加算されるため、影響は非線形に伝播する。

したがって次の3つは別の量である。

- prompt自体の文字数・token数（静的量）
- 実行時に消費されるtoken総量（動的量）
- 成果品質

本研究の問いは、**成果品質を維持したまま動的量を減らす制御は何か、そしてそれは静的量の削減と一致するか**である。

### 1.3 貢献

1. 実在コードベース上で、prompt差分だけを変数とした互換比較の基盤を構築した。
2. 効いた制御と効かなかった制御を、同一条件の反復測定として両方保存した（負の結果を破棄していない）。
3. 静的量と動的量の乖離を、方向が逆転する事例として定量化した。
4. 採点契約そのものの妥当性欠陥を検出・修正し、その影響範囲を記録した。
5. 上記を2026年7月のベンダ公式指針と対照し、一致点・追加点・未検証点を分離した。

---

## 2. 方法

### 2.1 用語

| 用語 | 定義 |
| --- | --- |
| prompt set / bundle | エージェントへ渡す指示書一式を1単位へ固定したもの |
| baseline | 比較起点となる現行promptの固定スナップショット |
| candidate | baselineから派生させた候補。`C1`〜`C81` |
| label / predicate | 1つのlabel（見出し付き制御単位）が1つのpredicate（条件付き振る舞いの判定文）を持つ |
| worker（SA session） | モデルが作業を分担するために起動する下位セッション |
| all-agent `total_tokens` | root agentと全descendant workerの最終usageの合算値 |
| model step | モデルが立ち止まって次の行動を決める単位 |
| case | 症状・対象・成功条件を定めた評価課題。`TC-F01`〜`TC-A06`ほか |

### 2.2 評価基盤（evaluation foundation v3）

評価は4つのLayerに限定し、各Layerは自分の出力だけを作り、前段のartifactを変更しない。

1. **Evaluation set** — どのcaseで測るかを固定する
2. **Execution** — 固定条件でpromptを実行し一次結果を保存する
3. **Quality rating** — case成果を0〜4で採点する
4. **KPI comparison** — 保存済み結果から比較viewを作る

扱うKPIは3つだけである。`quality_score`、all-agent `total_tokens`、`elapsed_seconds`。tool call、model step、worker routing、context継承、command内訳はdiagnosticとして確認し、KPIへ昇格させない（正本: [`prompt-comparison-workflow.md`](prompt-comparison-workflow.md)、[`evaluation-loop-manual.md`](evaluation-loop-manual.md)）。

### 2.3 互換条件（compatibility key）

2つの結果を比較してよいのは、評価集合revision、対象repository ref、model、Agent環境、TaskSpec、permission、fixture、executor parameter、case、反復条件、token accounting revision、採点契約が**すべて一致する**ときだけである。この一致を単一のハッシュで表し、異なるkeyのresultを同一比較へ混ぜない。

この規律には本論文にとって重要な帰結がある。**採点契約が異なる測定は連結できない。** 後述するC43→C69（v10）とC69→C71（v12）は隣接する2段の測定だが、契約revisionが異なるため単一の比較値へ乗算できない。

### 2.4 model-visible / private境界

caseは、実行役へ提示する情報（model-visible）と、採点用の正解・期待diff・oracleが参照する確認コマンド（private）を厳密に分離する。**privateに確認コマンドが存在することと、それが実行役へ課された必須試験であることは別である。** 必須試験はTaskSpecまたは適用されるrepository規則が要求するものに限られる。この区別の破れが実際に測定を歪めた事例を第4節で扱う。

### 2.5 基盤が出力しないもの

評価基盤は`winner`、改善・悪化の断定、KPIの優先順位、採用可否、release判断、projection判断を出力しない。数値を並べるだけであり、採否は人が別に判断する。この分離は本論文の解釈全体に及ぶ。

### 2.6 実測した基盤規模（2026-07-26時点）

| 項目 | 件数 |
| --- | ---: |
| baseline bundle | 2 |
| candidate bundle | 79（設計上はC81まで） |
| release bundle | 4 |
| 評価case | THE-CAPTION 20、`click` 14 case・17 revision |
| 評価集合 | THE-CAPTION 11、`click` 18 |
| evaluation profile | THE-CAPTION 167、`click` 20（JSON file数） |
| rating contract revision | THE-CAPTION 13（v1〜v13）、`click` 10（v1〜v10） |
| 公開評価result文書 | THE-CAPTION 145、`click` 5（各READMEを除く） |
| 評価基盤のtest | 76ファイル |

### 2.7 実行条件

modelとAgentは全評価resultで単一であり、reasoning effortだけを追試で変数化した。

- model: `gpt-5.6-sol`。**他のmodel名を明示したresultは0件であり、Claude系modelでの測定は存在しない。**
- reasoning: 主要測定は`high`。2026-07-26の追試でC71を`low` / `medium` / `high` / `xhigh` / `max` / `ultra`の6水準へ広げ、6条件の互換比較を`medium`でも取得した。
- Agent: Codex CLI、memories disabled、permission `workspace-write`、approval `never`
- 対象repository: THE-CAPTION commit `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- 反復: caseごと`N=5`を基本、継続試験は`N=5 × 18 Batch`（条件あたり1,260 run）

---

## 3. 結果

### 3.1 主対照実験: 精緻なpromptの実測costと0 byte対照

同一のevaluation set、target、model、Agent、TaskSpec、permission、fixture、executor parameter、採点契約（v9）、反復条件（expanded 12 case、各`N=5`、global queue `M=24`）に固定し、**prompt identityだけを変えた**4条件を各60 run実行した。

| prompt set | root `AGENTS.md` | score 4 / 3 | `quality_score`中央値 | all-agent token中央値 | token合計 | `elapsed_seconds`中央値 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline | 5,980 bytes | 58 / 2 | 100.000 | 10,826,033 | 60,750,594 | 3,705.409 |
| ControlFreeRepository | **0 bytes** | 59 / 1 | 100.000 | 2,808,523 | 14,877,979 | 1,135.178 |
| Candidate35 | root-control-only | 60 / 0 | 100.000 | 4,565,773 | 22,035,738 | 1,841.107 |
| Candidate41 | 3,482 bytes | **60 / 0** | 100.000 | **2,861,019** | 14,688,469 | **1,172.182** |

正本: [`Baseline / ControlFreeRepository / C35 / C41 comparison`](../evaluations/results/baseline-control-free-repository-c35-c41-outcome-quality-owner-diagnostic-v9-expanded12-n5_2026-07-19.md)。root byte数は各bundleの`files/AGENTS.md.txt`の実測値。bundleはいずれも19 targetを持つ（各`manifest.json`）。

この表から3つの事実が読める。

**(a) baselineの超過は約4倍だった。** BaselineのtokenはC41比で`+278.40%`、`elapsed`は`+216.11%`である。品質中央値は4条件すべて同値であり、score分布はbaselineが最も悪い（58 / 2）。すなわちbaselineの追加記述は、品質を買っていなかった。

**(b) root指示書を0 byteにしただけで、baseline比token中央値`-74.06%`。** ControlFreeRepositoryはroot `AGENTS.md`を空にし、path別のrepository instructionだけを残した条件である。それでも実行はTaskSpec、path-scoped repository authority、repository state（source、test、diff）の三層から制御されるため、成果は成立する。score分布は`59 / 1`で、baselineの`58 / 2`より良い。

**(c) 最良candidateは0 byte条件を効率で上回っていない。** C41のtoken中央値はControlFreeRepositoryより`+1.83%`大きく（60 run合計では`-1.29%`小さい）、`elapsed`中央値は`+3.16%`大きい。C41の達成は効率の上積みではなく、**0 byte条件の効率水準を保ったまま、残っていた品質欠陥1件（F10 monthly reviewのfinding location mismatch、`1 / 60`）を`0 / 60`へ閉じたこと**である。

(c)は本論文で繰り返し戻る論点である。「promptを減らせ」という指針の最適点は0ではない。0の近傍には、削除では閉じない低頻度の品質欠陥が残る。C41はそこへ1つのpredicateだけを足した。

なお`N=5`の`1 / 60`対`0 / 60`から低頻度誤経路の解消を一般化しない。これは一次result自身が明示する留保である。

### 3.2 効いた制御: 4つのメカニズム

効果量の大きい順に整理する。因果の詳細は[`control-mechanisms.md`](control-mechanisms.md)を正本とする。

#### メカニズム1: 不要なworker起動そのものを抑える（削減幅最大）

all-agent総量はworker 1体のusageを丸ごと加算する。root agentだけで完結できる作業でworkerを起動する経路を消すと、総量が最も大きく下がる。

C41は「criterion ownerを指す語列が現れただけではworkerを起動せず、TaskSpecが独立したproducer executionを明示的に指定した場合にのみ委譲する」というpredicateへ整理した。結果、worker spawnはほぼ0になり、C35比でtoken合計は`50.02%`少なく、12 caseすべてで`5 / 5`がscore `4`だった。expanded 12 caseではbaseline比all-agent中央値で最大`-4,335,047`（C15時点）を記録している。

**品質を保ったままtokenを削減できたのは、この系統だけである。**

#### メカニズム2: workerへ継承するcontextを必要十分まで絞る

C33はworker packetが十分なら継承を`none`にし、不足時も最小限のturnだけ継承した。C32比でtoken中央値`-24.63%`（約`-959,484`）。ただし`quality_score`中央値が`-6.250`低下した。

これは反例として重要である。「渡さない情報が判断に不要」と確認できないまま削ると品質を割る。

#### メカニズム3: 結論が変わらない場面での再判断・再readを止める

モデルは作業途中で繰り返しmodel stepへ戻る。この再入自体がtokenを消費する。

- **C69 `DECISION_BOUNDARY`**: 未発行invocationのtarget / permission / method / stop conditionを変えないresult間ではモデルへ再入しない。既知の相互非依存invocationは分割せず同一model stepから発行し、全result受領後に一度だけ次を判断する。
- **C71 `VALIDATION_CLOSURE`**: artifact変更後、TaskSpec-requiredなvalidation全件がbind済みなら、全件を個別invocationとして同一model stepから発行し、全resultを一度だけモデルへ返す。全件成功かつ全result bind済みなら、TaskSpec追加要求またはresult失効がない限りread / validationを追加せずterminalを判断する。

観測値（各々別の互換条件下）:

| 比較 | 採点契約 | token | tool call | model step | `elapsed` |
| --- | --- | ---: | ---: | ---: | ---: |
| C69 − C43（標準14項目 `N=5`） | v10 | 中央値`-26.21%` / 合計`-22.59%` | `-26.60%` | — | 中央値`-18.37%` |
| C69 − C43（同条件B18） | v10 | 中央値`-11.08%` / 合計`-13.00%` | `-15.29%` | — | 中央値`+4.12%` |
| C71 − C69（標準14項目B18） | v12 | 中央値`-26.14%` / 合計`-27.93%` | `-30.16%` | `-26.54%` | 中央値`-12.44%` / 合計`-11.71%` |

いずれもtokenとstep数を大きく削ったが、**評価上は両者とも事前gate不通過で`stopped`である**（理由は3.6節）。

#### メカニズム4: read経路を事前に確定し一括化・最短化する

参照resourceを逐次readするとread 1回ごとにstepとtokenが積む。

- **C50**（順序依存のないroot readを同一model stepへbatch）: F05 / F10でtoken合計`-40.08%`。しかし探索型のA01 / A02では`+15.70%`、全20 run合計は`-2.49%`にとどまった。
- **C63**（全文sourceを1つに固定し、確定済み証拠のreviewでのみ差分を実行前合成）: F10で`5 / 5`がscore `4`、tool call 3回、token合計`-52.90%`へ収束した。

局所では最大級に効くが、case横断では安定しない。C50はA02の探索拡大により停止した。

### 3.3 効かなかった制御: 表面圧縮の反例系列

本研究の負の結果は破棄せず保存されており、本論文の中心的証拠である。root promptのbyte数またはlabel数を減らすことを主眼とした8件のcandidateは、次の結果を示した。

| candidate | 変更 | root prompt静的量 | 実行時tokenの動的量 | 経路diagnostic | 判定 |
| --- | --- | ---: | ---: | --- | --- |
| C32 | 見出し・説明・重複表現を8制御規則へ縮約 | `-32.60%` | 中央値**`+6.45%`** | — | 縮約でのtoken削減を確認できず |
| C49 | worker制御6 labelを3 labelへ圧縮 | `-39.12%` | 20 run合計**`+13.21%`** | — | 停止 |
| C54 | 保存traceで必要性を確認できたcontrol coreだけを残す | `-36.56%` | 合計**`+9.44%`** | F10 model step / tool call `+5 / +5` | 停止 |
| C64 | 32 clauseを4 blockへ再配置しF coreを全文重複 | （重複により増） | F10 **`+28.90%`** | tool call `43 → 54`、model step `48 → 59` | 停止 |
| C65 | 32 clauseを重複なし11 labelへ短文化 | `-7.01%` | F10 **`+14.25%`** | tool call `43 → 49`、model step `48 → 54` | 停止 |
| C66 | label数・label順・clause所属を維持して圧縮 | `-1.43%` | F10 **`+31.36%`** | tool call `43 → 57`、model step `48 → 62` | 停止 |
| C67 | 重複文2件を正本labelへ統合 | `-4.72%` | 中央値`-2.33%`、70件合計**`+0.28%`** | 反復ごとの方向が不揃い | 採用未判断 |
| C68 | `INDEPENDENCE`から1文削除 | `-3.02%` | **`+1.16%`**（合計`+426`） | `elapsed` **`+26.04%`** | 停止 |

正本は各candidateの評価resultおよび[`candidate-history.md`](candidate-history.md)。

**8件中7件で実行時tokenが増加または実質不変だった。** 唯一中央値が減ったC67も、70件のtoken合計は`+0.28%`で反復ごとの方向が揃わなかった。C66は静的量をわずか`-1.43%`減らしただけで、F10のtokenが`+31.36%`、tool callが`43 → 57`へ増えている。

C64は逆向きの実験としても有効である。意味を保ったまま全文を各実行経路へ**複製**した場合、成果は25 / 25でscore `4`を保ったが、F10のtool callは`43 → 54`、tokenは`+28.90%`となった。静的量の増減と動的量の増減は、符号すら対応しない。

### 3.4 静的量と動的量の逆行

3.2節と3.3節を並べると、本研究の中心的な観測が現れる。root promptのbyte数（実測）と、そのcandidateで観測された実行時tokenの方向を対照する。

| prompt set | root `AGENTS.md` bytes | 直前比のbyte変化 | 観測された実行時tokenの方向 |
| --- | ---: | ---: | --- |
| ControlFreeRepository | 0 | — | baseline比 中央値`-74.06%` |
| C41 | 3,482 | — | C35比 合計`-50.02%`、control-free同水準 |
| C43 | 3,980 | +498 | C41比 合計`-0.52%` / 中央値`+4.60%`（方向不一致のためtoken値を採用根拠にしていない。C43の実際の獲得は品質で、score分布はC41 `64 / 1 / 5`からC43 `70 / 70`） |
| C69 | 4,291 | **+311** | C43比 中央値**`-26.21%`** |
| C71 | 4,987 | **+696** | C69比 中央値**`-26.14%`**、合計`-27.93%` |
| Baseline | 5,980 | — | C41比 中央値`+278.40%` |

C43からC71では、root promptを`3,980 → 4,987 bytes`（`+1,007 bytes`、`+25.30%`）へ**増やしながら**、2段の測定でtokenを各`-26.21%` / `-26.14%`削減している。

> **重要な留保**: C43→C69は採点契約v10、C69→C71はv12で測定されており、compatibility keyが異なる。したがってこの2段を乗算して単一の削減率とすることは本基盤の規律に反する。連結値は示さない。示せるのは「隣接する2段の測定がいずれも、byte増加と同時にtoken減少を記録した」という事実である。

対照的に、3.3節の8件は静的量を`-1.43%`から`-39.12%`まで減らし、動的量を`-2.33%`から`+31.36%`へ動かした。

**したがって、削減対象はprompt文字数ではない。** 効いたのは、labelを足してでも実行経路上の判断点を消したときだけである。

### 3.5 継続反復での再現性

最大規模の測定は、C69とC71を標準14項目・各`N=5`・18 Batch（条件あたり1,260 run、合計2,520 run）で実行したものである。

| 対象 | 公式score分布 | quality中央値 | token中央値 | `elapsed`中央値 | 全run token合計 |
| --- | ---: | ---: | ---: | ---: | ---: |
| C69 B18 | `4 / 3 / 2 / 1 = 1,257 / 1 / 1 / 1` | 100.000 | 2,868,587.0 | 1,152.270秒 | 264,226,988 |
| C71 B18 | `4 / 3 / 0 = 1,255 / 4 / 1` | 100.000 | 2,118,725.5 | 1,008.883秒 | 190,417,472 |
| C71 − C69 | — | 0.000 | `-749,861.5`（`-26.14%`） | `-143.387`秒（`-12.44%`） | `-73,809,516`（`-27.93%`） |

再現性の指標:

- **18 / 18 Batch**でC71のtoken中央値と`elapsed`中央値が小さかった。
- **13 / 14 case**でtoken合計と`elapsed`中央値が小さかった（増えたのはA01のみ、token合計`+6.49%`）。
- 2,520 / 2,520 runでall-agent tokenを完全取得。excluded attempt 0件、command protocol違反0件、root以外のsession 0件。
- 同一Batch・case・iterationの1,260対では、C71のtokenが小さい組935、`elapsed`が短い組886。token差と`elapsed`差のPearson相関`+0.586`。

正本: [`C69 / C71 validation closure v12 標準14項目 B18`](../evaluations/results/candidate69-candidate71-validation-closure-v12-standard14-continuous-n5-b18_2026-07-22.md)。

18 Batchすべてで方向が一致したことは、効率改善が単発の偶然でないことを示す。一方で`elapsed`と`token`の相関が`+0.586`にとどまることは、時間短縮をtoken削減の代理指標としてはならないことを示す。実際にC69のB18では、tokenが`-13.00%`である一方`elapsed`中央値は`+4.12%`だった。

### 3.6 効率と品質のトレードオフ: なぜC71は`stopped`なのか

C71はtokenを`-27.93%`、tool callを`-30.16%`、model stepを`-26.54%`削減し、`quality_score`中央値は100.000で同値だった。それでも評価上は`standard14_b18_evaluated / stopped`である。

理由は**中央値ではなく分布の裾**にある。公式v12分布はC69の`1,257 / 1 / 1 / 1`に対しC71が`1,255 / 4 / 1`。保存traceの意味確認では、C71に採点偽陰性1件と実質欠落4件があり、C69比で実質的な低得点が3件多かった。

C71の実質欠落4件の内訳:

| case | 件数 | 内容 |
| --- | ---: | --- |
| A02 | 3 | 正規起動先と既存testを満たしたが`git diff --check`を実行しなかった |
| A01 | 1 | 未固定の変更後modeを確認せず`strict`へ変更し、testファイルも変更して23 testを実行した |

このうちA01の1件は、メカニズムとして重要である。`VALIDATION_CLOSURE`は「artifact変更後」の領域に閉じた制御であり、仕様確定前には適用しないと明記されている。にもかかわらず、**検証実行が非適用領域である仕様確定前へ流入した**。closure制御が意図した境界を越えて働き得るという失敗形である。

また、failed shell commandはC69の140からC71の184へ増えた（`+44`）。効率改善だけを採用根拠にできない理由の一つである。

判定表は7条件のうち5条件を通過し、「実質的な品質後退なし」と「required validation欠落なし」の2条件で不通過だった。KPIの優先順位や閾値は評価基盤へ追加していないため、この判定は採用判断側の記録であり、一次resultやcomparison schemaを変更していない。

### 3.7 評価と採用の分離: 実例

C71は評価上`stopped`のまま、**別の明示判断**で2026-07-23にrelease status `projected`・approval `approved`・runtime projection `projected`となり、THE-CAPTION本体へ適用された（PR [#340](https://github.com/Kenn-dclxvi/THE-CAPTION/pull/340)、統合commit `326fdd343a50522629592d67b0f028fb66e94eb3`、変更対象はroot `AGENTS.md`のみ、`bash ./scripts/dev/verify_change_set.sh`は`362 passed / 3 skipped`）。品質gate不通過と未解決riskは取り消していない。

本体投影済みのreleaseは4件で、この順に積み上げられている。

| release（由来candidate） | 本体反映 | 実変更範囲 |
| --- | --- | --- |
| Candidate41 | PR [#334](https://github.com/Kenn-dclxvi/THE-CAPTION/pull/334) | 8 path |
| Candidate43 | PR [#335](https://github.com/Kenn-dclxvi/THE-CAPTION/pull/335) | 直前投影からroot `AGENTS.md`一つ |
| Candidate71 | PR [#340](https://github.com/Kenn-dclxvi/THE-CAPTION/pull/340) | 直前投影からroot `AGENTS.md`一つ |
| Candidate81 | PR [#343](https://github.com/Kenn-dclxvi/THE-CAPTION/pull/343) | 直前投影からroot `AGENTS.md`一つ |

C41・C43・C71は過去の投影履歴かつ巻き戻し先として保持され、`cancelled`にしていない。正本: [`prompts/releases/README.md`](../prompts/releases/README.md)と各release README。

これは方法論上の主張でもある。**評価は観測であり、採用は判断である。** 有限回の試験で将来挙動を100%保証することを採用条件にせず、残余riskは観測頻度だけでなく実利用での影響、検出可能性、回復可能性、rollback identityと合わせて扱う（[`future-roadmap.md`](future-roadmap.md)）。

### 3.8 Rating v13一律比較とreasoning effort追試

採点契約revisionを跨いだ過去resultを連結せず、Rating v13・標準14項目・各`N=5`・global queue `M=24`へBaseline、ControlFreeRepository、C5、C35、C43、C71の6条件を揃えた。reasoning `high`と`medium`はそれぞれ6条件 × 70 run = 420 runで、全件がvalidかつrateableだった。

| reasoning | C43 quality中央値 | C71 quality中央値 | C71 − C43 token中央値 | C71 − C43 elapsed中央値 |
| --- | ---: | ---: | ---: | ---: |
| `high` | 100.000 | 100.000 | `-978,840`（`-31.47%`） | `-66.453秒`（`-5.63%`） |
| `medium` | 100.000 | 100.000 | `-793,181`（`-29.19%`） | `-112.335秒`（`-10.59%`） |

正本は[`High 6条件result`](../evaluations/results/baseline-control-free-repository-c5-c35-c43-c71-v13-standard14-n5_2026-07-26.md)と[`Medium 6条件result`](../evaluations/results/baseline-control-free-repository-c5-c35-c43-c71-v13-reasoning-medium-standard14-n5_2026-07-26.md)である。reasoning effortはcompatibility conditionであるため、HighとMediumを同一のLayer 4 comparisonへ混ぜない。ここで示せるのは、各reasoning水準内の互換比較でC71とC43の品質中央値が同値で、C71のtoken中央値が約29〜31%小さかったことまでである。

C71単独では6水準、各70 runを取得した。

| reasoning | score分布 | quality中央値 | token中央値 | elapsed中央値 |
| --- | ---: | ---: | ---: | ---: |
| `low` | `4 = 70` | 100.000 | 2,000,274 | 901.850秒 |
| `medium` | `4 = 70` | 100.000 | **1,923,688** | 948.869秒 |
| `high` | `4 = 70` | 100.000 | 2,131,059 | 1,114.525秒 |
| `xhigh` | `4 = 70` | 100.000 | 2,263,485 | 1,382.917秒 |
| `max` | `4 = 70` | 100.000 | 2,382,990 | 1,851.930秒 |
| `ultra` | `4 / 0 = 69 / 1` | 100.000 | 3,407,392 | 2,188.151秒 |

`medium`は`high`比でtoken中央値`-9.73%`、elapsed中央値`-14.86%`、`low`はelapsed中央値`-19.08%`だった。`xhigh`以上はtokenとelapsedがともに`high`より増えた。`ultra`のscore `0` 1件は、search pattern内の文字列をtest実行と誤認したRating v13の採点偽陽性であり、immutableなresultは変更していない。正本は[`C71 reasoning 6水準result`](../evaluations/results/candidate71-reasoning-levels-v13-standard14-n5_2026-07-26.md)である。

後続のCandidate81は、MediumのF04で残った逐次model再入を対象に`VALIDATION_CLOSURE`一行だけを置換した。標準14項目70 / 70件でscore `4`を維持し、複数required command caseの1-step closureをC71の30 / 35から35 / 35へ上げた。一方、token合計は`+0.28%`、elapsed中央値は`+5.78%`であり、効率上の優位は示していない。この評価結果自体は採用、release、runtime projectionを意味しないが、その後の2026-07-27の明示判断でrelease status `projected`・approval `approved`・runtime projection `projected`となった。THE-CAPTION PR [#343](https://github.com/Kenn-dclxvi/THE-CAPTION/pull/343)の実効変更はroot `AGENTS.md`一つで、統合commitは`592e73aae4f5cf71964efea0d49836e8c894cbbc`、本体検証は`401 passed`だった（評価正本: [`C71 / C81標準14項目result`](../evaluations/results/candidate71-candidate81-validation-wrapper-precedence-v13-medium-standard14-n5_2026-07-26.md)、projection正本: [`Candidate81 release`](../prompts/releases/the-caption-3ce91a4-validation-wrapper-precedence-release-r1/README.md)）。

---

## 4. 測定装置の妥当性

効率研究では、採点契約の欠陥が結論を反転させ得る。本研究はその実例を検出し、修正した。

### 4.1 A02で起きた「要求と採点のずれ」

`TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING`は、一見あいまいだが実はrepository規則で一意に決まる正規の起動先を、質問せず正しく解決して実装できるかを測るcaseである。

- 実行役へ提示した成果条件は「shell構文、TaskSpecまたは適用されるrepository規則が要求する既存試験、最終差分の確認」という**抽象表現**であり、特定の試験コマンド名を含まない。
- 一方、採点側（private）には`git diff --check`という**特定コマンド**が置かれていた。
- 採点器はこの抽象条件を「`git diff --check`の実行必須」と読み替え、未実行を欠落として減点した。
- しかし`git diff --check`は末尾空白や競合markerのlintであり、A02の主眼であるrouting成立の確認とは別物である。

C71のB18でA02のscore 3は4件あり、意味確認により3件がこの**ずれ**、1件が別の採点偽陰性（wrapper内`pytest`の成功command展開失敗）と分かれた。すなわちA02の4件はいずれも本物の品質低下ではない。

### 4.2 契約revisionによる修正

採点条件はrevision別に固定し、in-placeで書き換えない。結果を見た後の基準変更は必ず新revisionとする。

| revision | 主眼 |
| --- | --- |
| v10 | 実行役に提示した成果境界だけを必須にする |
| v11 | F10数値lineの意味等価と位置診断を分離 |
| v12 | command evidenceのquote直列化を正規化 |
| **v13** | 提示した抽象成果条件を特定コマンドへ具体化して必須化することを禁じ、コマンド名までmodel-visibleに明示された必須試験だけを品質へ反映する |

v13がこのずれを塞いだ。C71のB18自体はv12で実施しており、v12契約とB18 resultはそのまま履歴として保持する。**過去resultを新契約で再採点したようには扱わない。**

### 4.3 解釈への影響

この修正により、C71 release artifactに保存された当時の未解決risk 2件の位置づけが分かれた。

| 当時のrisk（v12時点） | 観測 | v13後の現在解釈 |
| --- | ---: | --- |
| A02で`git diff --check`欠落 | 3 / 90 | 現在の未完了研究項目ではない。要求と採点のずれとして本物の品質低下と区別される |
| A01で未固定modeを確認せず実装・試験へ進んだ | 1 / 90 | 現在も残る品質上のrisk |

当時のrelease riskの記録は取り消さない。正本: [`a02-rating-divergence.md`](a02-rating-divergence.md)、[`research-backlog.md`](research-backlog.md)。

### 4.4 一般的な含意

この事例は本論文の外部比較にも及ぶ。ベンダ公式指針が報告する「eval scoreが10〜15%改善」のような主張は、その採点契約がmodel-visible境界を守っているかに依存する。抽象的な成果条件を採点側で特定手段へ具体化すれば、手段を変えた条件は実体のない減点を受ける。**効率化の測定では、効率化された側が「省略した」ように見えやすいため、この偏りは方向性を持つ。** 2026-07-26に6条件・計420件の最初のv13互換resultを登録した。v12以前のresultは同一comparisonへ混ぜない。

---

## 5. 2026年7月ベンダ公式指針との対照

2026年7月、両ベンダがprompt設計指針を更新した。いずれも本研究の主要な結論と同方向である。

### 5.1 OpenAI GPT-5.6 Sol 指針

公式のmodel guidanceおよび報道による要点。

- **lean vs elaborate**: 内部testで「よりleanなsystem promptがeval scoreを約10〜15%改善し、総tokenを41〜66%削減した」。
- **除去方針**: 「各指示は一度だけ述べる」。「taskに関係するtoolだけを露出し、説明は簡潔に保つ」。「examplesとstyle guidanceは、product要件を符号化する場合、または測定された欠落を補正する場合に残す」。
- **outcome-first**: 手順を規定せず、目標と成功条件、domain contextとhard constraint、承認境界を述べ、実行手順はモデルに決めさせる。
- **停止条件 / 自律境界**: 「answer、explain、review、diagnose、planの依頼では、関連資料を確認して結果を報告する。依頼が求めない限り変更を実装しない。change、build、fixの依頼では、範囲内のlocalな変更を行い、非破壊的な検証を確認なしに実行する。外部書き込み、破壊的操作、購入、範囲の実質的拡大には確認を要する」。安全なlocal操作を明示的に列挙し、不要な承認要求を避ける。
- **API側の統制**: `text.verbosity`（`low` / `medium` / `high`）、reasoning effortは移行時に一段下げて試す、Programmatic Tool Callingは境界の明確なworkflowに適する。
- **旧promptは害になり得る**: GPT-5.5 / 5.4向けに最適化したpromptは結果を悪化させ得るため、複製ではなく監査を推奨。

### 5.2 Anthropic Claude Opus 5 指針

- **task scopeと過剰検証**: 「promptに明示的な検証指示（『非自明なtaskには最終検証stepを含める』『検証にsubagentを使う』）が含まれる場合は削除せよ。この種の指示はClaude Opus 5で過剰検証を起こし、削除すると品質を損なわずに無駄なtokenが減る。別の検証stepを追加するlegacy harness scaffoldingにも同じことが当てはまる」。
- **subagent起動の制御**: 「Claude Opus 5は以前のmodelより積極的にsubagentへ委譲する。委譲は真に独立した大きな作業では報われるが、小さなtaskへ適用するとcostと時間を増やす」。推奨文の例: 「数回のtool callで自分で終えられる作業を委譲するな。自分の作業の検証や再確認にsubagentを使うな。1体で足りるなら複数使わず、spawn数を低く保て」。
- **self-correction**: 「モデルが既に行う再確認を指示するな（『答えを再確認せよ』『応答前に再検証せよ』）。これらはモデル自身の振る舞いと複合し、結果を改善せずcostを増やす」。
- **過剰な徹底性**: 「blanketなdefaultを、より的を絞った指示へ置き換えよ」。「over-promptingを削除せよ。以前のmodelで起動不足だったtoolは、いまや適切に起動する。『迷ったら[tool]を使え』のような指示は過剰起動を招く」。推奨文の例: 「approachを選んだらcommitせよ。推論を直接否定する新情報に出会わない限り、決定を再訪するな」。
- **parallel tool callの最適化**: 独立したtool callは並列化する。促さなくても高い成功率だが、明示すればほぼ100%へ引き上げられる。
- **effortを第一のcost leverとする**: `low` / `medium`を品質が保たれる範囲で積極的に使う。

### 5.3 対応表

本研究が実測した制御と、両指針の対応を示す。左列は`gpt-5.6-sol`上の実測、右2列は公開指針の記述である。

| 本研究の制御（実測） | 実測効果 | GPT-5.6 Sol 指針 | Claude Opus 5 指針 |
| --- | --- | --- | --- |
| **C41 委譲境界**: owner語列だけではworkerを起動せず、TaskSpecが独立producer executionを明示した場合だけ委譲する | C35比token合計`-50.02%`、worker spawn≈0、60 / 60 score `4` | （直接対応する記述は薄い） | **ほぼ同一**。「Controlling subagent spawning」: 明示guidanceまたは決定的cap。「数回のtool callで自分で終えられる作業を委譲するな」「検証にsubagentを使うな」 |
| **C69 `DECISION_BOUNDARY`**: 未発行invocationの選択を変えないresult間ではモデルへ再入しない | 中央値`-26.21%`、tool call`-26.60%`。B18で合計`-13.00%` | outcome-first（手順を規定しない） | **同じ不変条件の自然言語版**。「approachを選んだらcommitせよ。推論を直接否定する新情報に出会わない限り決定を再訪するな」 |
| **C71 `VALIDATION_CLOSURE`**: 変更後のrequired validation全件を同一model stepで一括発行し、全件成功後は根拠なきread / validationを追加しない | 合計`-27.93%`、tool call`-30.16%`、model step`-26.54%`、18 / 18 Batch再現 | 「各指示は一度だけ述べる」、停止条件の明示 | **3記述が合流**。「Task scope and over-verification」（検証指示を削除せよ）＋「Self-correction」（既に行う再確認を指示するな）＋「Optimize parallel tool calling」（独立callの並列化） |
| **C43 `SPEC` / `spec_ready`**: 成果値をbindできるauthorityを限定し、bindできない未固定値は編集・試験前に確認して停止する | v10標準14項目70 / 70 score `4`。B18は1,260 / 1,260 valid、`4 / 3 / 1 = 1,255 / 4 / 1` | 「承認境界を定義する」「範囲の実質的拡大には確認を要する」 | 「異なる読みが実質的に異なる作業へ至る場合だけ確認せよ」 |
| **C50 / C63 read経路の事前確定** | F10で`-40.08%` / `-52.90%`。ただしA02で`+15.70%`、20 run合計`-2.49%` | Programmatic Tool Calling（境界の明確なworkflow向け） | parallel tool callの最適化 |
| **反例系列 C32 / C49 / C54 / C64〜C68**: 表面byte圧縮 | 静的`-1.43%`〜`-39.12%`に対し動的`-2.33%`〜`+31.36%`（多数が増加） | 「lean」をbyte削減と読むと**反例**。実体は「指示を一度だけ述べる」「tool説明の簡潔化」であり判断点削減と読めば整合 | 「remove them」は検証指示という**判断点**の削除であり、byte削減ではない |

### 5.4 本研究が公式指針へ追加する点

**(1) 削減対象の分離。** 両指針は「lean」「trim」「remove」という語で方向を示すが、byte削減と判断点削減を区別していない。本研究は同一基盤上で、8件のbyte削減candidateと3件のlabel追加candidateが**逆方向の結果**を出したことを示す。実務上の含意は明確である。promptを短くする作業と、実行経路を短くする作業は別の作業であり、前者を後者の代理指標にできない。

**(2) 下限の測定。** 両指針は「減らせ」と言うが、減らし切った状態を測っていない。本研究はroot promptを0 byteにした対照条件を持つ。その結果、精緻なbaselineの超過は実測で約4倍（token中央値`+278.40%`）であり、**削減余地の大部分はprompt自体ではなく、promptが誘発する実行経路にあった**。

**(3) 削除では閉じない品質欠陥。** 0 byte条件はscore `59 / 1`で、残余欠陥1件を残した。これはbyteを足さずには閉じなかった。C41は1つのpredicateを足して`60 / 60`にし、tokenは0 byte条件と同水準（中央値`+1.83%`、合計`-1.29%`）を保った。すなわち「lean」の最適点は0ではなく、**control-free効率＋最小限の境界predicate**である。指針を額面どおり適用して検証指示や委譲指示をすべて削除した場合、この残余欠陥がどこに現れるかは測っておく必要がある。

**(4) 効率向上の代償の定量。** Opus 5指針は検証指示の削除を「品質を損なわずに」と述べる。本研究の対応する制御（C71）は、`gpt-5.6-sol`上でtokenを`-27.93%`削減する一方、1,260 runで実質欠落がC69比`+3`件だった。さらに、closure制御が非適用領域（仕様確定前）へ流入する失敗形を特定した。効率改善は無償ではなく、代償は分布の裾に現れるため中央値では見えない。

**(5) 測定装置の妥当性要件。** 抽象的な成果条件を採点側で特定コマンドへ具体化すると、手段を変えた効率化条件が実体のない減点を受ける（第4節）。この偏りは方向性を持つため、効率化の主張では採点契約のmodel-visible境界を先に検証する必要がある。

### 5.5 相違点・未検証点

**(a) 単一model / 単一Agent条件。** 本研究の全評価resultは`gpt-5.6-sol` / Codex CLIの単一条件である。reasoning effortは6水準へ広げたが、Claude Opus 5での測定は**0件**である。したがって5.3節の一致は「異なるmodel系列で同方向の結論が独立に得られた」ことを示すにとどまり、本研究の制御がOpus 5上で同じ効果量を持つ保証はない。本リポジトリ自身の方針は、model / reasoning設定 / Agent / CLI / runtimeが変わる場合は新しいprofile revisionとして評価し、異なるmodelまたはruntimeのresultを同一compatibility comparisonへ混ぜないことである（[`future-roadmap.md`](future-roadmap.md)）。別model / 別CLIのprofile revisionは未実施である。

**(b) reasoning effort追試。** C71の6水準追試では、品質中央値を維持した範囲で`medium`がtoken中央値最小、`low`がelapsed中央値最小だった。`medium`は`high`比でtoken中央値`-9.73%`、elapsed中央値`-14.86%`である。一方、同じRating v13・標準14項目で測ったC71とC43のtoken中央値差は`high`で`-31.47%`、`medium`で`-29.19%`だった。少なくともこの2水準・`N=5`では、effort低下だけでC71の相対的な制御差は消えていない。ただしreasoningごとにcompatibility keyが異なるため、水準間の差は記述的比較であり、制御効果とeffort効果の加法性や因果分解までは主張しない。

**(c) API層の統制。** `text.verbosity`とProgrammatic Tool Callingはprompt層の外にあり、本研究では未測定である。reasoning effortは2026-07-26の追試で新しいprofile revisionのcomparison conditionとして変数化したが、prompt差分と同一comparisonへ混ぜていない。本リポジトリのroadmapは「安定して効果が確認された機械的な制御は自然言語promptへ積み増さず、型付きTaskSpec、permission gate、scheduler、validation DAG、producer identity、terminal stateなどのruntime機構へ移す」方針を持ち、ベンダがAPI parameterへ移した動きと同方向である。

**(d) 指針は単一runの推奨、本研究は反復測定。** 公式指針は推奨文とその内部eval結果を示すが、case別分布、反復間の方向一致、失敗形の分類は公開されていない。本研究は18 Batchでの方向一致（18 / 18）と、case別（13 / 14）、対別（935 / 1,260）まで開示している。効果量の比較ではなく、**検証可能性の粒度**が異なる。

---

## 6. 考察

### 6.1 promptは文章ではなく実行経路の仕様である

本研究の全体を貫く結論は、[`prompt-control-design-principles.md`](prompt-control-design-principles.md)が定式化した関係に集約される。

```text
正味token差
= 制御文の読解cost
 + 追加された判断・確認cost
 - 回避できた探索・context継承・再読・再試行・手戻りcost
```

第3項が第1項・第2項を上回るときだけ、制御は正味で効く。C41・C69・C71は第3項が支配的だった。C32・C49・C54・C64〜C68は第1項を減らしただけで第3項を動かせず、いくつかは第2項（label間の関係と例外の増加）を増やして正味で悪化した。

したがって設計原則は「規則を増やさない」でも「文字数を減らす」でもなく、**将来の不要な判断経路を先に消す**である。そして消す対象を具体的に示せないpredicateは追加しない。

### 6.2 効果量の階層

観測された効果量は、制御が触る対象の階層で決まった。

| 階層 | 制御対象 | 効果量 | 例 |
| --- | --- | --- | --- |
| 1 | 処理量そのもの（worker起動） | 最大 | C41: 合計`-50.02%` |
| 2 | モデル再入回数（判断・検証の一括化） | 大 | C69 / C71: `-26%`〜`-30%` |
| 3 | read回数と順序 | 中（局所的、case横断で不安定） | C63: F10で`-52.90%`、全体では不安定 |
| 4 | prompt表面（byte、label数） | 有意差なし、しばしば悪化 | C32 / C65 / C66 |

この階層は、all-agent tokenの合算構造から予測できる。worker 1体の起動は子セッションのusage全体を加算するため、階層1が支配的になる。以降はmodel step数、tool call数、そして静的入力量の順に寄与が小さくなる。

### 6.3 品質は中央値では守れない

`quality_score`中央値は本研究の主要な比較で一貫して100.000だった。C71も同値である。それでも採用gateは分布の裾で不通過となった。1,260 runのうち4件の実質欠落が判断を分けた。

これは反復規模の設計に直接影響する。`N=5`（60 run）では、`4 / 1,260`の頻度の欠陥は観測されない可能性が高い。本基盤が`N=5`のtargeted試験を先に置き、成立した場合だけ標準評価と継続反復（B18、1,260 run）へ進む段階設計を採るのは、この非対称性への対応である。低頻度の誤経路は少数反復で不在を証明しない。

### 6.4 ベンダ指針との関係の読み方

2026年7月の両指針と本研究の一致は、偶然ではなく同じ構造から出ていると考えられる。model世代が上がると、以前は必要だった足場（明示的な検証step、委譲の指示、徹底性の要求）がモデル自身の既定挙動と**二重化**する。二重化した指示は経路を増やすだけになり、costだけが残る。両指針の「削除せよ」も、本研究の「判断点を消せ」も、この二重化の解消を指している。

ただし帰結は同一ではない。指針は削除を推奨し、本研究は**置換**を推奨する。0 byte条件が残した欠陥1件は、削除では閉じず、1つの境界predicateで閉じた。指針の削除リストを適用した後に何が残るかは、それぞれの環境で測るべき量である。本リポジトリの設計原則が「新規追加より置換と削除を優先する」としつつ、「候補のroot promptが短くなったこと自体を効率化としない」と併記しているのは、この両面を扱うためである。

---

## 7. 限界と妥当性の脅威

1. **単一model / 単一runtime。** modelは`gpt-5.6-sol`、AgentはCodex CLIであり、他model・他CLIでの再現は未確認。reasoning effortは6水準で追試したが、model系列とruntimeの一般化にはならない。
2. **公開targetは1 repository・2 Bundleに限る。** 評価resultを持つtargetはTHE-CAPTION commit `3ce91a4`と公開target `pallets/click`の2つになった。`click`ではBundle AとC81全文のBundle Bを同じStd14条件で各70 run評価した。Bundle Bは70 / 70件のscore `4`を維持し、Bundle A比token中央値`-23.96%`、elapsed中央値`+2.86%`だった（正本: [`Click Bundle A / B result`](../evaluations/targets/click/results/click-control-free-c81-full-standard14-n5_2026-07-26.md)）。token削減方向は再現したがelapsed短縮は再現せず、別公開repository、他言語、個別predicateへの一般化はまだ成立していない。
3. **採点は多くの場合、独立blind raterによるものではない。** 複数の一次resultがこれを明示している。採点は固定契約による自動auditである。
4. **契約revisionを跨いだ比較は不可能。** v1からv13まで13 revisionがあり、compatibility keyが異なるresultを混ぜられない。3.4節の2段の測定を連結できないのはこの理由による。現行契約はv13で、6条件・計420件の互換resultをHighとMediumでそれぞれ登録したが、両reasoning間およびv12以前のresultとは互換比較できない。
5. **反復規模の上限。** 条件あたり最大1,260 run。これ未満の頻度の誤経路について不在を主張しない。
6. **効かなかった制御の方が多い。** 効率で明確に効いたのは4メカニズムのうち実質2系統（worker抑制、再入削減）であり、うち再入削減系（C69・C71）は品質gateを通過していない。context削減系（C33）は品質を`-6.250`割った。read経路系（C50）はcase横断で不安定だった。
7. **未評価・診断限定のartifactが残る。** candidate bundle 79件のうち`not_evaluated`が2件。C45〜C48はblind quality ratingを持たない`diagnostic_only`枝であり、標準14項目やB18と互換な品質比較ではない。bundleの存在は評価済みを意味しない。
8. **未完了の研究項目が残る。** C71の11 label監査のうち3件（`CONTEXT` / `INDEPENDENCE` / `RECOVERY`）は「根拠なし」判定が暫定であり、既存の保存データでは決着しない。A01の3択variation診断は未実施。F10 location mismatchはprompt側の変更を停止し、evidence interface要件として別軸へ移した。索引は[`research-backlog.md`](research-backlog.md)。
9. **投影済みcandidateの残余risk。** C71は品質gate不通過のまま本体へ投影されている。当時のrelease artifactに保存された未解決risk 2件は取り消されていない。うちA01側は現在も品質上のriskとして残る。
10. **本論文自体の位置。** この文書は総説であり、いずれの状態についても正本ではない。

---

## 8. 結論

promptを実行制御として定義し、prompt差分だけを変数とする互換比較を反復したところ、次が観測された。

1. 精緻に書かれたroot指示書は、`gpt-5.6-sol`上で実行時tokenを約4倍に増やしていた（token中央値`+278.40%` vs 最良candidate）。その超過は品質を買っていない（score分布はbaselineが最悪）。
2. root指示書を0 byteにした対照条件だけで、baseline比token中央値`-74.06%`を達成した。削減余地の大部分は文面ではなく、文面が誘発する実行経路にあった。
3. 削減対象はprompt文字数ではない。静的量を`-1.43%`〜`-39.12%`減らした8件は動的量を`-2.33%`〜`+31.36%`へ動かし多数が悪化した一方、labelを足した3件はいずれもtokenを`26`〜`30%`削減した。C43からC71では静的量を`+25.30%`増やしながら、2段の測定でtokenが各`-26%`減った。
4. 効果量の階層は、worker起動 ＞ model再入 ＞ read経路 ＞ prompt表面の順である。
5. 「lean」の最適点は0ではない。0の近傍には削除では閉じない低頻度の品質欠陥が残る。最良candidateは0 byte条件の効率を保ったまま、1つの境界predicateでその欠陥を閉じた。
6. 効率改善の代償は分布の裾に現れ、中央値では見えない。1,260 runで4件の実質欠落が採用gateを分けた。
7. 採点契約そのものが結論を歪め得る。抽象的な成果条件を採点側で特定コマンドへ具体化する欠陥を検出し、v13で塞いだ。この偏りは効率化された側を不利にする方向を持つ。

これらは2026年7月のOpenAI GPT-5.6 Sol指針およびAnthropic Claude Opus 5指針と同方向であり、両指針が語で混在させているbyte削減と判断点削減の区別、下限条件の測定、削除では閉じない残余欠陥、効率向上の代償の定量、測定装置の妥当性要件を追加する。reasoning effortは6水準で追試し、`medium` / `low`が`high`より低いtokenまたはelapsedを示しても、C71とC43の相対差は消えなかった。一方、modelとAgentは`gpt-5.6-sol` / Codex CLIの単一条件であり、Opus 5を含む別model・別CLIでの再測定は未実施である。

最後に、本基盤が一貫して分離してきた区別を再掲する。**評価は観測であり、採用は判断である。** 本基盤は`winner`も採否も出力しない。C71が評価上`stopped`のまま本体へ投影されている事実は、この分離が運用上も維持されていることを示す。

---

## 参考

### 本リポジトリの一次資料

- 評価基盤のLayerと境界: [`prompt-comparison-workflow.md`](prompt-comparison-workflow.md)（正本）
- 評価実行手順: [`evaluation-loop-manual.md`](evaluation-loop-manual.md)（正本）
- 制御設計原則: [`prompt-control-design-principles.md`](prompt-control-design-principles.md)（正本）
- リポジトリ契約: [`repository-contract.md`](repository-contract.md)（正本）
- 初見向け全体像: [`repository-overview.md`](repository-overview.md)
- 制御メカニズムの横断整理: [`control-mechanisms.md`](control-mechanisms.md)
- Candidate系譜と観測: [`candidate-history.md`](candidate-history.md)
- 採点ずれの個別事例: [`a02-rating-divergence.md`](a02-rating-divergence.md)
- 未完了研究項目: [`research-backlog.md`](research-backlog.md)
- 長期方針: [`future-roadmap.md`](future-roadmap.md)
- C71 label監査台帳: [`candidate71-control-abstraction-analysis.md`](candidate71-control-abstraction-analysis.md)
- candidate系譜と現在状態の一覧: [`prompts/candidates/README.md`](../prompts/candidates/README.md)
- release / approval / projection: [`prompts/releases/README.md`](../prompts/releases/README.md)

### 主要な一次評価result

- 主対照実験: [`Baseline / ControlFreeRepository / C35 / C41 expanded12 N=5`](../evaluations/results/baseline-control-free-repository-c35-c41-outcome-quality-owner-diagnostic-v9-expanded12-n5_2026-07-19.md)
- 最大規模の継続試験: [`C69 / C71 validation closure v12 標準14項目 B18`](../evaluations/results/candidate69-candidate71-validation-closure-v12-standard14-continuous-n5-b18_2026-07-22.md)
- 現行契約の互換比較: [`Baseline / ControlFreeRepository / C5 / C35 / C43 / C71 v13 標準14項目 N=5`](../evaluations/results/baseline-control-free-repository-c5-c35-c43-c71-v13-standard14-n5_2026-07-26.md)
- 現行契約・Mediumの互換比較: [`Baseline / ControlFreeRepository / C5 / C35 / C43 / C71 v13 Medium 標準14項目 N=5`](../evaluations/results/baseline-control-free-repository-c5-c35-c43-c71-v13-reasoning-medium-standard14-n5_2026-07-26.md)
- reasoning effort追試: [`C71 reasoning 6水準 v13 標準14項目 N=5`](../evaluations/results/candidate71-reasoning-levels-v13-standard14-n5_2026-07-26.md)
- Mediumでのvalidation closure安定化: [`C71 / C81 v13 Medium 標準14項目 N=5`](../evaluations/results/candidate71-candidate81-validation-wrapper-precedence-v13-medium-standard14-n5_2026-07-26.md)
- 再入境界: [`C43 / C69 model reentry decision boundary v10 標準14項目 N=5`](../evaluations/results/candidate43-candidate69-model-reentry-decision-boundary-v10-standard14-n5_2026-07-22.md)
- 成果値境界: [`C43 outcome authority boundary v10 標準14項目 B18`](../evaluations/results/candidate43-outcome-authority-boundary-v10-standard14-continuous-n5-b18_2026-07-20.md)
- all-agent token再集計: [`v3 all-agent token reaccounting`](../evaluations/results/v3-all-agent-token-reaccounting_2026-07-16.md)
- 公開target Clickの反復確認: [`click control-free F01-only P1-c N=5 B=3`](../evaluations/targets/click/results/click-control-free-f01-only-p1c-n5-b3_2026-07-26.md)
- 公開target ClickのF02追加確認: [`click control-free F02-only N=3`](../evaluations/targets/click/results/click-control-free-f02-only-n3_2026-07-26.md)
- 公開target ClickのBundle A baseline: [`click control-free Std14 N=5`](../evaluations/targets/click/results/click-control-free-standard14-n5_2026-07-26.md)
- 公開target ClickのBundle A / C81全文比較: [`Click Control-Free / C81全文 Std14 N=5`](../evaluations/targets/click/results/click-control-free-c81-full-standard14-n5_2026-07-26.md)
- 現行rating contract: [`outcome-abstract-condition-preserving-owner-diagnostic-v13.json`](../evaluations/rating-contracts/outcome-abstract-condition-preserving-owner-diagnostic-v13.json)

### 外部資料（2026-07-25取得）

- OpenAI, "Model guidance" (GPT-5.6 prompt guidance), <https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6>
- Anthropic, "Prompting Claude Opus 5", <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5>
- Anthropic, "Prompting best practices", <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices>
- Decrypt, "Stop Over-Prompting: OpenAI's New GPT-5.6 Guidelines Change Everything", <https://decrypt.co/373439/openai-new-gpt-5-6-prompt-guide-chatgpt>
- TechTimes, "GPT-5.6 Prompting Guide: Lean System Prompts Now Outperform Elaborate Scaffolding", <https://www.techtimes.com/articles/320650/20260715/gpt-56-prompting-guide-lean-system-prompts-now-outperform-elaborate-scaffolding.htm>
