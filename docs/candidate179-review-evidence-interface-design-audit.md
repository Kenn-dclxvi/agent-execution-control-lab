# Candidate179 review evidence interface 設計監査

## 対象と情報封鎖

設計identity`candidate179-review-evidence-interface-r26`を実装前に監査した。各review producerには次の3入力だけを許可した。

- `AGENTS.md`
- `docs/candidate179-review-evidence-interface-design.md`
- 直接親Candidate177の`files/AGENTS.md.txt`

会話履歴、Candidate178、評価case、fixture、oracle、rating contract、評価result、他文書およびgit diffは禁止入力とし、対象編集も禁止した。reviewでは抽象型の存在を仮定せず、必須fieldのconstruction authority、既存入力からの構成可能性、root可視性および外部runtime非依存まで検査した。

## 初期設計で確認した問題

初期設計は、起動前source、取得、reviewer resultの三境界を分けたが、次の誤りがあった。

- 既存入力にないsource、manifest、packet item identityを仮定した。
- registryの対象domainを閉じず、source omissionを許した。
- 取得範囲をreviewerの自己申告または外部wrapperの証明へ依存させた。
- runtime snapshotと取得resultのbindingを落とした。
- 構造化valueの再serializationを要求した。
- 三終端の排他、Candidate177のcontract basis、boundary dependency basisおよびsupport一意性を落とした。

取得範囲を新しいsystem-owned envelopeで証明する方向は、repository外のexecutor、tool adapterまたはwrapper変更を必要とするため破棄した。Candidate179はCandidate177のallowed read、forbidden input、semantic projectionおよびsafe aggregationを変更せず、source classとreview resultの写像だけを扱う設計へ戻した。

## 一般修正

reviewで得た反例はcase固有分岐ではなく、次の一般条件へ統合した。

1. observation source identityはreview operationと既存observation identityから構成する。
2. fixed packet itemはsemantic projectionの構文的output occurrenceをcanonical sequenceへ置き、packet item locatorからidentityを構成する。非構造化値は意味分割せず一itemとする。
3. finite manifest全descriptorとsemantic packet全itemを起動前registryへ過不足なく写す。
4. registry membershipと、実際に引用するfixed supportのpath別eligibilityを分ける。
5. observation acquisition resultはreview operation、producer、runtime snapshot、result、source、status、value、individual terminal、receiptを一形で保持する。
6. acquisitionを`admissible_success / admissible_non_success / inadmissible_acquisition`へ排他的に分類し、receipt欠落やunsafe aggregationをsupportへ昇格させない。
7. reviewer terminal result自体を一つのimmutable assessment recordとし、acquisition entryを一度だけ保持する。
8. runtime事実は有限grammarのinstance binding leafだけで表し、inline literalによるreceipt迂回を禁止する。
9. `counterexample_found`は実使用supportだけ、`no_counterexample_found`はmanifest全件receiptとfixed packet integrity、`unavailable`は全required sourceの型付きpartitionへbindする。
10. 同一review operationのassessmentは一回だけとし、dependency失効後は同operationを`unavailable`で停止する。再reviewは新しいoperation identityで行う。

## 最終review

r26の独立reviewは`no_counterexample_found`だった。次を確認した。

- source kindをreviewerの説明、結果fieldまたは取得方法から変更できない。
- 起動後に生まれるproducer result、snapshot、statusおよびreceiptを起動前必須fieldへ逆流させない。
- source identityとpacket item locatorを意味判断なしに構成できる。
- acquisition result、意味判定、support bindingおよびterminalを一つのroot可視recordへ閉じる。
- Candidate177の反例優先終端、individual receipt、safe aggregation、forbidden input、semantic projectionおよび局所失効を保持する。
- rootはidentity、schema、集合、receiptおよび参照だけを照合し、反例意味を再判定しない。
- 外部executor、tool adapter、runtime hook、wrapperまたはTarget本体の変更を必要としない。

この結果は設計反例の不在を示す。実装、評価、採用、releaseまたはTarget本体へのprojectionを意味しない。
