# Candidate173 Rating v14 Medium Standard14 N=50

## 結論

Candidate173のStandard14を各case 50件、合計700件へ拡張した。既存N=5の70件を再実行せず、各caseの不足45件、合計630件だけを新規発行した。追加630 / 630件はvalid、excluded attempt 0、runner error 0だった。既存分と合わせた700 / 700件がScore `4`で、Standard14の品質条件は通過した。

一方、機序ではF02の1 / 50件で、TaskSpecのcriterion owner文字列`independent contract check`を独立producer executionの要求として扱い、独立review operationを起動した。全体では1 / 700件である。これはルート`OWNER_ROLE`が禁止するowner文字列からのproducer選択であり、N=5では見えなかった低頻度のreview admission誤経路である。したがって現在状態は`quality_passed / review_admission_mechanism_failed`とし、品質通過だけで採用へ進めない。

## 実行前ゲート

- reference result: Candidate147 `f7baeadc5bd44399ac13cc0e0a8aff48`
- Evaluation set: `the-caption-standard14-r1 / r1`
- Evaluation set identity: `2096d15e9d5d072e09e92313caa296caf8853c5e86f205d4d9f819b576263c33`
- Rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol / medium`
- CLI / Python: `0.146.0 / 3.14.5`
- permission: `workspace-write / never`
- executor: global queue、設定上の`M=24`
- token accounting: all-agent `v1`
- atomic comparison key: `60226e5443eee2f26127d089ce73626988b8c7aab3bb3c72b999d3b387875ce1`

最初のpreflightはN=50登録profileを実行profileとして渡したため、基準resultの履歴coverage 5と登録coverage 50の不一致でslot発行前に停止した。atomic runではNはselection provenanceであるため、既存C147拡張経路と同じく、実行preflightにはN=5互換profileを使用し、N=50 profileは50件selectionのresult登録だけへ使用した。修正後preflightは630 slotをauthorizeした。

## 品質結果

全14 caseが各50 / 50件でScore `4`だった。

| 観測 | 結果 |
| --- | ---: |
| valid | 700 / 700 |
| Score `4` | 700 / 700 |
| Score `3`以下 | 0 / 700 |
| 新規excluded attempt | 0 |
| 新規runner error | 0 |
| command protocol violation | 0 |

F10 monthly reviewの数値位置診断は`exact = 43`、`mismatch = 7`だった。Rating v14では成果と必須応答が成立しているため7件もScore `4`として保持する。この診断を品質失敗へ事後変更しない。

## review route診断

| 観測 | 件数 |
| --- | ---: |
| root-only session | 699 / 700 |
| multi-session | 1 / 700 |
| owner result `available` | 1 / 700 |
| owner result `not_applicable` | 150 / 700 |
| owner result `failed` | 549 / 700 |

誤経路はrun `3bfebd82b8aa49e6bfb6d059c3d80854`、F02 iteration 44の一件だけだった。rootは開始時にcriterion ownerを「指定された独立contract check」と解釈し、実装後に`/root/independent_contract_check`へF02-C3を割り当てた。独立result自体はPASSで成果品質への悪影響はなかったが、TaskSpecは独立producer execution identityを明示していない。したがって、これは必要な敵対的設計reviewではなく、criterion owner文字列からproducerを選んだ過剰起動である。

## Candidate147とのN=50比較

両selectionはatomic comparison keyとexecution stratumが一致する。

| KPI中央値 | Candidate147 | Candidate173 | C173 - C147 |
| --- | ---: | ---: | ---: |
| quality | 100.000 | 100.000 | 0.000 |
| all-agent tokens | 1,390,207 | 1,485,058.5 | `+94,851.5`（`+6.82%`） |
| elapsed seconds | 826.211 | 743.275 | `-82.936秒`（`-10.04%`） |

N=50の記述比較であり、tokenとelapsedの方向が異なるため、単一の効率優位へまとめない。

## 一次証拠

- profile: [`candidate173-concrete-counterexample-adjudication-v14-reasoning-medium-standard14-global-m24-n50-cli0146-r1.json`](../profiles/candidate173-concrete-counterexample-adjudication-v14-reasoning-medium-standard14-global-m24-n50-cli0146-r1.json)
- primary result: [`16c1efe030e64d5cbfd8b7426ed7c2df.json`](16c1efe030e64d5cbfd8b7426ed7c2df.json)
- result content SHA-256: `b37273ccc51b77f6bfea66c00d3d3dfa0f64cdad65b9bc6df7e6fdff1adc54da`
- audit: [`candidate173-concrete-counterexample-adjudication-standard14-n50-audit-r1.json`](candidate173-concrete-counterexample-adjudication-standard14-n50-audit-r1.json)
- atomic pool: `263dad2009b3897188931433b41be5a659c265d7f1e824a8d5c3251419500920`
- Candidate173 selection / analysis: `ea4bfb17d22c4cdba092fe2eec9acff1` / `dd844f2163ac4b7c81641392bb0e932e`
- Candidate147 selection / analysis: `ac21abcb439f4e4aadf7885d3cf5f7a2` / `afaabb50ff084b4094eb103b7068f39f`
- registered result: `16c1efe030e64d5cbfd8b7426ed7c2df`
- result compatibility key: `3cadbf8880cff04eff776e2981b028f605122a4dbe621b99b805915497d7517f`
- raw run root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate173-concrete-counterexample-adjudication-v14-medium-standard14-n50-cli0146-20260810-r1`

## 状態境界

- Target r2: `quality_passed / required_review_mechanism_passed`
- Standard14 N=50: `quality_passed_700_of_700 / unexpected_review_route_1_of_700 / mechanism_failed`
- candidate modification: `not_performed`
- adoption: `not_decided`
- release: `not_created`
- runtime projection: `not_projected`
