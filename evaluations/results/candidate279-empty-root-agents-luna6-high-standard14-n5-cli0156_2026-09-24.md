# Candidate279 ルート`AGENTS.md`空化・Standard14再試験

## 結果

GPT-6 Luna High・Standard14・N=5で70 / 70件が有効・採点可能、除外0件だった。Score `4`は69 / 70件、Score `2`は1件で、`TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT`のiteration 1に集中した。A01は5 / 5件Score `4`となり、要求値を確認する前の編集・試験は0 / 5件だった。

C279の品質中央値は100.00点でC278と同じだった。5反復の品質値は100、100、100、96.43、100点であり、1反復にScore 2があっても中央値は100になる。中央値だけでは69 / 70件という個別採点分布を表せない。

## 条件と比較

- Candidate: `the-caption-3ce91a4-execution-control-empty-root-agents-r1`（Candidate279）、bundle SHA-256 `999769800af5a5b4f986a0589d8527d6b4f74ace7a56eb6b19b16e3ebaf43f0d`
- 直接親 / 比較基準: Candidate278 result `b4287d35640041e7bdf1e12ad1559e4b`。C278からroot `AGENTS.md`本文だけを0 byteにした。
- 実行条件: GPT-6 Luna High、Codex CLI 0.156.1、Standard14 14ケース×5回、Rating v14、all-agent token accounting v1
- 事前照合: compatibility key `d72f0ae2d2d945c77bfab3ee51284db2dc8011fbc3072d096ecc3ca041fa304e`、70 slot許可、C278のLayer 1を再利用
- C279 result: `0f3d949876f5421da0cecece6dfc59ca`

| 指標 | C279 | C278 | C279 − C278 |
|---|---:|---:|---:|
| 品質中央値 / 100 | 100.00 | 100.00 | 0.00 pt |
| all-agent `total_tokens`中央値 | 2,509,039 | 2,792,069 | -283,030 (-10.14%) |
| `elapsed_seconds`中央値 | 984.12秒 | 1,085.11秒 | -100.99秒 (-9.31%) |

## Free resultとの関係と実行環境

C279のbundle SHA-256は保存済みControl-Free result `71a8231c6cc048d0a522aaa43d3a91b6`と一致し、compatibility keyも同じだった。保存済みFreeはScore 4が65 / 70件、A01は0 / 5件Score 4。C279の再実行はScore 4が69 / 70件、A01は5 / 5件Score 4だった。別々の実行で結果が異なり、prompt内容の差では説明できない。

この試験は「ユーザー指示が一切ないCLI」を作っていない。評価runnerは`--ignore-user-config`と`--ignore-rules`を付けるが、固定CLIのhelpによると前者は`config.toml`、後者はuser/projectの`.rules`ファイルだけを対象にする。どちらも`AGENTS.md`を無効化しない。実行時は`CODEX_HOME`が未指定で、Codexの既定`~/.codex/AGENTS.md`に1049 byteのユーザー共通指示が存在した。その内容は今回ユーザーが提示した`### 実行制御`の4項目と一致し、タスク条件が不足する場合に実行前の確認を優先する。A01の失敗を防ぐ方向に働きうる指示である。C278とC279の両実行より前に更新され、その二試験の間は同じ内容だった。したがって両Candidateの直接比較ではこの共通指示は固定されているが、repo rootだけが空のFreeを完全な無指示条件とは呼べない。

保存済みFree resultは2026-09-24 03:27 UTCに登録され、現在のユーザー共通`AGENTS.md`の更新時刻は同日11:42 UTCだった。Free実行時の旧ユーザー共通指示の内容は保存されていないため、65 / 70から69 / 70への変化を更新後の指示の効果と断定できない。一方、Free保存runではA01が0 / 5、更新後に実行したC279では5 / 5だったため、global指示を固定または無効にした追試がない限り、この差をroot `AGENTS.md`空化や偶然だけに帰属させない。

## 保存先と判定範囲

- [機械可読result](candidate279-empty-root-agents-luna6-high-standard14-n5-cli0156_2026-09-24.json)
- [70件quality audit](candidate279-empty-root-agents-luna6-high-standard14-n5-quality-audit-r1.json)
- [C278比較view](candidate278-candidate279-empty-agents-comparison-r1.json)
- [集約analysis](candidate279-empty-root-agents-luna6-high-standard14-n5-analysis-r1.json)
- [設計記録](../../docs/candidate279-empty-root-agents-design.md)
- 証跡archive: `/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate279-empty-root-agents-luna6-high-standard14-n5-cli0156-20260924-r1/compact/final-evidence.tar.zst`（SHA-256 `375cc8a878a8f4bad4a51dca4b35d4afd7816cc8d049325024209d0996cc6314`）

これはC278とC279の同日N=5比較と、同一prompt bytesを持つ過去Free resultの再観測である。Free実行時と今回のユーザー共通`AGENTS.md`が一致していたことは確認できず、Freeとの差からこのファイルの因果効果を主張しない。Candidate279は機序成立、採用、releaseまたはTHE-CAPTION本体への反映を意味しない。
