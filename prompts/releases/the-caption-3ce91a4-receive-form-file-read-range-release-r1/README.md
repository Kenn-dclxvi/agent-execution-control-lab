# 候補316 リリース

## 結論

候補316（C316）を、そのままの内容でリリースした。

リリース状態は`released`、承認状態は`approved`である。THE-CAPTION本体へは投影していない（`not_projected`）。

承認は、2026-10-12の利用者の判断（「C316をリリース扱いにする」）による。同じ日に、利用者はC316の「# 実行制御」を自分の共通指示（`~/.claude/CLAUDE.md`と`~/.codex/AGENTS.md`）に置いた。これはTHE-CAPTION本体への投影ではなく、このリポジトリの外での利用者による適用として記録する。

## 識別情報

- リリース識別子: `the-caption-3ce91a4-receive-form-file-read-range-release-r1`
- 元候補: `the-caption-3ce91a4-receive-form-file-read-range-r1`
- 元候補の固定commit: `e8c64839cbd057ce5fc9ce97d9200cd7cd9fcb95`
- bundle SHA-256: `0a1cbfe43a0333230a81d42a746d94c3f0375e5786e0d864fba9686c39b9651a`（元候補と同じ）
- 内容関係: 候補316と同一内容のリリーススナップショット
- 候補316から変更した対象: なし
- 本文: root `AGENTS.md`の「# 実行制御」6項目（1,687バイト）。ほかの18対象はTHE-CAPTIONの現在の内容のまま

## 評価範囲

- 評価集合: `the-caption-standard14-r1`（固定Standard14、14ケース）
- 条件: 実行環境を切り離し、負荷を見て次のrunを始める発行（CPU使用率70%以下、間隔1秒、合計24本）。費用は単価表`api-standard-2026-10-10-r2`で換算
- Free比（N=5、各70件）:

| モデル | 点数分布（Free → C316） | 費用の差 | 経過時間の差 |
| --- | --- | ---: | ---: |
| GPT-6.1 Sol Low | 4点69件・0点1件 → 4点70件 | −31.28%（幅より下） | −20.61%（幅より下） |
| GPT-6 Astra Low | 4点68件・0点2件 → 4点70件 | −32.94%（幅より下） | −21.65%（幅より下） |
| Claude Code Sonnet 5.5 low | 4点65件・0点5件 → 4点70件 | −11.17%（幅より下） | −6.62%（幅より下） |
| Claude Code Opus 5.5 low | 4点69件・0点1件 → 4点70件 | −11.64%（幅より下） | −8.27%（幅より下） |

- 累積N=20: Sol LowとSonnet lowで各280件すべて4点。費用の中央値はSol Low 0.6310 USD、Sonnet low 0.6246 USDで、どちらもC313（N=5）の幅より下

## 未解決risk

- 固定Standard14の範囲の観測である。Opus lowとAstra LowはN=5だけ。
- Freeとの品質差は、A01（期待結果が依頼から決まらないケース）で結果が決まる前に作業を始める失敗の抑止に限られる。ほかの13ケースはFreeでも4点だった。
- Standard14ではサブエージェントが起動しないため、担当を分ける項目を外した影響は観測していない。
- 2行目（事前調査を絞る）と6行目（判断に必要な範囲だけ読む）は、モデルの判断に頼る部分を含む。
- 個人の共通指示として全プロジェクトに置いた場合の効果は計測していない。リポジトリ側の指示と一緒に読まれる条件は、評価の条件と違う。

## 承認状態

- リリース準備: `complete`
- リリース状態: `released`
- 採用承認: `approved`
- 本体反映: `not_projected`
- 承認根拠: 2026-10-12の利用者の判断
- リポジトリ外での適用: 利用者が`~/.claude/CLAUDE.md`の「# 実行制御」の節と`~/.codex/AGENTS.md`の全文に置いた。2026-10-12に、どちらもこのリリースのroot `AGENTS.md`と同じ文面であることを確認した。

## 根拠

- [FreeとC316の4モデル比較](../../../evaluations/results/free-c316-four-models-standard14-n5_2026-10-12.md)
- [C316の累積N=20](../../../evaluations/results/c316-sonnet55-sol61-low-standard14-n20_2026-10-12.md)
- [C316のSol Low](../../../evaluations/results/c316-sol61-low-standard14-n5_2026-10-12.md)、[C316のSonnet low](../../../evaluations/results/c316-claude-sonnet55-low-standard14-n5_2026-10-12.md)
- [候補315・316設計記録](../../../docs/candidate315-candidate316-c313-file-read-receive-form-design.md)
- [候補316 manifest](../../candidates/the-caption-3ce91a4-receive-form-file-read-range-r1/manifest.json)
