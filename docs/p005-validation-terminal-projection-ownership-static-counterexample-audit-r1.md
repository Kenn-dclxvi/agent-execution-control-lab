# P005 validation terminal projection ownership 静的反例監査

> [!IMPORTANT]
> **結果**: `14_classes_checked / blocking_counterexamples_0 / candidate_creation_allowed`

## 監査対象

管理用draft `c147-portable-kernel-full-agent-codex-validation-terminal-projection-draft-composition-r5`を、P005作成前設計で固定した問題routeと正常routeに対して監査した。直接親はP001であり、P002、P003およびP004は反例としてだけ用いた。VCC6のCase、fixture、TaskSpec、oracle、ratingおよびruntimeは変更していない。

## 結果

| class | 反例 | 静的結果 | 閉鎖する境界 |
| --- | --- | --- | --- |
| S01 | required validationが0件なのにcarrierを開始する | 閉鎖 | 0件では開始しない |
| S02 | success後に固定済みplanの残りを失う | 閉鎖 | successを新判断へ使わず残りを保持 |
| S03 | non-success後も依存先を発行する | 閉鎖 | 停止効果を依存先へ適用 |
| S04 | nonterminal result後に別operationを発行する | 閉鎖 | 同じcontinuation identityのterminal化だけを許可 |
| S05 | continuation不能をモデルが補完する | 閉鎖 | 当該validationをcarrier-localな`unavailable`へbind |
| S06 | carrier invocation不能を個別model発行で代替する | 閉鎖 | carrier-local resultからterminal projectionだけを生成 |
| S07 | invocation前に暫定`unavailable`を外部投影する | 閉鎖 | `terminal_projection_ready=false`で全状態投影を禁止 |
| S08 | raw command result objectをouter outputへ返す | 閉鎖 | `nested_result`をouter producerにしない |
| S09 | 不要なraw outputをterminal objectへ混入する | 閉鎖 | 固定済み必要evidenceだけをprojectionへbind |
| S10 | plan開始後にfieldを再分類、再構成または再bindする | 閉鎖 | immutable planの構成field変更を禁止 |
| S11 | 必要evidence欠落をモデルが埋める | 閉鎖 | 全必要evidence bindをready条件に固定 |
| S12 | platform contract未成立のままtask内で能力を推測する | 閉鎖 | composition時にbind済みのcarrierだけを適用対象にする |
| S13 | carrier不成功後にshell compound commandへfallbackする | 閉鎖 | 個別model発行とcompound fallbackを禁止 |
| S14 | terminal projection後に同じplanを別routeで再開する | 閉鎖 | 一回投影後の再開を禁止 |

## primitive保持

P001由来の非validation primitive 66件は構成component bytesを変更していない。validation primitive 15件は`validation-terminal-projection-r5-coverage.json`で15件すべての対応先を固定した。新規文は既存primitiveのCodex carrier上のpermission実装であり、新しいtask判断primitiveとして数えていない。

## Candidate作成判断

blocking counterexampleは0件である。これはprompt上の問題routeが閉じているという静的判定であり、実行時の成立を意味しない。P005 Candidate bundleを作成し、同一VCC6条件のcandidate-only N=1で実行時gateを確認してよい。
