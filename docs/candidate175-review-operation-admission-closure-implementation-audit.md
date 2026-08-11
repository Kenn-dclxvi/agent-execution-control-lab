# Candidate175 review operation admission closure実装監査

## 結論

Candidate175の修正版について、一般修正を必要とする具体的反例は確認されなかった。変更していないADR9 r2の初回評価へ進める。

## 初回監査の反例

初回実装は一般`PRODUCER`と`OWNER_ROLE`も変更していたが、当時の設計文書はDESIGN_ADMISSION外を既存制御のままとしていた。このため、TaskSpecが自然言語で独立producer execution identityを明示していても、新設の専用binding形式でなければ起動できない範囲不一致の反例が成立した。

設計を再度開き、TaskSpecの明示指定を特定fieldまたはschemaではなく、producer execution identityと対応operation identityの直接かつ一意なbindとして定義した。identityを指定しないowner、criterion、pass conditionまたは説明文の役割語だけでは成立しない。DESIGN_ADMISSION required reviewでは、一般条件に加えて専用review contractとreview operationへの一意対応を要求する。

## 再監査

修正版の再監査は`no_counterexample_found`だった。次を確認した。

- 正当な自然言語producer指定を保持する。
- ownerまたはcriterionの役割語だけではworkerを起動しない。
- 一般operationは明示bindingがなければ既存どおりrootをproducerへbindする。
- required reviewは専用binding不足時にrootへfallbackせず、operation作成前に`unavailable`となる。
- review operation仕様はmanifest targetの存在、read成功、receipt、review resultを要求しない。
- packetは許可field-valueとprovenanceだけから新規構築し、禁止key、value、要約、存在状態、禁止source全体を含めない。
- projectionで判定可能なsourceをreviewerのallowed readへ重複追加しない。
- permission非許可、仕様不足、binding不足、projection不成立を全てoperation作成前`unavailable`へ写す。
- Candidate173のreview要否、具体的反例、三つのdisposition、result admission、artifact変更gateを保持する。
- Candidate173との差分はroot `AGENTS.md`の`PRODUCER`、`OWNER_ROLE`、`DESIGN_ADMISSION`という宣言済み範囲だけである。

## Identity確認

- prompt identity: `the-caption-3ce91a4-review-operation-admission-closure-r1`
- parent prompt identity: `the-caption-3ce91a4-concrete-counterexample-adjudication-r1`
- AGENTS SHA-256: `5154291ddb355189ca894cfcb404216ec36e402bba79628bd04d3f8fba356b8a`
- AGENTS Git blob: `4b5ebbd394f5d171149022f6a9a141b148102e29`
- bundle SHA-256: `251afdef36802c6ea3f2c4def3616288fa9054a22c028896c16418ba3e8a5061`

評価case、fixture、oracle、rating contract、合否条件は変更していない。
