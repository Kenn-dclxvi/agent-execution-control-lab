# Candidate305 C301の書式でC299の一項目だけを加える

2026-10-09。ベースをC302に決め、その弱点を潰す作業の一つとして、Candidate本文の作成前に固定する設計記録。[設計原則](prompt-control-design-principles.md)の全文を読み、「Candidateを作成する前の確認事項」の項目1〜9に対応させた。計測と記録は[計測と記録の基準r2](shared-instruction-evaluation-criteria-r2.md)に従う。一項目の設計の根拠は[C299の設計](candidate299-no-short-wait-time-design.md)にあり、この記録は繰り返さない。この記録ではbundleを作成しない。

## 目的と役割

- 系列：実行環境を切り離し、負荷を見て次のrunを始める発行の条件（CPU使用率70%以下、間隔1秒）で測る系列。比較の基準かつ直接の親はC301で、同じ条件で測ったSonnet lowの[`-r5`](../evaluations/results/c301-sonnet55-low-load-admission-trials_2026-10-09.md)と比べる。
- 測る理由：ベースのC302（C301＋C298＋C299）では、Sonnet lowが確認コマンドの出力をそのまま返し、退避された大きな出力を読み直す形が、2回の計測とも20件中13〜14件あった。C301は4〜5件、C298だけを加えたC303は7件だった。C299の一項目がこの形に関わるかを、C299だけを加えて確かめる。
- 利用者の指示により、Sonnet lowで確立するまでSolは測らない。
- 評価は計測であり、達成目標を置かない（r2）。
- 変更対象：root `AGENTS.md`の末尾に、C299の一項目をC301の書式（`- `の箇条書き）で加える。文の文字はC299・C302と同じ。C301の本文と他の18対象はC301とバイト一致を保つ。

## 1〜7

- 1（基準と最短経路）、3（開いている記述）、4（追加する条件）、5（境界と反証）、6（維持する正常経路）、7（新しい判断と影響）は、C299の設計記録の各項目のとおり。
- 2（問題経路）：C299が閉じる短い待機時間の指定は、Codexの経路であり、Sonnet lowでは起きていない。この計測は、閉じる経路の確認ではなく、Sonnet lowへの影響（出力の扱いの変化）の切り分けを目的とする。
- 追加する一項目：

> - コマンドの実行とその終了待ちで、ツールの既定値より短い待機時間を指定しない。

## 8. 評価ケース、比較単位、比較条件、記録する項目

- セル：Sonnet lowのStandard14の全14ケースN=5の計70件。
- 比較条件：C301のSonnet low `-r5`と同じで、prompt identityだけを変える。
- 記録する項目（r2）：品質、処理の適切さ、費用、経過時間（モデルの応答時間とコマンドの実行時間の内訳を含む）、生のトークン（参考）。
- 機序の診断（合否にしない）：`main_verify.sh`を出力そのままの形で実行した件数、出力が退避された回数、退避された出力を読んだ回数と文字数、F06とF07の`git diff --check`の成功件数。数え方は[C302の診断](../evaluations/results/c302-sol61-low-sonnet55-low-standard14-n5_2026-10-09-mechanism-diagnostics.json)と同じ。

## 9. 停止条件

C302の設計記録の項目9のとおり。

## 判断の限界

- 出力そのままの形は、C302の二回の計測とC303の一回、C301の二回の計測（いずれもN=5）による観測である。
- この記録は採用、release、本体反映を決めない。

## 参照

[設計原則](prompt-control-design-principles.md)、[C299の設計](candidate299-no-short-wait-time-design.md)、[C302の設計](candidate302-c301-success-closure-and-wait-time-design.md)、[C303の計測](../evaluations/results/c303-sol61-low-sonnet55-low-standard14-n5_2026-10-09.md)、[発行の条件の試行](../evaluations/results/c301-sonnet55-low-load-admission-trials_2026-10-09.md)。
