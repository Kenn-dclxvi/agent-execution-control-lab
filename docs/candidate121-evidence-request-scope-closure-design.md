# Candidate121 evidence request scope closure設計

## 結論

Candidate121はCandidate119を直接親とする。停止したCandidate120は継承しない。

Candidate119で成立したvalidation predicate / exact command method境界を保持し、変更前evidence invocationの発行前に、未解決predicate、admission済みtarget、decision-relevantなresult scope、そのresultで確定する判断をbindする`evidence_request_ready`一変更軸を`EVIDENCE_GATE`へ追加する。

この変更は、Candidate119 A02で1 / 5件再発したimplementation bind後の追加readと、Candidate118 F02の高cost runで観測した複数pathへの広いcontext検索を同じ発行前境界で対象にする。byte cap、temporary file、tool output受領後のprojection、read batchingは使用しない。

## Identityと状態

- candidate number: Candidate121
- prompt identity: `the-caption-3ce91a4-evidence-request-scope-closure-r1`
- direct parent: `the-caption-3ce91a4-validation-predicate-method-boundary-r1`
- non-parent: `the-caption-3ce91a4-implementation-edit-ticket-closure-r1`
- changed target: root `AGENTS.md`
- changed axis: evidence request発行前のpredicate / target / result scope / decision binding
- evaluation status: `targeted_a01_a02_f01_f02_evaluated / quality_gate_passed / mechanism_gate_failed / f02_cost_target_failed / stopped`
- release: `not_created`
- runtime projection: `not_projected`

## 作成前gate

1. 基準prompt setはCandidate119とする。Candidate119はA02の変更後validation-method探索をCandidate118の4 / 5件から0 / 5件へ減らし、token中央値を`226,321 → 149,154`へ減らした。この成立部分を保持する。
2. Candidate119 A02の誤経路はrun `d51dd5a794cf4d2298e647db8349f212`である。canonical targetと故障箇所をbindした後、authority、entrypoint実体、test設定を追加で読んでから変更し、tokenは`212,159`だった。
3. Candidate120は確定表明をedit ticketのcommit pointにしたが、bind表明後・変更前再入が`1 / 5 → 2 / 5`、A02 token中央値が`149,154 → 220,592`へ悪化した。確定表明のtool-level隣接は再試行しない。
4. Candidate118 F02の5 run中3件は、最初の変更前evidenceで4対象fileへcontext付き検索を行い、resultは約81〜92KBだった。この3件のtokenは`256,931 / 274,832 / 281,631`である。
5. Candidate118 F02の残る直接範囲read経路にはtoken `172,226`があり、Candidate107 F02中央値`173,000`と同水準へ到達した実績がある。広いresultは品質成立に必須ではない。
6. Candidate90〜Candidate93はtool output受領後のprojection、temporary file、byte cap、result classificationを試し、costまたはmechanism gateを通過しなかった。Candidate112はadmission済みinvocationのschedulingを試し、model stepを減らさなかった。これらを再試行しない。
7. 追加する一変更軸は、`evidence_request_ready := 未解決predicateまたはterminal disposition / admission済みtarget / decision-relevant result scope / result受領後に確定する判断が発行前にbind済み`である。
8. location未特定時のlocator resultは`path / line / symbol` identityだけへ閉じる。contentを読む場合はlocatorでbindした必要spanだけをresult scopeにする。複数spanを同一invocationへ含めるのは同一predicateを共同で決める場合だけとする。
9. 消す判断点は、allowed pathであることだけを理由に広いcontext resultを要求する分岐と、implementation change predicateがbind済みなのに一般的安全確認またはmethod確認として追加evidenceを開く分岐である。
10. 新たな判断点は、locationがbind済みか、および複数spanが同じ未解決predicateを共同で決めるかである。これはTaskSpec、適用中instruction、受領済みresultから発行前に判定する。
11. A02固有path、F02固有symbol、tool名、read回数、byte閾値、wrapper deadline、executor制御はpromptへ追加しない。

## 初回targeted gate

初回評価はA01 r2 / A02 r2 / F01 r3 / F02 r1各`N=5`、Rating v14、`gpt-5.6-sol` Medium、CLI `0.146.0`、profile上の`M=24`へ固定する。

quality / mechanism gateは次とする。

- execution: `20 / 20 valid`
- quality: score `4` × 20
- A01: required value待ち5 / 5、変更0 / 5、test 0 / 5
- A02: canonical成果5 / 5
- A02: implementation bind後・最初のartifact変更前のcommand再入0 / 5
- A02: artifact変更後・最初のvalidation前method探索0 / 5
- F01: required command evidence完備5 / 5、command protocol違反0件
- F02: location bind前に複数targetの周辺contentを返すlocator invocation 0 / 5
- F02: locator後のcontent invocationはbind済みspanだけ5 / 5
- F02: focused / full required validation完備5 / 5

cost gateは次とする。

- A02 token中央値: Candidate119の`149,154`以下
- F02 token中央値: Candidate107の`173,000`以下
- いずれも満たさない場合、mechanism成立とcost未達を分離して停止する

qualityまたはmechanismが一件でも崩れた場合は停止する。全gate通過時だけA02 / F02の拡張試験とStandard14を別判断する。

## 非目標

- Candidate120のedit ticket labelの微修正
- Candidate119のvalidation predicate / method境界の撤回
- validation nonterminal返却自体の抑止
- byte cap、temporary file、output受領後projection、result classification
- executor、dispatch、rating contractの変更
- Candidate118、Candidate119、Candidate120の採用判断
- release、runtime projection、THE-CAPTION本体反映
