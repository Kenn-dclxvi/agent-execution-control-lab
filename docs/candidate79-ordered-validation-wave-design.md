# Candidate79 ordered validation wave設計記録

## 結論

Candidate79はCandidate71を直接sourceとする。Candidate71の11 labelと最短正常経路を維持し、`VALIDATION_CLOSURE`の一predicateだけを置換する。

順序依存を持つrequired validationも、先行resultの成功時だけ後続を発行する順序付き個別invocation群として、一つのmodel stepへ閉じる。shell commandの結合、required command、個別exit、失敗時停止、TaskSpec、executor parameterは変更しない。

## Candidate作成前gate

1. 基準prompt setは`the-caption-3ce91a4-validation-closure-r1`（Candidate71）とする。最短正常経路は、artifact変更後に完全なrequired-validation集合をbindし、順序制約を保った個別invocation群を一つのmodel stepから発行し、全result受領後に一度だけterminalまたは継続を判断する経路である。
2. 保存済みrating v13、Medium、F04、`N=5`では、5 / 5 runが3 required commandを別々のtop-level model stepから発行した。4 / 5 runでは`npm ci`とlint、lintとbuildの間にagent commentaryが入り、validation中間のmodel再入は計8回だった。
3. F04 TaskSpecは3 commandを「順に」実行し、command evidence protocolは1 commandずつの個別`exec_command`を要求する。Candidate71も個別invocationを同一model stepから発行すると定めるが、順序依存時の発行方法と先行失敗時の停止を明示していない。このためMediumではTaskSpecの逐次表現を優先する経路が残った。
4. 置換する一つのpredicateは、`validation_wave_ready := artifact変更完了 ∧ TaskSpec-required validationのidentity / command / dependency order / individual pass condition / stop conditionが全件bind済み`である。成立時は、相互非依存commandを同時に、順序依存commandを先行success時だけ後続へ進む順序付き個別invocation群として、同一model stepから発行する。
5. このpredicateが消す判断点は、成功したvalidationを一件受領するたびに、既知の次commandを発行するかをmodelへ戻して判断する中間再入である。全件成功後の根拠のない追加read / validationを抑える既存terminal closureも維持する。
6. 新しいlabelは増やさない。増える条件はdependency orderのbindと、順序依存時の先行successによるfail-stopだけである。tool名、case名、command列、worker、shell command結合は追加しない。
7. 品質はCandidate71とCandidate79をrating v13、Medium、F04 r2、各`N=5`の互換条件で確認する。両条件とも5 / 5 valid・rateable・score `4`、required validation欠落0、protocol違反0、zero driftを必須とする。
8. KPIは`quality_score`、all-agent `total_tokens`、`elapsed_seconds`とする。validation中間のmodel再入、post-validation追加read、top-level tool callはdiagnosticとして記録する。Candidate79で中間再入が減り、tokenとelapsedが減る方向を期待する。
9. score `4`未満、required validation欠落、protocol違反、順序違反、workspace drift、中間再入が減らない、またはtoken / elapsedのいずれかが期待と逆方向の場合は停止する。Candidate79へ補助predicateを継ぎ足さず、標準14項目、採用、release、本体反映へ進めない。

九項目を定義済みであるため、Candidate79のbundle、F04対象profile、構造testを作成できる。

## 変更境界

- direct source: Candidate71
- 置換: root `AGENTS.md`の`VALIDATION_CLOSURE`一行
- 非変更: 残り18 target、TaskSpec、case、rating、permission、executor parameter、command evidence protocol、THE-CAPTION runtime
- evaluation scope: F04 r2、Medium、各`N=5`の対象試験だけ
- adoption / release / runtime projection: 未実施

## Candidate状態

- candidate number: Candidate79
- prompt identity: `the-caption-3ce91a4-ordered-validation-wave-r1`
- evaluation status: `targeted_evaluated`
- state: `stopped`

## 対象試験結果

Candidate71とCandidate79をF04 r2、Rating v13、Medium、各`N=5`の互換条件で新規実行した。両条件とも5 / 5件がvalid・rateableかつscore `4`だった。

Candidate79の1-step closureはCandidate71の3 / 5から0 / 5へ減った。all-agent token中央値は`225,041 -> 263,038`（`+16.88%`）、elapsed中央値は`104.990 -> 107.598秒`（`+2.48%`）だった。

作成前gate 9の停止条件に該当するため、Candidate79へ補助predicateを追加せず停止する。標準14項目、採用、release、本体反映へ進めない。

## Evidence

- [Candidate71設計](candidate71-validation-closure-design.md)
- [Candidate71 reasoning level結果](../evaluations/results/candidate71-reasoning-levels-v13-standard14-n5_2026-07-26.md)
- [Candidate71 / Candidate79 F04対象結果](../evaluations/results/candidate71-candidate79-ordered-validation-wave-v13-medium-f04-n5_2026-07-26.md)
- [Prompt制御の検討原則](prompt-control-design-principles.md)
