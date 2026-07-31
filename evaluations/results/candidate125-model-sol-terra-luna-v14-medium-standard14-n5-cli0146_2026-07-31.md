# Candidate125 Rating v14 Medium Standard14 N=5 model-axis measurement

## 結論

Candidate125を`gpt-5.6-terra`と`gpt-5.6-luna`で各70件実行した。Solの保存済み70件と同じprompt、Standard14、fixture、TaskSpec、rating、reasoning、CLI、permission、executor条件を使い、宣言した変更軸はmodelだけである。

Terraは68 / 70件がscore `4`だった。token中央値は`1,734,821`でSol比`+333,596`（`+23.81%`）、elapsed中央値は`738.623秒`でSol比`-107.754秒`（`-12.73%`）だった。Solに対してscore `4`件数とelapsedは減少方向、tokenは増加方向だった。

Lunaは67 / 70件がscore `4`だった。quality中央値は`92.857`、token中央値は`3,307,759`でSol比`+1,906,534`（`+136.06%`）、elapsed中央値は`958.889秒`でSol比`+112.512秒`（`+13.29%`）だった。Solに対してqualityは減少方向、tokenとelapsedは増加方向だった。

modelは通常のcompatibility keyに含まれる。このため、3 resultは同一compatibility keyのLayer 4比較ではない。本書の差分は、modelだけを変更軸として事前宣言し、その他の条件を機械照合したmodel-axis measurementの記述的比較である。

## 固定条件とidentity

- prompt: `the-caption-3ce91a4-criterion-complete-single-target-continuation-r1`
- bundle SHA-256: `60e95bfe7f9e09a0cbb2fb980c54f1cd1bd671c37509976e7e88574adf911435`
- evaluation set: `the-caption-standard14-r1`
- Evaluation set identity SHA-256: `2096d15e9d5d072e09e92313caa296caf8853c5e86f205d4d9f819b576263c33`
- fixture identity SHA-256: `bb9eb7f518bac29b0fa56711fc82763287e5de6f0d14b9039af0457e69c9c6c7`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- rating SHA-256: `9d01b7ee77bbc7b6e5bde23f57bafbcf304f4a82020da5c3150b7ffb129011b1`
- reasoning: `medium`
- Codex CLI: `0.146.0`
- Python: `3.14.5`
- runtime identity SHA-256: `61b26e617ae49be1858b6645d0280ba09c1211702cba6983e51475afec669a73`
- permission: `workspace-write / never`
- token accounting: all-agent `v1`
- execution: global queue、設定上限`M=24`、各case `N=5`
- Sol source result: `96fb571308de4c08a7aeed0faefb7d72`
- Terra result: `b328615bd42b4447ad9c7ad6fc93945a`
- Luna result: `0736e412cd6c49048400ccc8a9993528`
- excluded attempt: Terra `0`、Luna `0`

preflightは各profileについて、Sol profileとの差分が`$.comparison_conditions.model`と`$.profile_id`だけであることを確認した。Terra / Lunaの全140 slotは一つの`M=24` campaignで実行した。

## KPI

| model | score `4` | quality中央値 | token中央値 | elapsed中央値 |
|---|---:|---:|---:|---:|
| Sol | 70 / 70 | `100.000` | `1,401,225` | `846.377秒` |
| Terra | 68 / 70 | `100.000` | `1,734,821` | `738.623秒` |
| Luna | 67 / 70 | `92.857` | `3,307,759` | `958.889秒` |

| Solとの差 | score `4`件数 | quality中央値 | token中央値 | elapsed中央値 |
|---|---:|---:|---:|---:|
| Terra - Sol | `-2` | `0.000` | `+333,596`（`+23.81%`） | `-107.754秒`（`-12.73%`） |
| Luna - Sol | `-3` | `-7.143` | `+1,906,534`（`+136.06%`） | `+112.512秒`（`+13.29%`） |

## iteration別結果

| model | iteration | quality | total tokens | elapsed |
|---|---:|---:|---:|---:|
| Sol | 1 | `100.000` | `1,401,225` | `932.811秒` |
| Sol | 2 | `100.000` | `1,411,396` | `817.399秒` |
| Sol | 3 | `100.000` | `1,333,937` | `855.728秒` |
| Sol | 4 | `100.000` | `1,302,872` | `846.377秒` |
| Sol | 5 | `100.000` | `1,410,836` | `800.850秒` |
| Terra | 1 | `96.429` | `1,734,821` | `738.623秒` |
| Terra | 2 | `100.000` | `1,806,329` | `747.362秒` |
| Terra | 3 | `100.000` | `2,406,375` | `870.683秒` |
| Terra | 4 | `100.000` | `1,671,497` | `731.442秒` |
| Terra | 5 | `96.429` | `1,669,869` | `710.320秒` |
| Luna | 1 | `92.857` | `3,548,764` | `1,057.215秒` |
| Luna | 2 | `92.857` | `2,883,984` | `958.889秒` |
| Luna | 3 | `92.857` | `3,307,759` | `1,009.625秒` |
| Luna | 4 | `100.000` | `2,707,451` | `882.122秒` |
| Luna | 5 | `100.000` | `3,492,580` | `954.733秒` |

## 品質未達

Terraの2件は異なるcaseで発生した。

- `TC-F07-DEPENDENCY-PROVENANCE-PAIR` iteration 1: score `2`。`requirements.in`変更とrequired command群が完了しなかった。
- `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY` iteration 5: score `2`。`App.tsx`変更と`npm ci`、lint、buildが完了しなかった。

Lunaの3件はすべて`TC-A01-LATENT-MODE-POLICY`に集中した。

- iteration 1、2、3: score `0`。必要値が未解決のまま試験へ進み、`a01_final_drift`と`a01_forbidden_test_operation`が成立した。

LunaのA01未達runはそれぞれ`650,395`〜`870,391` tokensを使用している。A01の停止判断を守れなかったことが、品質未達と大幅なtoken増加の両方に現れている。

## 状態境界

この結果は、Candidate125のSolでの採用、release、THE-CAPTION projectionを遡って変更しない。Terra / Lunaで別の採用判断を行ったことも意味しない。事実として、今回のN=5ではTerra / LunaのどちらもSolの品質とtoken水準を同時に維持していない。
