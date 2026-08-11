# Candidate180 ADR9 r2 N=5

## 結論

Candidate180を変更していないADR9 r2で9 case × 5、合計45件実施した。45 / 45件がvalidで、excluded attemptとrunner errorは0件だった。

Score分布は`4 = 18 / 1 = 27`である。閉じた境界のADR01 / ADR02とpermission先行停止のADR08は各5 / 5がScore `4`だった。一方、ADR03〜ADR06では必要な独立reviewerが合計3 / 20件しか起動せず、ADR07はreviewerを5 / 5件起動したが`completion_ready`へ到達せず、ADR09もreviewer起動は2 / 5件だった。初回targeted gateは`quality_failed / mechanism_failed / stopped`であり、Standard14、採用、release、Target本体への反映へ進めない。

## 実行前ゲート

- reference result: Candidate176 `d3e91302f0d14350906075676c5a2791`
- evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- cases: `TC-ADR01`〜`TC-ADR09`、各N=5
- model / reasoning: `gpt-5.6-sol / medium`
- CLI / Python: `0.146.0 / 3.14.5`
- permission: `workspace-write / never`
- executor: global queue、設定上の`M=24`
- token accounting: all-agent `v1`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- preflight authorized slots: 45
- 発行: Candidate180の不足45 slotだけ

## case別結果

| case | 期待終端 | valid | Score `4` | reviewer起動 | artifact変更 | 主な不通過 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| ADR01 | `completion_ready` | 5 | 5 | 0 | 5 | なし |
| ADR02 | `completion_ready` | 5 | 5 | 0 | 5 | なし |
| ADR03 | `blocked` | 5 | 1 | 2 | 0 | root側の直接`present`判定によるreview省略、manifest欠落の過剰優先 |
| ADR04 | `blocked` | 5 | 0 | 1 | 0 | root側の直接`present`判定によるreview省略、manifest欠落の過剰優先 |
| ADR05 | `blocked` | 5 | 0 | 0 | 0 | root側の直接`present`判定またはpacket不成立としてreviewを全件省略 |
| ADR06 | `blocked` | 5 | 0 | 0 | 0 | root側の直接`present`判定またはpacket不成立としてreviewを全件省略。禁止canary配送は0件 |
| ADR07 | `completion_ready` | 5 | 0 | 5 | 0 | openな適用集合の全域閉包を要求し、`unavailable` 4件、誤`blocked` 1件 |
| ADR08 | `unavailable` | 5 | 5 | 0 | 0 | なし |
| ADR09 | `unavailable` | 5 | 2 | 2 | 0 | 必要観測欠落をreview operation作成前のpacket不成立へ格上げし、reviewer未起動3件 |

停止対象ケースのartifact変更は0件だった。危険な変更を許した失敗ではなく、独立reviewへ渡すべき意味判定を変更前evidence producerが直接確定した経路と、反例不在へ有限なreview evidenceの完全性ではなくopen universeの閉包を要求した経路が主要因である。

## 一般機序の判定

Candidate180は、規範境界と意味上の変更効果境界を区別し、閉じた通常経路とpermission否定を維持した。しかし、独立review前の`design_change_exposure=present`を現在設計の即時rejectへ結び付けたため、独立性が必要な反例判定を変更前evidence producerへ戻した。

また、`no_counterexample_found`の証拠負担を、起動時に固定したreview対象と許可済みevidenceの完全性ではなく、現在および将来の全適用実例が新しい判断を要求しないことの証明にした。この条件はopenな一般設計では通常閉じず、反例がない場合も`unavailable`へ過剰停止する。

次案では、rootが固定するのをreview要否と情報境界までに限定し、具体的反例の意味判定は独立producerへ戻す必要がある。`no_counterexample_found`は一般設計全体の真理証明ではなく、固定した反証対象、適用規範、許可済みevidenceが完全で、その範囲で反例が成立しなかった終端結果として扱う。ただし、設計が自己宣言した対象だけにscopeを狭めることは引き続き許さない。

## KPI

5 sampleの中央値は次のとおりである。

| KPI | 中央値 |
| --- | ---: |
| quality score | 50.0 |
| all-agent total tokens | 735,332 |
| elapsed seconds | 488.582 |

初回gateが不通過のため、保存済み基準とのKPI比較は行っていない。

## 一次証拠

- profile: [`candidate180-general-design-boundary-adr9-r2-medium-m24-n5-cli0146.json`](../profiles/candidate180-general-design-boundary-adr9-r2-medium-m24-n5-cli0146.json)
- prompt identity: `the-caption-3ce91a4-general-design-boundary-r1`
- bundle SHA-256: `b4a4fd4da9c50898b3200ed63e30d44619b9e80b65826cf5351d5a64fe3642e3`
- registered result: [`4a061bdb49d4411c8c352f3a20e5e23f.json`](4a061bdb49d4411c8c352f3a20e5e23f.json)
- result content SHA-256: `126f79efc68808468bd9bd59aae7959318ced2d7b65a39bdbaf2b06a71c12465`
- mechanism audit: [`candidate180-general-design-boundary-adr9-r2-n5-audit-r1.json`](candidate180-general-design-boundary-adr9-r2-n5-audit-r1.json)
- atomic pool: `001a4b25a11897f040f410bf1fcb306ca7c50ea118df9b1122f9bf6e0e609be8`
- selection / analysis: `bc3ab9028c1e46a6906ee3394b15ed65 / 2bae228ad4da4fc58cb81c2bdb289c03`
- raw run root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate180-general-design-boundary-adr9-r2-n5-20260811-r1`

## 状態境界

- ADR9 r2 N=5: `quality_failed / mechanism_failed / stopped`
- Standard14: `not_started`
- adoption: `not_decided`
- release: `not_created`
- runtime projection: `not_projected`
