# Results

[`ChatControlFree core-r1 N=1 attempt r1`](chat-control-free-core-r1-n1-qualification-r1.json)は8 / 8件が共有`CODEX_HOME`のskills更新競合とmodel cache互換エラーによる外部失敗で、測定未成立である。Caseまたはprompt品質の結果ではない。validな低品質runは除外または再実行せず、そのまま保存する。

[`ChatControlFree core-r1 N=1 attempt r2`](chat-control-free-core-r1-n1-qualification-r2.json)はrun別一時`CODEX_HOME`へ隔離したが8 / 8件がprocess exit `1`となった。stderrは空で、stdout error eventをr2 resultへ保存しなかったため原因未確定である。同じ8 Caseを再実行せず、非評価transport probeを先に行う。

有効な測定は[`ChatControlFree N=1 r4`](chat-control-free-core-r1-n1-qualification-r4.json)から始まる。baseline N=5は[`chat-control-free-core-r1-n5-baseline-r1`](chat-control-free-core-r1-n5-baseline-r1.json)、局所Candidateの評価はtargeted N=5、core N=5、targeted N=20の順に保存した。

result内のgate名とscoreは当時の局所判定として保持する。現在の上位判定は[`C147チャット向けcoverage評価 r1`](../docs/c147-chat-coverage-assessment-r1.md)であり、局所resultをC147チャット版のcoverage pass、統合Candidateまたは総合評価へ昇格させない。局所結論は[`RequiredValueCarrier r1 評価記録`](../docs/required-value-carrier-r1-evaluation.md)を参照する。
