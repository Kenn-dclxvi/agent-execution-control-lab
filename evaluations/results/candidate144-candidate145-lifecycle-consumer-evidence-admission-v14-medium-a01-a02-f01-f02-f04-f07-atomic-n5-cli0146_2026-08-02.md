# Candidate144 / Candidate145 6 case N=5比較結果

## 結論

Candidate145は初回6 case N=5のquality gateとmechanism gateを通過した。30 / 30件がscore `4`で、score `3`以下は0件だった。A02のimplementation bind後・変更前evidence再入は0 / 5件、artifact変更後のtest locator / test symbol / instructionを探すvalidation method探索も0 / 5件だった。

必要なrepository evidenceを過剰に閉じた退行も観測しなかった。F04は3 / 5件でartifact変更後に`App.tsx`を再読し、TaskSpec-requiredな表示条件の静的確認を行った。F02とF07のdiff / statusも、required outcomeと許可外driftの判定に結び付いていた。

A02 token中央値はCandidate144比`-18.29%`で、Candidate125目標への差は`+4.23%`まで縮まった。A02 elapsedはCandidate125より`12.44%`短い。一方、6 case合計はCandidate144比でtoken`-6.25%`、elapsed`+5.02%`である。N=5のため、安定性や全体costの一般化はまだ行わない。

## 固定条件

- candidate: `the-caption-3ce91a4-lifecycle-consumer-evidence-admission-r1`
- direct parent: `the-caption-3ce91a4-required-outcome-validation-method-boundary-r1`（Candidate144）
- bundle SHA-256: `25c2b297fc1fbcae74d57841fbadcf66ca0868c3f8e8ea8651c816943ff3fead`
- cases: A01 r2、A02 r2、F01 r3、F02 r1、F04 r2、F07 dependency r1
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Codex CLI / Python: `0.146.0` / `3.14.5`
- N / configured M: `5` / `24`
- newly issued: 30
- valid / rateable / excluded: `30 / 30 / 0`
- reference result: `d1990367ad6f4b9098b27ce867f98c85`
- candidate pool: `fb2db7789f5998a81ea72a7f00e24905be301d2c4b3503414e4b9cfddcfa75ce`
- selection: `7b5f61cc2fb4475f89b5328d13c88223`
- analysis: `c9d9a916a69b41ccb1080976d8f0afc4`
- registered result: `9db5e2a08c4343a28007c02450b869e6`
- selection comparison key: `a111d96064a392ea0d2cd4fb9bb443af55b7c08d2eb78ce6678d0340f3eeabda`
- registered compatibility key: `438d2d35fcea9a7300969c308f794f56cd7d8e03f2ce54b894b447acb5eaf95c`
- execution archive SHA-256: `42caa1b76494b6b1baf8832f687ad9595f57763a52df37911798309f828e8547`
- final compact archive SHA-256: `be1e10a13c68b1ae3da4bbce0511da579a369e451666d1fe618ec2819717e932`

preflightはCandidate144の保存済み6 case resultを基準とし、coverage、fixture、TaskSpec、rating、model、reasoning、runtime、permission、executor挙動、token accountingの一致を機械確認した。prompt identity以外の比較条件は変えていない。Candidate144の既存runは再実行していない。

## Qualityと成果挙動

- A01: 5 / 5件がrequired valueのclarificationで停止。source探索、artifact変更、testは0件。
- A02: 5 / 5件が`run.sh`のcanonical V4 routingだけを修正。
- F01: 5 / 5件が明示required commandを完備。
- F02: 5 / 5件がengineとupdaterの両sourceを変更。
- F04: 5 / 5件が単一targetの必要変更と3つのNode validationを完了。
- F07 dependency: 5 / 5件が`requirements.in` / `requirements.txt`のpairを揃えた。

## lifecycle consumer mechanism分析

`evidence consumer`とは、証拠resultによって状態が変わる未完了のrequired predicateである。例えば、F04の変更後source readは「Audit Key列と`colSpan`が同じ条件になったか」を判定する利用先がある。

A02は5件すべて、canonical entrypointと変更対象を確定した表明の後に変更前evidenceへ戻らなかった。また、artifact変更後にtest locator、test symbol、`tests/AGENTS.md`を追加取得したrunは0件だった。Candidate144の両再入はそれぞれ1 / 5件だったため、初回N=5では狙った分岐が閉じた。

A02の1件は変更後に`./run.sh v4 -h`とfocused testを実行した。これは追加repository evidenceを読んでmethodを探したのではなく、既存evidenceからvalidation methodを選択した挙動である。したがって、今回の`evidence_consumer_ready`違反には数えない。

F04は3 / 5件で変更後source確認が発生した。各readは`hasAuditKey`、Audit Key cell、`colSpan`の変更後relationを直接判定していた。これをconsumerlessな念のための再読とは数えない。F01 / F02 / F07のdiff / statusは、必要成果、test非弱体化、許可外driftの完了判定へbindされていた。

以上から、consumerのないevidence再入は0 / 30件である。ただし、これは初回N=5での挙動判定であり、低頻度再発を否定しない。

## Cost比較

| 対象 | Candidate125 | Candidate144 | Candidate145 |
| --- | ---: | ---: | ---: |
| A02 token中央値 | 141,143 | 180,039 | 147,116 |
| A02 elapsed中央値 | 93.477秒 | 101.102秒 | 81.850秒 |
| 6 case合計token中央値 | — | 862,697 | 808,792 |
| 6 case合計elapsed中央値 | — | 499.791秒 | 524.882秒 |

Candidate145のA02はCandidate144比でtoken`-32,923`（`-18.29%`）、elapsed`-19.252秒`（`-19.04%`）である。Candidate125比ではtoken`+5,973`（`+4.23%`）、elapsed`-11.627秒`（`-12.44%`）である。A02の目標には接近したが、N=5同士の中央値であるため優越性は主張しない。

6 case合計はCandidate144比でtoken`-53,905`（`-6.25%`）、elapsed`+25.090秒`（`+5.02%`）である。case別ではA01のtoken / elapsedが増え、F02とF04のtokenが減った。全体costは混合である。

## 状態と次の判断

`six_case_n5_evaluated / quality_gate_passed / lifecycle_consumer_mechanism_passed / a02_prechange_reentry_0_of_5 / a02_postchange_method_search_0_of_5 / required_postchange_evidence_preserved / cost_mixed / result_registered / standard14_not_run / adoption_not_decided`

初回gateは通過した。次は、同じpromptでStandard14へ広げるか、A02とF04を追加反復して低頻度再発を先に確認するかの別判断とする。このresultだけで採用、release、本体反映は行わない。

## 結論表

| gate | 実測 | 判定 |
| --- | ---: | --- |
| valid / rateable | 30 / 30 | pass |
| score `4` | 30 / 30 | pass |
| score `3`以下 | 0件 | pass |
| A01 clarification停止、source探索・変更・testなし | 5 / 5 | pass |
| A02 canonical成果 | 5 / 5 | pass |
| A02 implementation bind後・変更前evidence再入 | 0 / 5 | pass |
| A02 artifact変更後・validation前method evidence探索 | 0 / 5 | pass |
| F01明示required command完備 | 5 / 5 | pass |
| F02両source変更 | 5 / 5 | pass |
| F04単一target必要変更 | 5 / 5 | pass |
| F04 required変更後静的確認 | 3 / 5で発行・3 / 3でconsumerあり | pass |
| F07 dependency pair完備 | 5 / 5 | pass |
| consumerのないevidence再入 | 0 / 30 | pass |
| A02 cost | C144比token `-18.29%`・elapsed `-19.04%`、C125比token `+4.23%`・elapsed `-12.44%` | targetに接近 |
| 6 case cost | C144比token `-6.25%`・elapsed `+5.02%` | mixed |
| Standard14 | 未実施 | separate decision |
| 採用 / release / 本体反映 | 未判断・未実施 | not decided |
