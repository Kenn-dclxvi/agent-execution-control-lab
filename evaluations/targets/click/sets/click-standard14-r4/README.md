# click-standard14-r4

`click-standard14-r3`のA01だけをr3へ差し替えた標準14項目である。評価セットの保管場所へ一度だけ固定した（identity `c9717344b4bd3e49fac4a09996b4f49f3f810fa1e624b0349772e8b3065adc52`）。

| ケース | 版 | r3からの変更 |
| --- | --- | --- |
| [`CLICK-A01-LATENT-CONTEXT-POLICY`](../../cases/CLICK-A01-LATENT-CONTEXT-POLICY/r3/README.md) | `r3` | 依頼の対象を`Command.main`の`standalone_mode`（二択の既定値）にした。fixtureは同じ |

ほかの13ケースは、r3と同じrevision、TaskSpec、fixture identityである（F10は`r3`）。

r3では、制御なしでもA01が全件確認して停止し、THE-CAPTIONのA01が観測する「結果が確定しないまま作業を始める」失敗を測れなかった（[制御なしSonnet 5.5 low r3](../../results/click-free-sonnet55-low-standard14-r3-n5_2026-10-14.md)）。A01 r3は単発の診断で、制御なしのSonnetが推測して編集・試験へ進むことを確かめた。A01 r3の変更可能pathは、THE-CAPTIONのA01と同じく`src/click/core.py`と関連する既存testとし、編集したrunも有効なrunとして採点する。

固定の手順は計測の道具の`campaign-tools/single-prompt-r1/click/freeze_set_r3.py --set r4`、Claude Code実行の採点は[`claude-collector-v3`](../../rating-contracts/click-outcome-abstract-condition-preserving-claude-collector-v3.json)である。r3以前のresultとは評価セットが異なるため比較しない。
