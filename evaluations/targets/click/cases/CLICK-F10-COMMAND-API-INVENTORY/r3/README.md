# CLICK-F10-COMMAND-API-INVENTORY r3

r2と同じTaskSpecで、Repository Authorityの`src/AGENTS.md`をfixtureへcommitしたread-only、zero-drift caseである。

r2は`src/AGENTS.md`の有無をプロンプトバンドルで切り替え、authority availabilityを比べるために作った。共通指示のようにルートの指示だけを置くバンドルでは`src/AGENTS.md`が必ず欠けるため、どのプロンプトでも`authority_unavailable`で停止してscore `1`となり、プロンプトの違いを観測できなかった（[制御なしSonnet 5.5 low](../../../results/click-free-sonnet55-low-standard14-r2-n5_2026-10-14.md)）。

r3はauthorityをリポジトリ側の内容として固定し、どのプロンプトでもauthority確認、3 sourceの照合、一覧の返却という本来の作業を測る。`src/AGENTS.md`の本文は[`click-00e592c-repository-authority-r1`](../../../prompts/candidates/click-00e592c-repository-authority-r1/manifest.json)の同pathとバイト単位で同一である。seedは追加する一file（`private/seed.patch`）だけで、既存sourceは変更しない。r2の入力と結果は変更しない。
