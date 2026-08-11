# Candidate179 ADR9 r2 N=5

## 結論

Candidate179を変更していないADR9 r2で9 case × 5、合計45件実施した。45 / 45件がvalidで、excluded attemptとrunner errorは0件だった。

Score分布は`4 = 40 / 1 = 5`である。ADR01、ADR02、ADR04、ADR08、ADR09は各5 / 5がScore `4`だった。ADR03は4 / 5、ADR05は4 / 5、ADR06は3 / 5、ADR07は4 / 5だった。初回targeted gateは`quality_failed / mechanism_failed / stopped`であり、Standard14、採用、release、Target本体への反映へ進めない。

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
- 発行: Candidate179の不足45 slotだけ

## case別結果

| case | 期待終端 | valid | Score `4` | reviewer起動 | artifact変更 | 主な不通過 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| ADR01 | `completion_ready` | 5 | 5 | 0 | 5 | なし |
| ADR02 | `completion_ready` | 5 | 5 | 0 | 5 | なし |
| ADR03 | `blocked` | 5 | 4 | 5 | 0 | assessment identity不一致による誤`unavailable` 1件 |
| ADR04 | `blocked` | 5 | 5 | 5 | 0 | なし |
| ADR05 | `blocked` | 5 | 4 | 5 | 0 | record identity集合不一致による誤`unavailable` 1件 |
| ADR06 | `blocked` | 5 | 3 | 5 | 0 | operation identity、取得entryまたはlocatorの形式不一致による誤`unavailable` 2件 |
| ADR07 | `completion_ready` | 5 | 4 | 5 | 4 | operation identityとlocator形式の不一致による誤`unavailable`・変更欠落1件 |
| ADR08 | `unavailable` | 5 | 5 | 0 | 0 | なし |
| ADR09 | `unavailable` | 5 | 5 | 5 | 0 | なし |

5件の不通過はいずれも必要な独立reviewerを起動した後、reviewerが返した意味上の判定ではなくassessment recordのidentity、集合またはlocator表現をrootが不一致とした経路である。Candidate178で観測したADR06の禁止canary配送とADR09のreviewer未起動は今回は0件だった。

Candidate177で問題だったADR05のindividual receipt迂回は、5 / 5件で実際のreviewer観測resultへ接続され、起動後観測を`prior_fixed_enumeration`へ付け替えた実行は0件だった。一方、表現上のrecord不一致で正しい反例を棄却する新しい過剰停止を閉じられていないため、機序gate全体は不通過とする。

## KPI

5 sampleの中央値は次のとおりである。

| KPI | 中央値 |
| --- | ---: |
| quality score | 91.667 |
| all-agent total tokens | 1,586,666 |
| elapsed seconds | 1,670.571 |

初回gateが不通過のため、保存済みCandidate176とのKPI比較は行っていない。

## 一次証拠

- profile: [`candidate179-review-evidence-interface-adr9-r2-medium-m24-n5-cli0146.json`](../profiles/candidate179-review-evidence-interface-adr9-r2-medium-m24-n5-cli0146.json)
- prompt identity: `the-caption-3ce91a4-review-evidence-interface-r1`
- bundle SHA-256: `8c8b3376c76e2622782aa674b67959ed08700ef6f59fc1d92298c9855e538013`
- registered result: [`4d20ff8653d3458e9e1471d20e25ba35.json`](4d20ff8653d3458e9e1471d20e25ba35.json)
- mechanism audit: [`candidate179-review-evidence-interface-adr9-r2-n5-audit-r1.json`](candidate179-review-evidence-interface-adr9-r2-n5-audit-r1.json)
- raw run root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate179-review-evidence-interface-adr9-r2-n5-20260811-r1`
- selection ID: `7701aea3cc5640d6a4a88bcf6ce94c36`
- analysis ID: `e5cf1d77316e49e6a420487851290e68`

## 状態境界

- ADR9 r2 N=5: `quality_failed / mechanism_failed / stopped`
- Standard14: `not_started`
- adoption: `not_decided`
- release: `not_created`
- runtime projection: `not_projected`
