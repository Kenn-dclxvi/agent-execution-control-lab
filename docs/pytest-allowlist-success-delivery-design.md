# Pytest allowlist success delivery 第1版

## 結論

成功result全体を一律に抑制しない。Std14の保存済みC81 70 runで成功出力の`99.92%`を占めたpytest系だけを、exact argvとcaseへbindしたadapter wrapperの対象にする。TaskSpec、Candidate81 prompt、case、rating、model、reasoning、M / Nは変更しない。

履歴済み[`success-delivery/v1`](success-silent-delivery-design.md)はAIがcode localに成功rawを保持するprotocolだった。本revisionは`success-delivery/v2`として、対象commandの実行、成功raw保存、成功receipt生成、失敗raw返却を[`success_silent_command.py`](../scripts/success_silent_command.py)へ移す。

## Std14 command調査

保存済みCandidate81 Std14 70 runの固定required validationは7 case、各5回、実command 80件だった。

| command分類 | 実行回数 | 成功出力 |
| --- | ---: | ---: |
| pytestとpytestだけを起動する`main_verify.sh` | 45 | `4,337,669 bytes` |
| Node validation | 15 | `3,435 bytes` |
| `bash -n`、static assert、`git diff --check` | 15 | `0 bytes` |
| `git diff --name-only` | 5 | `165 bytes` |

第1版はpytest系だけを対象にする。Node validationは削減量が小さいため入れない。成功出力が0 bytesのcommandは効果がないため入れない。`git diff --name-only`、`git status --short`、`git diff`、source readは内容が判断材料なので対象外とする。

## Executor boundary

profileはcaseごとに次を固定する。

- exact argv
- required command group index
- `pytest`または`pinned_pytest_wrapper`のkind
- wrapper scriptを使う場合はrepository-relative pathとSHA-256

shell substringでは判定しない。`&&`、`;`、pipe、redirect、改行を含むargvはprofile parse時に拒否する。allowlist外commandをsuccess wrapperへ渡した場合は、実行前にexit code `64`で拒否する。

allowlist commandの成功時は、raw stdout / stderrをadapter localへbyte単位で保存し、modelへはcommand argv、exit code `0`、evidence IDだけを返す。nonzero時はchild commandのstdout、stderr、exit codeを変更せず返す。raw evidenceはstreamごとのbyte数とSHA-256で監査する。

## F02 N=5 gate

[`F02 profile`](../evaluations/profiles/candidate81-pytest-allowlist-success-delivery-v14-reasoning-medium-f02-global-m5-n5-r1.json)は履歴済みv1 profileから`profile_id`と`success_delivery`だけを変更する。

- quality: 5 / 5 score `4`
- exact allowlist: focused pytestとpinned `main_verify.sh`を各run 1回
- local raw evidence: 各run 2件、argv・exit code・byte数・SHA-256一致
- model-visible success output: raw pytest markerなし、4,096 bytes以下
- failure boundary: stdout、stderr、exit codeの同値probeがpass
- KPI: all-agent token中央値と合計、elapsed中央値と合計をv1およびsealed controlへ併記

F02はwrapper transportと保存機構の確認であり、Std14への一般化ではない。F02成立後も、F06でfocused pytestとdirect full pytestの組を確認してからStd14を判断する。A02の可変pytest commandとNode validationは本revisionへ含めない。

## F02結果

2026-07-29の[`F02 N=5 result`](../evaluations/results/candidate81-pytest-allowlist-success-delivery-v14-medium-f02-n5_2026-07-29.md)は5 / 5 score `4`、exact allowlist mechanism 5 / 5、local raw evidence failure 0件だった。5 runでraw `915,395 bytes`をadapter localへ保持し、validationのmodel-visible bytesは合計`5,525`、raw markerは0件だった。

instruction-based v1比のall-agent tokenは中央値`-8.65%`だったが、合計は`+1.87%`だった。機構成立と品質維持は確認したが、token総量削減は未確認である。次はF06だけを対象にし、F06成立前にStd14へ進めない。

## F06結果

同日の[`F06 N=5 result`](../evaluations/results/candidate81-pytest-allowlist-success-delivery-v14-medium-f06-n5_2026-07-29.md)は、focused pytestとfull pytestのexact allowlistを5 / 5 runで成立させ、5 / 5 score `4`を維持した。raw `896,030 bytes`をadapter localへ保持し、validationのmodel-visible bytesは合計`4,802`、raw markerは0件だった。

F06のall-agent tokenは中央値`179,199`、合計`829,560`、elapsedは中央値`91.509`秒、合計`431.612`秒だった。同じruntime・TaskSpec・Ratingで`success_delivery`だけを外したmatched controlは未取得である。F02もv1比token合計の削減を示していないため、Std14へ進む前にF06 matched controlを取得する。

## F06 matched control結果

後続の[`F06 executor A/B`](../evaluations/results/candidate81-success-delivery-executor-ab-v14-medium-f06-n5_2026-07-29.md)は、control / treatmentとも5 / 5 score `4`だった。treatmentはmodel-visible result bytesを中央値`-67.33%`、合計`-64.47%`へ減らしたが、tokenは中央値`+41.76%`、合計`+22.29%`、elapsedは中央値`+25.94%`、合計`+7.63%`だった。model再入も中央値`4 → 7`、合計`22 → 31`へ増えた。

output削減とcost削減は分離した。model-visible wrapper方式は`cost_control_failed`として停止し、Std14へ進めない。再開条件は、modelにwrapper選択を要求せず元commandをexecutor側で透過interceptできる別revisionの実装可能性が確認できた場合だけとする。

## 透過interceptionの実装境界

現行`run_codex_evaluation.py`はCodexをopaque subprocessとして起動し、完了後のJSONLを監査する。adapterからcode mode内のnested `exec_command`を直接interceptするhookはない。このため、現在のv2はexact wrapper invocationをmodel-visible taskへ追記していた。

一方、`.venv`は各runでadapterが`venv_shim`として生成する管理対象である。元の`.venv/bin/python -m pytest ...`を変えずに扱う次の候補点は、このruntime shimである。ただし、pytest以外のPython invocationを完全透過で実行すること、exact argvだけを抑制すること、nonzero・signal・permission・runtime identityを維持することをfail-closed unit testで確認するまでは「実装可能」と確定しない。v2の文面短縮やreceipt短縮は次revisionにしない。

2026-07-29のruntime shim unit probeでは、元の`.venv/bin/python`をlauncherへ置換し、元interpreterをdelegateへ移す方式を確認した。exact argvの識別、成功rawのlocal保存、成功receipt、nonzero / signalの透過は成立した。一方、allowlist外のPython invocationで`sys.prefix`は一致したが、`sys.executable`が`.venv/bin/python`から内部の`.venv/bin/python.codex-delegate`へ変化した。macOSの`__PYVENV_LAUNCHER__`を明示した追試でも差は解消しなかった。

この差を`.pth`や`sitecustomize.py`で上書きすると、allowlist外のPython startupとmodule resolutionへ新しい介入を追加するため、「対象外commandは完全透過」というgateを満たさない。したがってruntime shim案は`stopped_before_profile / runtime_identity_failed`とし、v3 profileとN5は作成しない。再開条件は、Codex subprocessの内側で元commandのtool result deliveryだけをinterceptでき、command pathとtarget runtimeを置換しないexecutor hookが利用可能になった場合とする。

同日時点のCodex CLI `0.146.0`も確認した。`hooks` featureはstableで`PreToolUse` / `PostToolUse`を持つが、local binaryのhook contractは`PostToolUse`の`suppressOutput`とtool output更新をunsupportedとして拒否する。現行hookはfeedbackや停止判断の境界であり、shell command成功resultをmodel投入前にreceiptへ置換するdelivery境界ではない。したがって現行CLI上に再開条件を満たす公開hookはない。
