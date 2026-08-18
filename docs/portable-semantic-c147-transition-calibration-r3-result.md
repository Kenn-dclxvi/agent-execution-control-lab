# C147 transition contract r3校正結果

> [!IMPORTANT]
> **状態**: `completed / valid_14_of_14 / score4_13_of_14 / recovery_trigger_boundary_overbroad / heldout_r2_not_created / portable_prompt_unchanged`

## 結論

r3校正は`PIC-H04`と`PIC-H13`を解消したが、Score 4は13 / 14だった。`PIC-H14`で、許可済みenvironment recoveryを開始しながら同じoperationを失効させる応答が生じた。

r3は「明示effect scopeにあり、そのresultをrequired inputに持つ」ことを失効条件として広く定義した。しかし、通常actionがfailed inputによりbindingを失う場合と、許可済みrecoveryが`failed_environment`を合法な開始triggerとして受け取る場合は別である。r4では後者を失効から除外する。Case、oracle、C147およびresponse schemaは変更しない。

## 計測結果

- valid: 14 / 14
- schema valid: 14 / 14
- Score 4: 13 / 14
- mechanism passed: 13 / 14
- Score 2: `PIC-H14`
- token: min 15,419 / median 15,710 / max 15,957
- elapsed: min 9.536秒 / median 10.919秒 / max 14.099秒

## 停止境界

- r3を同じrevisionのまま修正または再発行しない。
- r3の13 / 14をportable Candidateとの比較値にしない。
- r4校正が14 / 14 Score 4になるまで、新しいheldoutとportable評価を発行しない。
