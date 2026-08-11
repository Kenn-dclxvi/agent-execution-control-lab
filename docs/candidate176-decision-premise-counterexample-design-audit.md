# Candidate176 設計判断前提の反証設計監査

## 初版

- result: `counterexample_found`
- implementation admission: rejected
- allowed inputs: 一般仕様、Candidate176初版、Candidate175実装promptだけ
- forbidden inputs: ADR9 / Standard14のケース、fixture、oracle、評価結果、過去監査、Candidate176実装

確認した反例は次の3件である。

1. 非明示の判断前提候補について不足根拠を作り、全manifest成功でも`unavailable`へ送れる。
2. 判断前提経路は規範predicateを必要としない一方、結果受入条件が従来の規範用`contract_basis`を前提としており、経路別証拠が閉じていない。
3. 前提と観測のsnapshot対応がreview起動前に固定されず、reviewerが後付けで同一視または分離できる。

初版は実装せず、第2版で`not_applicable`、型付き結果経路、起動前snapshot対応を追加した。第2版は新しいdesign identityとして再監査する。

## 第2版

- result: `counterexample_found`
- implementation admission: rejected

確認した反例は次の4件である。

1. 先行固定authorityの列挙だけで反証できる場合にもmanifest observation identityとsuccess receiptを無条件に要求していた。
2. 結果のpremise identity以外について、scope、snapshot、relation、receiptと起動前descriptorの完全一致が明示されていなかった。
3. 監査へ設計artifact全体を渡す指示が、artifact内の履歴・状態・先行監査情報を除外するCandidate175のsemantic projectionと矛盾した。
4. 規範経路の追加必須値に明示fieldがなく、discriminated unionを機械的に検証できなかった。

第2版は実装しない。第3版はsemantic designだけを独立review packetへ射影し、証拠源別descriptor、全field完全一致、排他的な経路別schemaを固定する。

## 第3版

- result: `counterexample_found`
- implementation admission: rejected

確認した反例は次の5件である。

1. `prior_fixed_enumeration` descriptorの証拠を確認せず`no_counterexample_found`へ進めた。
2. receipt metadataと、結果が反例として報告する具体的事実の値が一致する保証がなかった。
3. 単一値relationまたは基数predicateの直接否定が未定義だった。
4. 中間的な`continue`を終端的な`stop`の否定として扱えた。
5. 複数のboundary dependency basisを単一値へ変換する規則がなく、root生成または任意の`unavailable`が残った。

第3版は実装しない。第4版では全descriptor証拠完了を`no_counterexample_found`の前提にし、具体的事実の構造化field完全一致、predicate type別の否定、terminal phaseとhorizon、dependency basisの完全一致集合を固定する。

## 第4版

- result: `counterexample_found`
- implementation admission: rejected

第4版は、複数のpredicate typeと二つの証拠源を同時に扱ったため、descriptor、結果schema、親のmanifest descriptor、rootの機械照合の間に10件の非一意性が残った。主な問題は、identity名の不一致、証拠源別schema不足、predicate固有field不足、snapshot relationの未検証、dependency basisの役割欠落、factとreceiptの対応不足、`no_counterexample_found` schema不足、成立済み反例とmissingの優先順位矛盾、親のsemantic projectionとの不整合、rootによる自由記述の意味判定である。

第4版は実装しない。第5版は実測問題に必要な`relation_nonexistence`だけへ変更軸を限定し、証拠源をCandidate175のfinite manifest observationへ統一する。単一値、基数、terminal transition、先行固定列挙の新経路は本Candidateの対象外とする。

## 第5版から第12版

第5版から第12版は、前提sourceの選別責任、起動前descriptorと実行時witnessの区別、全source coverage、snapshot provenance、先行固定列挙との組合せなどの反例を受け、いずれも実装せずrejectした。

## 第13版

- semantic packet identity: `sha256:aac076e57ae2a093753444f9ce70d6bbb67038c4378e53c3472f5a97ea925cda`
- allowed inputs: 一般仕様、Candidate176第13版semantic packet、Candidate175 promptだけ
- result: `no_counterexample_found`
- implementation admission: passed

確認した境界は、明示前提への限定、複数`fact_supports`、supportごとの排他的source schema、同一instance / scope / snapshot / operation、非明示候補の`not_applicable`、成立済み反例の優先、root非代行、Candidate175制御の保持、case固有分岐の不在である。
