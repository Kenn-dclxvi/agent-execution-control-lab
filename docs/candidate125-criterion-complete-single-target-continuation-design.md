# Candidate125 criterion-complete single-target continuation設計

## 結論

Candidate125はCandidate122を直接親とする。停止したCandidate123とCandidate124は継承しない。C122のexact-target content waveとvalidation method境界を維持し、TaskSpec上の全未解決変更criterionを一つのeditable targetだけが所有する場合に限り、criterion-completeな同一target continuationを一度許可する。

`single change target`と`criterion-complete scope`は、C124で観測した二つの失敗を同時に閉じる一つの変更軸である。条件は複数だが、一つのpredicateへ無理に縮約しない。

## Identityと状態

- candidate number: Candidate125
- prompt identity: `the-caption-3ce91a4-criterion-complete-single-target-continuation-r1`
- direct parent: `the-caption-3ce91a4-prechange-evidence-wave-closure-r1`
- changed target: root `AGENTS.md`
- changed axis: criterion-complete single-target continuation
- evaluation status: `a02_n20_evaluated / standard14_evaluated / quality_gate_passed / a02_terminal_closure_passed / candidate107_token_target_passed / adoption_not_decided`
- release: `not_created`
- runtime projection: `not_projected`

## 保存traceから確定した不足

根拠は[`Candidate124 targeted result`](../evaluations/results/candidate122-candidate124-incomplete-content-continuation-v14-medium-a01-a02-f01-f02-f04-atomic-n5-cli0146_2026-07-31.md)とする。

1. F04は5件すべてが同じ`App.tsx`へ一度continuationした。
2. 760行まで取得した3件はscore `4`、620行で止めた2件は必要criterionを観測できずscore `2`だった。
3. したがってcontinuationの回数とtargetが同じでも、そのscopeがcriterionを覆わなければfalse stopは残る。
4. F02ではC124のcontinuation例外が複数target共同predicateにも開き、追加readが2 / 5件へ再発した。
5. F02 content waveはC122の5 / 5からC124の3 / 5へ後退し、token中央値も`124,719`から`188,908`へ増えた。

## 置換する制御

`single_change_target_ready := TaskSpecがeditable targetを一つだけ列挙し、その一targetが全未解決変更criterionを所有し、他のadmission済みtargetはvalidation capabilityまたは保持constraintだけを決める`

`continuation_scope_complete := 未観測criterionへ直接bindした同一targetのsymbol contextを全て覆う ∨ 同一targetの全未取得contentを終端まで覆う`

`single_target_continuation_ready := prechange_evidence_wave_ready ∧ single_change_target_ready ∧ 初回resultでeditable targetの存在とread可能性を確認済み ∧ 変更criterionが未観測 ∧ continuation_scope_completeなrequest identityを発行前にbind済み ∧ continuation未発行`

`single_target_continuation_ready=true`の場合だけ、その同一editable targetへcontinuation evidenceを一件許可する。根拠のない次のbounded chunk、別target、repository-wide search、一般的安全確認、implementation method探索、二回目のcontinuationを開かない。

複数editable targetが共同で変更predicateを決める場合は、このcontinuation routeを開かない。C122のexact-target initial content waveを維持し、その一waveでedit-readyまたは具体的terminal dispositionを判断する。

continuation後はartifact変更へ進むか、実際に観測した`missing / unreadable / contradiction / unsatisfied constraint`で停止する。単なる取得範囲不足をterminal absenceへ読み替えない。

## 初回targeted gate

初回評価はA01 r2 / A02 r2 / F01 r3 / F02 r1 / F04 r2各`N=5`、Rating v14、`gpt-5.6-sol` Medium、CLI `0.146.0`、profile上の`M=24`へ固定する。

- execution: `25 / 25 valid`
- quality: score `4` × 25
- F04: false stop 0 / 5
- F04: 初回範囲不足時はcriterion-completeな同一`App.tsx` continuationがちょうど1回
- F04: artifact変更と3 required Node validation完備5 / 5
- F02: exact target set content wave 5 / 5
- F02: initial content後の追加read 0 / 5
- F02: token中央値`173,000`以下
- A01: required value待ち5 / 5、artifact変更・test 0 / 5
- A02: canonical成果5 / 5、変更後validation method探索0 / 5
- F01: required command evidence完備5 / 5

一件でもqualityまたはmechanism gateを崩した場合は停止する。全gate通過時だけ、登録済みatomic runを再利用してStandard14不足caseへ進むかを別判断する。

## 停止条件

- F04で取得範囲不足をterminal absenceとする
- F04 continuationが未観測criterionを覆わないbounded chunkになる
- F02でinitial content後の追加readを開く
- F02 token目標を超える
- 25件中一件でもscore `4`未満

## 非目標

- file size、line数、bytes、read回数の一般上限
- case名、path、tool、shell commandのprompt固定
- unknown targetまたはsymbolの推測
- Candidate123 / Candidate124の継承
- executor、Codex CLI、tool adapter、runtime hook、外部wrapperの変更
- 採用、release、runtime projection、THE-CAPTION本体反映

## 評価結果

初回[`A01 / A02 / F01 / F02 / F04各N=5`](../evaluations/results/candidate122-candidate125-criterion-complete-single-target-continuation-v14-medium-a01-a02-f01-f02-f04-atomic-n5-cli0146_2026-07-31.md)は25 / 25 score `4`だった。F04 false stop 0 / 5、F02 content wave 5 / 5、F02 token中央値`124,094`で全targeted gateを通過した。

続く[`Standard14各N=5`](../evaluations/results/candidate118-candidate125-criterion-complete-single-target-continuation-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-07-31.md)は登録済み25 runを再利用し、不足45 runだけを実行した。最終70 / 70件はscore `4`、token中央値`1,401,225`でCandidate107目標比`-8.00%`だった。現在状態は`adoption_not_decided`である。

さらにA02を登録済み5 runから`N=20`へ拡張し、不足15 runだけを実行した。20 / 20件がscore `4`で、implementation bind後・最初のartifact変更前command再入は0 / 20件だった。Candidate118のA02 terminal closureを維持した。
