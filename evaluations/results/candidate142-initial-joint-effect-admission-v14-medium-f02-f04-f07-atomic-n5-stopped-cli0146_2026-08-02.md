# Candidate142 F02 / F04 / F07 N=5停止結果

## 結論

Candidate142のF02 / F04 / F07各N=5は、score `4 / 2 = 12 / 3`だった。F02がscore `4 / 2 = 2 / 3`、F04とF07は各5 / 5 score `4`である。score `2`が出たため停止し、追加24件とStandard14へ進めない。

C142が追加したinitial joint effect admissionは、F02の一target部分変更をC141の1 / 5から0 / 5へ閉じた。しかし、変更前の過大取得でrequired relationが出力途中に切れた3件を、成果変更なしのterminal stopへ変換しただけである。安全な失敗にはなったが、正常進行に必要な観測完全性は回復していない。

## 固定条件

- candidate: `the-caption-3ce91a4-initial-joint-effect-admission-r1`
- bundle SHA-256: `47a8c9d1d5ec0a03f48510b1f29f83459738c36fc9d7f71e5d69b7fef96c807a`
- cases: F02 r1、F04 r2、F07 dependency r1
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Codex CLI / Python: `0.146.0` / `3.14.5`
- N / configured M: `5` / `24`
- newly issued: 15
- valid / rateable / excluded: `15 / 15 / 0`
- pool: `05b0bf98c298d860fb1d779790b44608512d6ccec0e8597a97a9eb8c2f3b57d0`
- selection: `2e491f0725674829b75f40e91b7c4b9a`
- analysis: `472797ccd05448be9fb59a0218af0f88`
- registered result: `43d3dd113e314367a2fbeb58588bbd2a`
- selection comparison key: `008104d71d8980189b90ae60033bcfa118e1211b46be30dea8f7484eacfbcc7b`
- registered compatibility key: `1a160baf02c918304673639cae670d6d9bad5d235e33e965d641f60fef339d93`
- median quality / tokens / elapsed: `83.333` / `354,961` / `198.532秒`
- execution archive SHA-256: `a290997a5d0a80ca6895e2ce6a4c216aa99ea012fc2f4db59bc693b566c1446e`

中央値qualityは5つのselection iterationの中央である。公式score分布と停止判断は15 run全件で判定する。owner / producer evidenceは15件ともdiagnostic-onlyでineligibleだったため、quality scoreの成否には使用していない。

## F02の切り分け

### 成功2件

run `06c2f0d521f449aa9c6b2db6b63c6476`は、2 sourceの関係を約25,221文字で取得した。run `71e452b71cc145ffb819b66826279cab`は、開始identityを独立取得した後、2 sourceと2 testを約50,150文字で取得した。

両件とも変更前に次を判定した。

1. primary refreshが日付を渡していない。
2. updaterが選んだend dateをmarket history取得へ接続していない。
3. selective retryとdate-bound test contractは既に満たされている。

両件ともengineとupdaterだけを変更し、focused gateとfull gateを成功させた。

### 低Score 3件

run `8b7ab112a08541378d9cde760bf0c63a`、`68b42711075e4a5dbb5137aa54855b8b`、`116dd7beb54f41df8aed1b15d4c585c2`は、初回の取得出力がそれぞれ約138,205、88,239、60,488文字となった。いずれもrequired relationの一部が出力途中で切れたと判定した。

- 1件はupdater effectの未充足を観測したが、primary / selectiveの関係が未観測だった。
- 2件は共同所有するeffectの少なくとも一つを未観測のまま残した。
- 3件とも追加read、artifact変更、required validationを実行せず停止した。
- changed pathは0件であり、C141のようなengineだけの部分変更はなかった。

## 解釈

事実として、C142は共同所有domainの不完全観測から部分変更へ進む分岐を閉じた。F04とF07は各5 / 5であり、single-targetとdependency pairの成功経路は今回のN=5で維持された。

一方、C142は関係を観測できる取得requestの構成を改善していない。C141のF02過大取得は1 / 5だったが、C142では3 / 5だった。N=5同士なので発生確率の上昇は確定できない。ただし、新しい全effect state gateが変更後のadmissionだけでなく、変更前に広い取得を選ぶ理由として解釈された可能性がある。これは推測であり、次のCandidateの作成根拠にはまだできない。

次は新しい実行制御を足す前に、C141 / C142のF02全10件を「変更前evidence requestの作り方」と「result受領後のadmission」に分けて再監査する。特に、sourceとtestを一度に全量返す構成が、TaskSpecが求めるrelationの直接観測より優先される判断点を特定する。行数、bytes、output配送、executor制御は次案にしない。

## 状態

`f02_f04_f07_n5_evaluated / score_2_3_of_15 / quality_gate_failed / f02_partial_change_closed / f02_false_stop_3_of_5 / result_registered / stopped`

## 結論表

| case / gate | 実測 | 判定 |
| --- | ---: | --- |
| F02 score `4 / 2` | `2 / 3` | fail |
| F04 score `4` | `5 / 5` | pass |
| F07 score `4` | `5 / 5` | pass |
| 全体score `3`以下 | 3件 | stop |
| F02一target部分変更 | 0 / 5 | mechanism pass |
| F02変更前に全effect state観測 | 2 / 5 | fail |
| F02不完全観測から無変更停止 | 3 / 5 | quality fail |
| F04必要変更と既存effect保持 | 5 / 5 | pass |
| F07 dependency pair完備 | 5 / 5 | pass |
| 追加24件 / Standard14 | 未発行 | stopped |
