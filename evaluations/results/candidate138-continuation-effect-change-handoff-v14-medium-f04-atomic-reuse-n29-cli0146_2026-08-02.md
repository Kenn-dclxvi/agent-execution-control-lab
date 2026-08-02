# Candidate138 F04 atomic reuse N=29 result

## 結論

Candidate138のF04は、初段5件と追加24件の合計29 / 29件がscore `4`だった。score `3`以下、外部失敗、除外attemptは0件である。

追加run `21fa9bd90e354b028c3b04e9d0779491`では、model decisionが0件表示側を変更前にclosedとせず、C1の一行だけを変更し、変更後の静的source observerで`colSpan`を直接確認した。C137でartifact変更前に停止した位置から、effect-local change、pending effectのdirect validation、terminal closureまで到達した。

したがってF04上ではquality gateとmechanism gateを通過した。ただし単一targetのF04だけの結果であり、複数targetへ一般化しない。

## 固定条件

- candidate: `the-caption-3ce91a4-continuation-effect-change-handoff-r1`
- parent: `the-caption-3ce91a4-pending-effect-validation-admission-r1`
- bundle SHA-256: `b542f78becf313fbcc8226c904a2aa324fa4194983c4fc8ec14bcee57cbae7a5`
- case: `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY/r2`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Codex CLI / Python: `0.146.0` / `3.14.5`
- cumulative N / configured M: `29` / `24`
- reused / newly issued in extension: `5` / `24`
- pool: `0e28553b0e3fbfcbee6f73da7138a186c4f53b1310eff634851d349e602973a8`
- selection: `6211342a7bfa46648152b01830bccd58`
- analysis: `0a0f2126445d4649bdfc3c7c1116cd62`
- registered N=5 result: `6ebc3d97a03b4ef2ad8648e776d69caa`
- registered N=29 result: `29ddd1209b4f49f8b1418ea351e34be9`
- N=29 compatibility key: `aa64c2d280f64b221162a682e9b7395b878b56a8dee8d473b6bfef3cf62a0d15`

## 結果

初段5件は5 / 5 score `4`だった。全件が変更前にC2を充足済みと判断した通常経路だったため、同じpoolへ24件追加した。

追加24件も24 / 24 score `4`だった。累計中央値はquality `100.000`、token `186,853`、elapsed `105.782`秒である。

## handoff経路

run `21fa9bd90e354b028c3b04e9d0779491`は次の順で進んだ。

1. `hasAuditKey = true`を観測し、C1を未充足と判断した。
2. 0件表示側を初回変更へ含めず、変更後の静的検証で直接判定すると宣言した。
3. `hasAuditKey`の一行だけを変更した。
4. `npm ci`、lint、buildを順に成功させた。
5. 変更後source observerで`hasAuditKey`、header、row cell、`colSpan={hasAuditKey ? 7 : 6}`を直接確認した。
6. diffとstatusで変更が一行かつ許可path内であることを確認して完了した。

保存stdout自体には変更前`colSpan`行が含まれる。しかし判定対象はraw stdoutの存在ではなく、次のmodel decisionへeffect状態がどうbindされたかである。このrunはC2を初回変更の前提へ使わず、変更後direct validationへ明示的に渡した。

## 状態

`targeted_f04_atomic_reuse_n29_evaluated / score_4_29_of_29 / continuation_handoff_observed / pending_direct_validation_completed / quality_gate_passed / mechanism_gate_passed / result_registered`

## 結論表

| gate | 期待 | 実測 | 判定 |
| --- | ---: | ---: | --- |
| valid / rateable | 29 / 29 | 29 / 29 | pass |
| score `4` | 29 / 29 | 29 / 29 | pass |
| score `3`以下 | 0 | 0 | pass |
| handoff経路 | 1件以上 | 1件 | pass |
| handoff runの初回変更 | C1だけ | C1一行だけ | pass |
| handoff runのrequired validation | 全件成功 | 全件成功 | pass |
| validation result前のC2完了 | 0件 | 0件 | pass |
| 複数target汎用性 | 未評価 | 未評価 | separate gate |
