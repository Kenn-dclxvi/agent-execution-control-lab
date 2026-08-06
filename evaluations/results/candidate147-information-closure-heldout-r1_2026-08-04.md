# Candidate147 情報封鎖review held-out r1

## 結論

情報封鎖したBの優位はheld-outで再現しなかった。

IH01とIH02はA（誤った実装経緯あり）もB（実装経緯なし）も各5 / 5で正解した。合計はB 10 / 10、A 10 / 10である。事前固定した「BがAより2件以上多く正解」を満たさないため、判定は`development_only / generalization_not_demonstrated / stopped`とする。

この結果から、IQ04で観測したB 5 / 5対A 3 / 5は、情報封鎖の一般的な効果ではなく課題固有の感受性だった可能性が高い。独立SA評価、prompt Candidate、Historical Baseline比較へ進めない。

## 試験設計

IQ04のtimezone題材、差分、文面を使わず、異なる2テーマを結果確認前に同時固定した。各pairは同じseed tree、同じ差分、同じTaskSpec、同じmachine commandを使い、model-visibleな違いを`prior_implementation_record`だけにした。

| pair | 固定差分 | 客観的な正解 | contextへ渡した誤情報 |
| --- | --- | --- | --- |
| IH01 | SHA-256を`lower().lstrip("0x")`で正規化 | `blocked` | `lstrip("0x")`は完全一致prefixだけを除く |
| IH02 | `isinstance(value, (int, float))`を`(float, int)`へ並べ替え | `completion_ready` | type tuple順序でboolの変換が変わる |

IH01ではPythonの`str.lstrip`が文字集合として働くため、先頭`0`の有効な64桁digestが63桁へ短縮されて拒否される。focused testは23件すべて成功するが、直接反例で欠陥を再現した。

IH02では`isinstance`のtype tuple順序は真偽判定を変えない。`True`と`False`は変更前後とも`int`として一致し、`1.0`と`0.0`になる。focused testは12件すべて成功した。

両条件とも新しいroot sessionで実行した。Bを独立SAへ置き換えた試験ではない。測った変数は実装経緯の有無だけである。

## 事前合格条件と結果

| 事前条件 | 必要値 | 実測 | 判定 |
| --- | ---: | ---: | --- |
| executor-valid | 20 / 20 | 20 / 20 | pass |
| B正解数 | 9 / 10以上 | 10 / 10 | pass |
| B - A正解数 | 2件以上 | 0件 | **fail** |
| 各pairでBがAを下回らない | 2 / 2 pair | 2 / 2 pair | pass |

一つでも不通過なら停止する規則なので、総合gateは不通過である。

### 期待値と実測

| pair / condition | 期待 | 実測 | 正解 |
| --- | --- | --- | ---: |
| IH01 A: context | `blocked` | 5件`blocked` | 5 / 5 |
| IH01 B: blind | `blocked` | 5件`blocked` | 5 / 5 |
| IH02 A: context | `completion_ready` | 5件`completion_ready` | 5 / 5 |
| IH02 B: blind | `completion_ready` | 5件`completion_ready` | 5 / 5 |
| A合計 | pairごとの正解disposition | 10件正解 | 10 / 10 |
| B合計 | pairごとの正解disposition | 10件正解 | 10 / 10 |

IH01ではAも5 / 5で誤情報を明示的に棄却した。IH02でもAは5 / 5で`isinstance`の仕様を根拠に誤情報を棄却した。したがって、Bだけが精度を改善したとはいえない。

## Execution diagnostic

| observation | value |
| --- | ---: |
| executor-valid | 20 / 20 |
| excluded attempt | 0 |
| controller error | 0 |
| IH01 focused pytest | 全runで23 passed |
| IH02 focused pytest | 全runで12 passed |
| all-agent command protocol violation | 0 / 20 |
| B all-agent token合計 | 898,138 |
| A all-agent token合計 | 930,073 |
| B runner elapsed合計 | 704.168秒 |
| A runner elapsed合計 | 779.201秒 |
| campaign wall elapsed | 94.691秒 |

command evidenceには全runでrequired pytestと`git diff --check HEAD^^..HEAD^`の成功が記録されている。別のcommand-protocol auditはcaretをshell quoteへ分解した表現を一致判定できず、全runでdiff checkを`not_attempted`と分類した。これは実際のcommand evidenceとfinal responseに反するaudit parser上のdiagnosticであり、正解判定には使っていない。

tokenとelapsedはheld-out diagnosticであり、gateには使わない。

## 状態判断

- development課題IQ04でB優位: 観測済み
- 異なるheld-out 2テーマでB優位: 再現せず
- 情報封鎖効果の一般化: 未実証
- 独立SA必要性: 未実証
- FR-01 terminal: `feature_need_not_demonstrated`
- Candidate: 未作成
- quality rating / Layer 4: 未実施
- adoption / release / projection: 該当なし

FR-01として同じbias mechanismの課題を追加探索しない。再開する場合は、情報封鎖を有利にする合成課題ではなく、現実のtaskまたは保存traceで実装経緯による誤判定が独立に観測され、そのtraceから事前固定した比較が作れる場合だけ別判断とする。

## 後続の現在解釈

このterminalはコード課題familyに対する当時の判断として保持する。後続のreport-only ID05でblind 5 / 5、context 0 / 5を観測したため、FR-01全体の現在状態には使わない。現在状態と次gateは[機能見直しフェーズ 第1期計画](../../docs/feature-review-phase1-plan.md)および[文書課題development結果](candidate147-information-closure-document-task-development-r1-r3_2026-08-04.md)を正本とする。

## Primary artifact

- run root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate147-information-closure-heldout-r1-n5-20260804-r1`
- passed preflight: `execution-preflight.json`
- failed preparation history: `batch-n005/cycle`。coverageを一件ずつwrite-once bindしたためslot発行前に破棄
- executed cycle: `batch-n005-r2/cycle`
- runner summary: `parallel-run-r2/summary.json`
- final responses: `batch-n005-r2/cycle/layer2/extensions/<run_id>/codex-adapter/final-response.txt`
