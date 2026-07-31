# Candidate122 / Candidate123 preterminal result round closure Rating v14 Medium A01 / A02 / F01 / F02 atomic N=5

## 結論

Candidate123は停止する。20 / 20件はvalidだったが、qualityはscore `4 / 2 = 19 / 1`で、事前gateの20 / 20 score `4`を満たさなかった。

失敗したF02 1件は、正常なdetached HEADで`git branch --show-current`の出力が空になる状態を`branch identityを確定できない`と誤分類した。`pwd`とbranchだけを確認して停止し、TaskSpecが同じ開始identityとして要求したHEADと`git status --short`、content evidence、artifact変更、required validationを実行しなかった。これは外部環境失敗ではなく、Candidate123が追加したidentity failure stopの判定条件不足である。

現在状態は`targeted_a01_a02_f01_f02_evaluated / execution_valid / quality_gate_failed / a01_clarification_terminal_passed / a02_prechange_round_gate_failed / f02_start_identity_classification_failed / result_registered / stopped`とする。Standard14、採用、release、runtime projection、本体反映へ進めない。

## Identity

- Candidate123 prompt: `the-caption-3ce91a4-preterminal-result-round-closure-r1`
- bundle SHA-256: `9547acd587c5a00979089055d8edd37825009763d77d19429cf5a097c40f7115`
- direct parent: `the-caption-3ce91a4-prechange-evidence-wave-closure-r1`（Candidate122）
- profile: `candidate123-preterminal-result-round-closure-v14-reasoning-medium-a01-a02-f01-f02-global-m24-n5-cli0146-r1`
- Candidate123 pool: `79f32b27775f88901f4fc1bf059a1078b059f0162f100451a53d220628d02ea7`
- Candidate123 selection: `77ac577d82e14900be615c72a8ce390f`
- Candidate123 analysis: `f3232203a6ca4650b908c279fc921b17`
- Candidate123 result: `0f5d1bf818314e4d8b03d6fbc4bfb499`
- reference Candidate122 result: `c68a9fe2beee47d38865653706f9c87e`
- compatibility key: `5fd07842276b862329d72268b59256341c4869c85ccec19c7a534aa669a7a083`
- execution archive SHA-256: `a1e4d2a640fd0fe9a7e1a52227930e41b68f4c57adbef84df4ab5027f13c6dc3`
- final archive SHA-256: `8f6064eaf65a51c3ea8ffc00aea04b14c836645a1cf24596b774e03a287b67a7`

## Quality

| case | valid | score 4 | score 2 | 判定 |
|---|---:|---:|---:|---|
| A01 | 5 / 5 | 5 | 0 | 通過 |
| A02 | 5 / 5 | 5 | 0 | 通過 |
| F01 | 5 / 5 | 5 | 0 | 通過 |
| F02 | 5 / 5 | 4 | 1 | 不通過 |
| 合計 | 20 / 20 | 19 | 1 | quality gate不通過 |

F02失敗runは`1e7e688f437745388315ad6058866753`である。final responseは、detached HEADの空branch名を理由に変更とtestを行わず停止したと明記している。Rating v14は、required成果2 sourceの変更欠落とrequired command 2件の未実行を検出し、score `2`とした。

## Mechanism監査

`result round`は、同じmodel stepから一件以上のread-only commandを発行し、完了resultを受け取って次のtool、artifact変更、またはterminalを判断するまでを1回と数える。

| gate | 結果 | 判定 |
|---|---:|---|
| A01 required value待ち | 5 / 5 | 通過 |
| A01 clarification前command | 0 / 5 | 通過 |
| A01 artifact変更 / test | 0 / 5 | 通過 |
| A02 canonical成果 | 5 / 5 | 通過 |
| A02 artifact変更前result round 1回以下 | 3 / 5 | 不通過 |
| A02 identity / evidenceをshell compoundへ結合しない | 4 / 5 | 不通過 |
| A02 artifact変更後・最初のvalidation前method探索 | 0 / 5 | 通過 |
| F01 required command evidence | 5 / 5 | 通過 |
| F02 full start identity確認 | 4 / 5 | 不通過 |
| F02 exact target set content wave | 4 / 5 | 不通過 |
| F02 required validation完備 | 4 / 5 | 不通過 |

A02の2件は変更前に2回または3回resultをmodelへ返した。A02 TaskSpecは編集targetの`run.sh`を固定するが、canonical entrypointを示すauthority pathは固定しない。したがって、Candidate123の`admission済みevidence identityが発行前にbind済み`条件は全runをfast pathへ入れず、設計した5 / 5 closureを強制できなかった。

## Cost

case中央値は次のとおりである。

| case | Candidate122 | Candidate123 | C123 - C122 | 先行指標 | 指標判定 |
|---|---:|---:|---:|---:|---|
| A01 | `37,381` | `18,780` | `-49.76%` | C118 `18,431`以下 | `+1.89%`で未達 |
| A02 | `165,870` | `129,460` | `-21.95%` | C107 `125,559`以下 | `+3.11%`で未達 |
| F01 | `109,096` | `111,064` | `+1.80%` | C107 `127,797`以下 | `-13.09%`で通過 |
| F02 | `124,719` | `122,135` | `-2.07%` | C107 `173,000`以下 | 数値上`-29.40%`、ただしquality失敗runを含むため通過判断に使わない |

4-case aggregate中央値はtoken `384,471`、elapsed `227.443秒`だった。Candidate122比はtoken `-89,079`（`-18.81%`）、elapsed `-17.250秒`（`-7.05%`）である。ただし、aggregate quality中央値`100.000`はF02の1件失敗を隠すため、Candidate123の成功根拠にはしない。

## C107 A02との照合で分かったこと

Candidate107 A02の5件はtoken `116,569 / 121,650 / 125,559 / 148,349 / 214,943`だった。中央値runも変更前に開始identity、`run.sh`、entrypoint実体を別result roundで確認している。したがって、A02がC107中央値へ到達する条件を「変更前result roundが必ず1回」とする仮説は強すぎた。

保存traceが支持するのは次の二点である。

1. 不要なresult roundはcost増加要因になり得るが、round数だけでtokenを決めない。
2. 未指定authority pathを解決するA02では、判定に必要なevidence identityを発行前に全件bindできるという前提が成立しない。

このため、Candidate123の二つの追加条件をそのまま次候補へ継承しない。C122はtargeted gate通過済みの別状態として保持し、Candidate123の停止でC122の結果を失効させない。
