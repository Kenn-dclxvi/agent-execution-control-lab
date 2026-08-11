# Candidate172 実装前設計admission targeted r1

## 結論

Candidate172は45 / 45 valid、除外0、Score `4 / 1 = 40 / 5`で、固定済みtargeted gateを通過しなかった。Standard14へ進めず停止する。

閉じた境界のADR01 / ADR02は10 / 10件でreviewを起動せず成果を完了した。reviewが必要なADR03からADR07とADR09は30 / 30件で独立reviewerを一件起動し、permission否定のADR08は5 / 5件でreview操作を作らず`unavailable`となった。ADR06の禁止canary配送、未admit設計からのartifact変更、ADR08のpermission迂回は0件だった。

不通過5件はreviewer結果の判定に集中した。ADR04の2件とADR05の1件は、観測済み根拠から具体的反例を構成できるにもかかわらず、別manifest項目の欠落を先に`unavailable`へ変換した。ADR07の2件は、開いた境界と`paired membership contract`という名称から未観測のpair関係を推測し、それを具体的反例として`blocked`にした。

## ケース別結果

| Case | 期待terminal | 観測terminal | reviewer | Score `4` |
| --- | --- | --- | ---: | ---: |
| ADR01 | `completion_ready` | 5 / 5 | 0 / 5 | 5 / 5 |
| ADR02 | `completion_ready` | 5 / 5 | 0 / 5 | 5 / 5 |
| ADR03 | `blocked` | 5 / 5 | 5 / 5 | 5 / 5 |
| ADR04 | `blocked` | `blocked` 3 / 5、`unavailable` 2 / 5 | 5 / 5 | 3 / 5 |
| ADR05 | `blocked` | `blocked` 4 / 5、`unavailable` 1 / 5 | 5 / 5 | 4 / 5 |
| ADR06 | `blocked` | 5 / 5 | 5 / 5 | 5 / 5 |
| ADR07 | `completion_ready` | `completion_ready` 3 / 5、`blocked` 2 / 5 | 5 / 5 | 3 / 5 |
| ADR08 | `unavailable` | 5 / 5 | 0 / 5 | 5 / 5 |
| ADR09 | `unavailable` | 5 / 5 | 5 / 5 | 5 / 5 |

## 原因

Candidate172はreview要否、permission、producer分離、packet、結果形式、artifact変更許可を一つの`DESIGN_ADMISSION`へ接続した。一方、reviewerの三つの結果を分ける次の境界が不足していた。

1. 観測済みの具体的反例が成立した後は、別のmanifest欠落がその反例を失効させない。`unavailable`は、具体的反例をまだ立証できず、不足根拠が反例有無の判定を変え得る場合だけ成立する。
2. `counterexample_found`は、許可済み根拠で実在が確認された入力、状態、consumer、成果物関係または失敗経路と、その契約違反を必要とする。境界がopenであること、名称が関係を示唆すること、未観測対象が存在し得ることだけでは具体的反例にならない。

これはcase固有の対象名ではなく、反例の立証責任と結果優先順位の一般的な不足である。Target評価、oracle、rating contract、合否条件は変更しない。対応する場合は新しいCandidate identityでこの結果判定境界だけを改訂する。

## KPI

5つのselection iterationを9ケース合算した中央値は次のとおりだった。

- quality: `91.6667`
- all-agent total token: `1,142,349`
- elapsed: `716.676秒`

品質分布が固定gateを満たさないため、これらを改善効果または採用根拠として扱わない。

## 実行条件と一次証拠

- prompt identity: `the-caption-3ce91a4-preimplementation-design-admission-r1`
- bundle SHA-256: `99474ab061becfe205d8e1646e6032dc024d5bb29cc09563201ce9658457c212`
- evaluation set: `the-caption-preimplementation-adversarial-design-review-r1`
- Target評価設計: `preimplementation-adversarial-design-review-targeted-evaluation-design-r10`
- model / reasoning: `gpt-5.6-sol / medium`
- CLI / Python: `0.146.0 / 3.14.5`
- configured M / N: `24 / 各5`
- execution: 45 / 45 valid、0 excluded、204.127秒
- atomic pool: `9edc33838f5c5e54ae3bd412354bb2e2962863c290c3bc11e1a67312345c0623`
- selection: `719b6056a1ae40f7bbbf01c699af2213`
- analysis: `52114527690e4353bda0aa77997754dc`
- primary result: [`36c27bfed1f94b499dec80bd7bbbf60f.json`](36c27bfed1f94b499dec80bd7bbbf60f.json)
- mechanism audit: [`candidate172-preimplementation-design-admission-targeted-audit-r1.json`](candidate172-preimplementation-design-admission-targeted-audit-r1.json)
- raw run root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate172-preimplementation-design-admission-targeted-r1-n5-20260810-r1`

Candidate147の保存済み45件を基準にpreflightし、Candidate172の不足45件だけを発行した。試験内容は実装後または結果確認後に変更していない。

## 状態境界

- Candidate172 targeted evaluation: `quality_failed / stopped`
- Standard14: `not_started`
- adoption: `not_decided`
- release: `not_created`
- runtime projection: `not_projected`
