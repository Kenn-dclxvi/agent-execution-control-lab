# C301のGPT-6.1 Sol Low・Sonnet 5.5 low、Standard14 N=5（実行環境を切り離した新しい系列の基準、2026-10-09）

2026-10-09。[実行環境の計画](../../docs/agent-runtime-venv-isolation-plan-r1.md)の6として、実行環境を切り離した新しい評価系列（`shell_environment.revision: fixed-path-workspace-venv-r1`）の基準を測った。利用者の指示により、基準はC280そのものではなく、C280のrootの`AGENTS.md`のMarkdownの書式を揃えた[C301](../../docs/candidate301-c280-uniform-markdown-design.md)とした。**両セルとも有効70件すべてが4点だった。品質中央値は両セル100。全エージェントトークン中央値はSol Low 2,041,902、Sonnet low 794,780。経過時間中央値はSol Low 658.29秒、Sonnet low 271.86秒。** 除外と再試行は両セルとも0件だった。

この系列には保存済みの結果がなく、比較相手を持たない単独の計測である。旧系列（C280〜C300）の結果とは実行環境が違うため比較せず、差をプロンプトの効果として扱わない。

## 条件

- プロファイル：[Sol Low](../profiles/c301-sol61-low-standard14-n5-cli0159-isolated-shellenv-20261009-r1.json)、[Sonnet low](../profiles/c301-claude-sonnet55-low-standard14-n5-cli2288-shellenv-r1.json)。同じ系列のC280のプロファイルから、prompt identityだけを替えた。
- prompt identity：`the-caption-3ce91a4-outcome-binding-uniform-markdown-r1`、bundle SHA-256 `ba025ba64b54ec8d7fc9fb5cf244168f9fd0ec0ed613737f557bb164c349b7a2`。
- 実行環境：両セルとも、エージェントへ渡す環境を固定値と作業ツリーの`.venv`（PATHの先頭、`VIRTUAL_ENV`）、空の`ZDOTDIR`から組み立てた。Sol Lowは`-c allow_login_shell=false`で起動した。140件すべてで、起動前の確認（`shell-environment/receipt.json`の`ok`）が通り、個人のシェル設定は読まれていなかった。
- モデルと実行器：Sol Lowは`gpt-6.1-sol`、推論設定`low`、Codex CLI 0.159.0。Sonnet lowは`claude-sonnet-5-5`、推論設定`low`、Claude Code 2.1.288。権限、ツール、採点契約、ケース、fixture、TaskSpecは旧系列と同じ。
- 評価セットとfixtureは、C280 Sol Lowで固定したLayer 1を両セルへ写して使った。
- 評価コードはコミット`52f926a`のもの。発行方式は両セルとも`wave_barrier`、`max_workers`は24。両セルを同時に発行した。発行前の確認は[発行前の記録](c301-sol61-low-sonnet55-low-standard14-n5-shellenv_2026-10-09-preflight.json)にある。
- 日本時間2026-10-09 15:29:39〜15:36:24に実行した。

## 結果

| セル | 4点 | 品質中央値 | 全エージェントトークン中央値 | 経過時間中央値 |
| --- | ---: | ---: | ---: | ---: |
| Sol Low | 70 / 70 | 100.00 | 2,041,902 | 658.29秒 |
| Sonnet low | 70 / 70 | 100.00 | 794,780 | 271.86秒 |

中央値は、14ケースを合算した各反復の値を5回分集計した値である。反復ごとの合計は、Sol Lowがトークン2,001,409〜2,327,547、経過時間614.06〜811.94秒、Sonnet lowがトークン780,608〜834,686、経過時間262.37〜322.12秒だった。

## 診断（合否にしない）

- A02では、10件すべてでテストのコマンドが成功し（`N passed`）、その後に報告した。Sol Lowは`.venv/bin/python -m pytest`、Sonnet lowは`python -m pytest`などをそのまま使った。旧系列のSonnet lowで多かった、確かめていない環境の制約を理由にテストをやめる処理は見られなかった。
- 品質監査の診断値：Sol Lowは`command_protocol_violations` 0件、Sonnet lowも0件。

採用、追加反復、release、本体反映は行っていない。次にどのCandidateを測るかは、利用者が決める。

## 一次アーティファクト

- Sol Low：[登録結果](822c2115d5ca41c684039db0a3900894.json)・[品質監査](c301-sol61-low-standard14-n5-shellenv_2026-10-09-quality-audit.json)
- Sonnet low：[登録結果](a4fe6d1acb4246489c6901409efd8acf.json)・[品質監査](claude-sonnet55-low-c301-standard14-n5-cli2288-shellenv_2026-10-09-quality-audit.json)
- 両セル：[発行前の記録](c301-sol61-low-sonnet55-low-standard14-n5-shellenv_2026-10-09-preflight.json)
