# Candidate273のAstra medium N=5計測

利用者の指定により、設計時のSol基準ではなく、Astra内のC147対Candidate273を測る。モデル間の差をprompt効果へ帰属しない。初回は既存設計のA01・A02・F01・F02・F04・F07 dependencyの6ケース各N=5、30件。品質低下・採点不能・実行無効・互換条件不一致、または事前のコスト条件不通過で拡張を停止する。

## 準備の修正

初回準備r1は、6ケースの基準結果へ元の14ケースcoverageを持つLayer 1を渡したため、coverage照合で停止した。発行は0件。r2は元のset.jsonと全fixtureを保存状態から複製し、過去の実行範囲メタデータを持ち込まず、6ケースの新規coverageを正規の比較準備コマンドで固定した。元のLayer 1、TaskSpec、fixture、評価基盤コードは変更していない。

## 固定条件

- model / reasoning: `gpt-6-astra / medium`
- CLI: `0.153.3`。保存基準と同じexact executable・hashを照合。PATHへのfallbackなし
- Python: `3.14.5`。共有runtimeの固定hashを照合
- 並列上限: `24`
- Rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- token accounting: 全エージェント、`v1`
- C147の元result: `654d171e89a547d9af421ec9ee05ad96`
- 6ケース選択result: `2c5c5b8c1576471b81f2c05947a92a08`
- Candidate273 pool: `8216874dea93220feba1686f0089ce6594540fe8ea7f526a1c3ad0993b3ae6e4`
- Candidate273 bundle: `748b9eb7137ebfb63866ad18155f10b5dbd2ab6c644fd95c4c5873e80e823910`

`prepare-comparison-layer1`、`prepare_atomic_plan.py`、`preflight-comparison`、`verify-comparison-preflight`はr2で通過した。非prompt条件、全fixture、選択範囲、capsuleと実行計画を機械照合した。

ローカル証跡: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate273-v14-medium-six-case-astra-n5-cli0153-20260905-r2`。生ログはcommit対象にしない。

プロファイル: [Astra medium 6ケースN=5](../evaluations/profiles/candidate273-outcome-evidence-core-v14-medium-six-case-astra-m24-n5-cli0153-r2.json)。最終計測結果は完了後に別の一次resultへ記録する。

## 計測完了

[一次結果](../evaluations/results/candidate273-c147-astra-medium-six-case-n5_2026-09-05.md): 30 / 30件がScore 4。トークン+110.84%、経過時間+6.04%でコスト条件不通過。初回N=5で拡張を停止した。
