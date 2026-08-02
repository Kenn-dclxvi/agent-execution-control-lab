# 分岐開閉の事後符号化（保存済みデータの再解析）

> [!IMPORTANT]
> **本文書は新規測定を含まない。** 保存済みのprompt bundleとresultだけを使う。既存resultをin-placeで変更せず、再採点もしない。
>
> **目的**: [`execution-control-research-paper-reframed-draft.md`](execution-control-research-paper-reframed-draft.md) の§7.5が置く「分岐の開閉」という軸について、**同じ研究が生んだ軸を同じ研究の結果で確かめている**という§12.2の構造的限界を、事後の頑健性チェックによってどこまで解けるかを確定する。
>
> **状態**: 符号化を124件について完了（第5節・第7節）。**独立検証群による検定は保存済みデータの構造上成立しない**（第6節）。**§12.2の構造的限界は解消していない。** 到達点と未完了部分は第6節を正とする。

---

## 1. なぜ符号化が必要か

論文§7.5の軸は、研究前半の保存済み観測から抽出し、後半の候補設計の先行制約として使っている。したがって後半の測定は軸の独立検証ではない（§12.2）。

この構造は、新規の対照実験なしには完全には解けない。**「原則が予測する方向と逆の候補」を意図して作る設計を実施していない**ためである。

しかし保存済みデータには、次の性質がある。

| 性質 | 実数 |
| --- | --- |
| 候補bundleの総数（このリポジトリにcommit済み） | 124件 |
| **root `AGENTS.md`本文を保持しているbundle** | **124 / 124** |
| **親identityをmanifestから辿れるbundle** | **124 / 124** |
| resultへリンクを持つ候補（候補index基準、未commit分を含む133件中） | 127件 |
| 状態に`stopped`を含む候補（同。すべて軸の成立後） | 76件 |

すなわち、**各候補が何をしたかを、KPIを一度も参照せずにprompt側だけから確定できる。** これを使えば、判定入力（prompt本文の差分）と判定対象（保存済みKPI）を構造的に分離した符号化ができる。

要約文書（`candidate-history.md`ほか）は使わない。**それらは結果を見た後に書かれている可能性を排除できないため**であり、リポジトリ規則も要約文書を数値の正本にしないと定めている。

---

## 2. 符号化基準（結果を参照する前に固定した）

### 2.1 判定入力

各候補について、**親bundleのroot `AGENTS.md`と当該候補のroot `AGENTS.md`のunified diff**だけを入力とする。

- 親identityは各候補の`manifest.json`の`content_relation.source_prompt_identity`または`baseline_prompt_identity`から取る。
- root本文は各bundleディレクトリ配下の`files/AGENTS.md.txt`とする。候補は`prompts/candidates/`、比較元は`prompts/baselines/`の各identityディレクトリにある。
- rootの形式は1行1ラベルであり、diffの追加行が追加された述語に対応する。

**入力に含めないもの**: 当該候補のresult、score、token、経過時間、状態、設計文書、系譜文書。

### 2.2 符号化する2つの二値

追加された述語（複数ある場合は各々）について次を判定する。

**(a) 観測可能性 `observable`**

> その述語の真偽が、**モデルが実行時に観測できる状態・証拠・結果**から判定できるか。

- `true`の例: 参照先が明示入力または一意な正本へbind済みか、変更が完了したか、必須検証のidentityとpass条件が揃ったか、受領resultが未発行invocationの条件を変え得るか。
- `false`の例: 「適切に」「慎重に」「必要に応じて」など判定主体の裁量に還元される語、モデルが観測できない外部状態への言及、実行環境の内部挙動の指定。

**(b) 停止性 `gating`**

> その述語が`false`のとき、**後続の実行経路を実際に止めるか**。

- `true`の例: `false`の間は着手しない、開始しない、変更を行わない、既定で禁止する。
- `false`の例: 分類・記録・優先順位・報告様式の指定にとどまり、経路の可否を変えない。参照先を教えるだけの索引。上限値・回数・行数による打切り（**打切りは経路を止めるが、止める条件が観測された成立ではなく代理値であるため`gating=false`とする**）。

**「分岐を閉じた」= `observable ∧ gating` がともに`true`**。それ以外は「閉じていない」。

### 2.3 区間の分割

軸を記録した文書 [`prompt-control-design-principles.md`](prompt-control-design-principles.md) の初版commitは**2026-07-19**である。各候補bundleの`manifest.json`の初回追加commit日で区間を分ける。

| 区間 | 定義 | 件数 | 論理的な位置 |
| --- | --- | ---: | --- |
| **成立前** | 初回commitが2026-07-19より前 | **33件** | 軸を制約に使っていない。符号化と結果が真に独立 |
| **成立後** | 初回commitが2026-07-19以降 | **91件** | 軸を先行制約として設計。軸の適用限界を測る区間 |

日付は`git log --diff-filter=A -- <dir>/manifest.json`の最古commitから取る。**`--follow`は使わない**（manifest間のrename検出で全件が最古commitへ結び付くため）。

### 2.4 この手続きが担保しないこと

- **符号化者は盲検ではない。** 論文執筆の過程で、約15件の候補についてKPIを既に知っている。完全な盲検は成立しない。
  - 対策として、(i) 基準をこの節で結果参照前に固定し、(ii) 全件の判定根拠（diffの該当行）を第4節へ開示する。第三者が同じ入力から再符号化できる状態にすることで検証可能性を確保する。**盲検の代替であり、盲検ではない。**
- **述語の効果を分離しない。** 1候補が複数の述語を追加した場合、符号化は述語単位でも、結果は候補単位にしか結び付かない。
- **符号化は本研究の軸の定義に依存する。** 軸そのものの妥当性を独立に検証するものではない。検証するのは「軸が、軸の成立前に作られたartifactの成否も説明するか」である。

---

## 3. この再解析が答える問いと、答えない問い

**答える問い**

1. 軸の成立前（33件）で、「分岐を閉じていない」と符号化された候補は、実行量を下げなかったか。**軸が生成される前のartifactを軸で説明できるか。**
2. 軸の成立後（91件）で、「分岐を閉じた」と符号化された候補のうち、停止したものはどれだけあるか。**分岐を閉じることは十分条件か。**

**答えない問い**

- 個々の述語の寄与（ablationなし）
- 軸が別の指示書設計・別のエージェント実装で成立するか
- 軸が唯一の説明であること（他の軸で同じ分割が得られる可能性を排除しない）

---

## 4. 符号化中に基準へ加えた変更

符号化を始めてから、固定した基準では判定できない区別が2つ現れた。**いずれも結果を参照する前に発見し、全件へ一律に適用した。**

### 4.1 「経路を閉じる」と「モデル往復を閉じる」は別である

第2節の基準(b)は「後続の実行経路を止めるか」を問う。しかし実際の候補には、**実行経路の可否は変えず、同じ実行を1つのmodel stepへまとめるだけ**の述語が多数あった（`FIXED_READ`、`ROOT_BATCH`、`TASK_CLOSED_READ`、`MACHINE_BOUNDARY`、`DECISION_BOUNDARY`、validation wrapperなど）。読み取り自体は減らず、減るのはモデルへの往復である。

**論文§7.5の表はこの2つを同じ軸に入れている。** 「証拠取得の既定禁止」（探索という実行経路を閉じた）と「経路の事前合成」（往復を閉じた）が同じ列に並んでいる。

そこで基準(b)を2つに分けた。

| 次元 | 定義 |
| --- | --- |
| `gate_path` | 述語が`false`のとき、**artifact変更・test・worker起動・taskの継続**のいずれかを止める |
| `gate_roundtrip` | 述語が`false`のとき、**invocationのmodel stepへの束ね方**が変わる（実行そのものは残る） |

符号は`closed_path` / `closed_roundtrip` / `closed_both` / `not_closed` / `opened`（root述語を削除しただけ） / `excluded`（root不変）とする。

### 4.2 候補単位への集約規則

1候補が複数の述語を追加した場合、**いずれか1つでも該当次元を満たせば候補をその符号とする**。この集約は`closed`側へ寄せる方向であり、「閉じていない候補が改善しなかった」という主張を弱める向きに働く。

---

## 5. 符号化結果

### 5.1 区間別の分布

| 符号 | 軸の成立前（33件） | 軸の成立後（91件） |
| --- | ---: | ---: |
| `closed_path`（経路を閉じた） | **15** | **33** |
| `closed_both`（経路と往復の両方） | **0** | **15** |
| `closed_roundtrip`（往復だけ） | **0** | **18** |
| `not_closed` | 12 | 25 |
| `opened`（root述語を全削除） | 2 | 0 |
| `excluded`（root不変） | 4 | 0 |

**往復を閉じる述語は、軸の成立前には1件も存在しない（0 / 33）。成立後は33 / 91（`closed_roundtrip` 18＋`closed_both` 15）である。**

この0 / 33は検出語の偏りではない。`model step` / 一括 / まとめて / 同時に / batch / 並行 / 往復 / tool callを含む広い語彙で成立前33件を再検索すると7件が該当するが、**すべて別義である**（`round`は変更round、`並行`は「並行に割り当てない」というproducer bindingの禁止、`まとめて`は「同種criterionを一つのworkerへまとめてよい」というworker統合）。往復の束ね方を扱う述語は成立前に存在しない。

**ただしこの移行を軸が駆動したとは言えない。** 軸を記録した文書の初版（2026-07-19）を確認すると、`model step`は3箇所に現れるが、いずれも**観測すべき診断値**としての言及である。

- 「評価では中央値だけでなく、score分布、case別token、tool call、**model step**、worker数、context継承方法を確認する」
- 「Candidate40はoperationとresult projectionの境界を明確にしたが、F10のtool call、**model step**、token合計をCandidate38から減らさなかった」
- 「想定するtoken、tool call、**model step**、worker routingの変化」

すなわち初版は、往復を**閉じよ**とは定めていない。**往復を閉じる操作は、この診断値を観測した結果として軸の成立後に現れたものであり、軸が先行制約として指示したものではない。** 論文§7.5は、後から現れたこの第2の操作類型を、既存の「分岐の開閉」という単一の軸へ事後的に吸収している。

### 5.2 符号化者への依存

同じ33件を、規則化の前に手作業で符号化していた。両者を比較する。

| | 手作業 | 規則 |
| --- | ---: | ---: |
| 閉じた | **24 / 33** | **15 / 33** |
| 閉じていない | 5 | 12 |
| 対象外 | 4 | 6 |

**一致は不十分である。** さらに、規則化の前段として作った語彙ベースの機械判定（否定表現を考慮しない版）と手作業の一致は**29 / 33（87.9%）**で、不一致4件はすべて否定または再表現に起因した。

- 「projection不能だけを**停止理由にしない**」を、`停止`という語の出現から`closed`と誤判定（2件）
- 「**念のため**を理由にしない」を、裁量語の出現から`not_closed`と誤判定（1件）
- 既存述語の再表現（圧縮）を新しい述語の追加と誤判定（1件）

**これが本再解析の最も重い結果である。** 「その記述は分岐を閉じているか」という判定は、**同一人物が基準を明文化する前と後で9件（33件中）変わる。** 論文§7.5の軸は、個別に文書化された7件の境界については成立するが、**候補集合全体へ適用できる再現可能な判定基準としては未確立である。**

### 5.3 経路を閉じることは十分条件ではない

成立後91件について、候補indexの状態から結果を取った。

| 符号 | 停止 | 採用・投影 | 観測のみ | 未評価 | 計 |
| --- | ---: | ---: | ---: | ---: | ---: |
| `closed_path` | 25 | 1 | 6 | 1 | 33 |
| `closed_both` | 12 | 1 | 2 | 0 | 15 |
| `closed_roundtrip` | 14 | 0 | 3 | 1 | 18 |
| `not_closed` | 16 | 0 | 9 | 0 | 25 |

**経路を閉じたと符号化された48件（`closed_path`＋`closed_both`）のうち37件が停止している。** 分岐を閉じることは実行量の低下と結び付いた条件を作るが、**採用に至る十分条件ではない。**

**この表から停止率の差を読まないこと。** 停止理由（品質gate未達、機構不成立、誤停止の増加、実行中断）は候補indexに機械可読な形で入っておらず、各resultの本文にある。また成立後の候補は日付が遅く、扱う問題も難しくなっている。符号と停止の関連を因果として読める設計ではない。

---

## 6. この再解析が到達できない部分

**軸の成立前区間を独立検証群として使う設計は、候補indexの状態列では実行できない。**

| 区間 | 状態列に現れる語 |
| --- | --- |
| 成立前（33件） | `observed_n5` 20件、`observed_targeted_n5` 2件、`observed_f02_n1` 2件、ほか。**`stopped`は0件** |
| 成立後（91件） | 状態文字列に`stopped`が直接埋め込まれている |

状態の語彙が研究の途中で変わっており、**結果変数が区間をまたいで比較できない。** 成立前区間で「閉じていない候補は実行量を下げなかったか」を判定するには、各候補のresult本文から親比のtoken方向と品質分布を取り直す必要がある。

**この取り直しを実施しても検定は成立しない。** 全resultを走査し、各候補とその親が同一result内に併記されている（すなわち同一の互換条件で比較されている）かを機械照合した。

| 成立前の符号 | 親子が同一resultに併記 | 併記なし |
| --- | ---: | ---: |
| `closed_path` | 10 | 5 |
| `not_closed` | 4 | 8 |
| `opened` | 1 | 1 |
| `excluded` | 2 | 2 |

**識別力を持つ群（`not_closed` 12件＋`opened` 2件）のうち、親との比較が保存されているのは5件だけである。** しかも欠落は偏っている。`command-evidence-projection`、`phase-result-projection`、`compact-execution-control`、`control-free-generic`、`task-spec-default-precedence`、`gate-evidence-binding`など、軸が「閉じていない」と分類する候補の側が落ちる。

早期の候補は単独評価か、親を含まないグループ比較として測られている。**したがって「軸の成立前区間を独立検証群として使う」という設計は、追加作業では回復できない。保存済みデータの構造上の制約である。**

本文書はこの再抽出を実施しない。実施しても得られるのは5点の観測であり、そこから軸の説明力を主張できない。

したがって本再解析が確定したのは次の3点である。

1. **軸は2つの別の操作を含んでいる**（実行経路を閉じる／モデル往復を閉じる）。往復側は軸の成立後にしか現れない（0 / 33 対 33 / 91。広い語彙で再検索しても成立前に該当なし）。**かつ軸の文書初版は往復を閉じよとは定めておらず、`model step`を診断値として観測するとだけ述べている。第2の類型は事後に単一の軸へ吸収された**
2. **軸を候補集合へ適用する判定は符号化者に依存する**（同一人物で33件中9件が変わる）
3. **経路を閉じることは採用の十分条件ではない**（48件中37件が停止）

**§12.2の構造的限界は解消していない。** 本再解析が示したのは、限界の所在がより具体的になったこと、すなわち「軸が研究の産物である」ことに加えて「軸が単一の判定基準へ落ちていない」ことである。

---

## 7. 全件の符号化表

判定入力は各行の`+追加/-削除`に対応するroot本文diffだけである。第三者が同じdiffから再符号化できる。

| 候補（identityの制御名部分） | 初回commit | 区間 | root diff | 追加label | 符号 |
| --- | --- | --- | --- | --- | --- |
| `current-copy` | 2026-07-15 | 成立前 | +0/-0 | — | `excluded` |
| `sa-routing` | 2026-07-15 | 成立前 | +8/-6 | — | `closed_path` |
| `sa-routing-test-boundary` | 2026-07-15 | 成立前 | +0/-0 | — | `excluded` |
| `revision-2` | 2026-07-15 | 成立前 | +82/-49 | — | `closed_path` |
| `command-evidence-projection` | 2026-07-16 | 成立前 | +7/-1 | — | `not_closed` |
| `completion-persistence` | 2026-07-16 | 成立前 | +1/-0 | — | `not_closed` |
| `context-efficiency` | 2026-07-16 | 成立前 | +11/-3 | — | `closed_path` |
| `control-free-generic` | 2026-07-16 | 成立前 | +0/-58 | — | `opened` |
| `control-free-repository` | 2026-07-16 | 成立前 | +0/-58 | — | `opened` |
| `executor-discretion` | 2026-07-16 | 成立前 | +12/-9 | — | `closed_path` |
| `phase-result-projection` | 2026-07-16 | 成立前 | +8/-7 | — | `closed_path` |
| `c1-counter-applicability-boundary` | 2026-07-16 | 成立前 | +2/-2 | — | `closed_path` |
| `non-machine-route-cardinality` | 2026-07-16 | 成立前 | +3/-1 | — | `closed_path` |
| `review-route-entry-boundary` | 2026-07-16 | 成立前 | +0/-0 | — | `excluded` |
| `sa-context-sufficiency-boundary` | 2026-07-16 | 成立前 | +2/-0 | — | `closed_path` |
| `selected-role-control-input-boundary` | 2026-07-16 | 成立前 | +3/-1 | — | `closed_path` |
| `task-spec-default-precedence` | 2026-07-16 | 成立前 | +23/-15 | — | `not_closed` |
| `validation-authority-precedence` | 2026-07-16 | 成立前 | +2/-2 | — | `not_closed` |
| `control-free-operation-boundary` | 2026-07-17 | 成立前 | +15/-0 | — | `not_closed` |
| `control-free-owner-result-gate` | 2026-07-17 | 成立前 | +8/-0 | — | `closed_path` |
| `owner-role-identity-binding` | 2026-07-17 | 成立前 | +3/-3 | — | `not_closed` |
| `runtime-owner-result-binding` | 2026-07-17 | 成立前 | +2/-2 | — | `closed_path` |
| `single-producer-operation-binding` | 2026-07-17 | 成立前 | +7/-1 | — | `not_closed` |
| `criterion-owner-evidence-binding` | 2026-07-17 | 成立前 | +1/-1 | — | `not_closed` |
| `gate-evidence-binding` | 2026-07-17 | 成立前 | +5/-7 | — | `not_closed` |
| `operation-qualified-evidence` | 2026-07-17 | 成立前 | +4/-4 | — | `not_closed` |
| `owner-worker-lifecycle-gate` | 2026-07-17 | 成立前 | +1/-1 | — | `closed_path` |
| `required-owner-result-gate` | 2026-07-17 | 成立前 | +3/-3 | — | `closed_path` |
| `compact-execution-control` | 2026-07-18 | 成立前 | +8/-29 | SPEC,PRODUCER,TERMINAL,OWNER | `closed_path` |
| `operation-terminal-closure` | 2026-07-18 | 成立前 | +2/-0 | — | `not_closed` |
| `owner-result-state-separation` | 2026-07-18 | 成立前 | +2/-2 | SPEC,OWNER | `closed_path` |
| `root-control-only` | 2026-07-18 | 成立前 | +0/-0 | — | `excluded` |
| `worker-context-sufficiency` | 2026-07-18 | 成立前 | +1/-0 | CONTEXT | `not_closed` |
| `criterion-result-projection` | 2026-07-19 | 成立後 | +1/-0 | PROJECTION | `closed_path` |
| `exact-evidence-location` | 2026-07-19 | 成立後 | +1/-0 | LOCATION | `not_closed` |
| `operation-result-projection-boundary` | 2026-07-19 | 成立後 | +3/-3 | SPEC,CONTEXT,ROOT | `not_closed` |
| `owner-aligned-result-unit` | 2026-07-19 | 成立後 | +1/-1 | PRODUCER | `not_closed` |
| `owner-metadata-delegation-boundary` | 2026-07-19 | 成立後 | +2/-2 | PRODUCER,OWNER_ROLE | `closed_path` |
| `result-unit-evidence-binding` | 2026-07-19 | 成立後 | +3/-3 | SPEC,CONTEXT,OWNER | `closed_path` |
| `complete-spec-readiness-boundary` | 2026-07-20 | 成立後 | +1/-1 | SPEC | `closed_path` |
| `outcome-authority-boundary` | 2026-07-20 | 成立後 | +1/-1 | SPEC | `closed_path` |
| `spec-readiness-boundary` | 2026-07-20 | 成立後 | +1/-1 | SPEC | `closed_path` |
| `applicability-domain-boundary` | 2026-07-22 | 成立後 | +2/-2 | CONTEXT,ROOT | `not_closed` |
| `atomic-spec-operation-gate` | 2026-07-22 | 成立後 | +1/-2 | SPEC | `closed_path` |
| `cross-label-predicate-deduplication` | 2026-07-22 | 成立後 | +2/-2 | PRODUCER,INDEPENDENCE | `not_closed` |
| `evidence-backed-control-core` | 2026-07-22 | 成立後 | +25/-9 | — | `closed_path` |
| `explicit-delegation-control-boundary` | 2026-07-22 | 成立後 | +3/-6 | DELEGATION,CONTEXT,COMPLETION | `not_closed` |
| `fixed-evidence-route-projection` | 2026-07-22 | 成立後 | +1/-0 | FIXED_EVIDENCE_READ | `closed_roundtrip` |
| `independent-review-operation-removal` | 2026-07-22 | 成立後 | +1/-1 | INDEPENDENCE | `not_closed` |
| `judgment-authority-boundary` | 2026-07-22 | 成立後 | +2/-3 | PRODUCER,ROOT | `not_closed` |
| `machine-decision-boundary` | 2026-07-22 | 成立後 | +1/-0 | MACHINE_BOUNDARY | `closed_roundtrip` |
| `model-reentry-decision-boundary` | 2026-07-22 | 成立後 | +1/-0 | DECISION_BOUNDARY | `closed_roundtrip` |
| `operation-method-capsule` | 2026-07-22 | 成立後 | +1/-1 | OPERATION | `not_closed` |
| `prebound-operation-graph` | 2026-07-22 | 成立後 | +8/-9 | READINESS,OPERATION,PRODUCER,TERMINAL | `closed_path` |
| `premise-dependency-boundary` | 2026-07-22 | 成立後 | +1/-0 | DEPENDENCY | `closed_path` |
| `purpose-bound-read-route` | 2026-07-22 | 成立後 | +1/-1 | READ_ROUTE | `closed_roundtrip` |
| `purpose-separated-operation-graph` | 2026-07-22 | 成立後 | +18/-8 | READINESS,OPERATION,PRODUCER,COMPLETION | `closed_path` |
| `read-only-operation-batch` | 2026-07-22 | 成立後 | +1/-1 | FIXED_READ | `closed_roundtrip` |
| `resolved-fixed-read-boundary` | 2026-07-22 | 成立後 | +1/-0 | FIXED_READ | `closed_roundtrip` |
| `resolved-premise-input-boundary` | 2026-07-22 | 成立後 | +2/-2 | CONTEXT,ROOT | `not_closed` |
| `root-independence-boundary` | 2026-07-22 | 成立後 | +1/-0 | INDEPENDENCE | `closed_path` |
| `root-operation-completion-boundary` | 2026-07-22 | 成立後 | +2/-2 | DELEGATION,COMPLETION | `not_closed` |
| `root-read-batch` | 2026-07-22 | 成立後 | +1/-0 | ROOT_BATCH | `closed_both` |
| `self-contained-execution-paths` | 2026-07-22 | 成立後 | +22/-5 | READINESS,OPERATION,PATH,SCOPE | `closed_path` |
| `shared-operation-core` | 2026-07-22 | 成立後 | +17/-7 | READINESS,SCOPE,PRODUCER,TERMINAL | `closed_path` |
| `task-closed-read-route` | 2026-07-22 | 成立後 | +1/-0 | TASK_CLOSED_READ | `closed_both` |
| `task-enumerated-read-boundary` | 2026-07-22 | 成立後 | +1/-1 | FIXED_READ | `closed_roundtrip` |
| `topology-preserving-compression` | 2026-07-22 | 成立後 | +6/-6 | SPEC,PRODUCER,TERMINAL,CONTEXT | `closed_path` |
| `validation-closure` | 2026-07-22 | 成立後 | +1/-0 | VALIDATION_CLOSURE | `closed_both` |
| `authority-bound-validation-fast-path` | 2026-07-23 | 成立後 | +9/-8 | — | `closed_both` |
| `closed-validation-state` | 2026-07-23 | 成立後 | +1/-1 | VALIDATION_CLOSURE | `closed_roundtrip` |
| `final-state-validation-wave` | 2026-07-23 | 成立後 | +3/-1 | — | `closed_path` |
| `terminal-closure-preserving-compression` | 2026-07-23 | 成立後 | +1/-1 | VALIDATION_CLOSURE | `closed_both` |
| `triggered-exception-transition` | 2026-07-23 | 成立後 | +1/-0 | EXCEPTION_TRANSITION | `not_closed` |
| `typed-execution-state-machine` | 2026-07-23 | 成立後 | +201/-11 | — | `closed_both` |
| `ordered-validation-wave` | 2026-07-26 | 成立後 | +1/-1 | VALIDATION_CLOSURE | `closed_both` |
| `project-index-navigation` | 2026-07-26 | 成立後 | +1/-0 | PROJECT_INDEX | `not_closed` |
| `root-validation-wrapper` | 2026-07-26 | 成立後 | +1/-1 | VALIDATION_CLOSURE | `closed_both` |
| `validation-wrapper-precedence` | 2026-07-26 | 成立後 | +1/-1 | VALIDATION_CLOSURE | `closed_both` |
| `producer-gate-deduplication` | 2026-07-28 | 成立後 | +1/-1 | PRODUCER | `not_closed` |
| `bound-output-route` | 2026-07-29 | 成立後 | +1/-0 | OUTPUT_INGRESS | `not_closed` |
| `concise-output-ingress` | 2026-07-29 | 成立後 | +1/-0 | OUTPUT_INGRESS | `not_closed` |
| `delegation-marginal-value-boundary` | 2026-07-29 | 成立後 | +1/-1 | OWNER_ROLE | `closed_path` |
| `delegation-value-boundary` | 2026-07-29 | 成立後 | +1/-1 | OWNER_ROLE | `closed_path` |
| `dispatch-time-worker-admission` | 2026-07-29 | 成立後 | +1/-1 | DECISION_BOUNDARY | `closed_both` |
| `parallel-worker-admission` | 2026-07-29 | 成立後 | +1/-1 | PRODUCER | `closed_path` |
| `planning-first-producer-selection` | 2026-07-29 | 成立後 | +4/-3 | PLAN,PRODUCER,OWNER_ROLE,DECISION_BOUNDARY | `closed_both` |
| `producer-local-invocation-wave` | 2026-07-29 | 成立後 | +1/-1 | DECISION_BOUNDARY | `closed_roundtrip` |
| `producer-plan-fast-path` | 2026-07-29 | 成立後 | +3/-3 | PRODUCER,OWNER_ROLE,DECISION_BOUNDARY | `closed_both` |
| `result-classification` | 2026-07-29 | 成立後 | +1/-0 | OUTPUT_INGRESS | `not_closed` |
| `tool-output-ingress-boundary` | 2026-07-29 | 成立後 | +1/-0 | OUTPUT_INGRESS | `not_closed` |
| `additional-investigation-trigger` | 2026-07-30 | 成立後 | +1/-1 | METHOD | `not_closed` |
| `compact-validation-terminal-wait` | 2026-07-30 | 成立後 | +1/-1 | VALIDATION_PLAN | `closed_roundtrip` |
| `decision-evidence-boundary` | 2026-07-30 | 成立後 | +1/-0 | EVIDENCE_SCOPE | `not_closed` |
| `decision-round-closure` | 2026-07-30 | 成立後 | +1/-1 | DECISION_BOUNDARY | `closed_roundtrip` |
| `decision-round-closure-r2` | 2026-07-30 | 成立後 | +1/-1 | DECISION_BOUNDARY | `closed_roundtrip` |
| `operation-criterion-totality` | 2026-07-30 | 成立後 | +3/-3 | SPEC,TERMINAL,OWNER_ROLE | `closed_path` |
| `outcome-source-closure` | 2026-07-30 | 成立後 | +1/-0 | OUTCOME_SOURCE | `not_closed` |
| `prechange-evidence-freeze` | 2026-07-30 | 成立後 | +1/-1 | SPEC | `closed_path` |
| `prechange-evidence-receipt` | 2026-07-30 | 成立後 | +1/-1 | SPEC | `closed_path` |
| `required-judgment-owner-boundary` | 2026-07-30 | 成立後 | +1/-1 | SPEC | `closed_path` |
| `staged-evidence-admission` | 2026-07-30 | 成立後 | +1/-0 | EVIDENCE_GATE | `not_closed` |
| `successful-validation-result-projection` | 2026-07-30 | 成立後 | +1/-1 | VALIDATION_CLOSURE | `closed_both` |
| `validation-completion-sheet` | 2026-07-30 | 成立後 | +1/-0 | VALIDATION_PLAN | `closed_roundtrip` |
| `validation-terminal-return` | 2026-07-30 | 成立後 | +1/-1 | VALIDATION_PLAN | `not_closed` |
| `validation-wrapper-reentry-closure` | 2026-07-30 | 成立後 | +1/-1 | VALIDATION_PLAN | `closed_roundtrip` |
| `authority-location-discovery` | 2026-07-31 | 成立後 | +1/-1 | EVIDENCE_GATE | `closed_path` |
| `criterion-complete-single-target-continuation` | 2026-07-31 | 成立後 | +1/-1 | EVIDENCE_GATE | `closed_path` |
| `evidence-admission-scheduling-boundary` | 2026-07-31 | 成立後 | +1/-1 | EVIDENCE_GATE | `not_closed` |
| `evidence-request-scope-closure` | 2026-07-31 | 成立後 | +1/-1 | EVIDENCE_GATE | `closed_both` |
| `explicit-authority-delegation` | 2026-07-31 | 成立後 | +1/-1 | EVIDENCE_GATE | `not_closed` |
| `implementation-authority-delegation` | 2026-07-31 | 成立後 | +1/-1 | EVIDENCE_GATE | `closed_path` |
| `implementation-bind-terminal-closure` | 2026-07-31 | 成立後 | +1/-1 | EVIDENCE_GATE | `closed_path` |
| `implementation-edit-ticket-closure` | 2026-07-31 | 成立後 | +1/-1 | EVIDENCE_GATE | `closed_path` |
| `incomplete-content-continuation` | 2026-07-31 | 成立後 | +1/-1 | EVIDENCE_GATE | `closed_path` |
| `outcome-implementation-boundary` | 2026-07-31 | 成立後 | +2/-2 | SPEC,EVIDENCE_GATE | `closed_path` |
| `prechange-evidence-wave-closure` | 2026-07-31 | 成立後 | +1/-1 | EVIDENCE_GATE | `closed_path` |
| `preterminal-result-round-closure` | 2026-07-31 | 成立後 | +1/-1 | EVIDENCE_GATE | `closed_path` |
| `spec-ready-evidence-phase-boundary` | 2026-07-31 | 成立後 | +1/-1 | EVIDENCE_GATE | `closed_path` |
| `validation-predicate-method-boundary` | 2026-07-31 | 成立後 | +3/-3 | VALIDATION_CLOSURE,VALIDATION_PLAN,METHOD | `closed_both` |
| `validation-ticket-decision-boundary` | 2026-07-31 | 成立後 | +1/-1 | VALIDATION_PLAN | `closed_roundtrip` |
| `validation-ticket-model-return-boundary` | 2026-07-31 | 成立後 | +1/-1 | VALIDATION_PLAN | `closed_roundtrip` |
| `validation-ticket-outer-wait-closure` | 2026-07-31 | 成立後 | +1/-1 | VALIDATION_PLAN | `closed_roundtrip` |
| `validation-ticket-terminal-closure` | 2026-07-31 | 成立後 | +1/-1 | VALIDATION_PLAN | `closed_roundtrip` |
