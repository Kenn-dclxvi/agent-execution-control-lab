# Candidate95 required judgment owner boundary Rating v14 Medium A02 N=5 B20

## 結論

Candidate95のA02限定B20は、20 / 20 batch、100 / 100件をvalid・rateableとして完了した。公式scoreは100 / 100件が`4`で、excluded attempt、再試行、品質failure、command protocol violationは0件だった。各batchは独立したresultへ登録し、final compactまで完了した。

100 / 100件がrepository authorityから正規routeを解決し、`run.sh`だけを変更して成功した試験証拠を残した。owner clarificationによる停止、未変更停止、required validation欠落は0件だった。全件root-onlyで、child sessionとchild tokenも0だった。

現在状態を`a02_b20_evaluated / route_stability_gate_passed / standard14_quality_gate_passed / aggregate_cost_both_higher / adoption_not_decided`とする。これはA02の固定条件内で低頻度再発を観測しなかった証拠であり、他caseや別runtimeへの普遍的な保証ではない。Candidate81は採用・投影済みbaselineのままとし、Candidate95の採用、release、本体反映は行わない。

## 固定条件

| 条件 | 値 |
| --- | --- |
| prompt | `the-caption-3ce91a4-required-judgment-owner-boundary-r1` |
| bundle SHA-256 | `8c845f18bd6ed86d6f2f19281ba1257f0f1a213fa1c3466c76ede402451ee190` |
| profile | `candidate95-required-judgment-owner-boundary-v14-reasoning-medium-a02-global-m5-n5-cli0146-r1` |
| evaluation set / case | `the-caption-standard14-r1` r1 / `TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING` r2 |
| repetition | A02 × `N=5` × 20 batch、計100 slot |
| model / reasoning | `gpt-5.6-sol` / `medium` |
| rating | `outcome-terminal-state-evidence-owner-diagnostic-v14` |
| execution | global queue、`M=5` |
| Codex CLI | `0.146.0` |
| token accounting | all-agent v1 |
| target commit / tree | `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b` |
| fixture digest | `bece63e466ad63f5ad0c40f23d2ac98b6a26f2033c1e6d883838e1ed6ab3ca87` |
| evaluation set identity SHA-256 | `d71205651b5e57b2d3f5af3509d184215093baa479c0896aa0613f648987ce7f` |
| compatibility key | `e5740fe6edb0efabde9aaab3ccb624d31984ddeaa6fc32076a82266b313b9833` |

既存のCandidate95 A02 targeted profileを変更せず、20個のappend-only resultとして反復した。case、TaskSpec、fixture、rating、model、reasoning、CLI、permission、M / Nを変更していない。標準14全体のB20ではない。

## 集計

- valid / rateable / score `4`: `100 / 100 / 100`
- excluded attempt / 再試行: `0 / 0`
- 20 resultのquality中央値の中央値: `100.000`
- 20 resultのall-agent token中央値の中央値: `223,400`
- 20 resultのelapsed中央値の中央値: `77.208秒`
- 100件all-agent token合計: `22,755,305`
- 100件run elapsed合計: `7,764.785秒`
- controller実行時間合計: `1,822.293秒`
- campaign開始から全保存完了まで: `1,865.289秒`、31分5.289秒
- command protocol violation: `0`
- owner-producer evidence inadmissible: `0`
- route: root-only `100 / 100`、session合計`100`、child token `0`
- final archive SHA-256不一致: `0 / 20`

## Owner境界の診断

保存event上の観測は次のとおりである。

- `criterion owner=none`を明示したrun: 50 / 100
- `git log`を実行したrun: 47 / 100
- `git blame`を実行したrun: 15 / 100
- Git authorをcriterion ownerへbindしたobservable message: 0 / 100
- owner clarificationで停止したrun: 0 / 100

Git履歴readは正規routeの来歴確認として残っており、cost診断である。`git log`または`git blame`の実行だけをGit authorのowner化とは扱わない。一方、50件は`owner=none`を外部messageへ明示していないため、100件すべてが同じ内部binding表現を採用したとは主張しない。成果状態と採点は、最終変更path、正規route、成功した試験証拠へbindしている。

## 各batch

| batch | result ID | result content SHA-256 | token中央値 | elapsed中央値 | score 4 | final archive SHA-256 |
| ---: | --- | --- | ---: | ---: | ---: | --- |
| 1 | `7c3640522ee749eebebe7e7fc20e45ab` | `4e97b3efc09f46cd369dd969e232c6b951302c3638bc379849a1812752bdf617` | 207,107 | 74.704秒 | 5 | `753b8b2a0b4ee05de6f967e58e0eba7721fbb4d22d71c796c7ec0acb259243bb` |
| 2 | `c75115de971049de988e59c1cddee5e3` | `5e71caf5f25e858a1efc7f51c63a26128c85e8fe71b295723d13d7a4162dba40` | 185,618 | 65.076秒 | 5 | `404ce352a81aa0384bdecd703c75481dd49e675c1ddcce13ee4b1f32d6b7b574` |
| 3 | `db90d45021b84488a5a7eccb454715d8` | `d0b47a284ac619b55444ff577fdc69308032172aee2e8dafecc6b343bba2348e` | 222,097 | 71.020秒 | 5 | `b94a6c8779b23776cc9fa1c9dc9944c0440246c3d5a784094a90f53f6099ba2a` |
| 4 | `521bdce64a6f483b855be04ddc6d4785` | `4431c55ce915f3b7f25dabf42ca3eabe2c44c1dcdfdc2bb629f245a6a77cf786` | 220,090 | 80.756秒 | 5 | `6ad387dceb2d73b97d134be422c1851a97e8ebff357f0f26de391318b3115ef5` |
| 5 | `7bee48f87a0f40d4b6866aa74255123d` | `dd741ae84bdb18c38107d9951665df3248edb63d79b16f6cf2cc73018166c35d` | 199,356 | 69.415秒 | 5 | `7a9937c69fb086f2466c325ee0f7a3956f8f8a34acf111ad062fe77a85520f11` |
| 6 | `971b302a93c24469b6ed73a1d94bddff` | `395b7edb34d03256e6b04100b401cc1ec858751e2b50c83f330a0a3077e36b98` | 224,703 | 82.337秒 | 5 | `653ff260c9ec9e043eddb31fac463000fcc12c79e948d5e0244a4fbc138a5987` |
| 7 | `071c9b1ffc2d4fedbd37b0666962490e` | `51fef991a54f2759afd4adffba9c6d17100a141cb4aaa76662f52870ef962fb1` | 247,474 | 81.702秒 | 5 | `917ceed3f7e61be82271c2956539263307d3c200bd23f4194926eec981984c02` |
| 8 | `35761c1f5d854aaba3787febb0c1307a` | `50c53f1256889a3db2a7f923eee2a13e0c5744c17f2179b45fc780158e5e3599` | 219,420 | 78.517秒 | 5 | `f38848f59fb7a3ff61829ae1cf946820ff51a4ee7c53bbebbc4f1b7e2a862af4` |
| 9 | `2e7e4ede07c54f348ea435fe5be85c99` | `aae4ee5c1efa6ac6fb0609ba49f25206975a438c5898bb2fa0a83b5071e0cd0e` | 225,860 | 73.112秒 | 5 | `a6ff93749762605264d324e0a07e8bf521f534fc55aa8f35bb123c2e486e44a9` |
| 10 | `ee4c672770f949d89e2325d101f8bc86` | `aa68f2e2d5ba90197edd6797ab77d45dae403cd7495e17876f50cfec827c3709` | 225,844 | 81.272秒 | 5 | `25b2bd42d59fef9867acb273afa5da242c6b626c96b53bcd5258da0c9c4103d5` |
| 11 | `b315679c7e6a42ce95d8314858447bdd` | `38909093939fc70da4b8307e47eac6f47cc33a8d1c242ad5ed8689e00fe4ac78` | 259,331 | 74.833秒 | 5 | `bc216d013a1b2cd2b8ebeb3c6473559e90ced6878e3912ab469e1d5d6016bc38` |
| 12 | `b1ee61c4b3d24267b88c9ce78b6bcb6d` | `7048a0898f135fe508a7c856fe575c15a23620b26dda632fb710ce110a93ae06` | 251,011 | 76.161秒 | 5 | `8ae54861f0ba5dcb972ddfa739900b8fab4c322f1c4627275c3ecabdce14206a` |
| 13 | `4c0b5047b1234c50b28b4a1754f6c00e` | `7336c5946c13f5c3b9497146a7c43701130297e92da8fb440dbe1d5c58c747a0` | 192,001 | 78.255秒 | 5 | `e7076711b6188c435ef4f71d6181605f35a1fe1067fca5e70d0e12effac1f09a` |
| 14 | `9b978302b70d43d18f4d412881143335` | `dd94a8cf3fc043bc5adce8e5c279fcf25ceb417c0d9409726c79c4aad1f64b8e` | 212,925 | 81.977秒 | 5 | `5a468ba1c1b5e958c38535c409fb9ff414fe6f2c95e1acd3f0e777de4d86ae0a` |
| 15 | `460999ec0a87447891c7d7700e70ee9c` | `b3f42c9aa4fbb8019c5005130ed644785121e168e8b0ac4e7090315f1980bc87` | 239,931 | 74.614秒 | 5 | `85229d617682872269787e0eb0ea1ced619cf6c3b9c126c9a212768deaaee8ee` |
| 16 | `d6644961d095403eb337ab26198faefe` | `e135d34233643db653ce807e5ea902206fc000df958644efabe2f62600dc6865` | 234,804 | 78.731秒 | 5 | `468b777c00ecec2c32173720abc0828b6024997c7a4e21d749982b790d908a8a` |
| 17 | `98f338e409cd4112a58f512183d0be7f` | `b420ab1ae61f81fa036e62f6c866953777051203b02db0c5122ba50deadce110` | 217,492 | 74.495秒 | 5 | `cbf5a7136571fce0fff4eac40825c59097181a1661454a59fce8e8d127564990` |
| 18 | `08cd320859f844f48dfcb59c7346978e` | `1deb1d38b13ed68bc7df3a990e249ccee2c5a40bd694dc47281bdfa762b1d22c` | 267,903 | 73.823秒 | 5 | `7655cf4625cad64ea98c77c2aa77791379cbeb961f70af898591d2157835b95a` |
| 19 | `ec4ae45ee83a4e79b316725006dff989` | `d6c60fac63cdbbe7bca373510458a21233d9395fb0deb4acbb99b142e03217e9` | 232,088 | 80.544秒 | 5 | `9175533e308ec6e3db048438e29ef9d7c102cb655fc5e9a5928963c09fa37485` |
| 20 | `69739dc8814542efa2cf084c71d01c71` | `ae09b97d968d76db883fa2e5c38d08b10c0d54589d0d1506587e6ac10d3198de` | 212,833 | 78.929秒 | 5 | `ebc108a26a19a01161b8a41524393cc9b3ef663bb910ef33613915646cc0f399` |

## 保存場所

- profile: [`candidate95-required-judgment-owner-boundary-v14-reasoning-medium-a02-global-m5-n5-cli0146-r1`](../profiles/candidate95-required-judgment-owner-boundary-v14-reasoning-medium-a02-global-m5-n5-cli0146-r1.json)
- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate95-required-judgment-owner-boundary-v14-medium-a02-continuous-n5-b20-cli0146-20260730-r1`
- result registry: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3`

全20 batchにexecution seal、result registration、final compact receipt、execution / final evidence archiveが存在する。非公開raw evidenceはverification checkoutへ保持し、このrepositoryへcommitしない。
