# Candidate147 F06 authority route 原因監査

> [!IMPORTANT]
> **状態**: `N100_21_runs_reaudited / command_routes_21_classified / model_visible_inputs_21_verified / required_path_instruction_reads_17 / redundant_root_rereads_6 / result_unused_failed_probes_2 / ADR9_saved_runs_450_checked / ADR9_redundant_root_reads_111 / isolated_prompt_trial_not_ready`
>
> Candidate147 F06 N=100結果の`authority追加read 21 / 100`を、保存済みall-agent command evidenceへ戻して再分類する。この監査は既存resultの品質、token、elapsedまたは当時の集計を変更しない。21件を一括して不要readまたは最適化可能costとは扱わない。

## 結論

旧`authority_lookup`指標は、`AGENTS.md`または`.agents`を含むcommandを数えた挙動指標であり、必要なpath-local repository instruction readと、広い探索、root再読、結果を使わないprobeを区別していなかった。

21 runの内訳は次である。

| route | run数 | 観測 |
|---|---:|---|
| path-local instructionだけを含む | 13 | `tests/AGENTS.md`を読み、対象testへ適用するruleを確認した |
| path-local instructionとroot instructionの両方 | 4 | `tests/AGENTS.md`に加えてroot `AGENTS.md`も明示readした |
| root instructionだけ | 2 | root `AGENTS.md`をreadしたが、`tests/AGENTS.md`のreadは記録されていない |
| discoveryだけ | 2 | `.agents / .codex`等をprobeしたが、`AGENTS.md`本文のreadは記録されていない |

したがって、17 / 21件は対象pathへ適用されるinstructionを確認したrunである。これを成果に寄与しない不要readと判定する根拠はない。むしろrepository instructionを変更前に確認する正常経路である。

全21件の最初のtool発行前inputも照合した。root `AGENTS.md`のC147本文は21 / 21件ですでにmodel-visibleだった一方、`tests/AGENTS.md`本文は0 / 21件だった。したがって、root本文を明示readした6件は、開始時点で不足していたrepository authorityを取得したのではなく、同じ制御本文を再取得したrouteである。これに対し、path-local instructionの17件は開始時点で不足していた適用ruleを取得している。

最適化余地があり得るのは、path-local instructionの意味を削ることではなく、次のrouteである。

- root instructionが既にmodel-visibleである場合のroot再読。
- targetが`tests/unit/...`へ固定済みなのに、`find ..`、repository全体`rg`、`.agents / .codex`探索を行うroute。
- path-local instruction identityを一意に解決した後も別authority候補を探すroute。

ただし、これは直ちにpromptへ固定path、読取り回数またはlocator commandを追加する根拠ではない。保存traceから直接確認できたのは、重複root取得6件と、結果を使わない失敗probe 2件である。これを防ぐための新しいprompt predicateが非対象経路へ追加判断を生まないことはまだ評価されていない。

## model-visible inputの照合

21 runすべてについて、最初のcustom tool callまたはfunction callより前のmessageを照合した。

| input | tool発行前にmodel-visible | toolによる本文read | 因果上の扱い |
|---|---:|---:|---|
| root `AGENTS.md`のC147本文 | 21 / 21 | 6 / 21 | 6件は同じ制御本文の再取得 |
| `tests/AGENTS.md`本文 | 0 / 21 | 17 / 21 | 17件はtargetへ適用される未取得ruleの取得 |

root本文の可視性は見出し`# THE-CAPTION execution control`と`SPEC`冒頭文の両方で確認した。path-local本文の非可視性は`# tests instructions`がtool発行前inputへ存在しないことを確認した。root-only 2件のread後messageも、開始identity、clean status、既存helperおよび隣接test書式を変更根拠としており、root再読で新しいmethod、constraintまたはstop conditionが追加された記録はない。

この照合により、旧21件を一括した「authority read cost」ではなく、次の三つを分けられる。

1. 未取得のpath-local instructionを読む正常経路。
2. 既にmodel-visibleなroot instructionを再取得する経路。
3. authority本文を取得せず、失敗結果も後続判断へ使わないprobe経路。

## command単位のroute分類

本文readとは別に、21件で使われたlocatorとprobeをcommand単位で分類した。一つのrunが複数区分へ入るため、件数は合計21にならない。

| command route | run数 | 代表形 | 判定 |
|---|---:|---|---|
| target subtree locator | 5 | `find tests -name AGENTS.md` | target既知時のbounded locator。正常経路候補 |
| repository locator | 6 | `rg --files -g AGENTS.md` | rootとpath-local候補を列挙。root再読へ進まない限り直ちに不要とはいえない |
| parent-wide locator | 6 | `find .. -name AGENTS.md` | target ancestor chainより広い探索。最適化候補 |
| root本文read | 6 | `sed ... AGENTS.md` | 全件で開始時点から同じC147本文がmodel-visible。重複取得 |
| path-local本文read | 17 | `sed ... tests/AGENTS.md` | 開始時点では未取得。保持する正常経路 |
| hidden control probe | 5 | `.agents / .codex`の`find / rg` | うち2件は本文readなし、`exit 2`後も結果を使わず変更へ進行 |

discovery-only 2件ではprobe resultがいずれも`exit_code=2`だった。直後の変更判断は、開始identity、clean status、対象testの既存helperと隣接書式だけを根拠にしており、probe失敗をmethod、constraint、permissionまたはstop conditionへbindしていない。したがって、この2件は「探索したがauthorityを取得できなかった」だけでなく、保存trace上でresult effectを持たなかった失敗probeである。

## ADR9での変更軸観測可能性

現行系列の最初の試験はADR9でなければならないため、Candidate147 ADR9 r2 N=50の保存済み450 runも同じ条件で再監査した。

| case | root `AGENTS.md`再取得run |
|---|---:|
| ADR01 | 13 / 50 |
| ADR02 | 7 / 50 |
| ADR03 | 16 / 50 |
| ADR04 | 11 / 50 |
| ADR05 | 15 / 50 |
| ADR06 | 14 / 50 |
| ADR07 | 13 / 50 |
| ADR08 | 10 / 50 |
| ADR09 | 12 / 50 |
| 合計 | 111 / 450 |

111 runに対応する112 taskでroot本文readを確認した。1 runではrootとchildの両taskが同じ本文を読んでいた。112 / 112 taskすべてで、read前のmodel-visible inputにC147の`SPEC`冒頭を含むroot本文が存在した。したがって、H1の再取得軸はF06だけの局所挙動ではなく、ADR9全9ケースで直接観測できる。

一方、H1だけを変えるC147直接childは、ADR9の既知のreview品質失敗を変更対象にしない。C147 ADR9 r2 N=50はScore `4 / 1 = 161 / 289`である。H1試験をADR9で品質通過させる目的でreview制御も同じCandidateへ入れると、重複取得とreview completionの二つの因果軸を混ぜる。H1単独CandidateがADR9を通過しない状態では、現行順序によりStandard14を開始できない。

このため、新prompt setの作成許可はあるが、現時点では作成・発行しない。これはH1が観測不能だからではなく、現行のADR9先行gateではH1単独効果の品質gateを分離できないためである。保存済み111件は再現した誤経路として保持し、別軸を混ぜずに評価できる条件が成立するまで`optimization_hypothesis / isolated_prompt_trial_not_ready`とする。

## 旧指標の定義

保存済み`analyze_f06.py`は、command文字列へ次の正規表現が一致する数を`authority_lookup_count`としていた。

```text
(?:^|[/ ])(?:AGENTS\.md|\.agents)(?:$|[/ '\"])
```

この定義には次が同じ一件として入る。

- `sed ... tests/AGENTS.md`
- `sed ... AGENTS.md`
- `find .. -name AGENTS.md`
- `rg --files -g AGENTS.md`
- `find .agents ...`
- `.agents / .codex`の存在probe

したがって、旧結果の「authority追加read」は厳密には「authority関連文字列を含む追加command」であり、全件がreadでも、全件が不要探索でもない。

## 21 runの分類

### path-local instructionだけを含む13件

```text
017b2a48a583469a93fcbac170c39243
86da43cbf056475586fd32d0dc348c66
c3a3f5e0b79d4fbd829b0f56927c0b77
39cf89a927d84fb985b4f9bd081e5716
4a8cf10f968e4c2fb4d7ec33e4e90de2
68bb7bb9461c4bfea6650f9d750f8da9
707cbe4b447444b3b1ddbf15596638db
905ad91436234e869f18545e7697beb9
aa1f399efd3047218bc1a1c3ea9e348c
af00a4f24e9e404c842508b563a9fcf0
bcfc01ec79ee46bd8eaecf11a9bd2fdc
c4d44f7455344d9e9e26ae2e65ee15e8
f61861f9791e4df7bbd7d19fdaf05215
```

この群には直接`tests/AGENTS.md`を読むrouteと、`find / rg`で適用instructionを特定してから読むrouteがある。両者を同じcostとして扱わず、instruction readとlocator探索を分ける必要がある。

### path-local instructionとroot instructionの両方を含む4件

```text
6bc464bb67884f4596a9016ac8a13b00
f5d4eb04653b44d7ace28b946ca0bee5
fd93c915ee7d4999aa7507e4027743f7
de1838ec43334d3e9a074d0bf4039f70
```

path-local instruction readは正常経路候補である。root再読の必要性は、実行時にroot instructionが既にmodel-visibleだったか、read resultがmethod、constraintまたはstop conditionを変えたかを別に判定する必要がある。

### root instructionだけを含む2件

```text
e022a52863dc48deb78ba799af3bdafb
b4df8039cd484b32b5209cc6ee29682b
```

この2件はpath-local `tests/AGENTS.md`を読んでいないため、単純に「authority確認が多い安全側route」とも評価できない。root再読を削減対象にする前に、root instructionがmodel-visible inputへ既に含まれたかを確認する必要がある。

### discoveryだけの2件

```text
707dd4ff645043d7a8c06f7526067f1c
d6a336b8667a4a35ae8b5684c2825626
```

`.agents / .codex`を探したが、command evidence上はauthority本文を読んでいない。この2件は、旧指標中で最も明確なunproductive locator route候補である。ただし2件だけを根拠に新prompt predicateは作らない。

## `EVIDENCE_GATE`との対応

C147の`EVIDENCE_GATE`は、`spec_ready=true`後にtargetへ適用中のrepository instructionを変更前evidenceとして許可する。F06のtargetは`tests/unit/test_market_units_snapshot.py`であり、`tests/AGENTS.md`はそのtargetへ適用されるpath-local instructionである。

したがって、17件のpath-local instruction readは`EVIDENCE_GATE`が誤って開いた無関係authority探索とは判定できない。現在の問題はeligibilityではなく、適用instructionを解決するlocator routeの広さと、既にmodel-visibleなinstructionの再読可能性である。

これは制御群の境界監査にも影響する。

- `SPEC × EVIDENCE_GATE`のoutcome / implementation境界を狭める根拠にはならない。
- `EVIDENCE_GATE`のallowed readからrepository instructionを外す根拠にはならない。
- 最適化仮説を作るなら、必要なinstruction readを保った`target -> applicable instruction identity`解決だけを対象にする。
- locatorを固定pathやcase固有pathへhard-codeしない。

## 現在の因果分類

| 仮説 | 判定 | 理由 |
|---|---|---|
| authority関連21 runを全て削減できる | `rejected` | 17件はpath-local instructionを読んでいる |
| `EVIDENCE_GATE`が無関係authority readを21件許可した | `rejected` | 旧指標がread、locator、root再読、probeを混合している |
| locator探索を狭められる | `optimization_hypothesis` | discovery-only 2件と広い`find / rg` routeを観測した |
| root再読を省ける | `supported_diagnostic` | root本文は21 / 21で事前可視、readした6件で新しいresult effectなし。ただしprompt変更の純便益は未評価 |
| path-local instruction readを省ける | `change_not_justified` | repository instruction遵守に必要な正常経路である可能性が高い |
| discovery-only失敗probeを省ける | `supported_diagnostic` | 2件とも`exit 2`で、後続判断へresult effectを持たなかった |
| locator commandをpromptで一意に固定する | `change_not_justified` | 境界制御ではなく方法固定になり、非対象repositoryへのspilloverが未評価 |

## 次へ進む条件

1. 正常経路を「既にmodel-visibleな有効instruction resultは再取得せず、未取得のpath-local instructionだけをtargetから解決する」と固定する。
2. 追加predicateではなく、C147の既存`EVIDENCE_GATE`内で重複取得を許す表現を狭く置換できるかを検討する。
3. command名、固定path、読取り回数をpromptへ固定せず、model-visible resultの充足と失効だけで判定できる形にする。
4. ADR9全9ケースのroot再取得111 / 450を対象経路として保持する。ただしADR9の独立したreview品質失敗をH1へ帰属させない。
5. H1単独の品質・機構gateを別軸なしで固定できるまでprompt Candidateを作らず、Standard14も開始しない。

## 参照

- [`Candidate147 制御群・境界重複・最適性監査`](c147-control-group-overlap-optimality-audit.md)
- [`Candidate147 F06 N=100結果`](../evaluations/results/candidate147-result-effect-scope-v14-medium-f06-atomic-reuse-n100-cli0146_2026-08-02.md)
- [`Candidate147 ADR9 r2 N=50結果`](../evaluations/results/candidate147-result-effect-scope-adr9-r2-n50_2026-08-10.md)
- 保存済みbehavior analysis: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate147-result-effect-scope-v14-medium-f06n100-cli0146-20260802-r1/c147-f06-n100-behavior-analysis.json`
- 保存済みanalysis script: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate147-result-effect-scope-v14-medium-f06n100-cli0146-20260802-r1/analyze_f06.py`
