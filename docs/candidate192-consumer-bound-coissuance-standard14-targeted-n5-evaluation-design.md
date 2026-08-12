# Candidate192 Standard14共同発行対象9ケース・F04対照 N=5評価設計

> **位置づけ**: Candidate192初回targeted gate／10ケース各N=5／評価前固定

## 目的

Candidate191で共同発行退行を実測した9ケースと、変更前step数がC147から増えなかったF04対照だけを使い、Candidate192の`DISPATCH_ADMISSION`が狙った経路を成立させ、真正dependencyを越えて発行しないことを確認する。Standard14全14ケース、ADR9全9ケース、N=20または別TPO系列へ先に広げない。

## 対象

- 共同発行退行9ケース: A01、A02、F01、F02、F03、F07 canonical、F07 dependency、F08、F10 inventory
- 対照: F04
- 各ケースN=5、合計50 slot
- reference: Candidate191の登録済みStandard14 atomic runから同じ10ケース各5件だけを選んだresult `4b3fcabe4a004d9a945f6d1bcbdecfdc`
- Candidate192: 新規50件だけを発行し、基準runを再実行しない

F04は変更前stepがC147とCandidate191で`2 -> 2`だった対照であり、「同時発行すべき」と事前決定したケースではない。各invocationのresult effectから真正dependencyを判定する。

## 品質gate

- 50 / 50 valid
- Score `4 = 50`
- required outcome、許可path、required validationおよびterminalを各ケースの固定oracleどおり成立させる
- 不要review producer、root代行、禁止情報配送または危険なartifact変更を0件とする

## 機序gate

1. A01ではresult consumerのない開始identity commandを0 / 5とする。
2. A01以外の退行8ケースでは、開始identity resultが許可済みreadのtarget、permission、methodまたはstop conditionを変えない場合、identity確認とそのreadを同じmodel stepから発行する。
3. 退行9ケース45件で、operation identity、lifecycle、predicate、consumerまたはresult格納先の分離だけを理由に追加の変更前result roundを作らない。
4. F04を含む全50件で、先行resultが後続invocationのtarget、permission、methodまたはstop conditionを変え得る場合は、そのdependencyを越えて共同発行しない。
5. 共同発行する観測も個別result contractを保持し、compound invocationのaggregate resultで個別stateを補完しない。
6. Candidate191で成立した`OWNER_ROLE`、review適用、current/prior result admissionおよびterminal経路を退行させない。

tokenとelapsedは互換KPIとして記録するが、単独の中央値改善を機序成立の代用にしない。各runのmodel step、command、result consumerおよびdependencyを保存traceで直接監査する。

## 停止条件

qualityまたは機序gateの不一致が一件でもあれば、そのrunを保持して停止する。validな低品質runを再実行で置き換えず、残り4ケース、ADR9拡張、採用、releaseおよびprojectionへ進まない。

## 状態

`design_fixed / preflight_ready / authorized_50 / issued_50 / quality_passed / mechanism_failed / stopped`

実行結果は[`Candidate192 Standard14対象9ケース・F04対照 N=5`](../evaluations/results/candidate192-consumer-bound-coissuance-standard14-targeted-n5_2026-08-12.md)を正本とする。50 / 50 validかつScore 4だったが、A01のconsumerなし開始identityが2 / 5、退行8ケースのidentity/read同一model step発行が1 / 40だった。停止条件に従い、残り4ケースとADR9へは拡張しない。
