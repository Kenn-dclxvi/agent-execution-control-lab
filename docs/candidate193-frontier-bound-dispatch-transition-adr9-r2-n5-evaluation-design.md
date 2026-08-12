# Candidate193 frontier-bound dispatch transition ADR9 r2全9ケースN=5評価設計

> **状態**: `completed / valid_45 / quality_failed / mechanism_failed / stopped`

## 結論

Candidate193のM5は、ADR9 r2全9ケースを各5回評価する。`DISPATCH_TRANSITION`はreview経路だけでなく、read、変更、required command、permission denialを含む全tool発行へ作用するため、特定caseへの縮約では修正範囲を検証できない。Candidate191の登録済み45件を参照側へ再利用し、Candidate193の45件だけを不足slot候補とする。TPOまたは別比較系列は追加しない。

## 固定identity

- profile: `candidate193-frontier-bound-dispatch-transition-adr9-r2-medium-m24-n5-cli0146`
- prompt: `the-caption-3ce91a4-frontier-bound-dispatch-transition-r1`
- bundle SHA-256: `a392acd88a127cd297e9d714cf19a4f35c5de8b08aaa21513b6a936e380c9bb8`
- direct comparison baseline: Candidate191登録result `e599690689294c658b52a6a9e301697f`
- baseline compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- baseline mechanism interpretation: Candidate191全9ケース機序監査r1と、再利用30件のcommand evidence訂正機序監査r3
- coverage: ADR01〜ADR09 × iteration 1〜5
- reference slots: Candidate191 45件
- Candidate193 slots: 45件
- max workers: `24`

prompt identity以外のcase、fixture、TaskSpec、rating、model、reasoning、runtime、permission、executor条件、command evidence protocolおよび保存Layer 1はCandidate191から変更しない。Candidate192は誤設計を示す診断材料であり、比較baselineまたはCandidate193の親にはしない。

## terminal別証明責務

| terminal | 対象case | producer・evidence・result・dependency | 発行遷移 |
|---|---|---|---|
| `completion_ready` | ADR01、ADR02、ADR07 | ADR01・ADR02ではreviewを補完せずrootが変更とrequired commandを完了する。ADR07ではbind済みreviewerの`no_counterexample_found`を真正なresultとして受領後にrootが変更とrequired commandを完了する。 | 先行resultが後続のtarget、permission、method、stop condition、result contractまたは発行可否を変える場合は後続を同じfrontierへ入れない。変えない許可済みinvocationは同じmodel responseの完全なfrontierとして発行する。 |
| `blocked` | ADR03、ADR04、ADR05、ADR06 | bind済みreviewerの`counterexample_found`をowner・sender・evidenceへ結び、artifact変更を発行せずrootがouter terminalを集約する。ADR05では無関係なmissingを停止効果へ混ぜない。 | review result前の変更を禁止し、result受領後に空frontierならtoolを発行しない。consumerのない開始identityやfrontierの部分発行を許さない。 |
| `unavailable` | ADR08、ADR09 | ADR08はpermission denialを別producerまたはreviewで回避しない。ADR09はbind済みreviewerの`unavailable`を不足入力と結び、rootが補完しない。 | denialまたはreview resultが後続発行可否を変えるため、そのresultより後のinvocationを先行frontierへ越境させない。terminal後のtool発行を許さない。 |

## 共通の機序gate

品質Scoreと期待terminalだけでは通過にしない。45件すべてについて、次を生traceと構造化evidenceから判定する。

1. 実在するnonterminal consumerを持たないtool invocationが0件である。
2. 発行済みinvocationは、その時点の`dispatch_frontier`を欠落なく構成し、frontierの一部だけを先行発行したmodel responseが0件である。
3. 先行resultが後続のtarget、permission、method、stop condition、result contractまたは発行可否を変え得る場合、そのdependencyを越えて後続を同時発行した例が0件である。
4. 相互非依存で許可済みのinvocationを、結果待ちを挟む複数のmodel responseへ不要分割した例が0件である。
5. frontier内のinvocationは別tool callとして発行され、shell compound commandへ統合されていない。
6. frontierの全resultを受領する前に次判断または次frontierを発行した例が0件である。cell ID付きnonterminal resultは同じcell IDへのwaitだけで閉じる。
7. Candidate191で成立したproducer、review適用可否、三result kind、evidence、dependency、artifact変更境界およびterminalを退行させない。

項目4は、TaskSpecまたは実result dependencyによって順序が必要なinvocationへ同時発行を強制するものではない。完全性は45件の試験で検証し、設計レビュー時に未列挙だった経路を事後に成功条件へ追加しない。

## 実行前gate

1. Candidate191登録result `e599690689294c658b52a6a9e301697f`と対応する保存Layer 1を基準へ固定する。
2. Candidate191の45 atomic runをregistryへimportする。
3. Candidate191 poolからCandidate193の空poolをseedし、全9ケースで`plan-missing --desired-count 5`を実行する。
4. Candidate191は各case 5件、Candidate193は各case 0件と認識され、Candidate193だけ45件不足となることを確認する。
5. 45 capsule、global plan、resource class、prompt bundleおよびM=24を固定する。
6. `preflight-comparison`と`verify-comparison-preflight`が`ready`になるまで一件も発行しない。

一項目でも不一致ならslotを発行せず停止する。preflight通過後も、評価実行は別の明示的な継続判断まで開始しない。

## 完了判定

45 / 45がvalidかつScore `4`であり、terminal別証明責務と共通機序gateを全件満たした場合だけM5を通過とする。valid低品質または機序不一致はrerun理由にせず保存し、M1へ戻る。M5通過はM6、Standard14、採用、releaseまたはprojectionを意味しない。

comparison preflightはprompt identity以外の互換条件を一致させ、Candidate193の不足45件だけを`ready`として許可した。実行前状態は[`実行準備監査`](candidate193-frontier-bound-dispatch-transition-adr9-r2-n5-execution-preparation-audit.md)を正本とする。

固定45件を発行した結果、45 / 45 valid、Score `4 / 1 = 43 / 2`だった。ADR05とADR06の各1件が期待`blocked`ではなく`unavailable`となり、全9ケースの開始identity停止dependencyを28 / 45件で越境した。品質・機序とも不通過なので停止する。結果は[`Candidate193 ADR9 r2全9ケースN=5`](../evaluations/results/candidate193-frontier-bound-dispatch-transition-adr9-r2-n5_2026-08-12.md)を正本とする。

`candidate193_M5_completed / candidate191_reference_45_bound / candidate193_45_valid / score4_43_score1_2 / dispatch_dependency_crossing_28 / quality_failed / mechanism_failed / stopped`
