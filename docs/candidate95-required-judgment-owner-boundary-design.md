# Candidate95 required judgment owner boundary設計記録

## 結論

Candidate95は、停止済みCandidate94を直接sourceとする。変更軸は、`criterion owner`を単なる`non-machine risk`ラベルではなく、operation完了に必要な`non-machine judgment result`へ限定することである。

root `AGENTS.md`の`SPEC`だけを置換する。repository authorityからrequested outcome valueを一意にbindでき、別のnon-machine judgment resultを要求しないcriterionには、risk記載の有無にかかわらず`criterion owner=none`をbindする。Candidate94のoperation-local readinessと`unavailable` terminal failureは維持する。

## Candidate作成前gate

1. 基準prompt setは`the-caption-3ce91a4-operation-criterion-totality-r1`（Candidate94）とする。最短正常経路は、repository authorityからA02の正規entrypointを一意にbindし、別の人間判断を要求せず`owner=none`として`run.sh`の修正とrequired validationへ進む経路である。
2. 保存済み誤経路は、Candidate94 Rating v14 Medium標準14 N=5のA02 iteration 5、run ID `851b97526bb449e4ac2e0b257faf1747`である。正規entrypoint `src.app.entrypoints.v4_daily_main`を特定した後も、TaskSpecの`non_machine_risk=canonical entrypoint selection`に反応してcriterion ownerを質問し、許可された変更と試験を開始しなかった。
3. A02 TaskSpecとrepository authorityだけではこの誤経路を防げない。requested outcome valueは一意に解決できる一方、Candidate94の`SPEC`はriskを持つcriterionのownerを独立したreadiness値として必須化し、owner用repository authorityの定義を持たないためである。
4. 置換する一つのpredicateは`required judgment owner boundary`である。criterion ownerをbindする条件を「non-machine riskの記載」から「operation完了にnon-machine judgment resultがrequired」へ狭める。
5. このpredicateが消す判断点は、repository-resolvableな成果値を得た後にGit authorなどからownerを追加探索するか、owner clarificationで停止するか、という二分岐である。
6. 新たに増えるlabel、tool、retry、worker routeはない。新しい判断語は`non-machine judgment resultがrequired`だけであり、TaskSpecのrequired outcomeとpredicateから判定する。risk自体を無視せず、別の人間判断結果が実際にrequiredならowner bindingを維持する。
7. targeted評価は既存Rating v14、Medium、A02 r2、Codex CLI `0.146.0`、各`N=5`を変更せず使う。Candidate95は5 / 5 valid・rateable・score `4`、不要clarification 0件、正規route修正5 / 5、required validation 5 / 5を必須とする。
8. token、elapsed、tool call、Git履歴探索はdiagnosticとして記録する。主判定は成果品質とrouteであり、cost改善はCandidate成功条件にしない。
9. score `4`未満、owner clarification、Git authorをownerへbindする追加探索、正規route未修正、required validation欠落、A02 TaskSpec・fixture・rating・runtime条件のdriftが一件でもあれば停止する。targeted通過前に標準14、採用、release、本体反映へ進めない。

九項目を固定済みであるため、Candidate95のfull bundleと構造testを作成できる。評価profileはcandidate作成後の別artifactとして固定する。

## 変更境界

- direct source: Candidate94
- 変更target: root `AGENTS.md`一つ
- 置換label: `SPEC`
- 維持: Candidate94の`TERMINAL`、`OWNER_ROLE`とその他8 label
- 非変更: 残り18 target、TaskSpec、case、fixture、rating、permission、executor、runtime
- 非目標: risk分類の削除、human approvalの省略、worker起動条件変更、retry追加、採用、release、runtime projection

## Candidate状態

- candidate number: Candidate95
- prompt identity: `the-caption-3ce91a4-required-judgment-owner-boundary-r1`
- evaluation status: `not_evaluated`
- state: `draft`
- release: `not_created`
- runtime projection: `not_projected`

## 後続評価状態

2026-07-30に[`Rating v14 Medium A02 N=5`](../evaluations/results/candidate95-required-judgment-owner-boundary-v14-medium-a02-n5-cli0146_2026-07-30.md)を実行した。5 / 5件がvalid・rateable・score `4`で、owner clarification、Git authorによるowner探索、品質failureは0件だった。A02 targeted gateを通過した。

続く[`Rating v14 Medium標準14 N=5`](../evaluations/results/candidate81-candidate95-required-judgment-owner-boundary-v14-medium-standard14-n5-cli0146_2026-07-30.md)も70 / 70件がvalid・rateable・score `4`だった。Candidate81比の中央値はtoken `+2.62%`、elapsed `+7.30%`で両方増えた。現在状態を`standard14_evaluated / quality_gate_passed / aggregate_cost_both_higher / adoption_not_decided`とする。構築時状態とmanifestは履歴として変更しない。

さらに[`A02 N=5 B20`](../evaluations/results/candidate95-required-judgment-owner-boundary-v14-medium-a02-continuous-n5-b20-cli0146_2026-07-30.md)を実行した。20 / 20 batch、100 / 100件がvalid・rateable・score `4`で、owner clarification停止、未変更停止、required validation欠落は0件だった。現在状態を`a02_b20_evaluated / route_stability_gate_passed / standard14_quality_gate_passed / aggregate_cost_both_higher / adoption_not_decided`へ更新する。これはA02固定条件内の観測であり、標準14全体のB20ではない。

その後、採用前のmatched確認として[`Candidate81 / Candidate95 A02 N=5 B20比較`](../evaluations/results/candidate81-candidate95-required-judgment-owner-boundary-v14-medium-a02-continuous-n5-b20-cli0146_2026-07-30.md)を確定した。両者100 / 100 score `4`だった。Candidate95はCandidate81比でtoken中央値`-1.72%`、elapsed中央値`-6.50%`で、Holm補正後にelapsedだけ有意だった（`p=0.008442`）。このtriggerに従い、[`標準14 N=5 B20`](../evaluations/results/candidate81-candidate95-required-judgment-owner-boundary-v14-medium-standard14-continuous-n5-b20-cli0146_2026-07-30.md)を両者各1,400件実行した。

標準14 B20ではCandidate81が1,400 / 1,400 score `4`、Candidate95がscore `4 / 2 / 1 = 1,398 / 1 / 1`だった。A02の1件はrisk記載から具体的ownerを再要求し、F06の1件はTaskSpecの`owner=independent contract check`を未具体化の役割と解釈して、いずれも変更・test前に停止した。これはCandidate95が消すはずだったowner clarification経路の低頻度再発であり、Rating偽陰性ではない。Candidate81比の中央値もtoken`+4.49%`、elapsed`+5.53%`で、両方Holm補正後に有意な悪化だった。事前のzero-failure gateに従い、最終状態を`standard14_b20_evaluated / quality_gate_failed / route_stability_gate_failed / cost_both_significantly_higher / stopped`とする。採用、release、本体反映へ進めない。

## Evidence

- [Candidate94 bundle](../prompts/candidates/the-caption-3ce91a4-operation-criterion-totality-r1/manifest.json)
- [Candidate94標準14結果](../evaluations/results/candidate81-candidate94-operation-criterion-totality-v14-medium-standard14-n5-cli0146_2026-07-30.md)
- [Prompt制御の検討原則](prompt-control-design-principles.md)
