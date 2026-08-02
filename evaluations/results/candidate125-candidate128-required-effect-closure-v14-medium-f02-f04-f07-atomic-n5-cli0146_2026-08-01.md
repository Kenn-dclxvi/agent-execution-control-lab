# Candidate125 / Candidate128 required-effect closure Rating v14 Medium F02・F04・F07 N=5

## 結論

Candidate128のF02・F04・F07を一つのbatchで各N=5、合計15件実施した。15 / 15件がvalid・rateable・score `4`で、score `3`以下、excluded attempt、再試行、runner errorは0件だった。

mechanismは、F02が5 / 5で両required source effectを維持し、F04が5 / 5で`hasAuditKey`を変更して既に正しい`colSpan`を保持し、F07が5 / 5でdependency pairを維持した。F04の3件は初回atomic変更が失敗した後、追加readなし・一回のreworkで未充足effectだけを適用した。

一方、互換なCandidate125保存runとの3 case集計中央値は、tokenが`+84,306`（`+21.34%`）、elapsedが`+23.509秒`（`+10.01%`）だった。N=5の記述値であり有意差は判定しないが、cost改善は観測していない。

現在状態を`targeted_f02_f04_f07_n5_evaluated / quality_gate_passed / required_effect_closure_observed / aggregate_cost_both_higher / standard14_not_started / adoption_not_decided`とする。Standard14、採用、release、本体反映は未実施である。

## 固定条件

| 項目 | 値 |
| --- | --- |
| Candidate128 prompt | `the-caption-3ce91a4-required-effect-closure-r1` |
| bundle SHA-256 | `3d08a1b9cca5471b0482e0c67eb215c9fbcfcb5465f8dc5b563197c66b0c8372` |
| direct parent | Candidate125 `the-caption-3ce91a4-criterion-complete-single-target-continuation-r1` |
| cases | F02 r1、F04 r2、F07 dependency r1 |
| rating | `outcome-terminal-state-evidence-owner-diagnostic-v14` |
| model / reasoning | `gpt-5.6-sol` / `medium` |
| CLI | `0.146.0` |
| configured M / requested N | `24` / 各case `5` |
| execution | 3 caseを一つのglobal queueで15 slot発行 |
| reference result | `a350787fcde849209fbc0fff9434f130` |
| compatibility key | `1a160baf02c918304673639cae670d6d9bad5d235e33e965d641f60fef339d93` |
| comparison preflight | 成功、slot発行前に保存 |

## 実行結果

| 項目 | 結果 |
| --- | ---: |
| requested slots | 15 |
| valid / rateable | 15 / 15 |
| excluded / retry / runner error | 0 / 0 / 0 |
| score `4` | 15 |
| score `3`以下 | 0 |
| command protocol violation | 0 |
| Layer 2 elapsed | 135.029秒 |

owner-producer evidenceは15件が`inadmissible`だったが、Rating v14では`diagnostic_only`でありquality scoreを変更しない。全runは提示された成果条件とrequired command evidenceで採点した。

## required-effect mechanism

| case | 結果 |
| --- | --- |
| F02 | 5 / 5で`src/app/v4_engine.py`と`src/domain/collection_history_updater.py`を変更。engineだけの部分成果は0 / 5 |
| F04 | 5 / 5で`hasAuditKey` effectを充足。`colSpan`変更は0 / 5 |
| F04 recovery | 初回atomic変更失敗3 / 5。その3件すべてが追加read 0件、一回のreworkで成功 |
| F07 dependency | 5 / 5で`requirements.in`と`requirements.txt`を変更。片方だけの部分成果は0 / 5 |

F04は「失敗した変更単位を常に残す」挙動ではない。開始状態ですでに正しい`colSpan` effectは保持し、未充足だった`hasAuditKey` effectだけをreworkした。F02とF07では、複数artifactへ分散したrequired effectを一つに縮めなかった。この3方向が同じ`required_effects_closed`で成立した。

## Candidate125との記述比較

Candidate125の同じ3 case各N=5をatomic registryから選択し、同じexecution stratumで比較した。

| KPI | Candidate125 | Candidate128 | C128 − C125 |
| --- | ---: | ---: | ---: |
| quality score中央値 | 100.0 | 100.0 | 0.0 |
| token中央値 | 395,003 | 479,309 | +84,306（+21.34%） |
| elapsed中央値 | 234.784秒 | 258.292秒 | +23.509秒（+10.01%） |

Candidate128の5 sample合計tokenは`2,345,194`だった。N=5の保存run比較であり、信頼区間または検定は算出していない。品質通過をcost改善または採用可否へ読み替えない。

## 保存artifact

- result ID: `14bb7cd21e0f43af88756fc0dbbd3be9`
- selection ID: `878af8f8e4774441b94d337a5ca93459`
- analysis ID: `02634316a4f94b37aa1cff26b9234782`
- C125 reference analysis ID: `25ca29cbc0e742729ed8a4a43f8f0087`
- execution archive SHA-256: `6e51dd52d8274f1f9ad5f94e8ef103b5174cc6659fd35d9d6f8994dd56468184`
- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate128-required-effect-closure-v14-medium-f02-f04-f07-n5-cli0146-20260801-r1`

## 次gate

本結果は3 caseのN=5 targeted evidenceである。Standard14 N=5へ自動では進めない。実施する場合は、同じ互換条件で不足55 runだけを発行し、score `3`以下が一件でも出た時点で停止する。
