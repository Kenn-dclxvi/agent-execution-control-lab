# Candidate165 Standard14 review route分析

> 後続見直し: 本文で使うHR03のroot `0 / 5`対独立SA `5 / 5`は、HR03 r1の期待terminalが証拠から一意に決まらないため、精度改善の根拠としては失効した。C165 Standard14の独立SA実質修正0 / 41、通常caseへの系統起動40件、F10 root review 5 / 5というtrace事実と、review admission過大という結論は維持する。詳細は[Candidate166 Review4 HR03 case妥当性見直し](candidate166-review4-case-validity-analysis.md)を参照する。

## 結論

Candidate165のStandard14 70件は、追加試験を作る前にreview admissionの問題を切り分ける保存traceとして使える。

- 70 / 70件はScore `4`で、成果品質の退行は観測しなかった。
- 独立SAを起動した41件のうち、40件はrootが既に得た結論の確認だった。
- 残る1件の不合格は成果欠陥ではなく、rootがreview後に実施すると固定していた終了時status確認を、reviewerが未提示として扱ったものだった。
- 独立SAが実質的な欠陥を新しく発見し、成果修正へ結び付けたrunは0 / 41件だった。
- Standard14のTaskSpecには、FR-01で独立SAを必要とした「同じreview criterionについてrootへ渡された誤った先行評価」がない。それでもC165は、rootがartifactを実装または調査したことを理由に、8 case 40件で系統的に独立SAを起動した。
- 独立SAを使わなかったF10 monthly 5件では、contextがcleanなroot reviewが実欠陥を正しく検出し、5 / 5件がScore `4`だった。

したがって、C165で成立した狭い機能は「誤った先行評価を受け取ったrootからreview producerを分離し、そのresult authorityを維持すること」である。Standard14で追加された広い挙動は「rootが実装・調査しただけで独立SAへ切り替えること」であり、必要性も成果改善も実証されていない。

現在の判断は`targeted_information_closure_effect_verified / standard14_false_positive_review_admission_observed / substantive_review_correction_0_of_41 / adoption_stopped_pending_narrower_admission`とする。一次resultのscore、KPI、diagnostic statusは変更しない。

## 分析対象と境界

- 一次result: [Candidate165 Standard14 N=5](../evaluations/results/candidate165-review-result-admission-v14-medium-standard14-atomic-n5-cli0146_2026-08-04.md)
- 比較対象: 同じcompatibility keyのCandidate147 Standard14 N=5
- 対象run: 14 case × 5 iteration = 70件
- 使用した情報: 登録済みanalysis、rating view、root / descendant trace
- 非目標: 保存済みrunの再採点、KPI追加、41件の起動数だけをreview価値とみなすこと

この分析は保存traceの後続解釈であり、新しいevaluation slotを発行していない。

## 41 / 14 / 15件の読み方

Rating v14のowner evidence statusは、reviewの正否ではなく、独立criterion ownerのadmissible resultを確認できたかというdiagnosticである。

| 保存status | 件数 | 人間向けの意味 |
| --- | ---: | --- |
| `available` | 41 | 独立SA resultを一件確認した |
| `failed` | 14 | 独立SA resultがなかった |
| `not_applicable` | 15 | 独立owner resultを要求しないcaseだった |

`failed` 14件の内訳は、clarification停止5件、out-of-scope判断4件、root review 5件である。全件Score `4`なので、14件をreview失敗または成果失敗として扱わない。

case別のrouteは次の通りだった。

| case | 独立SA | 独立SAなし | 対象外 |
| --- | ---: | ---: | ---: |
| A01 / A02 / F01 | 0 | 0 | 15 |
| F02 / F03 / F04 / F06 / F07 canonical / F07 provenance / F08 / F10 entrypoint | 40 | 0 | 0 |
| F05 out-of-scope | 1 | 4 | 0 |
| F05 clarification / F10 monthly | 0 | 10 | 0 |

F05 out-of-scopeは同じcaseで4件がroot境界確認、1件だけが独立SAとなり、成果はすべて同じだった。これはreview admission境界の低頻度な揺れであり、独立SAによる改善ではない。

## なぜ通常caseで独立SAが起動したか

C165の`review_context_clean`は、rootがreview対象artifactのproducerでないことと、rootが先行finding等を受領していないことの両方を要求する。そのため、rootが実装producerまたは調査producerになった時点でcontextをuncleanと判定できる。

保存traceでもF02、F03、F10 entrypointなどは、作業開始時点から「rootが実装または調査を担当し、変更後のnon-machine riskだけを独立reviewerへ渡す」と計画していた。Standard14の14 TaskSpecには`prior_implementation_record`がなく、FR-01のHR03で観測した誤った先行評価もない。

したがって、40件の系統的な起動は情報封鎖が必要なcontextを検出した結果ではない。次の二つを同じ`review_context_clean=false`へまとめた結果である。

1. rootが同じcriterionについて誤ったfinding、disposition、completion評価を先に受け取った。
2. rootが単にartifactを実装または調査した。

FR-01で成果差を確認したのは1だけであり、Standard14で広く発火したのは2である。

## 41件のreview resultが成果を変えたか

descendantのterminal resultを確認すると、40 / 41件はpassまたはroot方針の確認だった。新しいblocking defectを示し、artifactまたは利用者向け結論の修正へ結び付いたrunはなかった。

唯一のFAILはF10 entrypoint iteration 5だった。reviewerは終了時`git status --short`の証拠が未提示であることを理由にしたが、root traceではその確認をreviewer受領後に行う実行票として先に固定していた。rootは予定どおりstatusを確認し、最終成果はScore `4`になった。

これはreviewによる欠陥発見ではなく、terminal evidenceが揃う前にreviewを発行したscheduling不整合である。C165の広いreview routeは、重複確認だけでなく、後続予定の証拠を早期にmissing扱いする経路も追加した。

## root reviewで閉じた直接証拠

F10 monthly 5件では、rootはartifact producerでも先行評価の受領者でもなかったため、`review_context_clean=true`として自らreview producerになった。5件すべてで引数`--format-test`と`--force`の取り違えを正しく特定し、Score `4`だった。

この結果から、少なくともC165 Standard14内のclean-context reviewについては、独立SAを使わないroot reviewの成果不足は観測されていない。

一方、HR03ではrootが誤ったproducer評価を受け取った状態で0 / 5、情報封鎖した独立reviewerが5 / 5だった。この二つは矛盾しない。必要な境界は「rootがartifactを知っているか」ではなく、「rootが同じcriterionの先行評価を受け取り、その評価が判断を歪め得るか」である。

## case別costとの対応

互換なCandidate147と各case N=5中央値を記述比較すると、系統的に独立SAを起動した8 caseはすべてtokenが大きく増えた。

| case | SA起動 | C147 token | C165 token | token差 | elapsed差 |
| --- | ---: | ---: | ---: | ---: | ---: |
| F02 | 5 / 5 | 128,236 | 276,193 | `+115.4%` | `+17.4%` |
| F03 | 5 / 5 | 104,320 | 212,349 | `+103.6%` | `+39.7%` |
| F04 | 5 / 5 | 151,170 | 296,449 | `+96.1%` | `+19.4%` |
| F06 | 5 / 5 | 151,542 | 235,838 | `+55.6%` | `+39.3%` |
| F07 canonical | 5 / 5 | 102,504 | 231,626 | `+126.0%` | `+30.4%` |
| F07 provenance | 5 / 5 | 87,284 | 163,402 | `+87.2%` | `+55.5%` |
| F08 | 5 / 5 | 113,067 | 214,439 | `+89.7%` | `+96.3%` |
| F10 entrypoint | 5 / 5 | 87,934 | 198,359 | `+125.6%` | `+99.1%` |

独立SAなしのF05 clarification、F05 out-of-scope、F10 monthlyのtoken差はそれぞれ`+2.0%`、`+2.1%`、`+2.4%`だった。case中央値の差を合計した記述値では、全token増加の約83.5%が上記8 caseに分布する。

ただしA02は独立SAなしでもtoken`+135.2%`だった。したがって、集約token`+75.79%`とelapsed`+34.99%`の全量をreview起動へ因果bindしない。A02はreview admissionと分離したprompt interactionとして残す。

## command protocol diagnostic

C165では52件の`command_protocol_violations`が19 / 70 runに分布した。

- 独立SAあり: 36件、14 / 41 run
- 独立SAなし: 0件、0 / 14 run
- review対象外: 16件、5 / 15 run。すべてA02

この分布も独立SAだけを原因とは確定できない。一方、独立SA routeではdescendant command、result受領、reviewと終了時evidenceの順序が増え、36件の違反と早期FAIL 1件が同じ経路に現れた。採用時に無視できない運用複雑性である。

## 切り分け結果

| 問い | C165までの答え |
| --- | --- |
| 誤った先行評価をrootへ渡すとreview精度が落ちるか | HR03でroot 0 / 5。落ちた |
| 情報封鎖した独立SAで回復できるか | HR03で5 / 5。回復した |
| clean contextでも常に独立SAが必要か | F10 monthly root review 5 / 5と、Standard14の修正寄与0 / 41から、必要性は確認できない |
| C165は必要な条件だけでSAを呼んだか | いいえ。通常の実装・調査を理由に40件で系統起動した |
| 41件のreviewが品質を改善したか | 実質修正0件。改善は確認できない |
| C165を現在のまま採用できるか | できない。狭い有効条件より発動条件が広い |

## 次のうち手

新しい課題を追加する前に、Candidate165の設計軸を次の一変更へ限定する。

- 維持する: TaskSpec-bound non-machine riskだけをreview対象にする。独立reviewerのresult authorityと情報封鎖を維持する。
- 削る候補: `rootがreview対象artifactのproducerでない`をclean-context条件にする部分。
- 独立SAへ切り替える条件: rootが、同じreview criterionに対するproducerまたはreviewerのfinding、disposition、completion評価を事前に受領した場合。
- root reviewにする条件: reviewは必要だが、上記の先行評価を受領していない場合。rootが実装または調査したという事実だけでは独立SAへ切り替えない。

この一変更を設計した後の最初のgateは、新課題の探索ではなく、既存の固定課題で二つを同時に確認することである。

1. HR03 r1を再利用せず、期待terminalをallowed evidenceから一意に導けるr2で独立SA 5 / 5と事前成果条件5 / 5を確認する。
2. Standard14で系統的に独立SAを起動した既存caseを使い、誤った先行評価がない場合はroot reviewへ戻る。

ただし比較slotを発行する前に、Candidate、対象case、期待route、quality gate、互換Layer 1を別artifactで事前固定する。C165の一次resultをこの解釈へ書き換えず、採用、release、projectionには進めない。
