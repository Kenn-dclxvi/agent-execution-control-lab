# Candidate198停止後のC147構造化変更前review方向レビュー

> **結果**: `direction_review_passed_after_revision / initial_blocking_counterexamples_3 / unresolved_blocking_counterexamples_0 / reviewed_states_20 / candidate_implementation_allowed`

## 結論

[`C147構造化変更前review設計`](post-candidate198-c147-structured-prechange-review-design.md)を、case名に依存しない20状態で確認した。初稿には、C147の`EVIDENCE_GATE`がreview前にartifact変更へ進める競合、C147の開始経路をそのまま戻すことでADR9 r2のidentity/read共同発行を再現する競合、三result kindのterminal条件不足という3件のblocking counterexampleがあった。

設計を改訂し、`START_BOUNDARY`、`EVIDENCE_GATE`末尾の`prechange_transition`、一つの`PRECHANGE_REVIEW` lifecycleへ責任位置を分けた。`PRECHANGE_REVIEW`内部は八責任へ分けるが、責任分離自体をtool発行、producer起動、result待機またはmodel step分割にしない。改訂後の20状態では未解決blocking counterexampleは0件となった。

次に許可するのは、Candidate147を直接親とする新Candidate prompt artifactの作成と静的検証である。Candidate175、Candidate191またはCandidate198のprompt本文を親または差分元にしない。評価profile、case、rating contractおよび評価slotはCandidate実装と静的検証が完了するまで作成しない。

## レビュー入力

- [`C147構造化変更前review設計`](post-candidate198-c147-structured-prechange-review-design.md)
- Candidate147の13条項原文
- Candidate175のADR9 r2 / Standard14 N=5保存結果
- Candidate191の責任構造とStandard14コスト機序再判定
- Candidate197とCandidate198のADR9 r2保存結果および機構監査
- ADR9 r2とStandard14のmodel-visible TaskSpecが固定する開始stop scope、review contractおよび変更境界

private oracle、case ID、期待terminal、採点用commandおよび過去findingを一般状態の判定入力にしない。保存結果は具体的な誤経路と成立経路の診断にだけ使い、後続Candidateのprompt本文または機構を継承しない。

## 初稿で成立したblocking counterexample

### 1. `implementation_bound`後の変更直結

C147の`EVIDENCE_GATE`は、`implementation_bound=true`を変更前evidence operationのterminal resultとし、未発行evidenceを失効して次にartifact変更を発行する。初稿はC147の13条項を保持したまま、その後へreviewを置こうとしていたため、明示reviewが必要でもreview前のartifact変更を禁止できなかった。

修正版では`EVIDENCE_GATE`末尾のこの遷移だけを`prechange_transition`へ置換した。review非適用なら直接変更、review適用かつreadyならreview、適用されるがreadyでなければ変更せず`unavailable`とする。admissibleな`no_counterexample_found`だけが同じ変更predicateを開く。

### 2. C197の開始経路退行の再現

初稿は通常発行順序をC147へ完全に戻していた。しかしCandidate197では最初の実repository operationを三値identityだけに限定できたrunが4 / 45で、41件がidentityとreadを共同発行した。ADR9 r2のmodel-visible TaskSpecはidentity mismatch時にreadを含むrepository operationを禁止するため、この経路を戻すとreview接続が正しくても開始機構で停止する。

修正版では全operationの候補選択を追加せず、開始identity、mismatch時stop scope、required result valueおよび最初の実repository operation集合だけを`START_BOUNDARY`へ固定した。mismatch時にreadも禁止する場合はidentityだけ、readを禁止しない場合はC147の`DECISION_BOUNDARY`に従って必要readと共同発行する。

### 3. 三result kindのterminal条件不足

初稿の`current_review_result_admissible`はresult kindと観測の対応だけを要求し、具体的反例、反例なし、判断不能の成立条件を分けていなかった。このままでは、無関係なmissingで真正counterexampleを失効させる、required scope未確認で`no_counterexample_found`を受け入れる、一般的不確実性だけで`unavailable`にする経路が残った。

修正版では`counterexample_result_ready`、`no_counterexample_result_ready`および`unavailable_result_ready`を別条件にした。result admissionはresult kindに対応するterminal条件の成立を要求し、rootは意味判断を再実施しない。

## 改訂後の責任配置

```text
START_BOUNDARY
  -> C147通常operation
  -> implementation_bound
  -> prechange_transition
       -> review非適用: artifact変更
       -> review適用: PRECHANGE_REVIEW
  -> artifact変更
  -> C147 required validation
  -> terminal
```

`PRECHANGE_REVIEW`の内部責任は次の八つである。

1. `APPLICABILITY`
2. `EXECUTION_PERMISSION`
3. `OPERATION_READY`
4. `PACKET`
5. `OBSERVATION`
6. `JUDGEMENT`
7. `RESULT_ADMISSION`
8. `CHANGE_EFFECT`

これはC191の責任追跡上の長所を使うための構造であり、八つのoperationまたはmodel stepではない。`dispatch_dependency(a, b)`は`a.result`が`b`の必要性、target、permission、methodまたはstop conditionを変え得る場合だけ成立する。

## 一般20状態

| # | 一般状態 | 必須経路 | 判定 |
|---:|---|---|---|
| 1 | 開始identity contractなし | `START_BOUNDARY`非適用でC147通常経路 | 反例不成立 |
| 2 | mismatch時にreadを含むrepository operation禁止 | 最初はidentity一件だけ | 反例不成立 |
| 3 | mismatch時に変更とrequired commandだけ禁止 | identityと必要な固定済みreadを同じmodel stepから発行可能 | 反例不成立 |
| 4 | methodの既知outputがrequired identity valueの一部だけ | 開始methodとして選ばない | 反例不成立 |
| 5 | 全fieldを返し得るmethodの実resultだけがfield不足 | outer `unavailable`へ早期変換せず同じpredicateへ継続 | 反例不成立 |
| 6 | identity mismatch | TaskSpecが禁止したoperationを発行せず固定stopへ閉じる | 反例不成立 |
| 7 | identity一致 | `START_BOUNDARY`を再開せずC147通常経路へ進む | 反例不成立 |
| 8 | 明示review contractなし | review operation、packet、producerおよび追加stepなしで変更へ進む | 反例不成立 |
| 9 | review contractのrequired scopeが空 | owner語列に関係なくreview非適用 | 反例不成立 |
| 10 | 明示review、permission allowed、packet形成可能 | `implementation_bound`後にreviewを一件だけ起動 | 反例不成立 |
| 11 | 明示review、permission denied | reviewerも変更も発行せず`unavailable` | 反例不成立 |
| 12 | 許可fieldまたはprovenance不足 | rootが補完せずreviewerも変更も発行しない | 反例不成立 |
| 13 | descriptor固定済みtargetがmissing | operationは起動し、reviewerがnon-value observationとして扱う | 反例不成立 |
| 14 | concrete counterexample成立かつ無関係なmissingあり | `counterexample_found`をadmitし、対応変更だけを`blocked` | 反例不成立 |
| 15 | required scopeと必要manifestが全件valueで反例なし | `no_counterexample_found`をadmitし、他のC147 gate後に変更 | 反例不成立 |
| 16 | 未解決predicateとそれを閉じ得るnon-valueあり | `unavailable`をadmitし、対応変更を許可しない | 反例不成立 |
| 17 | producerまたはsessionがnonterminal | review operationもnonterminalで変更しない | 反例不成立 |
| 18 | producer terminalだがsender、subjectまたはcertificate不一致 | C147の既存結果境界に従い`unavailable`、root補完なし | 反例不成立 |
| 19 | review非適用のread-only成果 | 追加reviewを形成せず、TaskSpec明示producerがあればC147 `PRODUCER`で扱う | 反例不成立 |
| 20 | `counterexample_found`後に別案を試す | 同一reviewを再開せず、新しい変更predicateとsubject identityで開始 | 反例不成立 |

## 通常経路とコスト境界

review非適用時は`prechange_transition`の分類だけでartifact変更へ進み、review operation、packet、producer、observationまたはmodel returnを作らない。Standard14では追加reviewer 0件を固定機構条件とする。

開始時の発行集合はreview責任から独立させる。Standard14でidentity resultが許可済みreadの必要性、targetまたはpermissionを変えない場合、C147の共同発行を維持する。ADR9 r2でmismatchがreadを禁止する場合はidentityだけを先行させる。責任名またはlifecycle順序だけを理由にmodel stepを分けない。

prompt bytes、条項数または責任数の削減を効率成立の代用にしない。ADR9通過後のStandard14でmodel step、生trace、all-agent tokenおよびelapsedを保存し、共同発行退行の有無を直接確認する。

## 実装許可境界

次Candidateは次の形に限定する。

- direct parent: Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`
- changed target: root `AGENTS.md`だけ
- C147の既存13条項のうち、`EVIDENCE_GATE`末尾の一遷移だけを置換
- 新規top-level条項: `START_BOUNDARY`と`PRECHANGE_REVIEW`の二件
- `PRECHANGE_REVIEW`内部: 八責任。ただし責任ごとのoperation、tool callまたはmodel stepを作らない
- current review resultだけを扱い、保存済みprior result再利用を入れない
- ticket、receipt、ledger、adjudication commandまたは共通dispatch機構を追加しない
- 評価系列はADR9 r2全9ケースN=5を先に行い、通過後だけStandard14全14ケースN=5を行う

Candidate artifact作成時点は`not_evaluated`とする。静的検証はdirect parent、target集合、非変更18 target、C147の12条項逐語保持、`EVIDENCE_GATE`差分位置、二新規条項、禁止機構不在および歴史的Candidate identity不在を確認する。

## 状態

`post_candidate198_structured_prechange_direction_review_passed / initial_blocking_counterexamples_3 / unresolved_blocking_counterexamples_0 / reviewed_states_20 / c147_direct_parent_required / start_boundary_and_prechange_review_separated / evidence_gate_transition_only / responsibility_not_model_step / current_result_only / ADR9_then_Standard14_only / candidate_implementation_allowed / candidate_not_created / profile_not_created / evaluation_not_started`
