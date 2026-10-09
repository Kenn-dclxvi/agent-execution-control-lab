# Candidate302 C301の書式でC298とC299の二項目を加える

2026-10-09。利用者の依頼（新しい基準で29x系を一度計測する。C300以降のCandidateはC301の書式を親にする）を受けて、Candidate本文の作成前に固定する設計記録。[設計原則](prompt-control-design-principles.md)の全文を読み、「Candidateを作成する前の確認事項」の項目1〜9に対応させた。計測と記録は[計測と記録の基準r2](shared-instruction-evaluation-criteria-r2.md)に従う。二項目それぞれの設計の根拠は[C298の設計](candidate298-post-validation-success-command-closure-design.md)と[C299の設計](candidate299-no-short-wait-time-design.md)、二項目を同時に加える点は[C300の設計](candidate300-c298-c299-combined-design.md)にあり、この記録はそれらを繰り返さず、新しい系列で変わる点だけを記す。この記録ではbundleを作成しない。

## 目的と役割

- 系列：実行環境を切り離した系列（`shell_environment.revision: fixed-path-workspace-venv-r1`）。比較の基準かつ直接の親はC301（`the-caption-3ce91a4-outcome-binding-uniform-markdown-r1`）の[一つの待ち行列での計測](../evaluations/results/c301-onequeue-sol61-low-sonnet55-low-standard14-n5_2026-10-09.md)。C300は加える文の出所であり、親ではない。
- 29x系の中からC300の二項目を選んだ理由：旧系列で費用を数え直したとき、両セルともC280より費用が下がったのはC300だけだった（Sol Low −5.7%、Sonnet low −2.1%、[試算](../evaluations/results/kpi-cost-weighting-trial_2026-10-09.json)）。C292〜C296は、Claudeの課題文の指定（必須の確認は個別の呼び出しで実行する）と食い違う検証の一括化を含むため、[判定基準r1](shared-instruction-evaluation-criteria-r1.md)の試験の条件に従って対象から外す。C297は指示文の誤りで外す。C298とC299を単独で測るかは、C302の記録を見て利用者が決める。
- 評価は計測であり、達成目標を置かない（r2）。
- 変更対象：root `AGENTS.md`の末尾に、C298の一項目とC299の一項目を、この順で、C301の書式（`- `の箇条書き）で加える。文の文字はC300と同じにする。C301の本文と他の18対象はC301とバイト一致を保つ。

## 1. 比較の基準と、正常な最短経路

基準はC301（一つの待ち行列での計測）。正常な最短経路はC298とC299の設計記録と同じである。

## 2. 保存traceで確認した問題経路（新しい系列）

基準のC301の保存traceで、二項目が閉じる操作がまだ起きていることを確かめた。

| 項目 | 閉じる操作 | C301での観測（1反復あたり） |
| --- | --- | --- |
| C298 | 必須の確認（full gate）がすべて成功した後のコマンドの発行 | Sol Low 10〜11回、Sonnet low 3〜4回。ただしF06とF07の後続には、TaskSpecが別に求める確認（`git diff --check`など）が含まれるため、この数は閉じる対象の上限である |
| C299 | ツールの既定値（実行10秒、終了待ち5秒）より短い待機時間の指定 | Sol Low 13〜18回（値はすべて1000ミリ秒）。待機だけの呼び出しは4〜8回 |

数え方：C298はcommand evidenceの試行順で、最後に成功したfull gateより後のコマンドを数えた。C299はCodexのコード実行の本文から`exec_command`と`write_stdin`の`yield_time_ms`を数えた。旧系列の観測（C298の設計とC299の設計）と同じ種類の操作が、新しい系列でも残っている。

## 3. 開いている記述と、TaskSpec・正本で防げない理由

C298とC299の設計記録の項目3のとおり。新しい系列での変更はない。

## 4. 追加する条件の全件

C301の末尾に、次の二項目をこの順で加える。

> - 必須の確認コマンドがすべて成功した結果を受け取った後は、コマンドを発行せずに報告する。
> - コマンドの実行とその終了待ちで、ツールの既定値より短い待機時間を指定しない。

どちらも既存の操作の発行またはパラメータを禁止・限定する文であり、新しい操作の発行を求めない。文の文字はC300と同じで、箇条書きの記号だけをC301の書式に合わせる。

## 5. 禁止行動、開放経路、閉じる境界、反証

各項目の対応はC298とC299の設計記録の項目5、二項目の重なりはC300の設計記録の項目5のとおり。

## 6. 維持する正常経路

C298とC299の設計記録の項目6のとおり。TaskSpecが求める確認（F06とF07の`git diff --check`など）は、C298の一項目が禁止する「必須の確認がすべて成功した後」に当たるかをモデルが判断する余地がある。C298の旧系列の記録では、この確認は残っていた。新しい系列でも、処理の適切さの分類でこの確認が抜けていないかを記録する。

## 7. 新しく増える判断と、変更対象外への影響

- 新しい判断：統合による新しい判断はない。
- 固定分：249バイト。
- 変更対象外：A01、A02、F05の二件、F10の二件はコマンドの確認がないか少ないため、固定分以外の差は見込まない。

## 8. 評価ケース、比較単位、比較条件、記録する項目

- セル：Sol LowとSonnet low、各Standard14の全14ケースN=5の計70件。
- 比較条件：C301の`-20261009-r3`プロファイルと同じで、prompt identityだけを変える。両セルの全スロットを一つの待ち行列（合計24本）で発行する。準備・実行・登録は`campaign-tools/single-prompt-r1/campaign.py`（`prepare`、`run-all`、`finalize`、`compare`）で行う。
- 記録する項目（r2）：品質、処理の適切さ（TaskSpecが明示する確認を最後の変更より後に成功させてから報告したか）、費用（基準の幅と比べた位置）、経過時間、生のトークン（参考）、使用量の内訳、機序の診断（上の項目2と同じ数え方で、二つの操作の回数）。記録は品質、処理の適切さ、費用の順に読む。

## 9. 停止条件

- 発行前の確認が通らなければ、一件も発行しない。
- invalid、採点不能は記録の対象にしない。外部失敗だけ、同じ枠で固定上限内に再試行する。有効な4点未満は削除、相殺、再実行しない。
- 各セル70件で記録し、自動で追加反復しない。結果に合わせてこの記録と案文を書き換えない。

## 判断の限界

- 項目2の観測は、C301のN=5の一系列による。
- この記録は採用、release、本体反映を決めない。

## 参照

[設計原則](prompt-control-design-principles.md)、[計測と記録の基準r2](shared-instruction-evaluation-criteria-r2.md)、[C298の設計](candidate298-post-validation-success-command-closure-design.md)、[C299の設計](candidate299-no-short-wait-time-design.md)、[C300の設計](candidate300-c298-c299-combined-design.md)、[C301の設計](candidate301-c280-uniform-markdown-design.md)、[C301の一つの待ち行列での計測](../evaluations/results/c301-onequeue-sol61-low-sonnet55-low-standard14-n5_2026-10-09.md)。
