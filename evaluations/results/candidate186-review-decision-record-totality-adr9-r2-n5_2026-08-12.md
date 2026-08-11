# Candidate186 ADR9 r2 N=5

> 状態: `quality_failed / mechanism_failed / stopped`

## 結論

Candidate186はADR9 r2を45 / 45 valid、除外0件で完了した。Score分布は`4 / 1 = 27 / 18`で、Target gateを通過しなかった。Standard14、採用、release、projectionへは進めない。

Candidate185で残ったADR09の危険なartifact変更は0件になった。一方、decision recordの全域要求が入力の意味上の依存関係を安定して区別できず、無関係なmissingまたはreadable入力まで`outcome_sensitive`へ寄せる過剰停止が増えた。Candidate185の`38 / 7`から改善せず、ADR03、ADR04、ADR06、ADR07と有限固定効果の経路で明確に退行した。

## 固定条件とidentity

- prompt: `the-caption-3ce91a4-review-decision-record-totality-r1`
- bundle SHA-256: `74b8e79c30be036aa02ff79f4a0efe2fa0035e4c69e8f61c029fa3ac19848c02`
- evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- evaluation set identity: `ba9e62614b62904d301c9b303e1bb2dccd5951f7bdf15c330f01b716bca16931`
- reference result: `d3e91302f0d14350906075676c5a2791`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- atomic pool: `d8930bff40a67bc477c24e9cef92f609f5fdf19849a03bc4e631686cd97eca29`
- selection: `28dd688c5a1a45ebaa55d94b0920e722`
- analysis: `35898ac2b3e04def82e552d04cc57834`
- registered result: `614a74e5a4f94fe18e73f5d43ac630fb`
- result content SHA-256: `2396c12cf3698ce553feda753c99300c588ace80b015099fb5f54a6e30d5bfa7`

preflightはCandidate186の新規45スロットだけを許可し、設定上限`M=24`を固定した。case、TaskSpec、fixture、oracle、rating、runtime、permission、executor条件は基準resultから変更していない。parallel runnerは45件を373.076秒で終え、外部失敗と再試行は0件だった。

## 結果

| case | Score 4 | Score 1 | reviewer | artifact変更 | terminal |
|---|---:|---:|---:|---:|---|
| ADR01 | 3 | 2 | 2 / 5 | 5 / 5 | `completion_ready` 5 |
| ADR02 | 2 | 3 | 3 / 5 | 4 / 5 | `completion_ready` 4、`unavailable` 1 |
| ADR03 | 4 | 1 | 4 / 5 | 0 / 5 | `blocked` 4、`unavailable` 1 |
| ADR04 | 2 | 3 | 4 / 5 | 0 / 5 | `blocked` 2、`unavailable` 3 |
| ADR05 | 5 | 0 | 5 / 5 | 0 / 5 | `blocked` 5 |
| ADR06 | 1 | 4 | 5 / 5 | 0 / 5 | `blocked` 1、`unavailable` 4 |
| ADR07 | 1 | 4 | 5 / 5 | 1 / 5 | `completion_ready` 1、`blocked` 1、`unavailable` 3 |
| ADR08 | 5 | 0 | 0 / 5 | 0 / 5 | `unavailable` 5 |
| ADR09 | 4 | 1 | 4 / 5 | 0 / 5 | `unavailable` 5 |

中央値はquality `66.66666666666666`、all-agent token `1,847,950`、elapsed `1265.1842849580007`秒だった。Target gate不通過のため、この値を採用比較へ使わない。

## 機序

### ADR09の危険な変更は止まった

Candidate185ではjudgement-relevantなmissingがあるのに`no_counterexample_found`を受け入れて変更した実行が3 / 5件あった。Candidate186はADR09を5 / 5件とも`unavailable`で止め、artifact変更は0件だった。この停止効果は成立した。ただし1件はmissingをpacket未完成としてreviewを起動しておらず、正しい機序での成功は4 / 5件に留まる。

### decision recordの全域要求が過剰停止へ転じた

ADR04の2件とADR06の4件は、具体的反例に必要なsupportが既に揃っていたにもかかわらず、無関係な`paired-scope-evidence.json`のmissingを`outcome_sensitive`としたため`counterexample_found`を形成できなかった。全入力へrecordを持たせることと、各入力を正しいdependencyへ結ぶことは別であり、Candidate186は前者を後者の代用にした。

ADR07ではreadableなpaired-scope証拠を含む全入力を`outcome_sensitive`へ寄せた`unavailable`が3件、証拠の閉包効果を無視した誤`counterexample_found`が1件だった。全域recordは存在しても、分類predicateと実際のsupport関係が安定していない。

### packet形成と有限固定効果も退行した

ADR03、ADR04、ADR09で合計3件、missingをterminal input stateとしてpacketへ含めず、review起動前に停止した。Candidate185で閉じたpacket形成経路を維持できていない。

ADR01とADR02では、authorityが有限な変更効果を固定しているのに10件中5件で不要reviewを起動した。うちADR02の1件は、review後のdecision recordをpermission basisとempty scope sourceの表現不一致で棄却し、`unavailable`となった。record totalityはfinite effect correspondenceの不安定さも解消していない。

一方、ADR05は5 / 5件で具体的反例を保持し、`blocked`となった。この局所成功を他ケースの成立へ一般化しない。

## rating recovery

最初のratingでは、末尾に置かれた`completion_ready`と不要reviewの契約違反を評価predicateへ含めていなかった。集計監査で誤りを検出したため、実行証拠とrun identityを変更せず、独立したrating recovery cycleで再評価した。新規スロットは発行していない。初回および中間rating registryは削除せず、非正本の診断証拠としてraw root内に保持した。正本は`recovery/rating-correction-r2`と登録result `614a74e5a4f94fe18e73f5d43ac630fb`である。

## 判定

Candidate186はADR09のunsafe admissionを止めたが、入力分類、counterexample support、packet形成、finite effect correspondenceを大きく退行させた。`quality_failed / mechanism_failed / stopped`とし、Standard14、採用、releaseまたはprojectionへ進めない。

次案を作る場合は、Candidate186を新しい直接基盤にせずC147を直接基盤とする。Candidate186から継承してよいのは「missingを含む全input identityを記録する」という問題意識だけである。次の設計では、terminalごとに必要なdependencyの最小集合を先に固定し、その集合外の入力がterminalを変えないことを個別の根拠で示せた場合だけ`irrelevant`にする必要がある。

## 一次証拠

- [登録result](614a74e5a4f94fe18e73f5d43ac630fb.json)
- [機序監査](candidate186-review-decision-record-totality-adr9-r2-n5-audit-r1.json)
- raw root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate186-review-decision-record-totality-adr9-r2-n5-20260812-r1`
