# Candidate170

Candidate169を親とし、C147の`result_effect_scope`と独立read共同発行の考え方をPRレビューの証拠取得へ翻訳する。正式なprompt identityは`pr-review-prompt-evidence-scope-r1`である。

変更軸はreview evidence schedulingだけである。関係レビュー役は7件の既知の独立readを最初のtool-use stepで発行し、全result受領後に一度だけ判定する。追加readはmissing、unreadable、具体的矛盾があり、未確定の判定を確定できる場合に限る。

finding採用条件、Case、Opus 1人の構成、rootの役割、model-visible情報、権限、review contract、採点、3 KPIは変えない。C02開発用固定ベンチマークの初回測定ではquality `4`と初回7件の共同readを確認したが、追加read 4件によりmechanismは不成立だった。C147の効果をこのターゲットへ一般化しない。
