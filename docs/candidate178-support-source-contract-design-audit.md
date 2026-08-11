# Candidate178 support source contract 設計監査

## 対象

- `docs/candidate178-support-source-admission-design.md`
- 直接親Candidate177の`files/AGENTS.md.txt`

各reviewは対象編集を禁止した独立producerへ固定し、評価result、過去review出力、Candidate178実装、期待判定、会話履歴およびその他のrepository fileを禁止入力とした。

## 初期案の破棄

初期案は`support source admission`を一predicateへ集約し、packet projectionをsource classとして扱った。反例修正を重ねるうちに、既存TaskSpecとrepository authorityが持つ信頼境界までCandidate178内のauthorization chainで再証明する設計へ拡張した。

この方向は、一つの変更目的と一predicateを混同し、新しい認証基盤を設計対象へ入れていたため破棄した。初期案のreview結果は実装許可へ使用していない。

## 再設計

変更目的を「reviewerのsource自己申告による根拠資格の変更を防ぐ」に戻し、次の協調要素からなる一つの一般契約として再設計した。

1. `observed_fact`と`prebound_authority`のsource資格
2. 起動前authority candidate packetと起動後completion
3. 完成済みsupportのpacket projection
4. 非authorityのreview subject reference
5. 全counterexample path共通のresult admission
6. source、manifest、projection、subject、terminal resultの局所失効

信頼起点は既存TaskSpec authority receiptまたは適用中repository authority receiptだけとし、Candidate178内でauthorization chainを作らない。

## 再設計後の主な反例修正

- TaskSpec item bindingとrepository artifact bindingを排他的reference形へ分けた。
- 無条件authorityへ存在しないruntime snapshotを要求しないsource別projection schemaにした。
- authority bindingと意味判定用semantic projectionを分けた。
- conditional applicabilityへ必要descriptor集合、個別observed support、決定的evaluation receiptを固定した。
- 正常なfalse評価を`not_applicable`としてno-counterexample closureへ含めた。
- conditional authorityの起動前candidate packetと起動後support completionを分けた。
- fixed design / boundary ledgerをauthorityではなくreview subjectとして分けた。
- Candidate177の旧source schemaを新schemaへ明示置換した。
- observed factにも意味判定用exact contentとcontent matching receiptを要求した。
- source、manifest membership、manifest全体closure、authority content、semantic projection、packet、review subject、review terminal resultを型付きdependencyへ固定した。

## 最終review結果

設計identity`candidate178-support-source-contract-restart-r26`に対する独立reviewは`no_counterexample_found`だった。

確認された閉包は次のとおりである。

- source偽装、receiptなし観測、hash-only意味補完をadmitしない。
- 正規packet projectionとcandidate packetはrepository再読込を要求しない。
- normative、decision-premiseその他のpath名変更でsource admissionを迂回できない。
- rootはidentity、schema、value、receipt、provenance、snapshot、lineageだけを照合し、反例意味を再判定しない。
- Candidate177のsafe aggregation、反例優先終端、result invalidation localityを保持する。
- `counterexample_found`は直接supportだけ、`no_counterexample_found`はfinite manifest全体closureへ依存する。

この結果は設計反例の不在を示す。実装、評価、採用、releaseまたはTarget本体へのprojectionを意味しない。
