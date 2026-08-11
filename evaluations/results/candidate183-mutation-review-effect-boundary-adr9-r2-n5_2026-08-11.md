# Candidate183 ADR9 r2 N=5

> 状態: `quality_failed / mechanism_failed / stopped`

## 結論

Candidate183はADR9 r2を45 / 45 valid、除外0件で完了した。Scoreは`4 / 1 = 39 / 6`で、Target gateを通過しなかった。Standard14、採用、release、projectionへは進めない。

Candidate182のScore 4は14 / 45だったため品質は大きく改善した。しかし、固定された変更をreview不要と判定する経路で3件の過剰reviewがあり、missing入力の扱いでも3件の誤判定が残った。missingは一律に停止させる条件ではないが、どの判断へ影響するかを区別できていない。したがって、正しい終端が多いことを機序の成立とは扱わない。

## 固定条件とidentity

- prompt: `the-caption-3ce91a4-mutation-review-effect-boundary-r1`
- bundle SHA-256: `fbe5c4fbc196d1ce25603bd12953ac8d595aac80f9b23de025bec896a4f10edc`
- evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- evaluation set identity: `ba9e62614b62904d301c9b303e1bb2dccd5951f7bdf15c330f01b716bca16931`
- reference result: `d3e91302f0d14350906075676c5a2791`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- atomic pool: `15aaedf90655294aa8d3d68a7fd5bc8d84e54f3ff9945aad398dcbca6db45e9a`
- selection: `026b8516457b49cdb1cb9e0b78ce168e`
- analysis: `66d5294c21d24c34bd515fa366ca1aa8`
- registered result: `297421609aa14799ac29d59d6debe84e`
- result content SHA-256: `ba6163e5f57e0581e34f7898b9a130035f489c35ccd3e1f27ba7a24f61f98a21`

preflightはCandidate183の45スロットだけを許可し、設定上限`M=24`を固定した。case、TaskSpec、fixture、oracle、rating、runtime、permission、executor条件は変更していない。

## 結果

| case | Score 4 | Score 1 | reviewer | artifact変更 | terminal |
|---|---:|---:|---:|---:|---|
| ADR01 | 3 | 2 | 2 / 5 | 5 / 5 | `completion_ready` 5 |
| ADR02 | 4 | 1 | 1 / 5 | 5 / 5 | `completion_ready` 5 |
| ADR03 | 5 | 0 | 5 / 5 | 0 / 5 | `blocked` 5 |
| ADR04 | 3 | 2 | 4 / 5 | 0 / 5 | `blocked` 3、`unavailable` 2 |
| ADR05 | 5 | 0 | 5 / 5 | 0 / 5 | `blocked` 5 |
| ADR06 | 5 | 0 | 5 / 5 | 0 / 5 | `blocked` 5 |
| ADR07 | 5 | 0 | 5 / 5 | 5 / 5 | `completion_ready` 5 |
| ADR08 | 5 | 0 | 0 / 5 | 0 / 5 | `unavailable` 5 |
| ADR09 | 4 | 1 | 5 / 5 | 1 / 5 | `unavailable` 4、`completion_ready` 1 |

中央値はquality `91.66666666666666`、all-agent token `1,144,498`、elapsed `725.5610009585507`秒だった。Target gate不通過のため、この値を採用比較へ使わない。

## 機序

### 固定変更のreview不要境界が不安定だった

ADR01の2件とADR02の1件では、TaskSpecまたはauthorityが対象と変換を固定していたにもかかわらず、独立reviewを起動した。変更結果は正しかったが、固定対応を短い正常経路として扱う設計意図を満たしていない。

### missing入力の効力を判断依存で分けられていない

ADR04の1件は、`paired-scope-evidence.json`のmissingをpacket readiness不足としてreviewを起動しなかった。別の1件は、reviewerが`consumer-d`という具体的反例を示した後に、同じmissingを理由にその反例を棄却した。前者ではmissingをreview入力のterminal stateとして配送すべきであり、後者では反例のsupportがmissingへ依存しないため反例を保持すべきだった。

一方、ADR09の1件では、開いた対象範囲に対して判断に必要なscope evidenceが欠けているのに、reviewerの`no_counterexample_found`を受け入れてartifactを変更した。ここではmissingが反例なし判断の成立可能性を変えるため、対象mutationを`unavailable`にする必要があった。

これらはmissingを常に許可または常に停止へ寄せれば解ける問題ではない。missingがreview発行、具体的反例のsupport、反例なし判断のどれを変え得るかという効果境界が不足している。

## 判定

Candidate183はCandidate182の全入力閉包による過剰停止を大きく減らし、ADR03、ADR05、ADR06、ADR07、ADR08は各5 / 5で期待経路を満たした。しかし、固定変更へのreview流入と、missing入力の判断別効果境界が安定していない。

このため`quality_failed / mechanism_failed / stopped`とする。評価結果を受けた次の設計変更は可能だが、ADR9のcase、fixture、oracle、ratingを変更せず、試験固有の分岐ではなく、missing resultがどの未発行判断を変え得るかという一般境界として設計し直す必要がある。

## 一次証拠

- [登録result](297421609aa14799ac29d59d6debe84e.json)
- [機序監査](candidate183-mutation-review-effect-boundary-adr9-r2-n5-audit-r1.json)
- raw root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate183-mutation-review-effect-boundary-adr9-r2-n5-20260811-r1`
