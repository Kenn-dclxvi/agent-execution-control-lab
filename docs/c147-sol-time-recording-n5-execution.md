# C147 Solの時間記録導入後N=5実行

利用者の「計測して」により、時間記録を追加したC147 Sol medium・Standard14全14ケース各N=5の70件を新規実行する。実行者はroot。旧runには新しい直接時計記録がないため、既存runを新計測済みとして再利用しない。計測機能の導入を変更軸とする別系列であり、prompt効果の比較、採用、release、本体反映は対象外。

基準の保存結果は`1dc4feb4282e42bdac2f19ddb6e80eaf`。prompt、model、reasoning、CLI 0.153.3、fixture、TaskSpec、採点、並列上限24を再利用し、追加した計測コードのhashをexecutor条件へ固定する。Layer 1は基準から複製し、実行前receiptで許容した変更軸以外の差がないことを確認する。未確認・不一致では発行しない。新条件は旧プールへ混ぜない。

全70件の実行有効性、採点、総所要時間と新しい診断記録の保存を確認する。正式な作業時間は入力配送境界未観測のためnullを保持する。欠測を0へ変換しない。実行時の上限と外部失敗方針は元のprofileを維持する。

実行証跡: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate147-sol-time-recording-standard14-n5-cli0153-20260906-r1`。

## 利用者による対象追加

「両方だよ」により、C274 Astra mediumも全14ケース各N=5の70件を追加する。基準は`e08fcf407d1244aca43f8a054fd993a8`。同じ時間記録コード、CLI 0.153.3と並列上限24を使い、Solの実行が終わってからAstraを開始する。両条件の140件を採点し、時間記録の取得状況を報告する。プロンプトとモデルがともに異なる比較として保持し、単独の効果へ帰属しない。

## 実行完了

両条件140件が完了し、すべて有効かつScore 4だった。[結果と時間記録の取得状況](../evaluations/results/c147-sol-c274-astra-time-recording-standard14-n5_2026-09-06.md)に記録した。直接CLI時計は140件取得、正式な作業時間は140件ともnull、ログ時刻の代替指標は139件取得だった。
