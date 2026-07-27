# Click repository sub-AGENTS比較設計

## 結論

Clickで、repository固有の階層別instructionが実行品質と実行量へ与える影響を、
root制御promptとは分離して確認する。比較するのは次の2条件である。

- No-AGENTS: rootと配下のどこにも`AGENTS.md`を配置しない。
- Repository sub-AGENTS: rootには配置せず、Clickに実在する`src/`、`tests/`、
  `docs/`だけへrepository固有の`AGENTS.md`を配置する。

両条件はClick Std14、Rating v10、Medium、N=5、M=24で実行する。既存の
Control-Free Bundle Aは0 byteのroot `AGENTS.md`を配置する別identityなので、
No-AGENTSの結果として流用しない。

## 作成前gate

1. 基準prompt setは`click-00e592c-no-agents-r1`とする。最短正常経路は、固定
   TaskSpecとrepository stateから必要な成果を作り、指定されたrequired validationを
   完了して停止する経路である。
2. 保存済みClick Control-Free Medium traceでは70 / 70件がscore `4`だった。
   一方、A02は429,730 token、16 model step、132.782秒であり、repository内の
   tox routingと検証経路の探索が他targetの対応caseより重かった。
3. Clickの固定target treeには`AGENTS.md`がなく、TaskSpecも`src/`、`tests/`、
   `docs/`ごとの配置、test、documentation規則を局所authorityとして与えない。
4. 変更する一つの構成軸は、root instructionを置かないまま、実在する3領域へ
   repository固有のsub `AGENTS.md`を追加することである。
5. この構成差が消すと想定する判断点は、正規source位置、近接test、標準test
   route、documentation検証を各taskで探索し直す判断である。
6. 新たに増えるのは3つのpath-scoped instructionと、その領域へ入ったときの
   読解である。root制御predicate、C81、外部reference file、存在しない
   `scripts/`階層は追加しない。
7. 品質維持は`click-standard14-r1`の14 caseで確認する。各条件70 / 70件を
   validかつrateableにし、score分布を記録する。
8. 公式比較はquality、all-agent token、elapsedの3 KPIだけとする。適用された
   instruction path、model step、commandは効果経路を調べるdiagnosticとする。
9. No-AGENTS比で品質低下、required command欠落、またはsub instructionが
   TaskSpecと衝突する結果が1件でもあれば、効率値にかかわらず水平展開候補として
   停止する。品質を維持しても、採用、release、Click本体への反映は判断しない。

## instructionの由来

THE-CAPTIONと同じく、rootの実行制御とrepository固有の階層指示を別fileとして
扱う。ただし本文はTHE-CAPTIONから転記せず、Click固定commitの次のauthorityに
限定して構成する。

- `pyproject.toml`: package layout、pytest、tox、typing、docs buildの設定
- `docs/contributing.md`: Click固有のtest環境、code style、Markdown 80文字幅
- `docs/testing.md`: `CliRunner`のprocess-global stateと並列testの制約
- 固定tree: `src/click/`、`tests/`、`tests/typing/`、`docs/`の実在

Clickには固定tree上に`/scripts`がない。したがってTHE-CAPTIONの4つのsub
instructionを機械的に移植せず、実在する3領域だけを対象とする。

## 比較identity

| 条件 | prompt identity | target |
| --- | --- | --- |
| No-AGENTS | `click-00e592c-no-agents-r1` | 0 |
| Repository sub-AGENTS | `click-00e592c-repository-subagents-r1` | `docs/AGENTS.md`、`src/AGENTS.md`、`tests/AGENTS.md` |

両bundleのsource commitは
`00e592cea702e0b2caa0dee42489fdb1c22cd845`、treeは
`c6aa87f15f2e44a6fcab33714e1eb91e2552d816`へ固定する。

## 非目標

- C81全文との比較または組合せ
- 3つのsub instructionを個別predicateへ分解した因果推定
- Click向けroot promptの最適化
- Candidate採用、release、pallets/click本体へのprojection

## Evidence

- [Click Control-Free Medium baseline分析](click-control-free-medium-baseline-analysis.md)
- [Prompt file bundle方式](prompt-file-bundle.md)
- [Prompt比較workflow](prompt-comparison-workflow.md)
