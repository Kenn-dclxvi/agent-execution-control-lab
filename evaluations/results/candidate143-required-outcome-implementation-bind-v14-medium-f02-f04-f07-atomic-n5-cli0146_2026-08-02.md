# Candidate143 F02 / F04 / F07 N=5結果

## 結論

Candidate143のF02 / F04 / F07各N=5は、15 / 15がscore `4`だった。F02は5 / 5でengineとupdaterの両sourceを変更し、一source部分変更と無変更停止は0件だった。F04は5 / 5で単一targetの必要変更を維持し、F07は5 / 5でdependency declarationとlock provenanceのpairを揃えた。

Candidate143はCandidate118を直接親にした。C122以降のone-wave、single-target continuation、effect-state再判定、joint-owner gateは継承していない。変更前evidence operationの終了条件だけを、artifact単位の変更可能性から、TaskSpecが明示したrequired outcome全体の`implementation_bound`へ置き換えた。

今回のN=5では、C122以降で失われた追加観測の自由度と、複数artifact間relationを揃えてから変更する境界を両立できた。ただし、N=5は初期機構確認であり、stability、Standard14、採用、releaseは未判断である。

## 固定条件

- candidate: `the-caption-3ce91a4-required-outcome-implementation-bind-r1`
- direct parent: `the-caption-3ce91a4-implementation-bind-terminal-closure-r1`（Candidate118）
- bundle SHA-256: `bdeb69132c59afca22fbaa1814f7cb312a3cd4c73fa07afbc11f5b20706583b4`
- cases: F02 r1、F04 r2、F07 dependency r1
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Codex CLI / Python: `0.146.0` / `3.14.5`
- N / configured M: `5` / `24`
- newly issued: 15
- valid / rateable / excluded: `15 / 15 / 0`
- pool: `c012e543efa299ff4a17bbbde7ef14b0d91c2c743b38a75ef157a20c6a670181`
- selection: `28226b8690534f48a0b8d9a0c360674c`
- analysis: `42a08644138a46b2984bd7862af97dc1`
- registered result: `6320c49c8f8647d2a6d62ae724ce7493`
- selection comparison key: `008104d71d8980189b90ae60033bcfa118e1211b46be30dea8f7484eacfbcc7b`
- registered compatibility key: `1a160baf02c918304673639cae670d6d9bad5d235e33e965d641f60fef339d93`
- median quality / tokens / elapsed: `100.000` / `528,180` / `268.031秒`
- execution archive SHA-256: `dd843ed3bb5cac2ea8f471991f3bdd845e1dcb8e081b9dc0295b60b733280b6e`

中央値は、同じiteration番号のF02 / F04 / F07を束ねた5つのselection sampleの中央である。score分布と停止判断は15 run全件で判定した。owner / producer evidenceは15件ともdiagnostic-onlyでineligibleだったため、quality scoreの成否には使用していない。

## F02で観測した挙動

5件すべてが変更前に次の関係を認識した。

1. primary refreshはhistory取得へdate boundを渡していない。
2. updaterは日付を選んでいるが、その値をhistory取得へ接続していない。
3. selective retryと既存test contractは保持対象である。

その後、5件すべてがengineとupdaterを変更し、focused gateとfull gateを成功させた。1件は既存testも強化したが、必要な2 source変更は維持した。

run `8145f04a5e554e2490be98d7268dffff`は、最初に広い検索結果を受け取った後、対象を絞った追加readへ進んだ。その追加観測で2 source間relationをbindし、両sourceを変更してscore `4`になった。C142では初回resultが不完全な3件が追加readなしで無変更停止したため、この差はC122以降のone-wave制約を継承しなかった効果と整合する。

ただし、この一件だけで取得量や追加read回数そのものを成功条件とはしない。Candidate143の境界は、TaskSpec上のrequired outcome全体を一つの実行可能なimplementation choiceへbindできたかだけである。

## F04 / F07で観測した挙動

F04は5件すべてが`src/web/market_units_editor/src/App.tsx`だけを変更した。必要なaudit column visibility変更と既存contract保持を満たし、追加target変更はなかった。

F07は5件すべてが`requirements.in`と`requirements.txt`を変更した。dependency declarationとlock provenanceのpair欠落はなかった。

この結果は、required outcome全体を終了条件にしても、単一target taskを不必要に複数target化せず、明示されたpair taskでは両artifactを揃えられたことを示す。

## 解釈

事実として、Candidate143は初期N=5でF02の部分変更とfalse stopをともに0件にした。C141は不完全観測から部分変更し、C142は同じ不完全観測を停止へ変えた。Candidate143は、不完全な初回観測をoperation terminalにせず、required outcome全体を実装できる状態まで観測を続けた。

設計上の違いは手続きの追加ではない。`implementation_bound`の完了対象を、一つのartifactに対する変更predicateから、TaskSpecが明示した全change effectとartifact間relationへ戻した点である。追加readの回数、対象数、bytes、行数は固定していない。

今回の結果はF02 / F04 / F07のN=5に限る。他のStandard14 caseで正常経路を維持するか、低頻度failureを抑えるかは未測定である。追加24件またはStandard14への進行は、今回の初期gate通過とは別判断にする。

## 状態

`f02_f04_f07_n5_evaluated / quality_gate_passed / required_outcome_implementation_bind_observed / f02_multi_read_recovery_observed / result_registered / stability_not_evaluated / adoption_not_decided`

## 結論表

| case / gate | 実測 | 判定 |
| --- | ---: | --- |
| F02 score `4` | 5 / 5 | pass |
| F04 score `4` | 5 / 5 | pass |
| F07 score `4` | 5 / 5 | pass |
| 全体score `3`以下 | 0件 | pass |
| F02両source変更 | 5 / 5 | mechanism pass |
| F02一source部分変更 | 0 / 5 | mechanism pass |
| F02無変更停止 | 0 / 5 | mechanism pass |
| F02追加観測後のrelation bind | 観測あり | mechanism observed |
| F04単一target必要変更 | 5 / 5 | pass |
| F07 dependency pair完備 | 5 / 5 | pass |
| stability / Standard14 | 未実施 | not evaluated |
| 採用 / release / 本体反映 | 未判断・未実施 | not decided |
