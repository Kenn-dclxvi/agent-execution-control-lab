# Candidate193 frontier-bound dispatch transition ADR9 r2全9ケースN=5

> **結果**: `45 / 45 valid / Score 4 = 43 / Score 1 = 2 / quality_failed / mechanism_failed / stopped`

## 結論

Candidate193のADR9 r2全9ケース各5件、合計45件は、Candidate191登録resultを基準にしたcomparison preflight通過後、固定global planとM=24で発行した。45 / 45 valid、除外0件、runner error 0件だったが、Scoreは`4 = 43`、`1 = 2`であり、M5の品質条件を満たさない。

加えて、全9ケースのTaskSpecは開始identity不一致時に停止すると明記しているため、開始identity resultは後続readの発行可否を変える真正dependencyである。Candidate193は28 / 45件でidentity確認と後続readを同じmodel stepへ越境発行し、正しい初回frontierは17 / 45件に留まった。`DISPATCH_TRANSITION`はCandidate192と異なる定義へ改訂したが、実挙動を一貫して拘束できなかった。品質と機序の両方が不通過なのでCandidate193を停止し、M6とStandard14へ進めずM1の原因分析へ戻る。

## identity

- prompt: `the-caption-3ce91a4-frontier-bound-dispatch-transition-r1`
- bundle SHA-256: `a392acd88a127cd297e9d714cf19a4f35c5de8b08aaa21513b6a936e380c9bb8`
- reference result ID: `e599690689294c658b52a6a9e301697f`
- Candidate193 pool key: `6922f60afac508cef6e254a08108e32f6eed2ad32814dc7bc7fce048b63ed3af`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- selection ID: `91d409171fe44296825601f1ac60b07d`
- analysis ID: `04e1affbb6f14535aba722bf70c313f3`
- registered result ID: `9630f826932c4abc91cc2a4598ca318d`
- result content SHA-256: `c583bb3905bca95349e3d6c670ad89c08c5f043a36b96775bc823fc22667f4c3`
- raw root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate193-frontier-bound-dispatch-transition-adr9-r2-n5-20260812-r1`

## case別結果

| case | Score 4 / 1 | terminal | reviewer | artifact変更 | identity/read同時発行 |
|---|---:|---|---:|---:|---:|
| ADR01 | 5 / 0 | `completion_ready` 5 | 0 | 5 | 3 / 5 |
| ADR02 | 5 / 0 | `completion_ready` 5 | 0 | 5 | 4 / 5 |
| ADR03 | 5 / 0 | `blocked` 5 | 5 | 0 | 3 / 5 |
| ADR04 | 5 / 0 | `blocked` 5 | 5 | 0 | 2 / 5 |
| ADR05 | 4 / 1 | `blocked` 4、`unavailable` 1 | 5 | 0 | 4 / 5 |
| ADR06 | 4 / 1 | `blocked` 4、`unavailable` 1 | 5 | 0 | 4 / 5 |
| ADR07 | 5 / 0 | `completion_ready` 5 | 5 | 5 | 3 / 5 |
| ADR08 | 5 / 0 | `unavailable` 5 | 0 | 0 | 1 / 5 |
| ADR09 | 5 / 0 | `unavailable` 5 | 5 | 0 | 4 / 5 |

reviewer cardinalityとartifact変更境界は45 / 45、required commandは15 / 15、ADR06の禁止canary配送は0件だった。これらの成立部分は保持する。

## 品質失敗2件

- ADR05 iteration 5 `29ec1617ce944e20aca6290305f885f8`: reviewerはpaired scope evidenceの欠落を理由に`counterexample_found`を作れず、rootは`unavailable`とした。期待terminalは`blocked`である。
- ADR06 iteration 5 `49a0fa751c4847b9a539c54e834529ad`: reviewerは`counterexample_found`を返したが、manifestの`positive_applicability_predicate`ではなく別fieldを観測したcertificateだった。rootは不真正resultを正しく拒否したが、期待terminalは`blocked`であり、結果は`unavailable`となった。

いずれもvalidな低品質runとして保存し、再実行で置き換えない。

## 発行遷移の失敗

全9ケースの開始identity契約は「不一致なら停止する」と明記する。したがって後続readはidentity resultに依存し、同じfrontierへ入らない。Candidate193は28 / 45件でidentityとreadを同じmodel stepから発行し、真正dependencyを越境した。同じcase内でも同時発行と分離が混在しており、`dispatch_frontier`定義がmodelの実発行を一意に拘束したとはいえない。

一方、compound identity/read commandは0件、root commandのmachine-bound終了状態は45 / 45で成立した。collectorが報告したcommand protocol違反171件は、reviewer wrapperの実コマンド37 / 37をcall IDでresultへ対応付けると全件に整数の終了状態があり、真正欠落0件の誤検出だった。この訂正後も、dependency越境28件とterminal不一致2件が残るため結論は変わらない。

## 後続の慎重な因果再判定

同じADR9 r2 TaskSpecと「開始identity不一致なら停止」の解釈をCandidate191の保存45件へ適用すると、identity/read越境は36 / 45、正しい分離は9 / 45だった。Candidate193は越境28 / 45、正しい分離17 / 45なので、直接親に対して8件の部分改善がある。したがって`DISPATCH_TRANSITION`を無作用として全棄却せず、一意拘束に十分だったとも扱わない。個別primitive、独立条項化および次Candidateの親はM1で保留する。

ADR05失敗は、具体的witness certificateに不要な`OBS-PAIRED-SCOPE=missing`をdependencyへ加えた`REVIEW_JUDGEMENT`の過大化だった。ADR06失敗は、reviewerが`positive_applicability_predicate`を観測せずにpositive applicabilityを主張し、rootがそのresultを正しく不受入にした経路だった。前者はidentity/readを正しく分離したrunであり、後者も共同発行resultがfield identityを変えた証拠はないため、2件を`DISPATCH_TRANSITION`の直接故障へ統合しない。

訂正機序監査r2はdispatch集計とcommand call-ID再監査には使えるが、全fieldを現在正本にしない。同監査は旧品質監査を入力にしたため、ADR06 iteration 2・3の`quality_score`が登録resultのScore 4と不一致である。また`result_kind_counts`は観測値ではなく期待値の件数であり、review pathの一部は文字列存在とterminal一致による近似である。品質は登録resultと訂正品質監査、review pathは生traceを正とする。この限定を加えても、Candidate193のM5不通過と停止判断は変わらない。

## KPI境界

9ケース一組の中央値はall-agent token `1,352,019`、経過時間`1,050.119秒`だった。iteration単位のquality中央値は`100.0`だが、これは2件のScore 1を消去しない。品質と機序が不通過なので、効率上の改善・悪化や採用可否へ一般化しない。

## 一次証拠

- [登録result](9630f826932c4abc91cc2a4598ca318d.json)
- [訂正品質監査](candidate193-frontier-bound-dispatch-transition-adr9-r2-n5-audit-r2.json)
- [訂正機序監査](candidate193-frontier-bound-dispatch-transition-adr9-r2-n5-mechanism-audit-r2.json)
- [慎重な機序再判定r3](candidate193-frontier-bound-dispatch-transition-adr9-r2-n5-mechanism-reassessment-r3.json)
- [評価profile](../profiles/candidate193-frontier-bound-dispatch-transition-adr9-r2-medium-m24-n5-cli0146.json)
- [評価設計](../../docs/candidate193-frontier-bound-dispatch-transition-adr9-r2-n5-evaluation-design.md)
- [実行準備監査](../../docs/candidate193-frontier-bound-dispatch-transition-adr9-r2-n5-execution-preparation-audit.md)

## 状態

`candidate193_M5_completed / valid_45 / score4_43_score1_2 / dispatch_dependency_crossing_28 / quality_failed / mechanism_failed / stopped / M1_reopened / M6_not_started / Standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`
