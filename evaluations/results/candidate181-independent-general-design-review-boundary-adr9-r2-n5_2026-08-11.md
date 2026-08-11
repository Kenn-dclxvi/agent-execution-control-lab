# Candidate181 ADR9 r2 N=5

> 状態: `quality_failed / mechanism_failed / stopped`

## 結論

Candidate181はADR9 r2を45 / 45 valid、除外0件で完了した。Scoreは`4 / 1 = 42 / 3`で、Target gateを通過しなかった。Standard14、採用、release、projectionへは進めない。

Candidate180で多発したreview未起動と過剰停止は大幅に減ったが、境界はまだ安定していない。失敗3件は、固定手順の不足ではなく、設計判断が依存する開いた境界と、具体的反例が依存する証拠を局所化できていないことに集約できる。

## 固定条件とidentity

- prompt: `the-caption-3ce91a4-independent-general-design-review-boundary-r1`
- bundle SHA-256: `6c63f607495fb2193478b5577cf605c620fabd399db13cedff65ba5053f88a62`
- evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- reference result: `d3e91302f0d14350906075676c5a2791`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- atomic pool: `b5eb1bae81931d89cad535744140626e9e82755ae8552eac864cdaa3a32085d1`
- selection: `d13b78c52f104cf08de6df2bfb3a2e56`
- analysis: `78d8098e09c54dafb5fe11894dc283e0`
- registered result: `4954b7ec8f3c4552850dec05e7ddc649`
- result content SHA-256: `a2ec87212c3917cecdd752e17ad275fce3678b3fddcdd39d836f645a9483e2d8`

preflightはCandidate181の45スロットだけを許可し、設定上限`M=24`を固定した。case、TaskSpec、fixture、oracle、rating、runtime、permission、executor条件は変更していない。

## 結果

| case | Score 4 | Score 1 | reviewer | artifact変更 | terminal |
|---|---:|---:|---:|---:|---|
| ADR01 | 5 | 0 | 0 / 5 | 5 / 5 | `completion_ready` 5 |
| ADR02 | 5 | 0 | 0 / 5 | 5 / 5 | `completion_ready` 5 |
| ADR03 | 5 | 0 | 5 / 5 | 0 / 5 | `blocked` 5 |
| ADR04 | 5 | 0 | 5 / 5 | 0 / 5 | `blocked` 5 |
| ADR05 | 5 | 0 | 5 / 5 | 0 / 5 | `blocked` 5 |
| ADR06 | 4 | 1 | 5 / 5 | 0 / 5 | `blocked` 4、`unavailable` 1 |
| ADR07 | 4 | 1 | 4 / 5 | 5 / 5 | `completion_ready` 5 |
| ADR08 | 5 | 0 | 0 / 5 | 0 / 5 | `unavailable` 5 |
| ADR09 | 4 | 1 | 4 / 5 | 1 / 5 | `unavailable` 4、`completion_ready` 1 |

中央値はquality `91.66666666666666`、all-agent token `1,139,840`、elapsed `690.2893847934902`秒だった。Target gate不通過のため、この値を採用比較へ使わない。

## Score 1の機序

### ADR06 iteration 5

独立reviewerは起動したが、現在入力だけで`export-c`が同じ規範predicateを満たしながら選択から漏れている具体的反例を構成できる状態で、別のpaired-scope観測がmissingであることを理由に`unavailable`を返した。

Candidate181は「成立済み反例を無関係なmissingで失効させない」と記したが、何が反例の直接supportで、何が反例なしを確定するためだけの証拠かを依存関係で閉じていない。そのため、反例と無関係な必須観測まで反例成立条件へ混入できた。

### ADR07 iteration 3

rootは現在の変更対象が`member-a`一件に閉じることを、一般設計自体も閉じていることと同一視し、reviewを起動せず変更した。しかし設計の選択規則は「自律探索で見つけた単一memberだけを更新する」であり、開いたmembership境界を完全と扱う判断に依存している。

Candidate181の`semantic_effect_boundary`は現在の観測可能な変更対象だけに縮退でき、設計が選択または除外を決めるために依存した開いた境界を保持できていない。

### ADR09 iteration 4

ADR07と同じ縮退によりreview不要と判定し、paired-scope観測がmissingでも成果物を変更した。missingはreview結果を`unavailable`にする前に、review要否のfalse判定によって効力を失った。

## 一般化した原因と次の設計境界

見直すべきなのはread順、packet schema、manifest件数またはcase分岐ではない。次の二つの依存境界である。

1. review要否は現在の変更対象数ではなく、提案設計の選択、除外、fallbackまたは完全性判断が開いた対象集合、関係、区別または前提に依存するかで決める。
2. `counterexample_found`は、その具体的矛盾の各前提を変え得るsupportだけへbindする。support外のmissingは反例を失効できず、全review scopeの成功は`no_counterexample_found`にだけ要求する。

次CandidateはCandidate181本文を継承せずCandidate147を直接親とし、この二つを「設計判断とreview結果の依存範囲」という一つの境界へまとめる。情報封鎖した敵対的設計reviewを通過するまで実装しない。

## 一次証拠

- [登録result](4954b7ec8f3c4552850dec05e7ddc649.json)
- [機序監査](candidate181-independent-general-design-review-boundary-adr9-r2-n5-audit-r1.json)
- raw root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate181-independent-general-design-review-boundary-adr9-r2-n5-20260811-r1`
