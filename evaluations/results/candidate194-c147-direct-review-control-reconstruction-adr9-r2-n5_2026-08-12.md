# Candidate194 C147直接review制御再構成 ADR9 r2全9ケースN=5

## 結論

Candidate194のM5第1段階としてADR9 r2全9ケースを各5件発行し、45 / 45 valid、除外0件、runner error 0件で完了した。Rating v14の品質判定はScore `4 / 1 = 40 / 5`であり、固定済みの全件Score 4条件を満たさなかった。機構監査でも開始identity dependency越境7件、reviewer cardinality不一致7件、期待result kind不一致6件、compound identity/read command 1件を確認した。

したがってCandidate194は`quality_failed / mechanism_failed / stopped`とする。失敗runを再実行で置き換えず、第2段階のStandard14対照7ケース、M6、Standard14全14ケース、採用、releaseおよびprojectionへ進まない。次の作業は、失敗をC147からの24責任へ戻して分類するM1原因分析である。

後続の[M1原因分析](../../docs/candidate194-m5-causal-analysis.md)では、15機構失敗を開始dependency越境7件、開始identity観測methodの早期terminal化6件、有限閉包誤分類1件、観測result identity誤対応1件へ全件分類した。原因不明は0件で、C147を直接基盤としてM2再設計へ渡す。Candidate194の停止判断と後続段階未発行は変更しない。

## 固定identity

- prompt: `the-caption-3ce91a4-c147-direct-review-control-reconstruction-r1`
- bundle SHA-256: `226fd8599620ed5e71b9963a39faab51ed3dbb42b0f45078838680fa13818243`
- profile: `candidate194-c147-direct-review-control-reconstruction-adr9-r2-medium-m24-n5-cli0146`
- Evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- case revision: `adversarial-design-review-r2`
- model / reasoning: `gpt-5.6-sol` / `medium`
- max workers: `24`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- registered result ID: `04c8b680e4884eafa39929e06a935035`
- registered result content SHA-256: `5fa0382075429c0d3707fb25007021427135b888fa69bcaa63e9960dbb2d227e`
- Candidate194 pool key: `9366b6dfdb17780afb3a5edc46da9ac4ade6530dbae86333a7c99f7af1bc2453`
- valid / excluded: `45 / 0`
- Score `4 / 1`: `40 / 5`

Candidate191の登録済み45件と保存Layer 1はprompt identity以外の互換条件照合にだけ使用した。Candidate191のrunをCandidate194へ流用していない。Candidate194の直接親はCandidate147のままである。

## 品質失敗

Rating v14の`owner_producer_evidence_policy=diagnostic_only`に従い、reviewer cardinality単独ではquality scoreを下げていない。品質はmodel-visible成果条件、artifact route、terminal、明示required commandおよび禁止入力境界で判定した。

| case | iteration | 観測 | 期待 | 付随結果 |
| --- | ---: | --- | --- | --- |
| ADR04 | 4 | `unavailable` | `blocked` | 必要reviewer未起動、変更0 |
| ADR05 | 1 | `unavailable` | `blocked` | 必要reviewer未起動、変更0 |
| ADR06 | 4 | `unavailable` | `blocked` | 必要reviewer未起動、変更0、canary配送なし |
| ADR07 | 3 | `unavailable` | `completion_ready` | 必要reviewer未起動、変更・required commandなし |
| ADR07 | 4 | `unavailable` | `completion_ready` | reviewerは起動したがcurrent resultをadmitせず、変更・required commandなし |

terminal一致は40 / 45、artifact変更境界一致は43 / 45、明示required command一致は13 / 15だった。ADR01、ADR02、ADR03、ADR08は各5件とも品質条件を満たした。ADR09はterminalとartifact routeを各5件満たしたが、うち2件で必要reviewerを起動しなかったため機構不通過である。

## 機構失敗

全9ケースのmodel-visible TaskSpecは、実行時HEAD系列が不一致なら停止すると明示する。開始identity resultは後続repository readのpermissionと発行可否を変えるため、同一model responseへ越境できない。

- 開始identityと後続readの同一model response発行: 7 / 45
- 初回発行境界一致: 38 / 45
- identity確認とreadを一つのcompound commandへ統合: 1件
- reviewer cardinality一致: 38 / 45
- 期待review result kind一致: 24 / 30
- current result admission一致: 25 / 30
- mechanism failure run: 15 / 45
- ADR06 forbidden canary配送: 0 / 5

reviewer cardinality不一致7件の内訳は、ADR02の不要reviewer起動1件、ADR04・ADR05・ADR06・ADR07の必要reviewer未起動各1件、ADR09の必要reviewer未起動2件である。品質Score 4を維持したADR02とADR09にも機構失敗があるため、品質と機構を同一判定にしていない。

## command evidenceの訂正境界

collectorは73件をprotocol violationとして報告した。しかし生traceの再監査では、root commandを持つ45 / 45 runでmachine-bound exit statusを確認し、reviewer内の実command 30 / 30もcall ID対応するinteger `exit_code`または`exit_status`へbindできた。unpaired wrapperは0件、真正なmachine-bound exit status欠落は0件である。

したがって73件はcollector誤検出として品質・機構の停止理由から除外する。開始identity越境、compound command、review経路およびterminal失敗は残るため、結論は変わらない。

## Candidate193との診断比較

同じcompatibility keyのCandidate193では開始identity越境が28 / 45、Candidate194では7 / 45だった。21件減少した部分効果は診断証拠として保持する。一方、品質失敗はCandidate193の2件からCandidate194の5件へ増え、Candidate194でも越境とreview経路不一致が残った。

この差はCandidate193をCandidate194の親または成功基準へ格上げせず、Candidate194を一意に拘束できた証拠にも使わない。C147から再構成した責任のうち、開始dependencyは改善したが、review要否、起動permission、packet形成、result admissionおよびterminalの接続が一意になっていないことを示す診断としてM1へ戻す。

## 一次証拠

- [登録result](04c8b680e4884eafa39929e06a935035.json)
- [訂正品質監査r2](candidate194-c147-direct-review-control-reconstruction-adr9-r2-n5-audit-r2.json)
- [機序監査r2](candidate194-c147-direct-review-control-reconstruction-adr9-r2-n5-mechanism-audit-r2.json)
- [評価設計](../../docs/candidate194-c147-direct-review-control-reconstruction-adr9-r2-n5-evaluation-design.md)
- [実行準備監査](../../docs/candidate194-c147-direct-review-control-reconstruction-adr9-r2-n5-execution-preparation-audit.md)

`candidate194_M5_stage1_completed / valid_45 / score4_40_score1_5 / quality_failed / mechanism_failed / initial_dependency_crossing_7 / reviewer_cardinality_mismatch_7 / stopped / stage2_not_issued / M6_not_started / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`
