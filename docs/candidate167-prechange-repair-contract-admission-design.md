# Candidate167 変更前修正契約 admission設計

> **位置づけ**: 破棄済み旧設計系列の履歴Candidate／現行設計へ継承しない

## 結論

Candidate167はCandidate166を直接の親とし、修正操作に限って、最初の成果物変更より前に修正契約を一度確定する。追加する変更軸は`REPAIR_CONTRACT_ADMISSION`だけとし、ケース名、対象文書、語句、期待terminal、評価用oracleをpromptへ入れない。

Candidate166問題資格確認では、修正不要ケースの不要変更、根拠不足ケースでの推測変更、先行評価と同方向の不要変更を一次traceで観測した。事前に固定した「clean 5 / 5かつperturbedだけが誤る」というCandidate作成条件は満たさなかったが、利用者が2026-08-09に、固定試験を変更せず、試験固有ではない設計方針に従って評価結果へ対応することを明示した。この指示によりCandidate作成停止だけを解除し、評価条件と合格条件は変更しない。

## Candidate作成前の固定事項

1. 基準prompt setはCandidate166 `the-caption-3ce91a4-prior-evaluation-review-admission-r1`とする。
2. 最短正常経路は、機械判定だけで必要な修正と修正後条件が決まる場合に人的判定を起動せず変更・検証へ進む経路と、許可根拠から修正不要を直接確定して無変更で完了する経路である。
3. 保存済み誤経路は、Candidate166問題資格確認のRC02 iteration 1、RC03 iteration 1〜4、RC06 / RC07全件で観測した不要変更または根拠不足時の推測変更である。
4. Candidate166の`REVIEW_ADMISSION`は品質レビューの担当を決めるが、修正の要否と修正後条件を最初の変更前に一つの結果へ結び付けない。C147の`implementation_bound`は実装方法を結び付けるため、修正自体が必要かという先行判断を閉じない。
5. 追加する一つのpredicateは`REPAIR_CONTRACT_ADMISSION`である。TaskSpecが欠陥または意味不整合の有無を確定し、存在する場合だけ是正することを求める修正操作へ適用する。
6. このpredicateは、先行評価を修正判断へ採用する判断点、修正要否未確定のまま実装方法へ進む判断点、根拠不足時にもっともらしい修正を推測する判断点を消す。
7. 新たに増える判断は、機械判定だけで閉じるか、修正契約の担当をrootと独立reviewerのどちらへ固定するか、結果を`no_repair_required / ready / unavailable`のどれへ結び付けるかである。判定はTaskSpec、machine result、同じ判定条件の先行評価受領、allowed readの直接根拠だけを入力にする。
8. 品質維持は、実装前に固定済みの七ケースを各`N=5`で確認する。ケース、oracle、TaskSpec、allowed read、iteration、rating contract、model、reasoning、CLI、`M=24`を変更しない。
9. 合格条件は35 / 35 valid、35 / 35 Score `4`と、評価設計に固定した全mechanism条件である。一件でも不成立ならStandard14へ進めず停止する。

## 一つの変更軸

`REPAIR_CONTRACT_ADMISSION`は、修正操作を次の三経路へ閉じる。

- 必須の機械判定だけで修正必要性と全修正後条件が決まる場合は、人的な修正契約を作らず既存の実装・検証へ進む。
- 非機械的な判定が必要で、allowed readから現在内容が条件を満たすと確定した場合は、変更せず必要な無変更確認だけで完了する。
- 非機械的な判定が必要で、allowed readから欠陥と修正後条件を確定できる場合だけ、その条件を`implementation_bound`へ渡して変更する。どちらも確定できない場合は、変更と検証を開始せず`unavailable`で停止する。

同じ判定条件の先行評価をrootが受領済みなら、修正契約の担当を情報封鎖した独立reviewerへ固定する。そうでなければrootへ固定する。独立reviewerは先行評価、処置判断、期待terminal、期待修正後内容を受け取らず、修正もしない。rootは独立reviewerの結果を比較、統合、再採点、補完しない。

## 非目標

- 評価ケース固有の語句、path、case IDによる分岐。
- 変更後レビューの常時起動。
- reviewerによる実装。
- 自動再修正ループ。
- Standard14、採用、release、projectionの同時判断。

## 評価順序

1. Candidate167 bundleと固定済みprofileのprompt identityだけを作成する。
2. Candidate166で使用した同じfrozen Layer 1を複製し、prompt identity以外の互換条件をpreflightで照合する。
3. Candidate167だけを七ケース各`N=5`で実行・採点する。
4. qualityとmechanismが全件通過した場合だけStandard14の保存確認へ進む。

## 状態

`design_complete / user_authorized_response_to_fixed_evaluation / one_axis_repair_contract_admission / fixed_cases_unchanged / candidate_materialized / targeted_35_of_35_valid / score4_21 / score1_14 / quality_gate_failed / standard14_not_started`
