# Candidate118 / Candidate119 validation predicate / method boundary結果

## 結論

Candidate119は、A02のartifact変更後から最初のvalidation commandまでに発生していたvalidation method探索を、Candidate118の4 / 5件から0 / 5件へ減らした。A02 token中央値も`226,321`から`149,154`へ`77,167`（`34.10%`）減った。

一方、Candidate118で0 / 5件だったimplementation bind後・最初のartifact変更前のcommand再入が1 / 5件発生した。A02 token中央値も事前目標のCandidate107 `125,559`以下には届かず、`23,595`（`18.79%`）上回った。したがってquality gateは通過したが、mechanism gateとcost gateは不通過である。A02 `N=20`、Standard14、採用、release、runtime projection、本体反映へ進めず、Candidate119を`stopped`とする。

## Identityと互換条件

- candidate: `the-caption-3ce91a4-validation-predicate-method-boundary-r1`
- direct parent / reference: `the-caption-3ce91a4-implementation-bind-terminal-closure-r1`
- bundle SHA-256: `26894d8cddaea8079ce15bcc7644691c2d14f0a042cd81bafb4e46d99478411c`
- Evaluation set: `the-caption-standard14-r1` / `r1`からA01 r2、A02 r2、F01 r3を選択
- Rating: v14
- model / reasoning: `gpt-5.6-sol` / `medium`
- CLI / Python: `0.146.0` / `3.14.5`
- case別N: 5
- profile上のM: 24
- comparison key: `89b8a73a23bd7e27f7ac6a417dcb9a5052d275deb93754e5637f7d061dfaf390`
- compatibility key: `4e4bb890ed87c028e2cfaec57bbd4813bcd970c7298c8f31aa580fcb803e0854`

Candidate118から変更したのはroot `AGENTS.md`のvalidation readiness一軸である。TaskSpecまたはcommand evidence protocolがexact commandを明示しないvalidationでは、predicate、順序、個別pass条件、stop条件がbind済みなら、exact commandを未解決identityではなくexecution methodとして扱う。TaskSpec、case、fixture、rating、executorは変更していない。

## 実行と品質

- 新規発行: Candidate119の不足15 runだけ
- execution: 15 / 15 valid、excluded 0、external failure 0
- quality: score `4` × 15
- A01: required value待ち5 / 5、変更0 / 5、test 0 / 5
- A02: canonical成果5 / 5、successful test evidence 5 / 5
- F01: score `4` 5 / 5、command protocol違反0件
- pool key: `76288ddae67040ab2839dbbee29df1693216b3b593913c6130298d5ca1c88e4b`
- selection ID: `6c5d3bd1a5bb40248cb63e909eb068ea`
- analysis ID: `88137a0ea4694ba997f81cf590394e8b`
- result ID: `58ac8afa4b844e23880e99889051f47a`

3 case集約中央値はCandidate118比でtoken `365,455 → 325,773`、差`-39,682`（`-10.86%`）だった。elapsedは`157.746 → 159.656`秒、差`+1.909`秒（`+1.21%`）だった。この集約値はtargeted 3 caseだけの結果であり、Standard14へ一般化しない。

## A02 mechanismとcost

| 判定項目 | Candidate118 | Candidate119 | gate |
| --- | ---: | ---: | --- |
| canonical成果 | `5 / 5` | `5 / 5` | pass |
| implementation bind後・変更前command再入 | `0 / 5` | `1 / 5` | fail |
| 変更後・最初のvalidation前method探索 | `4 / 5` | `0 / 5` | pass |
| token中央値 | `226,321` | `149,154` | C118未満はpass |
| C107 case目標 | `125,559` | `149,154` | fail |

Candidate119のA02 tokenは`129,094 / 133,160 / 149,154 / 154,976 / 212,159`だった。4件はcanonical implementationのbind後に直ちに`run.sh`を変更し、追加repository探索なしでvalidationへ進んだ。残るrun `d51dd5a794cf4d2298e647db8349f212`は、canonical targetを`src.app.entrypoints.v4_daily_main`、故障箇所を旧`daily_main`参照と明示した後、`src/AGENTS.md`、ADR、entrypoint実体、test設定を追加で読んでから変更した。この2 commandのうち後者はexit `2`だったが、変更後のrequired validationはすべて成功し、最終成果はscore `4`だった。

事実として、validation predicate / exact command境界は変更後method探索を閉じ、A02 costを大きく下げた。事実として、同じ候補はCandidate118の変更前terminal closureを5件すべてでは維持できず、C107のcase最小値にも届かなかった。したがって一つの制御で解決済みとは判断しない。

次の仮説はCandidate119を親として、すでに成立した変更後method境界を保持しながら、implementation bind後からartifact変更までのevidence admissionを別のpredicateで閉じることである。これはCandidate119のpredicateを撤回する案ではなく、保存traceが示した二つ目の不足制御を追加で検証する案である。

## 状態

`targeted_a01_a02_f01_evaluated / quality_gate_passed / postchange_method_boundary_passed / prechange_terminal_closure_failed / a02_cost_improved_vs_c118 / a02_cost_target_failed / result_registered / stopped`

## 証跡

- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate119-validation-predicate-method-boundary-v14-medium-a01-a02-f01-atomic-n5-cli0146-20260731-r1`
- execution archive SHA-256: `ab3d68f9e13fce57239461e6dad9b7fe8721331e19555c51b9d9cfd436babbe8`
- final archive SHA-256: `a2d82542db3f35d2a096770b1105c6d46c3d2ea2e0c54cd95c41ee1a313d3bbb`
- quality audit: `batch-001/quality-audit.json`
- selection: `candidate-selection.json`
- analysis: `candidate-analysis.json`
