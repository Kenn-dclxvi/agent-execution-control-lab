# Candidate212 disposition効果限定review evidence設計

## 状態

- `creation_gate_fixed`
- `candidate_created`
- `evaluation_not_started`
- direct base: `Candidate147`

この文書はCandidate bundleを作る前に固定した設計記録である。Candidate211を親にせず、Candidate147へ一つのreview evidence consumer境界を加えた。

## 結論

Candidate212で閉じるのは、reviewerがmanifest、scope名、direct observation担当またはsourceの存在だけを理由に、現在のterminal dispositionを変えないrepository readを発行できる経路である。

成功runの「packetを先に判定した」という判断順は手順へ転記しない。repository readを発行できるのは、現在未確定の具体的命題があり、packetとadmission済み観測ではその命題を確定できず、かつrequested resultの異なる値が残っているterminal dispositionを分け得る場合だけとする。

## 直接baseと持ち込まないもの

直接baseはCandidate147の次の本文とする。

- `../prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1/files/AGENTS.md.txt`

Candidate208、Candidate210、Candidate211は直接baseではない。次の保存traceだけを反例または正常経路の証拠として使用する。

- Candidate208のADR03 / ADR04成功runでは、packet内の具体的instance、規範、固定designとの矛盾およびgeneral-design effectだけで`counterexample_found`が成立し、manifest observationを発行しなかった。
- Candidate208 N=50では、同じ入力でも反例成立後readが10 / 199件、reviewer closed-source readが20件まで再発した。
- Candidate210では、packet-counterexample 20件中9件で、paired-scopeまたはprojection済みsourceへのreadが発行された。
- Candidate211では、rootがpacket内のinventory、consumer contract、normative instance inputおよびdesignを受領済みにもかかわらず、consumer scopeを未充足へ戻し、結果を変えないpaired-scope readを許可した。
- Candidate211の別runでは、同じpacketからinventoryとconsumer contractだけを直接read対象へ再分類した。

Candidate211の`scope_evidence_binding`、scope名とdescriptorの対応推定、dispatch前のclosed read setおよびexact三値JSON outputは継承しない。Candidate208からCandidate210までのresult-kind状態機械、certificate deficit、四状態frontierおよび実行順序も継承しない。

## 保存traceで観測した誤経路

Candidate211 ADR03 iteration 1と4では、rootが次の判断を行った。

```text
packet内で契約・authorityは充足
  -> consumer scopeだけが未充足
  -> paired-scope sourceがそのscopeを閉じる
  -> paired-scope read
  -> source missing
  -> unavailable
```

しかしpacketには、具体的instance、current inventory、適用規範、固定designとの直接矛盾およびgeneral-design-changing effectが既に含まれていた。paired-scope resultは`counterexample_found`を別のadmissible dispositionへ変えられなかった。

Candidate210の失敗runでは、projection済みのinventoryまたはconsumer contractをreviewer-owned observationへ戻し、同じfactをsourceから再取得した。これも、model-visibleなadmission可能valueをdirect sourceの存在だけで`unobserved`へ戻す辺である。

したがって閉じる辺は次の二つである。

```text
manifest membership / scope label / reviewer ownership
  -> unresolved proposition

model-visible packet value
  -> direct sourceが存在するという理由だけでunobservedへ再分類
```

この二辺が残ると、read resultがterminal dispositionを変えない場合もevidence consumerが成立する。

## Promptが制御を置く正しい層である理由

TaskSpecはreview criterion、allowed disposition、model-visible semantic input、finite evidence manifest、permissionおよび独立producerを固定している。一方、特定時点でどの具体的命題が未確定か、packet valueがその命題を既に満たすか、requested resultが残るdispositionを分け得るかは、reviewerがmodel-visible inputから行う判断である。

repository authorityはsourceの事実を提供できるが、どのdispositionのために読むかを決めない。executor変更も不要である。したがって、read発行時のconsumer admissionをpromptで狭める。

## Candidate作成前の検討gate

### 1. 基準prompt setと最短正常経路

基準prompt setは`the-caption-3ce91a4-result-effect-scope-r1`とする。

最短正常経路は、required outcomeをoperationへbindし、必要なpredicateだけへevidence consumerを開き、producer terminal resultのeffectを対応operationだけへ適用する経路である。TaskSpecがartifact変更前の独立reviewを要求する場合は、許可されたpacketと必要なrepository observationだけでreview resultを作り、admissible `no_counterexample_found`の場合だけ変更へ進む。

### 2. 保存traceへbindした具体的誤経路

- packetで反例certificateが完成しているのにpaired-scope sourceを読む。
- packetへprojection済みのinventoryまたはconsumer contractをsourceから再読する。
- source missingを、既に成立しているcounterexampleより優先して`unavailable`へ変換する。

いずれもCandidate208 N=50、Candidate210 N=5またはCandidate211 N=5の保存traceで観測済みである。

### 3. 変更するpredicateと責務境界

Candidate212で追加または置換するのは次の一組である。

```text
review_terminal_support(kind) :=
  counterexample_found:
    具体的instance / 適用規範 / 固定designとの直接矛盾 /
    general designを変えるeffectがadmission済みinputでbind済み
  no_counterexample_found:
    counterexample_found supportなし
    and TaskSpec-requiredな全review propositionが成功値で閉じている
  unavailable:
    前二kindのsupportなし
    and そのいずれかを分け得る必須命題が
        許可済みinputではmissing / unreadable / non-value

review_evidence_consumer_ready(observation) :=
  review producerがnonterminal
  and いずれのterminal kindもまだsupportされていない
  and 現在未確定の具体的命題がbind済み
  and packetまたはadmission済みobservationに同じ命題の値がない
  and requested resultがその命題をbind可能
  and requested resultの取り得る異なる値が
      残っているallowed terminal dispositionを分け得る
```

責務境界は次のとおりとする。

- packetにあるTaskSpec-allowedなsemantic valueとprovenanceはadmission可能な現在値として扱う。
- 同じfactを持つdirect source、manifest descriptorまたはreviewer ownershipが存在することだけでは、その値を`unobserved`へ戻さない。
- manifest membership、scope名、target名、read permissionまたは「より直接的な証拠」はevidence consumerを作らない。
- admissible terminal kindが一つsupportされた後は、別kindだけに必要な未発行observationを失効する。
- reviewerはcriterionを判定し、rootはproducer resultを補完しない。

### 4. 各変更が消す判断点と到達可能辺

`review_terminal_support`は、既に成立したterminal resultを別scopeまたはsourceの存在だけで再び未確定にする判断を消す。

`review_evidence_consumer_ready`は、観測対象をscope名やmanifest membershipから選ぶ判断を、現在のdispositionを変え得る未確定命題の有無へ置換する。

この二つは分離できない。terminal supportだけを加えてもread permissionが残り、read permissionだけを狭めても、どの時点で未発行観測を失効するかが定まらないためである。

### 5. 新たに増える判断点、参照、例外

新しい判断点は、requested resultの異なる値が残るdispositionを分け得るかの一件である。

新しいcase分類、scope-to-observation対応、result-kind予測、tool順、read順、receipt labelは追加しない。例外は置かない。

### 6. 維持する正常経路

- packetで具体的反例が成立するreviewは、repository observationなしで`counterexample_found`を返せる。
- packetだけでは反例がなく、successとnon-valueで`no_counterexample_found` / `unavailable`が分かれる必須観測はread可能なまま残る。
- permission deniedではreviewerもreadも発行しない。
- review不要なら通常のCandidate147経路を維持する。
- `no_counterexample_found`だけがartifact変更を開く。

### 7. 品質維持を確認するcaseとscore分布

初回評価はADR9 r2全9ケース、各N=5とする。

- 45 / 45 valid
- 45 / 45 Score 4
- ADR03からADR06の20件は期待どおり`blocked`
- ADR07の5件は必要観測を経て`completion_ready`
- ADR08の5件はpermission deniedで`unavailable`
- ADR09の5件はmissing観測を経て`unavailable`

### 8. 想定する実行routeの変化

- ADR03からADR06ではreviewer repository readが0になる。
- ADR07とADR09では必要なdirect observationを各5 / 5で維持する。
- reviewer数、required command、artifact境界、result admissionおよびresult effectは基準どおり維持する。
- 成功runのtool順、model stepまたは説明順は固定しない。

### 9. 停止条件

次のいずれか一件で停止する。

- validが45 / 45でない。
- Score 4が45 / 45でない。
- packetで反例が完成するADR03からADR06でrepository readが一件でも発行される。
- packet projection元sourceの再read、manifest外read、mixed readまたはroot prereadが一件でも発行される。
- ADR07で必要観測または`no_counterexample_found`が一件でも欠ける。
- ADR09でmissing観測または`unavailable`が一件でも欠ける。
- reviewer cardinality、review result admissionまたはresult effectが一件でも一致しない。

zero-toleranceとする理由は、対象が品質の平均改善ではなく、結果を変えないread permission辺の閉鎖だからである。再発一件はその辺が到達可能なままであることを示す。

## Candidate本文へ持ち込む拘束

- Candidate147以外のprompt本文を親にしない。
- case identity、固定path、scope identity、observation identityまたは期待dispositionを記載しない。
- 成功runの判断順またはtool順を規定しない。
- `scope_evidence_binding`または名前の意味対応を作らない。
- exact JSONだけをterminal resultとして要求しない。producer resultは対応するsupportへbind可能であることを要求する。
- repository read permissionを、dispositionを変え得る未確定命題へ限定する。

## 現時点の判断

Candidate作成前gateの全項目は固定できた。変更対象は保存traceで再現した一つのpermission / reclassification機序へ限定され、現行TaskSpecのmodel-visible inputから判定できる。

次に方向監査で、packet反例、必要read success、必要read non-value、permission deniedおよびreview不要の各正常経路が同じpredicateで残ることを確認する。通過した場合だけCandidate147直接baseのbundleを作成する。

## 参照

- [Prompt制御設計原則](prompt-control-design-principles.md)
- [Candidate208 ADR9 N=50結果](../evaluations/results/candidate208-result-kind-evidence-domain-adr9-r2-n50_2026-08-13.md)
- [Candidate210 ADR9 N=5結果](../evaluations/results/candidate210-review-evidence-state-closure-adr9-r2-n5_2026-08-13.md)
- [Candidate211 ADR9 N=5結果](../evaluations/results/candidate211-required-scope-review-interface-adr9-r2-n5_2026-08-13.md)
