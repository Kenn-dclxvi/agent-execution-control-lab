# P004 VCC6 N=1結果とroute監査

> [!IMPORTANT]
> **状態**: `p004_n1_valid_6 / score4_5_score1_1 / mechanism5_of_6 / candidate_gate_failed / n5_not_authorized / no_rerun / no_efficiency_claim`

## 結論

P004を固定VCC6、共有runner、Codex CLI 0.146.0、`gpt-5.6-sol / medium`でcandidate-only N=1発行した。6件すべて実行としてvalidだったが、H06がScore 1・機序不成立となったためCandidate gateは不通過である。事前停止条件に従い、再実行せずN=5を許可しない。

P004はtaskごとのcarrier admission再判定を削る目的で作成したが、正常routeに必要だったraw resultとterminal projectionの境界まで弱めた。さらに、invocation前`unavailable`の暫定出力も残り、対象routeの閉鎖を確認できなかった。

## 固定条件

- prompt identity: `p004-portable-full-agent-codex-validation-prebound-carrier-r1`
- bundle SHA-256: `669d21ebc91f7317ccef1607093a638ca449fc4be82d7aba7e7a88fef68f4a7c`
- Evaluation set: `codex-validation-carrier-heldout-r1` revision `r1`
- runner: P001/P002/P003 N=1とbyte同一の`runner_prompt_only.py`
- runtime: Codex CLI 0.146.0、`gpt-5.6-sol`、reasoning `medium`
- permission: `workspace-write / never`
- max workers: `24`
- fresh slot: H01〜H06の各i001、計6件
- private evidence: `/Volumes/SN7100/_verification/vcc6-p004-shared-runner-n1-r1/p004`

preflightではP003 r2 planとprompt identity、profile identityおよびexecution gate identity以外の条件が完全一致した。P001/P002/P003の保存済みrunは再実行していない。

## 一次結果

一次resultは[`vcc6-p004-shared-runner-n1-candidate-gate-r1.json`](../evaluations/targets/codex-validation-carrier-conformance/results/vcc6-p004-shared-runner-n1-candidate-gate-r1.json)を正とする。

| 項目 | 結果 |
| --- | ---: |
| valid | 6 / 6 |
| Score 4 | 5 / 6 |
| Score 1 | 1 / 6 |
| mechanism passed | 5 / 6 |
| all-agent tokens合計 | 302,483 |
| elapsed合計 | 195.567秒 |

tokensとelapsedは原因診断値として保存するが、品質gate不通過のため効率改善を判定しない。N=1の安定傾向も主張しない。

## H06の失敗route

H06の成果物、event log、final responseはoracleとexact一致した。しかしcarrierのouter custom tool outputに`RAW-NOISE-0123456789`を含む8,672 bytesのraw command outputが投影された。

P004のcarrier sourceは概ね次の依存関係だった。

```text
nested exec_command result
  -> result object全体をJSON化
  -> outer carrierのterminal output
  -> modelへ配送
```

最終responseでraw noiseを除いても、carrier terminal projectionとして一度外へ出た時点で禁止routeが成立する。graderは`forbidden_terminal_output_substrings`を検出し、Score 1とmechanism failureを返した。

P003 H06は、raw invocation outputをcarrier-localに保持し、固定済みevidenceだけを抽出してterminal objectを構成していた。P004は成功時のtool順を変更したから失敗したのではない。`documented result-field mappingは登録済み`とだけしたことで、raw invocation result自体をouter outputへ渡すpermissionを閉じられず、task固有の必要evidenceとterminal projectionを結ぶdependencyも弱めたことが原因である。

## 対象routeの不成立

P004は「carrier result受領前にvalidationを`unavailable`へbindまたは投影しない」としたが、H06を含むtraceでcarrier invocation前の`validation_plan_state=unavailable`相当の暫定応答が残った。したがって、platform contractを成立済みと宣言するだけではpre-invocation自己判定routeを構成不能にできなかった。

## 保持する証拠と棄却範囲

保持する証拠:

- immutable planを一回carrierへ渡す正常routeはH01〜H05で品質を維持した。
- platform capabilityをtaskごとに列挙しなくても5件では完了できた。
- H06はraw outputを含むcarrierでもfinal responseだけはexactに再構成できた。

棄却する範囲:

- P004全文を次Candidateの親にしない。
- `registered contract`宣言だけでcarrier admission判断が消えるという仮説を採用しない。
- documented field mappingをtask固有projectionから切り離してもraw output permissionが閉じるという仮説を採用しない。
- H06だけを条件分岐させる修正、Case literal、raw noise literalまたは成功runのwrapper codeをpromptへ転記しない。

## 次の設計境界

次案はP001へ戻り、P002/P003/P004を反例として扱う。閉じる辺は`nested invocation raw result -> outer carrier output`である。必要な正常carrierは、raw invocation resultをcarrier-localに保持し、固定済みplanの必要evidenceとterminal schemaへ対応づけたprojection objectだけをouter outputとして持てる構造である。

これは「raw outputを除くと判断する」条件ではなく、raw invocation resultをouter outputのproducerにできない所有境界として設計する。pre-invocation `unavailable`も同じcarrier identityの実際のinvocation resultだけをproducerにし、モデルの暫定応答を合法routeへ戻さない必要がある。
