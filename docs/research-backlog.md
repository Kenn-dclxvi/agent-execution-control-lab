# 研究バックログ（未完了項目の索引）

現在**未完了**の研究項目を、着手判断のために一箇所へ集める索引。長期方針は[`future-roadmap.md`](future-roadmap.md)、系譜と観測は[`candidate-history.md`](candidate-history.md)を参照する。

この文書は索引であり、判定の正本ではない。各項目の状態・数値・停止理由は「正本」列のartifactを正とする。ここに載っていることは、着手済み・評価済み・採用予定のいずれでもない。

## 1. label監査の未完了（再測定にfresh runが必要）

`Candidate71`の11 label監査で「根拠なし」判定が**暫定**のまま残る3件。いずれも既存の保存データでは決着しない。正本は[`candidate71-control-abstraction-analysis.md`](candidate71-control-abstraction-analysis.md)の「監査状況の分類」表。

| 項目 | 必要な再測定 | 結論をflipし得るか |
| --- | --- | --- |
| `CONTEXT`（`X1`） | A06 paired diagnostic。新規A06 case variant、bundle、gate、fresh runが必要。既存archiveでは事前sizingも不可 | **あり**。拡張方向（packet resolved premiseによる再読削減）が未検証 |
| `INDEPENDENCE`（`I1` = `F9`） | A / D scopeでの削除評価。Candidate68はF10-onlyのみ実測でun-run | 低い。F10ではruntime非改善 |
| `RECOVERY`（`R1 / R2`） | `environment_recovery_max>0`の正のrecovery scenario caseでの評価。現Evaluation setは`not_applicable`でun-run | 不明（効果未測定） |

## 2. `PRODUCER`の`P3`一文削除candidate（作成前gate定義済み・bundle未作成）

11 label監査で唯一「Candidate作成根拠あり」となった項目。`P3`の正本は`OWNER_ROLE`側にあり、`PRODUCER`側の短い再記述だけを削除する。gate 9項目は定義済みで、bundle・profile・評価は未着手。

- 正本: [`candidate71-control-abstraction-analysis.md`](candidate71-control-abstraction-analysis.md)（`PRODUCER`監査結果節と作成根拠節）
- 評価計画: Candidate71から`P3`一文だけを削除し、D01正例＋root-onlyでtargeted評価。新しいEvaluation setやrating revisionは作らない
- **番号に注意**: 同分析が作業呼称として使う「Candidate74」は、実際には別軸の`the-caption-3ce91a4-typed-execution-state-machine-r1`へ割り当て済みである。着手時は[`prompts/candidates/README.md`](../prompts/candidates/README.md)で現行の番号割当てを確認し、新しい番号で作成する

## 3. A01の3択variation診断

**未実施。** A01の現行2択caseを回帰基準として維持したまま、3択以上の未固定modeを持つvariationを診断用に追加する。設計条件は次のとおり。

- 2択で非現行値を選び、3択では確認して停止するなら、補集合選択の可能性が高い。
- 3択でも特定値を選ぶなら、mode名の意味、候補順序、現在値、test期待値などをauthorityへ変換している可能性を調べる。
- 現在値と候補順序を回転し、曖昧なら停止するcaseとrepository authorityから一意に解決できるcaseを対にして、過剰停止と未指定値補完の両方を観測する。

case追加の一般規則（追加根拠の限定、既存revisionを上書きしないこと、反復数の固定）は[`future-roadmap.md`](future-roadmap.md)の「評価setの役割と育て方」節を正本とする。

## 4. 投影済みCandidate71のrisk（当時の記録と現在解釈を分離）

Candidate71は評価上`stopped`（v12の品質gate不通過）のまま、別の採用判断でTHE-CAPTION本体へ投影済みである。当時のrelease artifactに保存された未解決riskは2件で、これはimmutableな記録として取り消さない。一方、rating v13による現在解釈では、この2件の位置づけが分かれる。

| 当時のrelease risk（v12時点） | 観測 | rating v13後の現在解釈 |
| --- | --- | --- |
| A02で`git diff --check`欠落 | 3 / 90件 | **現在の未完了研究項目ではない。** 実行役へ提示していない特定コマンドを採点側が必須化した「要求と採点のずれ」であり、本物の品質低下と区別される。v13でこのずれを塞いだ |
| A01で未固定modeを確認せず実装・試験へ進んだ誤実行 | 1 / 90件 | **現在も残る品質上のrisk。** v13でも品質上の問題として扱う |

- 当時の未解決riskの正本: [`Candidate71 release / projection`](../prompts/releases/the-caption-3ce91a4-validation-closure-release-r1/README.md)（v12結果は履歴として保持）
- 現在解釈の正本: [`control-mechanisms.md`](control-mechanisms.md)のrating v13節と[`a02-rating-divergence.md`](a02-rating-divergence.md)
- したがって研究項目として残るのはA01側の挙動である。A01の未固定mode確認は上記「3. A01の3択variation診断」と同じ論点に接続する

## 5. F10 location mismatch: exact coordinateのevidence interface（別軸）

**原因診断そのものは実施済みで、prompt側の変更は停止している。** `CLAIM_PROVENANCE` collectorと90件backfillの後、30件checkpoint診断（`max_30_diagnostic_valid_without_location_mismatch`で停止）、追加105件、coordinate representation診断、delayed reconstruction診断、implicit coordinate passive case-control、real-Agent representation recency診断、recorded-state collision受動監査まで到達した。

正本の現在判断は、repository-wideに削除できるprompt判断点を確認できないため、**prompt変更と追加model runをここで止める**ことである。残る未完了項目は次の一点。

- exact coordinateがhard requirementである場合に限り、modelが選んだexact line textをdeterministicなsource indexでone-based coordinateへ変換する**evidence interface要件を別軸で検討**する。prompt制御の変更軸としては扱わない。
- 正本: [`review-location-cause-diagnostic-plan.md`](review-location-cause-diagnostic-plan.md)（「対策判断への接続」節と各診断結果節）
- 制御graph側の判断（location mismatchを理由にroot規則を追加しない）は[`prompt-control-graph-review.md`](prompt-control-graph-review.md)を参照

## 6. 現行rating contract identity、一律比較、reasoning追試（解決済み・2026-07-26）

新規runへ適用する現行rating contractの指定が、評価基盤の正本（`owner-producer-quality-v8`）と後続文書（最新revision v13）で一致していなかった。**2026-07-25に現行をv13へ確定した。** 正本[`prompt-comparison-workflow.md`](prompt-comparison-workflow.md)の指定、評価実行手順[`evaluation-loop-manual.md`](evaluation-loop-manual.md)のLayer 3、契約台帳[`evaluations/rating-contracts/README.md`](../evaluations/rating-contracts/README.md)、および`scripts/evaluation_loop.py`の`SUPPORTED_QUALITY_RATINGS`をv13へ追従させ、v13 capsuleが受理されることをunit testで確認済みである。この項目は未完了ではない。

派生作業も2026-07-26に完了した。reasoning effortはcomparison conditionであり、水準ごとにcompatibility keyが異なる。水準内のprompt比較と、水準間の記述的比較を混同しない。

- [`Baseline、ControlFreeRepository、Candidate5、Candidate35、Candidate43、Candidate71のHigh標準14項目各N=5`](../evaluations/results/baseline-control-free-repository-c5-c35-c43-c71-v13-standard14-n5_2026-07-26.md)を最初のv13互換result集合として登録した。6条件 × 70件 = 420件で、v12以前のresultは同一comparisonへ混ぜない。
- [`Candidate71のreasoning 6水準`](../evaluations/results/candidate71-reasoning-levels-v13-standard14-n5_2026-07-26.md)を、`low` / `medium` / `high` / `xhigh` / `max` / `ultra`、標準14項目各`N=5`で記録した。`medium`がtoken中央値最小、`low`がelapsed中央値最小だった。
- [`6条件のMedium一律比較`](../evaluations/results/baseline-control-free-repository-c5-c35-c43-c71-v13-reasoning-medium-standard14-n5_2026-07-26.md)も420 / 420件を登録した。C71とC43のtoken中央値差はHigh `-31.47%`、Medium `-29.19%`であり、少なくともこの2水準ではeffort低下によって相対的な制御差は消えなかった。
- 2026-07-27以降の新規通常比較は`medium`を運用基準とする。既存`high` resultは履歴として保持し、reasoning effort自体の比較または既存互換条件の再現だけを例外とする。運用正本は[`evaluation-loop-manual.md`](evaluation-loop-manual.md)である。

## 7. `QUALITY_RATING`という汎用名がv8を指している（保守上の誤認risk）

`scripts/evaluation_loop.py`では現行契約が`QUALITY_RATING_V13`として登録されている一方、revision名を持たない汎用定数`QUALITY_RATING`は`owner-producer-quality-v8`を指し続けている。integration testの既定`quality_rating`もこの定数を使う。

- **実行上の不具合ではない**。run capsuleは`quality_rating`の明示指定を必須とし、v13は`SUPPORTED_QUALITY_RATINGS`へ登録済みで、v13の実挙動はunit testで検証している。
- 残るのは保守上のriskで、汎用名が現行契約を表すように見えるため、将来の変更時にv8を現行と誤認し得る。
- 解消するにはv8定数の改名（例: `QUALITY_RATING_V8`）とtest既定値の見直しが必要で、複数testの既定経路へ波及する。現行identityの確定（項目6）とは別の判断単位として扱う。

## 8. Layer 2 executorのClaude Code CLI置換（設計検討済み・実装未着手）

Layer 2 executorをCodex CLI（`codex exec`）からClaude Code CLI（`claude -p`）へ置き換える試験方法。2026-07-25に設計検討と前提のprobe実測を行い、**実装、pilot、本測定はいずれも未着手**である。

- 正本: [`claude-code-cli-evaluation-adapter-design.md`](claude-code-cli-evaluation-adapter-design.md)（実測値、adapter対応表、新設schema revision、未確定事項6件、段階計画Phase 0〜4）
- **Phase 0が先行条件**: 認証方式（API key + `CLAUDE_CONFIG_DIR`隔離、またはsubscriptionのまま開始gateで確認）が未決で、環境identityの固定方法がこの決定に依存する。決まるまでPhase 1のprobe設計を固定できない。
- 実装対象は新規adapterと新規collectorであり、既存の`scripts/run_codex_evaluation.py`、既存collector、既存registry resultは変更しない（[`scripts/AGENTS.md`](../scripts/AGENTS.md)）。
- **既存Codex resultとの互換比較は成立しない**。注入時点の差とtoken accountingの意味の差によりcompatibility keyが一致しないため、Claude Code条件はbaselineから再測定する独立系列として扱う（[`evaluations/AGENTS.md`](../evaluations/AGENTS.md)のCompatibility）。
- model名を明示したresultはすべて`gpt-5.6-sol`で、Claude系modelでの測定は0件である（[`execution-control-research-paper.md`](execution-control-research-paper.md)の限界節）。この項目はその限界に接するが、この項目自体はmodel比較を目的としない。executor置換の成立条件だけを扱う。

## 9. root `AGENTS.md`へのrepository index参照追加の効果（実施済み・停止）

**2026-07-26にCandidate78として実施し、停止した。** 投影済みCandidate71を直接sourceとし、root `AGENTS.md`へ条件付き`PROJECT_INDEX`一labelだけを追加した。index本文、残り18 target、評価条件は変更していない。

標準14項目各`N=5`は70 / 70件がscore `4`だったが、Candidate71比でall-agent token中央値は`+8.66%`、elapsed中央値は`+4.38%`だった。A02はindexを5 / 5で先に読んでもrepository-wide探索が5 / 5で残り、F10 Entryでは不要なindex readが2 / 5に増えた。事前停止条件に従い、追加改訂、採用、release、本体反映へ進めない。数値とidentityの正本は[`Candidate71 / Candidate78標準14結果`](../evaluations/results/candidate71-candidate78-project-index-navigation-v13-standard14-n5_2026-07-26.md)とする。

以下は着手前に固定した試験境界である。

- 変更単位: root `AGENTS.md`への参照追加1軸のみ。index本文はbundle targetとして既に固定済みのため、残り18 targetはcontent identicalなcandidate bundleになる。
- 観測: 3 KPI（`quality_score` / all-agent `total_tokens` / `elapsed_seconds`）を評価対象とし、target探索readとworker起動はdiagnosticへ置く。境界の正本は[`evaluations/AGENTS.md`](../evaluations/AGENTS.md)。
- 事前に両方向の仮説を置く。静的事実の参照でrepository探索readが減る方向と、root promptへの追加がcontextを増やすだけで動的tokenが増える方向の両方である。表面的なprompt短縮がall-agent tokenをほとんど動かさなかった既存知見（正本: [`control-mechanisms.md`](control-mechanisms.md)）から、静的byteの増減で効果を推定しない。
- read boundary / read route系candidate（C50、C56〜C59、C62、C63など）と論点が接近する。着手前に系譜を確認し、既存軸の再実行にならないことを確かめる。正本は[`prompts/candidates/README.md`](../prompts/candidates/README.md)と[`candidate-history.md`](candidate-history.md)。
- 比較条件: 既存Codex executor、標準14項目、rating v13で測れる軸である。項目6で取得したv13 Baselineをcomparisonへ使用できるが、repository index参照を追加するcandidateは別profile・別resultとして新規実行する。
- 項目8（Claude Code CLI executor置換）と同一比較単位へ混ぜない。executor変更とprompt変更を同じ比較単位へ入れない（root [`AGENTS.md`](../AGENTS.md)の共通変更規律）。
- candidate作成前gate 9項目（[`prompts/AGENTS.md`](../prompts/AGENTS.md)）を通してからbundleを作る。

## 10. 公開target repositoryでの計測系列と評価基盤のrepository汎用化（Bundle A / B Std14完了）

公開repositoryを対象とする独立系列として`pallets/click`を登録し、同じBundle Aで14 caseのqualification、追加case各`N=3`、Std14 `N=5`をLayer 1〜4まで実行した。**Std14は70 / 70件がvalid・rateableかつscore `4`である。** この項目が扱うのは、公開repositoryで計測系列を成立させ、その過程で「任意のtarget repositoryへ同じ手順を適用できる分離」を確定することである。prompt制御の新しい変更軸ではなく、計測条件側の軸である。

2026-07-26時点で次を完了している。

- target instance `click`を`layout: namespaced`、公開・第三者再現可能として登録
- control-free baseline bundle `click-00e592c-control-free-r1`を固定
- `CLICK-F01-ANSI-SEQUENCE-STRIP` r1を作成し、seed適用前後のfocused / full gateでfixtureをqualification
- `click-outcome-abstract-condition-preserving-v1`、`click-f01-only-r1`、P1-a profile r1 / r2を固定
- Codex CLI `0.144.0`、Python `3.14.5`、共有venv identityをprofileへ固定
- r1 profileはLayer 2開始前にall-agent token accounting宣言不足を検出し、result 0件のまま停止。履歴を上書きせず、r2でtoken accountingとrequired command evidence protocolだけを追加
- r2でP1-aを完了。quality `100.000`（raw score `4`）、all-agent token `180,871`、elapsed `77.811`秒、excluded attempt 0件
- `click-control-free-f01-only-global-m24-n5-r1`でP1-bを完了。5 / 5件がscore `4`、all-agent token中央値`189,977`（最小`170,228`、最大`202,176`）、elapsed中央値`80.475`秒（最小`79.323`、最大`85.443`秒）、excluded attempt 0件
- 同じ`N=5` profileを独立3 resultへ反復してP1-cを完了。15 / 15件がscore `4`、batch中央値の中央値はtoken `189,033`、elapsed `80.590`秒。batch中央値rangeはtoken `26,878`（`14.22%`）、elapsed `1.501`秒（`1.86%`）で、excluded attemptは全batch 0件
- F02 `CLICK-F02-STREAM-DEPRECATION-CONTRACT` r1をqualification。2 source fileの公開・非公開API contractをseedし、seed前focused `72 passed, 1 skipped`、seed後`2 collection errors`、fixture 2回のcommit / tree一致を確認
- rating contract v2、`click-f02-only-r1`、F02 N=3 profileを固定し、3 / 3件をscore `4`で登録。all-agent token中央値`303,563`、elapsed中央値`130.225`秒、excluded attempt 0件
- 残り12 caseを固定し、追加caseだけ各`N=3`で確認。現行revisionはすべて3 / 3件がscore `4`。F07 r1はcommand evidence照合不能の未rating履歴、F07-P r1 / r2は各3 / 3件score `3`の失敗履歴として保持
- runtime r2へ`uv==0.11.32`を追加し、identity `0a30733685c5fb3bb69abf136d6a8cdb04c4ec323f52dc6d1488f8d49a7cc952`を固定。F07-P r3はworkspace-local uv cacheで3 / 3件score `4`
- `click-standard14-r1`、rating v10、Std14 profileを固定し、70 / 70件をscore `4`で登録。5 iterationのall-agent token中央値`2,860,702`、elapsed中央値`1,235.719`秒、excluded attempt 0件
- THE-CAPTION Candidate81のroot本文をbyte-identicalに1 targetへ適用したBundle Bを固定し、同じStd14条件で70 / 70件をscore `4`として登録
- Bundle AからBundle Bはquality中央値差`0.000`、all-agent token中央値`-685,546`（`-23.96%`）、elapsed中央値`+35.384`秒（`+2.86%`）。THE-CAPTIONでのtoken削減方向は再現したが、elapsed短縮は再現しなかった
- 今後の運用基準を`medium`へ切り替え、Bundle AとC81全文のMedium Std14を各70 / 70件・全件score `4`で登録した。C81全文はBundle A比でtoken中央値`-28.79%`、elapsed中央値`-12.62%`となり、5 / 5 iterationでelapsedが短縮した
- THE-CAPTION ControlFreeRepositoryとの構成差を分離するため、Clickでtarget-local No-AGENTSとrootなしRepository sub-AGENTSをMedium Std14 N=5で比較した。両条件70 / 70件がscore `4`で、sub-AGENTS側はtoken中央値`+3.74%`、elapsed中央値`+7.90%`だった。ただしsub本文の初期context注入は0 / 70で、本文をreadしたA01 5 / 5だけがtoken中央値`+80.47%`となった。配置だけでは全caseへ水平適用されないため、Std14全体の本文効果とは扱わない

Bundle AのHigh一次結果は[`click control-free Std14 N=5`](../evaluations/targets/click/results/click-control-free-standard14-n5_2026-07-26.md)、Medium一次結果は[`click control-free Medium Std14 N=5`](../evaluations/targets/click/results/click-control-free-reasoning-medium-standard14-n5_2026-07-27.md)、HighでのBundle A / B比較は[`Click Control-Free / C81全文 Std14 N=5`](../evaluations/targets/click/results/click-control-free-c81-full-standard14-n5_2026-07-26.md)、Medium比較は[`Click Control-Free / C81全文 Medium Std14 N=5`](../evaluations/targets/click/results/click-control-free-c81-full-reasoning-medium-standard14-n5_2026-07-27.md)、sub instruction配置比較は[`Click No-AGENTS / Repository sub-AGENTS Medium Std14 N=5`](../evaluations/targets/click/results/click-no-agents-repository-subagents-reasoning-medium-standard14-n5_2026-07-27.md)を正本とする。High / MediumのBundle A traceとTHE-CAPTION ControlFreeRepository Mediumを使った[`baseline分析`](click-control-free-medium-baseline-analysis.md)では、Clickの軽さはreasoning量だけでなく、tool出力量`-50.46%`と小さいrepository contextに強く対応した。sub instruction配置追試により、THE-CAPTION側の4つのsub本文が常にmodel contextへ入っていたという仮定は置けなくなった。C81 MediumによりA02 / F06は大きく改善した。後続の[`残余経路分析`](click-c81-medium-residual-analysis.md)では、F01のtoken増加はpaired差中央値`-970`で安定悪化ではないと判定した。F04はC81でgit history探索がHigh / Medium合計`4 / 10`、Control-freeで`0 / 10`となり、両reasoningでelapsed合計が約16〜18%増えた。次operationはC81全文へ`PRECHANGE_EVIDENCE_SCOPE`一文だけを追加したClick CandidateのF04 Medium N=5 targeted gateである。新規制御探索とClick向け文言最適化は別判断とし、採用、release、runtime projectionも別gateとする。

### 現在の依存範囲（2026-07-26に実測）

repository非依存な層とtarget固有な層は次のとおりである。

| 層 | artifact | 実測した状態 |
| --- | --- | --- |
| Layer 1 fixture | `scripts/prepare_case_fixture.py` | CLI引数は`--case` / `--source-repo` / `--output`のみで、target repositoryはparameter。固有pathのhard-codeなし |
| Layer 2〜4実行 | `scripts/evaluation_loop.py` | clickで25 result・計481 runをappend-only登録。set / cycle / capsule / registry単位で動作し、target repositoryによる実行分岐を持たない |
| 制御prompt本文 | [Candidate71 release](../prompts/releases/the-caption-3ce91a4-validation-closure-release-r1/README.md)の`AGENTS.md.txt` | `SPEC`〜`RECOVERY`の13 labelは見出し語を除きproject固有語彙を持たない |
| bundle target map | THE-CAPTION releaseのmanifest 19 target、Clickは0 / 1 / 3 targetの4 prompt set | THE-CAPTIONのtarget側directory構造へ依存するmapを変更せず、`click`用mapをinstance配下の別bundleとして固定した。C81 root本文のbyte-identicalな水平適用、empty bundle、3つのsub instructionをそれぞれ独立identityで表現した |
| case artifact | 各case revisionの`trial-prompt-input.json`、`private/seed.patch`、`private/case-data.json` | 14 case・17 revisionをinstance配下へ固定。失敗revisionを上書きせず保持した |
| rating contract | THE-CAPTION v13、`click-outcome-abstract-condition-preserving-v1`〜v10 | case追加ごとに旧revisionを残し、現行v10で標準14項目を固定した |
| 採点補助 | Clickは固定rating contractとblind evidenceで採点 | 14 case・481 runのratingと登録が成立。target固有の新しいkernel分岐は追加していない |

したがって汎用化の対象は実行基盤ではなく、**case artifact / rating contract revision / 採点補助 / bundle target mapの4つ**である。`click`では4つをinstance配下へ分離し、共有kernelへtarget repositoryによる実行分岐を追加せず、3 KPI、compatibility key、append-only registryを含む端から端までの流用をBundle A / Bの標準14項目で確認した。未確認なのは第三者によるruntime再構築とnetwork遮断下のfull gateである。

この分離の境界とinstance台帳は[`evaluations/targets/README.md`](../evaluations/targets/README.md)で確定した。既存の計測系列はtarget instance `the-caption`（`layout: legacy_root`）として登録し、artifact pathを移動していない。

### target選定gate（この順で判定する）

1〜4は候補の機械的な絞り込み、5〜7は測定が成立するかの判定である。

1. **license**: seed patch、fixture条件、evidenceをこのrepositoryへ保存し公開するため、再配布可能なlicense（Apache-2.0 / MIT / BSD等）に限定する。
2. **offline再現性**: 依存を事前materializeした状態で、network遮断のまま全required gateがpassする。permissionは`approval_policy: never` / `sandbox: workspace-write`である（[profile実測](../evaluations/profiles/candidate1-expanded12-global-m24-n5-r1.json)）。
3. **容量**: self-contained fixtureをrun数ぶんmaterializeするため、soft 3 GiB / hard 5 GiBの運用値（[`evaluation-storage-maintenance.md`](evaluation-storage-maintenance.md)）に収まる。
4. **gate所要時間**: 標準14項目 × A / B × `N=5`で140 run規模になるため、1 runのfull gateがこの規模で回る長さである。
5. **測定感度**: 複数subsystemへ跨る変更、2階層以上のdirectory構造、worker委譲が意味を持つ広さを持つ。単一責務のlibraryでは`CONTEXT` / `OWNER_ROLE` / `INDEPENDENCE`の差がKPIへ出ない。
6. **天井効果の回避**: 既存setでもF05 out-of-scopeとF07 dependency pairは全runが`quality_score` 100である（[`cases/README.md`](../evaluations/cases/README.md)）。modelが解法を記憶しているseedはこれを悪化させるため、seed diffの取得元commitの新しさで制御する。
7. **prompt target collision**: target側が既に`AGENTS.md`等のauthority fileを持つと、bundle overlayでcase条件やtarget側規則が消える。F09が`prompt_target_collision`でexecution blockedになったのと同型のriskである。
8. **case供給**: 公開issue / PR履歴からreal taskを取得でき、case追加根拠自体を第三者が検証できる。
9. **実行判断点coverage**: 既存14項目が担保するworker起動、context継承、model再入、read、validation、停止、result bindingなどの判断点に、target固有の題材を対応付けられる。実装言語の一致自体はgateにしない。

### 独立系列としての扱い

- `target_repository_ref`はcompatibility keyの一項目である（[`evaluations/AGENTS.md`](../evaluations/AGENTS.md)）。**公開target系列を既存result集合と同一比較へ混ぜない。** baselineから再取得する。
- 項目8（Claude Code CLI executor置換）と同一比較単位へ入れない。executor変更とtarget変更を同時に入れると効果を切り分けられない。
- rating contractをcase単位で作り直す以上、`quality_score`の絶対値をTHE-CAPTION系列と比較しない。観察できるのは各系列内の差と、方向の一致だけである。

### 未確定事項

- `click`の容量、gate所要時間、通常環境での5回連続passはPhase 0で実測した。P1-cでbatch内・batch間分布、Std14で14 case横断の70 / 70 validを取得した。
- `.venv`を含むknown-good実行環境（[`cases/README.md`](../evaluations/cases/README.md)のself-contained fixture）を、第三者へどう再現させるかが未決である。lockfileからの再構築手順で足りるか、fixture条件として固定する必要があるかを判定していない。
- network遮断下のfull gateは未実測である。依存materialize後にnetworkを使わない見込みと、network遮断下でpassした事実を混同しない。
- instance境界、layout、descriptor、Click rating v10は固定した。Std14は固定contractとblind evidenceで採点できたため、target固有採点補助の自動adapter化は今回の完了条件ではない。別targetを追加するときに再評価する。

### 段階計画

1. **Phase 0**（実施済み）: gate 1〜9を判定し、`pallets/click`を選定した。追加実測により14項目すべての実行判断点へ対応可能と確認した。実測値と判定の正本は[`public-target-selection-phase0.md`](public-target-selection-phase0.md)とする。
2. **Phase 1 artifact準備**（実施済み）: instance、control-free bundle、F01型case、rating contract、set、P1-a profile、共有runtimeを固定した。
3. **Phase 1実測**（P1-c完了）: P1-a `N=1`で端から端までの成立、P1-b `N=5`でbatch内分布、P1-c `N=5 × B=3`でbatch間の散らばりを確認した。
4. **Phase 2 case展開**（実施済み）: 14 caseをqualificationし、追加caseだけ各`N=3`でBundle Aの成立を確認した。既存caseは追加のたびに再実行していない。
5. **Phase 3 Bundle A標準14**（実施済み）: `click-standard14-r1`を固定し、Bundle Aで70 / 70件をscore `4`として登録した。
6. **Phase 4 Bundle B水平比較**: Std14 baseline確立後に、1軸だけを変更した新しいCandidateをBundle Bとして固定し、同じStd14条件でBundle Aと比較する。content-identicalなBundle Bは作らない。

candidate bundleを作る段階ではcandidate作成前gate 9項目（[`prompts/AGENTS.md`](../prompts/AGENTS.md)）を通す。

## 着手時の共通条件

- 一つのcandidateで一つのpredicateまたは一つの変更軸だけを扱う（[`prompts/AGENTS.md`](../prompts/AGENTS.md)のcandidate作成前gate9項目）
- 設計原則の正本は[`prompt-control-design-principles.md`](prompt-control-design-principles.md)
- 評価・採用・release・projectionは別gateとして記録する（[`repository-contract.md`](repository-contract.md)）
