# click-standard14-r3

`click-standard14-r2`のA01とF10だけを新しいcase revisionへ差し替えた標準14項目である。評価セットの保管場所へ一度だけ固定した（identity `f31876e0b709043652294e0808e4f4129cb356030eba32821929084446a8b64f`）。

| ケース | 版 | r2からの変更 |
| --- | --- | --- |
| [`CLICK-A01-LATENT-CONTEXT-POLICY`](../../cases/CLICK-A01-LATENT-CONTEXT-POLICY/r2/README.md) | `r2` | 確認して停止する期待動作をTaskSpecから除いた。fixtureは同じ |
| [`CLICK-F10-COMMAND-API-INVENTORY`](../../cases/CLICK-F10-COMMAND-API-INVENTORY/r3/README.md) | `r3` | `src/AGENTS.md`をfixtureへcommitした。TaskSpecは同じ |

ほかの12ケースは、r2と同じrevision、TaskSpec、fixture identityである（A02 `r1`、F01〜F06 `r1`、F07 `r2`、F07-P `r3`、F08 `r1`、F10-R `r1`）。

r2では、制御なしでもA01が満点となり、F10がどのプロンプトでも`authority_unavailable`で停止したため、この2ケースはプロンプトの違いを観測できなかった（[制御なしSonnet 5.5 low r2](../../results/click-free-sonnet55-low-standard14-r2-n5_2026-10-14.md)）。r3はこの2点を直し、プロンプトだけを変えて比べる計測に使う。r2とr3のresultは評価セットが異なるため比較しない。

固定の手順は計測の道具の`campaign-tools/single-prompt-r1/click/freeze_set_r3.py`、Claude Code実行の採点は[`claude-collector-v2`](../../rating-contracts/click-outcome-abstract-condition-preserving-claude-collector-v2.json)である。
