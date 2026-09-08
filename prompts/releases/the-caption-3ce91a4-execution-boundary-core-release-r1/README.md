# Candidate274リリース

2026年9月8日の利用者依頼「C274 を the-captionに適用して。」に基づき、評価済みC274を内容変更なしでreleaseへ固定し、the-captionへの反映を承認した。

## 識別と反映範囲

- release identity: `the-caption-3ce91a4-execution-boundary-core-release-r1`
- source candidate: `the-caption-3ce91a4-execution-boundary-core-r1`
- bundle SHA-256: `7454c6921e60db3334d8308b9cc016833a6a8588bc2ca4c275d78197780e4e66`
- 実効変更はroot `AGENTS.md`のみ。C147から`CONTEXT`・`OWNER_ROLE`・`ROOT`・`INDEPENDENCE`を削除し、9条項を逐語保持する。
- 非rootの本体更新と`CLAUDE.md`のsymlinkを保持する。バンドル全19対象を本体へ上書きしない。
- 開始commit・ロールバック対象: `6b20adb5973f5d10173dcfb4866a792057ec77a5`
- 実行前の範囲・許可・検証: [反映計画](projection-plan.json)

## 評価根拠と限界

[Astra mediumのStandard14各N=5](../../../evaluations/results/candidate274-c147-astra-medium-standard14-n5_2026-09-05.md)は70/70件がScore 4で、C147 Astra比トークン−0.91%、総所要時間−26.52%だった。[時間記録導入後の再計測](../../../evaluations/results/c147-sol-c274-astra-time-recording-standard14-n5_2026-09-06.md)でもC274 Astraは70/70件がScore 4だった。別計測系列をN=10へまとめ直してはいない。

SolでのC274評価、N=20以降、未評価の委任経路での安全性は未確認である。トークン差の統計的優位、モデル単独の速度差は主張しない。正式な作業時間は配送境界未観測のため未取得。これらの評価範囲を保持したうえで、今回の明示依頼を採用・反映の根拠とする。過去の評価結果とC147の反映履歴は変更しない。

研究基盤自身の`AGENTS.md`は引き続きC147の制御原文を使用する。本体へのC274反映を、研究基盤の制御変更へ自動的に広げない。

## 反映結果

[the-caption PR #27](https://github.com/Kenn-dclxvi/the-caption/pull/27)をマージし、`/Users/kenn/repos/the-caption`のmainも更新した。

- merge commit: `446c57b1f5fd11d2bcc9f80c38aa266d1552a196`
- 検証: `bash scripts/dev/verify_change_set.sh`、415 passed・8 skipped。
- 初回は分離先の仮想環境配置により環境切り替えテスト1件が失敗。専用環境とログ出力先を用意して同じ全試験を再実行し通過した。
- 公開CI: `gitleaks`・`claude-review`ともsuccess。
- 反映後の差分は`AGENTS.md`のみで、C274本文とbyte一致。root `CLAUDE.md`のsymlinkを保持した。
- バンドル対象は13/19一致。残る6対象は本体側の更新を保持し、root以外の差分0件を確認した。
- 評価: `astra_medium_standard14_n5_evaluated`、採用: `adopted`、release・本体反映: `projected`。
- 許可、開始commit、対象、検証結果、ロールバック先の正本は[反映記録](projection.json)。

これはリポジトリ指示の更新であり、アプリケーションの起動・運用処理の再実行は行っていない。
