# C274 Astra highとmediumの比較計測

利用者の「C274 の推論レベルhighを実行してmiddleと比較して。」に基づき、rootがC274 Astra high・Standard14全14ケース各N=5（70件）を実行する。middleは既存設定値mediumとして扱う。基準は時間記録導入後のmedium結果`d2a5c2dbe2bd405c835a05afd2ddccae`で、既存70件を再利用する。

推論レベルだけをmediumからhighへ変更する。C274 bundle `7454c6921e60db3334d8308b9cc016833a6a8588bc2ca4c275d78197780e4e66`、gpt-6-astra、CLI 0.153.3、Python 3.14.5、固定Layer 1・fixture・TaskSpec・採点・全エージェントトークン集計・時間記録コード・並列上限24・各N=5を保持する。条件差を実行前に検査し、不一致なら発行しない。これは推論設定の比較であり、プロンプト効果の比較ではない。採用済みC274と本体設定を変更しない。

反復ごとの14ケース合計を求め、その5反復の中央値で品質・トークン・総所要時間を比較する。CLI実行区間とログ時刻は診断とし、正式な作業時間の欠測を補完しない。無効な試行は既存の最大3試行の規則で扱い、追加N・ケース拡張を行わない。

実行証跡は`/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate274-astra-high-standard14-n5-cli0153-20260908-r1`。`preparation.json`、`reasoning-only-receipt.json`とLayer 1の`model-runtime-axis-preflight.json`に基準・CLI実体hash・コードhash・fixture一致・推論設定だけの差を記録した。基準と同じCODEX_HOMEを用い、別の条件プールへ登録する。

## 実行完了

[highとmediumの結果](../evaluations/results/candidate274-astra-high-medium-standard14-n5_2026-09-08.md)へ集計を保存した。新規high70件と既存medium70件を比較し、基準resultは再実行していない。
