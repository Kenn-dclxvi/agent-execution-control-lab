# Candidate125〜Candidate132 六点control統合

## 結論

六点を同時に解く新しいglobal predicateは作らない。Authority、Effect state、Dependency、Closure / recoveryは既存制御で責務と再開条件を分離できている。Evidence coverageはCandidate131のF04 N=5で成立したが、N=29では低頻度failureが1件発生した。Change constructionへ独立したglobal gateを追加したCandidate132は、preimage抑止には成功した一方、Evidence coverageとEffect stateへ波及してscore `2`を1 / 5件発生させた。

Candidate131のcriterion-anchor経路を同一F04条件でN=5からN=29へ拡張した。追加24件の1件でscore `2`、全残存content fallback、変更・validation欠落が同時に発生したため停止した。stale preimageは0 / 29だった。

## 統合する理由

六点は成果の同じ段階を言い換えたものではない。各点が異なる入力と遷移を所有する。

1. Authority: 何を成果として要求するか、実装方法をどこから解決できるか。
2. Evidence coverage: その判断に必要なcurrent contentをmodelが受領したか。
3. Effect state: TaskSpecの各required effectが開始状態で充足済みか、未充足か。
4. Dependency: 複数effectの成立関係がTaskSpecの成果条件に含まれるか。
5. Change construction: 発行する変更が観測済みcurrent contentから構成されているか。
6. Closure / recovery: 変更result後もrequired effect集合を落とさず、validation、rework、停止を選べるか。

一つのpredicateへまとめると、変更前の未観測と変更後の未充足が同じfalseへ潰れる。Candidate126、Candidate129、Candidate132のfalse stopは、この混線が実害になることを示した。

## Point 1 Authority

### 既存制御

Candidate116は、利用者に観測可能なrequired outcomeの確定と、repository authorityから解決するimplementation choiceを別状態にした。Candidate118はimplementation choice、target、保持constraint、変更predicateがbindされた時点を変更前evidence operationのterminal resultにした。Candidate125、Candidate128、Candidate131はこの境界を継承している。

### 証拠

- Candidate116 Standard14 N=5: 70 / 70 score `4`。
- Candidate118 Standard14 N=5: 70 / 70 score `4`。
- Candidate118 A02 N=20: 20 / 20 score `4`、implementation bind後・変更前command再入0 / 20。

### 判定

新Candidateは不要である。将来、required outcome未確定のまま変更する、またはrepository authorityで一意に解決できるimplementationをauthority不足として停止する保存traceが出た場合だけ再開する。

## Point 2 Evidence coverage

### 既存制御

Candidate131は、未観測criterionごとにTaskSpecまたは受領済みcontent中の完全一致可能なanchorをbindし、同一target内の全一致箇所と周辺contentを一回で直接取得する。

### 証拠

F04 N=5は5 / 5 score `4`、direct anchor content 5 / 5、全残存content fallback、locator-only、false stopは各0 / 5だった。

### 判定

初段mechanismは通過したが、N=29ではdirect anchor 28 / 29、全残存content fallback 1 / 29、score `4 / 2 = 28 / 1`となった。低Score runはexact anchorを受領済みでもglobal readinessをfalse側として扱った。Point 2の低頻度安定性は未達である。

## Point 3 Effect state

### 既存制御

Candidate128の`required_effects_closed`は、TaskSpecの各required effectを、artifact変更resultで適用済み、または初回変更前evidenceで開始状態から充足済みへbindする。

### 証拠

F02、F04、F07各N=5の15 / 15件がscore `4`だった。F02は両source effect、F07はdependency pairを各5 / 5で保持した。F04は開始状態で正しい`colSpan`を5 / 5で保持し、未充足の`hasAuditKey`だけを5 / 5で変更した。

### 判定

新しいeffect admission predicateは追加しない。Candidate129は未観測effectを理由に観測済み未充足effectまで止め、3 / 5件でfalse stopとなった。Effect stateの入力はTaskSpec、model-visibleな変更前evidence、変更resultに限定する。

## Point 4 Dependency

### 既存制御

dependency自体がrequired outcomeならTaskSpecがpairまたは関係を固定し、Candidate128が全required effectをclosureまで保持する。

### 証拠

F02はdependency graphを新設せず両effectを5 / 5で閉じた。F07はTaskSpec明示pairを5 / 5で閉じた。Candidate131 F04の上流一行変更4件と下流3式変更1件はいずれもscore `4`で、後者に品質・cost実害は観測されていない。

### 判定

新Candidateは不要である。implementation methodとして上流変更を強制しない。全effectがclosedなのに依存不整合が残る保存traceが出た場合だけ再開する。

## Point 5 Change construction

### 試した制御

Candidate132は、発行予定変更がcurrent artifactとの一致を要求する削除行、置換前文字列、contextだけを最新のmodel-visible evidence中のexact valueへbindした。

### 証拠

F04 N=5でstaleまたは未観測preimageを持つ変更は0 / 5、必要な`hasAuditKey`変更は5 / 5だった。一方、direct anchor routeは4 / 5へ下がり、1件が全残存content fallback後に正しい変更だけを適用したものの、未観測の`colSpan` effectをclosedにできずvalidationを開始しなかった。score分布は`4 / 2 = 4 / 1`である。

### 判定

独立したglobal preimage gateは不採用とする。C132は停止する。C131 N=29でもstale preimageは0件だったため、Point 5を独立問題として再開しない。C131自体はPoint 2 stability gateで停止し、次案を作る場合はC128へ戻ってglobal readiness判断だけを置換する。

## Point 6 Closure / recovery

### 既存制御

Candidate128は各artifact変更result後に同じrequired effect集合を再判定する。全effectがclosedならvalidationへ進む。falseかつ一回のmachine reworkが可能なら、充足済みeffectを保持し、変更前にcurrent contentへbind済みの未充足effectだけを再発行する。未充足effectのcurrent contentが未bindなら停止する。

### 証拠

Candidate128 F04の初回atomic変更失敗3件は、追加readなし、一回のreworkで全件回復した。Candidate132のscore `2`は、model-visible evidenceで`colSpan`開始状態を確認できなかったため停止したもので、未証明effectを推測でclosedにしない保守側動作である。

### 判定

新Candidateは不要である。closureを緩めず、変更前coverage不足を変更後readやvalidation成功で代用しない。

## 次の検証

Candidate131 F04の既存5 atomic runを再利用し、追加24 runだけを発行して合計N=29にした。profileの`max_workers`はM=24に固定し、比較前にCandidate131 N=5 resultを直接bindして、prompt以外の互換条件とcandidate poolを機械照合した。

停止条件は次のとおりである。

- score `3`以下が一件でも発生する。
- direct anchor contentを使わず全残存content fallbackへ進む。
- staleまたは未観測preimageを持つ変更を発行する。
- 必要なartifact変更またはrequired validationを欠く。

score `2`、全残存content fallback、必要変更・validation欠落が同じ1件で発生し、停止条件に到達した。Point 2のF04 N=29 stabilityは不通過である。Point 5はF04の29件すべてでstale preimage 0件だったため、独立predicateを追加しない。

## 結論表

| Point | 現在のowner | 実測状態 | 新Candidate | 次の扱い |
| --- | --- | --- | --- | --- |
| 1 Authority | C116 / C118 | Std14各70 / 70、A02 N=20通過 | 不要 | 反例trace時だけ再開 |
| 2 Evidence coverage | C131 | F04 N=5通過後、N=29でscore `2` 1件 | C131停止 | C128からglobal readiness判断の置換を検討 |
| 3 Effect state | C128 | F02・F04・F07計15 / 15通過 | 不要 | 未充足effect脱落時だけ再開 |
| 4 Dependency | TaskSpec + C128 | pairと複数effectを各5 / 5保持 | 不要 | closed後の依存不整合時だけ再開 |
| 5 Change construction | Point 2 evidenceに従属 | C131 N=29でstale 0件、C132はscore `2` 1件 | C132停止 | 独立global predicateを追加しない |
| 6 Closure / recovery | C128 | F04初回失敗3件を一回で回復 | 不要 | closure誤判定時だけ再開 |
