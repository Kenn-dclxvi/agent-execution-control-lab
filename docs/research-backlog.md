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

## 6. 現行rating contract identityの確定（解決済み・2026-07-25）

新規runへ適用する現行rating contractの指定が、評価基盤の正本（`owner-producer-quality-v8`）と後続文書（最新revision v13）で一致していなかった。**2026-07-25に現行をv13へ確定した。** 正本[`prompt-comparison-workflow.md`](prompt-comparison-workflow.md)の指定、評価実行手順[`evaluation-loop-manual.md`](evaluation-loop-manual.md)のLayer 3、契約台帳[`evaluations/rating-contracts/README.md`](../evaluations/rating-contracts/README.md)、および`scripts/evaluation_loop.py`の`SUPPORTED_QUALITY_RATINGS`をv13へ追従させ、v13 capsuleが受理されることをunit testで確認済みである。この項目は未完了ではない。

派生作業も2026-07-26に完了した。

- [`Baseline、ControlFreeRepository、Candidate5、Candidate35、Candidate43、Candidate71の標準14項目各N=5`](../evaluations/results/baseline-control-free-repository-c5-c35-c43-c71-v13-standard14-n5_2026-07-26.md)を最初のv13互換result集合として登録した。v12以前のresultは同一comparisonへ混ぜない。

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

## 10. 公開target repositoryでの計測系列と評価基盤のrepository汎用化（未着手）

**未実施。** 現行の計測系列は非公開repository `Kenn-dclxvi/THE-CAPTION`をtargetにbindしており、第三者は同一caseを取得しても実行できない。この項目が扱うのは、公開repositoryを対象とする計測系列を独立に立ち上げ、その過程で「任意のtarget repositoryへ同じ手順を適用できる分離」を確定することである。prompt制御の新しい変更軸ではなく、計測条件側の軸である。

### 現在の依存範囲（2026-07-26に実測）

repository非依存な層とtarget固有な層は次のとおりである。

| 層 | artifact | 実測した状態 |
| --- | --- | --- |
| Layer 1 fixture | `scripts/prepare_case_fixture.py` | CLI引数は`--case` / `--source-repo` / `--output`のみで、target repositoryはparameter。固有pathのhard-codeなし |
| Layer 2〜4実行 | `scripts/evaluation_loop.py` | set / cycle / capsule / registry単位で動作し、target固有pathを持たない。`scripts/`と`layer2/`の`.py`に現れる固有語はschema名prefix `the-caption-prompt`（94件）、環境変数名、git author名、set idなどの識別子・記述文字列で、target repositoryによる実行分岐は持たない |
| 制御prompt本文 | [Candidate71 release](../prompts/releases/the-caption-3ce91a4-validation-closure-release-r1/README.md)の`AGENTS.md.txt` | `SPEC`〜`RECOVERY`の13 labelは見出し語を除きproject固有語彙を持たない |
| bundle target map | 同releaseのmanifest 19 target | `src/` `tests/` `scripts/` `docs/`階層のauthority fileと`docs/reference/project-contexts/the-caption.txt`という**target側のdirectory構造に依存**する |
| case artifact | 各case revisionの`trial-prompt-input.json`、`private/seed.patch`、`private/case-data.json` | `fixture.target_identity`へrepository / commit / treeをbindし、gate commandに`.venv/bin/python -m pytest ...`と`bash scripts/dev/main_verify.sh`を含む |
| rating contract | `evaluations/rating-contracts/outcome-abstract-condition-preserving-owner-diagnostic-v13.json` | `boundary_rules`と`case_quality_rules`を**case ID単位**（`TC-A01` / `TC-A02` / `TC-F10`等）で内包する |
| 採点補助 | `scripts/quality_audit_policy.py`、`scripts/standard14_quality_audit.py` | `src/domain/market_units_snapshot.py`、`src/domain/collection_history_updater.py`、`main_verify.sh`をhard-codeする |

したがって汎用化の対象は実行基盤ではなく、**case artifact / rating contract revision / 採点補助 / bundle target mapの4つ**である。この4つをtarget単位で差し替え可能な単位として分離できるかが、他repositoryでの計測成立条件になる。制御prompt本文と3 KPI、compatibility key、append-only registryは現状のまま流用できる見込みだが、実測は未実施である。

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
9. **言語分布**: 既存setはPython中心にReact / TypeScript（F04）、shell runner（F07）、docs-only（F08）を含む。1 repositoryで満たせない場合は初期setを縮小する判断が必要になる。

### 独立系列としての扱い

- `target_repository_ref`はcompatibility keyの一項目である（[`evaluations/AGENTS.md`](../evaluations/AGENTS.md)）。**公開target系列を既存result集合と同一比較へ混ぜない。** baselineから再取得する。
- 項目8（Claude Code CLI executor置換）と同一比較単位へ入れない。executor変更とtarget変更を同時に入れると効果を切り分けられない。
- rating contractをcase単位で作り直す以上、`quality_score`の絶対値をTHE-CAPTION系列と比較しない。観察できるのは各系列内の差と、方向の一致だけである。

### 未確定事項

- 候補repositoryの容量、gate所要時間、flaky率はいずれも未実測である。候補を固定してから実測する。
- `.venv`を含むknown-good実行環境（[`cases/README.md`](../evaluations/cases/README.md)のself-contained fixture）を、第三者へどう再現させるかが未決である。lockfileからの再構築手順で足りるか、fixture条件として固定する必要があるかを判定していない。
- instance境界、layout、descriptorは[`evaluations/targets/README.md`](../evaluations/targets/README.md)で確定した。残る未設計は**target固有採点補助のadapter化**であり、既存`scripts/quality_audit_policy.py`と`scripts/standard14_quality_audit.py`を変更せずに新instance用moduleをどう追加するかを決めていない（[`scripts/AGENTS.md`](../scripts/AGENTS.md)）。

### 段階計画

1. **Phase 0**（2026-07-26に実施済み）: gate 1〜4で候補を絞り、`pallets/click`をPhase 1候補とした。実測値と判定の正本は[`public-target-selection-phase0.md`](public-target-selection-phase0.md)とする。gate 9（言語分布）はPython単一のため不足が残る。
2. **Phase 1**: 各候補で最小1 case（F01型: 単一fileへseed patch + focused gate）をfixture qualificationする。
3. **Phase 2**: bit-identical bundleで`N=10`のnull calibrationを行う（[`TC-F01 r2 N=10`](../evaluations/results/TC-F01-r2_identical-bundle-n10_2026-07-15.md)と同じ手順）。flakyとtoken分散から感度の下限を確認する。
4. **Phase 3**: nullが通った1 repositoryだけで、F02型（cross-layer）とF10-R型（非破壊review）へ拡張する。制御差が観測されるのはこの2型である。
5. **Phase 4**: case pack一式と縮小setを公開単位として固定する。

candidate bundleを作る段階ではcandidate作成前gate 9項目（[`prompts/AGENTS.md`](../prompts/AGENTS.md)）を通す。

## 着手時の共通条件

- 一つのcandidateで一つのpredicateまたは一つの変更軸だけを扱う（[`prompts/AGENTS.md`](../prompts/AGENTS.md)のcandidate作成前gate9項目）
- 設計原則の正本は[`prompt-control-design-principles.md`](prompt-control-design-principles.md)
- 評価・採用・release・projectionは別gateとして記録する（[`repository-contract.md`](repository-contract.md)）
