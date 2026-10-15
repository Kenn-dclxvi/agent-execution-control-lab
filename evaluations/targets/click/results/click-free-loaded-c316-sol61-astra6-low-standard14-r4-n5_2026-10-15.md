# Click 制御なし（1文）とC316 GPT-6.1 Sol Low・GPT-6 Astra Low Standard14 r4 N=5

## 結論

Click Standard14 r4を、Codex（GPT-6.1 Sol LowとGPT-6 Astra Low）で、制御なし（指示を含まない1文の`AGENTS.md`）とC316を5回ずつ測った。比べる2つのプロンプトと2つのモデルを一つの待ち行列に交互に並べ、合計280件を最大24件同時で流した。

| モデル | 指標 | 制御なし（1文）の中央値（幅） | C316の中央値（幅） | 差 | 基準の幅に対する位置 |
| --- | --- | ---: | ---: | ---: | --- |
| Sol Low | 品質 | 92.86（92.86〜100.00） | 94.64（94.64〜100.00） | +1.92% | 幅の中 |
| Sol Low | 費用（USD） | 0.7288（0.6221〜0.8898） | 0.6362（0.6059〜0.7623） | −12.71% | 幅の中 |
| Sol Low | 経過時間（秒） | 414.88（355.66〜429.74） | 344.39（329.75〜365.93） | −16.99% | 幅より下 |
| Sol Low | 生のトークン（参考） | 1,490,639 | 1,182,418 | −20.68% | 幅より下 |
| Astra Low | 品質 | 100.00（92.86〜100.00） | 94.64（89.29〜100.00） | −5.36% | 幅の中 |
| Astra Low | 費用（USD） | 4.3002（3.4656〜4.3063） | 3.3927（3.1070〜3.4935） | −21.10% | 幅より下 |
| Astra Low | 経過時間（秒） | 458.33（410.13〜515.64） | 385.51（379.18〜411.26） | −15.89% | 幅より下 |
| Astra Low | 生のトークン（参考） | 1,529,036 | 1,120,380 | −26.73% | 幅より下 |

費用は単価表`api-standard-2026-10-10-r2`で両方を数え直した値。

C316は、A01の失敗（結果が決まらないまま作業を始める）を両モデルで0件にし、経過時間を約16〜17%減らした。一方で、制御なしでは起きなかった誤った停止が、F07-PとF06で計9件起きた。

## 品質

| モデル | 条件 | 点数の分布 | 4点未満のrun |
| --- | --- | --- | --- |
| Sol Low | 制御なし（1文） | 4点67、0点3 | A01 3件（0点） |
| Sol Low | C316 | 4点66、1点4 | F07-P 4件（1点） |
| Astra Low | 制御なし（1文） | 4点69、0点1 | A01 1件（0点） |
| Astra Low | C316 | 4点65、1点5 | F07-P 3件、F06 2件（1点） |

C316の1点の9件は、採点補助が変更pathの不一致と必須コマンドの未実行で止め、証拠を契約に照らして読んで判定した（判定記録は各計測ディレクトリの`adjudications.json`）。

- **F07-P（Sol 4件、Astra 3件）**：TaskSpecは「既存lockと隣接dependency groupから意図を解決する」と、既存の状態から結果を決めるよう明示している。runは値をそれらから確認しながら、C316の1行目（「既存の状態、候補を消去法で一つに絞れること…は、結果を決める根拠にならない」）を理由に、pytestの制約を利用者へ確認して停止した。1行目は、利用者の示した内容と「それが従うよう求めている指示や正本が直接定めている内容」で結果が決まるとしており、このTaskSpecはその指示に当たる。それでも、Codexの両モデルは既存の状態を使うこと自体を禁止と読んだ。Claude Code（Sonnet、Opus）のF07-Pでは起きなかった。
- **F06（Astra 2件）**：追加の指示を探すために自ら実行した`rg`（存在しない`.agents`と`.codex`を指定）が終了コード2を返し、TaskSpecの環境failure（`environment_recovery_max=0`）と見なして停止した。

## 費用

ケース別の費用の中央値（制御なし → C316）：

| ケース | Sol Low | 差 | Astra Low | 差 |
| --- | ---: | ---: | ---: | ---: |
| A01 | 0.0483 → 0.0199 | −58.8% | 0.1726 → 0.0852 | −50.6% |
| A02 | 0.0686 → 0.0775 | +12.9% | 0.4086 → 0.3416 | −16.4% |
| F01 | 0.0495 → 0.0725 | +46.5% | 0.4239 → 0.2521 | −40.5% |
| F02 | 0.0600 → 0.0679 | +13.3% | 0.4257 → 0.2693 | −36.7% |
| F03 | 0.0588 → 0.0690 | +17.4% | 0.3280 → 0.3429 | +4.5% |
| F04 | 0.0602 → 0.0358 | −40.5% | 0.3383 → 0.3368 | −0.4% |
| F05 clarify | 0.0128 → 0.0224 | +75.9% | 0.0999 → 0.0831 | −16.8% |
| F05-OS | 0.0131 → 0.0139 | +6.1% | 0.0787 → 0.0872 | +10.8% |
| F06 | 0.0553 → 0.0581 | +5.0% | 0.2852 → 0.1923 | −32.6% |
| F07 | 0.0490 → 0.0320 | −34.7% | 0.2764 → 0.2910 | +5.3% |
| F07-P | 0.0555 → 0.0342 | −38.4% | 0.3841 → 0.1712 | −55.4% |
| F08 | 0.0473 → 0.0306 | −35.4% | 0.2458 → 0.2016 | −18.0% |
| F10 | 0.0435 → 0.0328 | −24.7% | 0.3880 → 0.2362 | −39.1% |
| F10-R | 0.0458 → 0.0378 | −17.4% | 0.2626 → 0.2263 | −13.8% |

F07-P（両モデル）とF06（Astra）の削減には、作業せずに止まったrunの安さが含まれており、効率の改善としては数えられない。

キャッシュの条件は、Claude Codeのような片側だけの偏りがなかった。入力のうちキャッシュから読んだ割合は、Solで制御なし0.834、C316 0.803、Astraで0.855、0.828だった。

## 固定条件

- 評価セット：`click-standard14-r4` / `r4`
- 制御なし：`click-00e592c-control-free-loaded-instruction-r1`。C316：`click-00e592c-receive-form-file-read-range-r1`
- Agent / CLI：Codex `0.159.0`、実行ごとに空のホーム（個人の指示を切り離す）。推論low。セル`click-r4-sol`と`click-r4-astra`は、THE-CAPTIONのSol Lowの元のプロファイルにclick r4の対象側の条件を重ねたもので、Astraはモデル名だけが違う
- 発行：`one_queue_across_cells_and_prompts`（制御なしとC316、SolとAstraを一つの待ち行列に交互に並べる）、合計24本まで、負荷を見て発行。計測は2026-10-15 00:11〜00:23 UTC
- 採点：`click-outcome-abstract-condition-preserving-v11`
- 計測したコード：`a2561ad`

| モデル | 条件 | プロファイル | result ID |
| --- | --- | --- | --- |
| Sol Low | 制御なし（1文） | [`free-loaded-click-sol61-low-standard14-r4-n5-cli0159-isolated-shellenv-20261015-r1`](../profiles/free-loaded-click-sol61-low-standard14-r4-n5-cli0159-isolated-shellenv-20261015-r1.json) | `d9edba8df50c4e7b9c52708fc958ef82` |
| Sol Low | C316 | [`c316-click-sol61-low-standard14-r4-n5-cli0159-isolated-shellenv-20261015-r1`](../profiles/c316-click-sol61-low-standard14-r4-n5-cli0159-isolated-shellenv-20261015-r1.json) | `fafe83dc8cf14fb4ade905b2be7b8953` |
| Astra Low | 制御なし（1文） | [`free-loaded-click-astra6-low-standard14-r4-n5-cli0159-isolated-shellenv-20261015-r1`](../profiles/free-loaded-click-astra6-low-standard14-r4-n5-cli0159-isolated-shellenv-20261015-r1.json) | `d1a4974c37eb4bb092c1ceb0e4caf3d6` |
| Astra Low | C316 | [`c316-click-astra6-low-standard14-r4-n5-cli0159-isolated-shellenv-20261015-r1`](../profiles/c316-click-astra6-low-standard14-r4-n5-cli0159-isolated-shellenv-20261015-r1.json) | `53c1de6c5ac746f78cf4f4599679b4a1` |

## 経緯

2026-10-14夜には、同時に5件以上流すとOpenAI側から`429 Too Many Requests`が返り、計測を中止した。2026-10-15の再開時に、同時に6件流す診断（`runs/click-sol-path-check-c316-20261015-r2`）で429が出ないことを確かめてから測った。本計測の280件に429の失敗はなかった。

判定記録を足して`finalize`をやり直す流れをCodexで初めて通したとき、作成済みの担当者の証拠を上書きしようとして止まった。計測の道具（`campaign.py`の`rate_sol`）を、作成済みならそのまま使うよう直した。

## 証拠

- 計測ディレクトリ：`/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/click-free-loaded-codex-standard14-r4-n5-20261015-r1`、`runs/click-c316-codex-standard14-r4-n5-20261015-r1`（待ち行列の記録は前者の`campaign-round-1/`）
- 品質監査のSHA-256：Sol制御なし`6aee2e6968de5df60efc0bd2bbb725fa2675f2c59986b3b4bb018284be0f01f5`、Astra制御なし`f376a8ad9ee8272d78703f53aae8aed6a36e5e01c8e6f8715ce075b9eb35616d`、Sol C316`3a552167593f10f40d5cf47777c142e126ef7f98625ba7207ed2cb5ad1b0c02e`（判定記録`bc44f44eece15c00147900eb65151cd40264f4ff281f33c87a4e44aae9f55a92`）、Astra C316`3962ddf31365ecdf5756a8dc63135a9e1f3d77eb2339cf3d664c07afde27e5d7`（判定記録`561543aa6985988e2636f144c14bb0eb61628a0a660ae2b6f6189dad4d72c644`）

このresultは採用、リリース、本体への反映を意味しない。
