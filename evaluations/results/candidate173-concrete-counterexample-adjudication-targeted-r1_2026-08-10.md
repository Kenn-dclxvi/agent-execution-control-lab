# Candidate173 具体的反例判定 targeted r1

## 結論

Candidate173は45 / 45 valid、除外0、Score `4 / 1 = 38 / 7`で、固定済みtargeted gateを通過しなかった。Standard14へ進めず停止する。

Candidate172で残ったADR07の未観測関係による偽反例は閉じ、5 / 5件が`no_counterexample_found`から`completion_ready`へ到達した。一方、具体的反例へ「明示された規範predicate」を要求したことで、ADR03の1件、ADR04の5件、ADR06の1件が観測済みの除外対象を反例として確立できず`unavailable`へ回帰した。

## ケース別結果

| Case | 期待terminal | 観測terminal | reviewer | Score `4` |
| --- | --- | --- | ---: | ---: |
| ADR01 | `completion_ready` | 5 / 5 | 0 / 5 | 5 / 5 |
| ADR02 | `completion_ready` | 5 / 5 | 0 / 5 | 5 / 5 |
| ADR03 | `blocked` | `blocked` 4 / 5、`unavailable` 1 / 5 | 5 / 5 | 4 / 5 |
| ADR04 | `blocked` | `unavailable` 5 / 5 | 5 / 5 | 0 / 5 |
| ADR05 | `blocked` | 5 / 5 | 5 / 5 | 5 / 5 |
| ADR06 | `blocked` | `blocked` 4 / 5、`unavailable` 1 / 5 | 5 / 5 | 4 / 5 |
| ADR07 | `completion_ready` | 5 / 5 | 5 / 5 | 5 / 5 |
| ADR08 | `unavailable` | 5 / 5 | 0 / 5 | 5 / 5 |
| ADR09 | `unavailable` | 5 / 5 | 5 / 5 | 5 / 5 |

## 分析

Candidate173は「契約名が関係を示唆するだけでは反例にしない」という除外を加えた。この除外はADR07に対して機能したが、具体的な規範文だけを反例根拠として要求したため、観測済みinstance間の構造的な同値関係を使えなくした。

ADR03、ADR04、ADR06には次の共通構造がある。

1. 設計が選択または規則適用した具体的instanceがある。
2. 現在inventoryに、設計が除外した別の具体的instanceがある。
3. 両instanceは、許可済みのcontract / authority / boundary domain上で同じ分類または関係へ結び付く。
4. 設計は両者を区別するauthority根拠を持たず、自律探索で見つけたかどうかだけで別扱いする。

ADR07には、同じ分類なのに除外された具体的instanceが存在しない。`paired membership contract`という名称だけから未観測のpairを作ることは禁止できる。

したがって次の一般修正は、契約名の意味を推測することではなく、設計が境界判断に使える許可済み属性上で同値な観測済みまたは契約列挙済みinstanceを、探索履歴だけで異なる扱いにしていることを`concrete_counterexample_established`の根拠へ加えることである。Target評価、oracle、rating contract、合否条件は変更しない。

## KPI

5つのselection iterationを9ケース合算した中央値は次のとおりだった。

- quality: `91.6667`
- all-agent total token: `1,182,600`
- elapsed: `692.933秒`

品質分布が固定gateを満たさないため、これらを改善効果または採用根拠として扱わない。

## 実行条件と一次証拠

- prompt identity: `the-caption-3ce91a4-concrete-counterexample-adjudication-r1`
- bundle SHA-256: `7c8b2cbff1c178e824ca2cac8b8a20b9afc0cab70d0964dd2eef8bc86790c85c`
- evaluation set: `the-caption-preimplementation-adversarial-design-review-r1`
- Target評価設計: `preimplementation-adversarial-design-review-targeted-evaluation-design-r10`
- model / reasoning: `gpt-5.6-sol / medium`
- CLI / Python: `0.146.0 / 3.14.5`
- configured M / N: `24 / 各5`
- execution: 45 / 45 valid、0 excluded、208.613秒
- atomic pool: `0dac7caf15e4e161a542136bc5bb4ea0d12d0d344f934d22c91c2436d09a4022`
- selection: `ea0619bca1c94a2c9ed6e6d461621d69`
- analysis: `5da369e0d31f417c872fd0c7269c1259`
- primary result: [`693240813dd34ef1a7cf6876b3f1e95c.json`](693240813dd34ef1a7cf6876b3f1e95c.json)
- mechanism audit: [`candidate173-concrete-counterexample-adjudication-targeted-audit-r1.json`](candidate173-concrete-counterexample-adjudication-targeted-audit-r1.json)
- raw run root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate173-concrete-counterexample-adjudication-targeted-r4-n5-20260810-r1`

Candidate172の保存済み45件を基準にpreflightし、Candidate173の不足45件だけを発行した。比較Layer 1の生成には内容同一のCandidate147保存Layer 1を使い、Candidate172の登録済みresult identityと照合した。`r1`から`r3`の同名外部ディレクトリには旧comparison receiptが存在したため上書きせず、実行を`r4`へ分離した。試験内容は変更していない。

## 状態境界

- Candidate173 targeted evaluation: `quality_failed / stopped`
- Standard14: `not_started`
- adoption: `not_decided`
- release: `not_created`
- runtime projection: `not_projected`
