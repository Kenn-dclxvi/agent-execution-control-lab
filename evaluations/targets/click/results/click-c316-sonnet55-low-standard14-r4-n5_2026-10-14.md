# Click C316 Sonnet 5.5 low Standard14 r4 N=5

## 結論

THE-CAPTIONでリリースしたC316を改変せずにClickのrootへ置き、Click Standard14 r4をClaude Code（Sonnet 5.5、推論low）で5回ずつ測った。保存済みの[制御なしの基準](click-free-sonnet55-low-standard14-r4-n5_2026-10-14.md)と同じ単価表で比べると、品質と経過時間は基準の幅より良く、費用は基準の幅より上だった。

| 指標 | 基準の中央値（幅） | C316の中央値（幅） | 差 | 差（%） | 基準の幅に対する位置 |
| --- | ---: | ---: | ---: | ---: | --- |
| 品質（0〜100） | 92.86（92.86〜92.86） | 100.00（94.64〜100.00） | +7.14 | +7.69% | 幅より上 |
| 費用（USD） | 0.4489（0.4188〜0.4854） | 0.5233（0.5093〜0.5406） | +0.0744 | +16.57% | 幅より上 |
| 経過時間（秒） | 274.36（262.07〜322.36） | 234.65（229.45〜250.31） | −39.72 | −14.48% | 幅より下 |
| 生のトークン（参考） | 711,090（702,295〜775,095） | 701,045（675,976〜738,829） | −10,045 | −1.41% | 幅より下 |

- **品質**：A01は5件とも確認して停止し（`awaiting_required_value`）、基準の0 / 5から5 / 5へ変わった。THE-CAPTIONと同じく、結果が確定しないまま作業を始める失敗を抑えた。一方、F06の1件が主要成果を作らずに終わり、score `1`となった（下記）。点数の分布は4点69件、1点1件である。
- **費用**：A01は−48.8%だったが、ほかの13ケースはすべて増え（+5.9%〜+76.6%）、合計で+16.57%となった。増加の中心は、どのケースでも1回あたり約2,000〜2,400トークン増えたキャッシュ書き込み（1時間）である。作業量に関係なく毎回かかる固定の負担で、Clickでは1件あたりの費用が小さいため、A01の削減を上回った。
- **経過時間**：14ケースのうち12ケースで短くなった。

THE-CAPTIONのSonnet lowでは、Free比で費用−11.17%、経過時間−6.62%だった（[リリース記録](../../../../prompts/releases/the-caption-3ce91a4-receive-form-file-read-range-release-r1/README.md)）。品質面の効果はClickでも再現したが、費用の削減は再現しなかった。

## 固定条件

- 評価セット：[`click-standard14-r4`](../sets/click-standard14-r4/README.md) / `r4`
- プロンプト：[`click-00e592c-receive-form-file-read-range-r1`](../prompts/candidates/click-00e592c-receive-form-file-read-range-r1/manifest.json)（bundle SHA-256 `78546c434411c0450974f4757edc8bf013ae56e21f3cbebe32ee330e25ae6b74`）。THE-CAPTION C316のroot `AGENTS.md`と、それを指すroot `CLAUDE.md`のリンクを、バイト単位で同一のまま置いた（[設計記録](../../../../docs/click-c316-portability-design.md)）
- プロファイル：[`c316-click-claude-sonnet55-low-standard14-r4-n5-cli2288-shellenv-20261014-r1`](../profiles/c316-click-claude-sonnet55-low-standard14-r4-n5-cli2288-shellenv-20261014-r1.json)
- モデル / 推論 / Agent：`claude-sonnet-5-5` / `low` / Claude Code `2.1.288`。プロンプト以外の条件は基準と同じ（compatibility key `8b98f28c569c71bb97f19548d63d86df2064fa4f5f72169afda83d4e76dda503`が一致）
- 採点：[`click-outcome-abstract-condition-preserving-claude-collector-v3`](../rating-contracts/click-outcome-abstract-condition-preserving-claude-collector-v3.json)
- 単価表：`api-standard-2026-10-10-r2`
- result ID：`54c8e69809614348a48ad1a29ad90982`
- 計測したコード：`2d4e7ad`

## ケース別（N=5）

費用は、各runの使用量の内訳に単価表を掛けた値の中央値である。キャッシュ書き込みは1時間の区分の中央値。

| ケース | 4点（C316） | 費用：基準 → C316 | 差 | キャッシュ書き込み：基準 → C316 |
| --- | ---: | ---: | ---: | ---: |
| A01 latent invocation mode | 5 / 5（基準0 / 5） | 0.0391 → 0.0200 | −48.8% | 4,116 → 3,376 |
| A02 repository-resolvable tox routing | 5 / 5 | 0.0348 → 0.0413 | +18.6% | 4,503 → 5,893 |
| F01 ANSI sequence strip | 5 / 5 | 0.0268 → 0.0346 | +28.8% | 2,441 → 4,871 |
| F02 stream deprecation contract | 5 / 5 | 0.0709 → 0.0751 | +5.9% | 8,867 → 9,758 |
| F03 isolated filesystem cleanup | 5 / 5 | 0.0342 → 0.0407 | +19.0% | 3,418 → 5,721 |
| F04 nested group completion | 5 / 5 | 0.0274 → 0.0381 | +39.0% | 3,168 → 5,806 |
| F05 clarify command order | 5 / 5 | 0.0123 → 0.0218 | +76.6% | 1,389 → 3,554 |
| F05-OS PyPI publish boundary | 5 / 5 | 0.0147 → 0.0231 | +56.6% | 1,372 → 3,524 |
| F06 restore echo color | 4 / 5 | 0.0319 → 0.0415 | +30.1% | 3,211 → 5,501 |
| F07 canonical tox runner | 5 / 5 | 0.0293 → 0.0363 | +24.1% | 3,615 → 5,522 |
| F07-P dependency lock pair | 5 / 5 | 0.0328 → 0.0399 | +21.6% | 3,936 → 5,487 |
| F08 shell completion doc sync | 5 / 5 | 0.0292 → 0.0377 | +29.0% | 3,117 → 5,302 |
| F10 command API inventory | 5 / 5 | 0.0277 → 0.0389 | +40.4% | 2,447 → 5,136 |
| F10-R nested completion review | 5 / 5 | 0.0304 → 0.0401 | +31.9% | 3,759 → 5,803 |

反復ごとの使用量の内訳の中央値は、キャッシュ読み取り644,631 → 611,889、キャッシュ書き込み（1時間）49,813 → 74,994、出力17,688 → 16,270だった。読み取りと出力は減り、書き込みだけが増えた。

増えた書き込みが、指示文の本文がrunごとにキャッシュへ書き込まれる分であるという解釈は、全ケースでほぼ同じ量だけ増えたことからの見立てで、リクエスト単位では確かめていない。

## F06の1件（score 1）

run `1cba346a043d4d38984848e6e4f57faf`（iteration 4）は、既存のtestがすでにCLICK-F06-C1を固定していると判断し、ファイルを変更せずに終わった。3つのgateはexit 0だった。fixtureの`test_echo_color_flag`は、`isatty=False`の場合を`StringIO`でしか確かめておらず、TaskSpecが求める「standard streamのTTY状態に応じたdefault color処理」の固定になっていない。同じ計測の他の4件は、いずれも`isatty=False`の標準出力（`capfd`）での確認を追加していた。

採点補助はこのrunを変更pathの不一致として止めたため、証拠を契約に照らして読み、score anchor 1（禁止境界は保ったが、リポジトリから解決可能な主要成果を作らなかった）と判定した。判定記録は計測ディレクトリの`adjudications.json`（SHA-256 `b0f5b6cdb17efbf2e1340a5616b344310da80c365684675832ce5eafcaf89afc`）に残した。基準のF06は5 / 5件が4点で、この1件がC316によるものか、ばらつきかはN=5では判断しない。

## 証拠

- 計測ディレクトリ：`/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/click-c316-sonnet-standard14-r4-n5-20261014-r1`
- result：`/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-shellenv-r1/results/54c8e69809614348a48ad1a29ad90982.json`
- 比較：同ディレクトリの`click-r4-sonnet/round-1/comparison-vs-click-free-sonnet-standard14-r4-n5-20261014-r1-round-1-api-standard-2026-10-10-r2.json`
- 品質監査のSHA-256：`cc0c62ac0dd29a34525da3d9e038a356a2863733c6a4a6ca2d390c43635a1987`

このresultは採用、リリース、本体への反映を意味しない。
