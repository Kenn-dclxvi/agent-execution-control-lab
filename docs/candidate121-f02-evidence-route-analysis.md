# Candidate121 F02 evidence route分析

## 結論

Candidate121のF02 cost未達は、変更前tool resultのbytesだけでは説明できない。Candidate121は変更前evidence bytes中央値をCandidate118の`110,667`から`41,410`へ減らし、Candidate107の`53,938`も下回ったが、token中央値は`209,379`でCandidate107の`173,000`を上回った。

Candidate121で新しく増えた共通差は、locator identityを一度modelへ返してからcontent spanを読む二段階routeである。変更前evidence invocation数中央値はCandidate107 `6`、Candidate118 `3`、Candidate121 `5`で、Candidate121のagent message数中央値はCandidate107 / Candidate118の`5 / 5`に対して`6`だった。ただしCandidate121の最高token runは変更前evidence invocationが2件だけである。したがってinvocation数だけでも高costを一意に説明できない。

現時点で支持される次仮説は、bytes上限またはtarget cardinality制限ではなく、TaskSpecが同じpredicateへ使うexact target setをすでに列挙している場合に、locatorを独立resultにせず一つの変更前evidence waveへまとめ、そのterminal resultを`edit-ready`または`stop`にする境界である。ただしこの仮説はCandidate50の一般read batchingと区別し、明示target setかつ同一predicateの場合だけに限定する必要がある。まだCandidateは作成していない。

## 対象と方法

同じF02 r1、Rating v14、Medium、CLI `0.146.0`の保存済み各`N=5` traceをread-onlyで比較した。

- Candidate107: `the-caption-3ce91a4-validation-wrapper-reentry-closure-r1`
- Candidate118: `the-caption-3ce91a4-implementation-bind-terminal-closure-r1`
- Candidate121: `the-caption-3ce91a4-evidence-request-scope-closure-r1`

各runについて、最初のartifact変更より前に対象2 source / 2 testを参照したcommandを抽出し、次を数えた。

- all-agent `total_tokens`
- 変更前evidence invocation数
- 変更前evidenceのmodel-visible result bytes合計
- 最初のevidence invocationが参照したtarget数
- agent message数
- required validation発行数

identity確認だけの`pwd` / `git branch` / `git rev-parse` / `git status`は変更前evidence数とbytesから除いた。bytesは保存済み`codex-events.jsonl`の`aggregated_output`をUTF-8で数えた診断値であり、KPIではない。

## 変更前evidence

| Candidate | run | token | evidence invocation | result bytes合計 | 最初のtarget数 |
| --- | --- | ---: | ---: | ---: | ---: |
| C107 | `731d14e200784e5ba521056f3f5abfa6` | `194,683` | 6 | `91,259` | 1 |
| C107 | `bb092cd5c5fc4e4ba20f0990a5b0bc4c` | `172,171` | 7 | `53,938` | 1 |
| C107 | `d7ad0e2310c74bb88555bf9fc0f9b647` | `173,000` | 8 | `57,531` | 1 |
| C107 | `ccc2c68199e54d5687a69815f7408d4e` | `135,285` | 1 | `47,137` | 4 |
| C107 | `005ef1dc17054b10b58581395571332c` | `178,704` | 5 | `53,929` | 1 |
| C118 | `15e74962acec49589ebb34087d63a1c1` | `274,832` | 5 | `116,911` | 4 |
| C118 | `182a70d8584149e5adf43424bc1b2f38` | `235,508` | 8 | `55,380` | 1 |
| C118 | `a93fe98b6581410aa77624390b34ba8b` | `172,226` | 2 | `75,758` | 4 |
| C118 | `b76c0e2e823b4cfa96996a6afba306c6` | `256,931` | 2 | `110,667` | 4 |
| C118 | `c0ce1ae776a44891a8802480dbefcae0` | `281,631` | 3 | `117,059` | 4 |
| C121 | `8222db2db0a640eab42abeb4f4b88df5` | `209,379` | 6 | `31,585` | 4 |
| C121 | `748f28d315a546f4b132474055170b76` | `173,130` | 5 | `42,065` | 4 |
| C121 | `6ef5c387ca1c4992b6ae5dfc1dc83eef` | `171,805` | 6 | `32,285` | 1 |
| C121 | `d777cb47eaa44889aeec568aa94d030f` | `260,556` | 2 | `41,410` | 4 |
| C121 | `e31a84e02c894747a73d4127e5b7d7d6` | `212,712` | 5 | `43,657` | 4 |

中央値は次のとおりである。

| Candidate | token | evidence invocation | result bytes合計 |
| --- | ---: | ---: | ---: |
| C107 | `173,000` | 6 | `53,938` |
| C118 | `256,931` | 3 | `110,667` |
| C121 | `209,379` | 5 | `41,410` |

## 分かったこと

1. result bytes削減だけではC107水準へ戻らない。C121は3条件で最小bytesだが、tokenはC107より`21.03%`高い。
2. 最初のtarget cardinalityだけでは分かれない。4 targetを最初に読んだrunにはC107の最小`135,285`、C118の低値`172,226`、C118 / C121の高値が共存する。
3. evidence invocation数だけでも分かれない。Candidate121の最高値`260,556`は変更前evidence 2件で、低値`171,805`は6件だった。
4. Candidate121は巨大な`rg -C` resultを消したが、locator resultを独立に受領してcontentへ進むdecision roundを追加した。agent message数中央値はC107 / C118の5から6へ増えた。
5. Candidate121のfull validation再発は1 / 5件だけで、そのrunは`209,379`だった。最高値`260,556`では再発していないため、validation再入も今回のF02中央値未達の単独原因ではない。

## 次候補を作る条件

次の変更軸候補は`prechange evidence wave closure`である。

- TaskSpecがexact target setを列挙済みである。
- 全targetが同じ未解決predicateを共同で決める。
- このときlocatorを独立terminal resultにせず、一つのcontent evidence waveへまとめる。
- そのwaveのterminal resultで変更predicateをbindできれば直ちにartifact変更へ進む。
- bindできなければ、具体的な不足または矛盾を示して停止する。一般的な追加探索は開かない。

これは「常にreadをbatchする」Candidate50とは異なる。適用条件をexact target setと同一predicateへ限定する。A02ではrepositoryからcanonical implementationを解決するためtarget setが未確定なので、このfast pathを適用しない。

ただし同じ外形routeでもtokenの高低が残るため、現時点では効果確実とは言えない。Candidateを作る場合は、C119を直接親とし、C121のlocator-identity必須条件は継承しない。初回gateはA01 / A02 / F01 / F02各`N=5`で、A02の二つのclosure、F02のone-wave route、品質、F02 token `173,000`以下を同時に要求する。
