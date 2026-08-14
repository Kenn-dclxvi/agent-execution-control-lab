# Baseline current-r2 ADR9 r2 N=5 実行準備監査

## 結論

`ready / authorized_45 / issued_0`

実際のbaseline `the-caption-3ce91a4-current-r2`を、既存のADR9 r2全9ケースへ初めてbindした。TaskSpec、fixture、oracle、rating、model、runtime、permissionおよびexecutor条件は既存のADR9 r2保存条件と一致している。新しいcase revision、TaskSpec revision、評価基準またはtestは追加・変更していない。

## identity

- prompt: `the-caption-3ce91a4-current-r2`
- bundle SHA-256: `63225d2d7430bc20ac6d126a0070385461136ca82dad8a0744e2127a3668e48d`
- profile: `baseline-current-r2-adr9-r2-medium-m24-n5-cli0146-r1`
- profile SHA-256: `dd414958dd2eead5c804098f254ced037b911bb4be8a64186ff9ddf513921362`
- Evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- TaskSpec source: `preimplementation-adversarial-design-review-targeted-evaluation-design-r11`
- 条件参照result: Candidate224 `cc43543650a84911ad6ad7ca0e1cde46`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- atomic pool key: `cfa527d40527978147fa4c9f344fdc29da1f8c0b516befe6a44db9ef3006db01`
- frozen set SHA-256: `a18f4fff43f46ddaf808d3884184bd9596dca1443ceb261348d233d28b21e38e`
- coverage SHA-256: `1a15099b14906a1167085a38e6a233e46739e05ee060e7870e3bc230ececff67`
- global plan SHA-256: `9cbe67446f2a868ea02fe8762d9a39cc4ff313dbb4e228f3020e924ca5c9cc0c`
- comparison preflight SHA-256: `e80329ab3ba5d92e93a2ea43f48cf9e6a4ad48949e2616a6ad379351938914d3`
- execution root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/baseline-current-r2-adr9-r2-n5-20260814-r5`

条件参照resultは、ADR9 r2のfixture、TaskSpec、runtimeおよび評価条件を再利用するためだけに使う。Candidate224の挙動や制御をbaselineへ継承しない。global planは9ケース各5件、合計45 capsuleを持ち、全capsuleのprompt identity、bundle SHA、TaskSpec r11、case r2およびcomparison conditionsをpreflightで照合した。設定上の並列上限は24、発行済みslotは0件である。

## 実行前に停止した準備経路

正しい条件を確定するまでに作成した`r1`から`r4`は、いずれもslotを発行していない。

- 保存resultの所在とcomparison receiptの対応が不完全な経路
- ADR9 r1のpoolをADR9 r2へ誤って結び得る経路
- fixtureのcopy modeが保存条件と一致しない経路

これらは実行後の降格ではなく、preflight段階で停止した準備履歴として保持する。実行対象は上記`r5`だけである。

## 目的と停止

目的は、実際のbaselineがADR9で要求される品質と敵対的reviewをどのように実現するかを観測し、以後のCandidate比較に必要な経験的な基準を得ることである。試験の合格自体やCandidateの作成を目的にしない。

各runの最終成果物、必要reviewの実施、reviewer cardinality、review resultの受領と成果への反映、実行時間およびtokenを別々に観測する。有効な低品質runや必要reviewの欠落もbaselineの挙動を示す証拠として保持し、試験を通すためのrepair rerun、TaskSpec変更、case変更、評価基準変更またはtest変更は行わない。
