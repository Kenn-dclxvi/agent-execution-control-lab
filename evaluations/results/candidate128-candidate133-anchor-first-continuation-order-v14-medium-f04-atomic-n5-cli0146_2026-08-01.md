# Candidate128 / Candidate133 F04 targeted result

## 結論

Candidate133のF04 N=5は5 / 5件がscore `4`だった。しかしanchor-first mechanismは4 / 5件に留まった。1件が変更前にanchor contentを直接取得せず、`App.tsx`の1〜520行と521行以降を順に全量取得した。事前mechanism停止条件によりCandidate133を停止し、追加24件、F02、F07、Standard14へ進めない。

低Scoreは出なかったが、Candidate131 N=29の低Scoreを生んだ「exact anchorがある状態で全残存contentへ進む分岐」を消せなかった。最後に発行した`rg`はartifact変更と3 validationの後であり、変更前anchor-firstの成立証拠にはしない。

## 固定条件

- candidate: `the-caption-3ce91a4-anchor-first-continuation-order-r1`
- parent: `the-caption-3ce91a4-required-effect-closure-r1`
- bundle SHA-256: `02fc0269da596ebe0a7b63dffc015c89bc9191ebbbda44b09a00c8e5554f6c6f`
- case: `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY/r2`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Codex CLI / Python: `0.146.0` / `3.14.5`
- N / M: `5` / `24`
- pool: `da9f23fbf09a2a3c2db1840359a64f1035a2409fbe4199df6e8628412b478815`
- compatibility key: `1a3b75ac2311cda9630a15db6ee0ab8c3d8e51bb46d4c63c44954fc5a958c24a`
- selection: `2c8c5b415f5f4811b152d0bcd4003994`
- analysis: `6231727c98b64536b3ee4848b85cd2e5`
- registered result: `df291a5e3c1b4d23a823dea6e607e232`
- excluded attempt: 0

## 結果

| iteration | run | score | 変更前continuation | artifact変更 | validation |
| ---: | --- | ---: | --- | --- | --- |
| 1 | `42cedb2df3f24dc691d7a0ad80742dc1` | 4 | direct anchor | `hasAuditKey`一行 | 3 / 3成功 |
| 2 | `0b5d191ec8974e84ba74abd10c0f543d` | 4 | 全残存contentへ直行 | `hasAuditKey`一行 | 3 / 3成功 |
| 3 | `c3df142021994239b159cf2f2f4fc26f` | 4 | direct anchor | `hasAuditKey`一行 | 3 / 3成功 |
| 4 | `a4ddb736b5254561be5615edb5437846` | 4 | direct anchor | `hasAuditKey`一行 | 3 / 3成功 |
| 5 | `fc09ef8f260a4bdfa4843071881a6817` | 4 | direct anchor | `hasAuditKey`一行 | 3 / 3成功 |

iteration 2は初回waveで`App.tsx` 1〜520行を取得し、一回のcontinuationで521行目以降を取得した。変更前にanchor検索を発行していない。変更とvalidation完了後の最終確認で初めて`rg 'const hasAuditKey|...|colSpan=|...'`を発行した。

全5件でstale preimage、`colSpan`変更、artifact変更失敗は0件だった。必要な一行変更と3 validationは5 / 5件で完了した。

## 解釈

Candidate133はcontinuation resultの順序を規定したが、その前提となる`observed_anchor_set`が空かどうかの判断を残した。iteration 2はTaskSpecと初回contentにexact-match可能な語があっても集合を空側として扱った。したがって、Candidate131の`criterion_anchor_ready`を`observed_anchor_set`へ言い換えただけでは、fallback選択前のmeta-judgmentを消せない。

5件中央値はquality `100.000`、token `169,795`、elapsed `86.531`秒だった。mechanism gate不通過のため効率は判断しない。

次案を作る前に、anchor集合の有無をmodelの新しい分類判断にせず、TaskSpecに既出のexact lexical valueから直接request identityを作れるかを監査する。特定caseの語、固定command、executor変更は解決策にしない。

## 状態

`targeted_f04_n5_evaluated / quality_gate_passed / mechanism_gate_failed / anchor_first_4_of_5 / full_content_direct_1_of_5 / stale_preimage_0_of_5 / result_registered / stopped`

## 結論表

| gate | 期待 | 実測 | 判定 |
| --- | ---: | ---: | --- |
| valid / rateable | 5 / 5 | 5 / 5 | pass |
| score `4` | 5 / 5 | 5 / 5 | pass |
| score `3`以下 | 0 / 5 | 0 / 5 | pass |
| anchor-first continuation | 5 / 5 | 4 / 5 | fail / stop |
| 全残存contentへ直接進む | 0 / 5 | 1 / 5 | fail |
| staleまたは未観測preimageを持つ変更 | 0 / 5 | 0 / 5 | pass |
| 必要変更とrequired validation完備 | 5 / 5 | 5 / 5 | pass |
