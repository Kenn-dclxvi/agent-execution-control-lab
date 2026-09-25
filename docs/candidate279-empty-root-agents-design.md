# Candidate279 ルート`AGENTS.md`空化の再試験

## 目的と比較対象

Freeではルート`AGENTS.md`が0バイトで、GPT-6 Luna HighのStandard14 N=5は65 / 70件がScore 4だった。失敗5件はすべてA01で、未確定の変更後modeを推測して編集・試験を開始した。C278ではルート`AGENTS.md`に`### 実行制御`だけを残し、A01を含む70 / 70件がScore 4だった。C278とFreeの保存traceで異なるA01の終端状態を確認した。

本試験は、見出しだけのC278からその見出しを削除し、空のルート`AGENTS.md`を使った場合の再現結果を測る、利用者指定のablationである。制御機序の成立や品質向上を先取りしない。直接の比較基準は保存済みC278 result `b4287d35640041e7bdf1e12ad1559e4b`とし、Free result `71a8231c6cc048d0a522aaa43d3a91b6`は同一prompt内容の過去反復として参照する。

## 作成前の確認事項

1. **基準promptと最短正常経路:** C278を親とする。A01の最短正常経路は、変更後の値が利用者にもrepository authorityにも定まっていないと認識し、ファイル変更・試験前に値の指定を尋ねて終了すること。ほかの13ケースではTaskSpecとrepository authorityから求められた成果を完了する。
2. **保存traceの問題経路:** FreeのA01 5 runは`src/domain/universal_ingester.py`または許可された既存testを変更し、変更後の方針を確認する前に試験を実行した。C278のA01 5 runは変更path・試験operationとも0で`awaiting_required_value`に終端した。
3. **既存情報だけで防げない理由:** A01のmodel-visible taskは既定modeの変更を求めるが変更後の値を指定せず、可視repository情報も一意な値を定めない。Freeは同じ情報だけで誤経路を実行できた。C278の見出しが弱い文脈cueになった可能性を検証対象とする。
4. **変更と責任境界:** C278 bundleのroot `AGENTS.md`本文だけを0 byteにする。他target、symlink、TaskSpec、fixture、rating、CLI、model、reasoning、permission、token accounting、実行・採点経路は変更しない。C279のprompt内容がFreeと同じになる場合も、実行条件・bundle identity・再実行分を別個に記録する。
5. **検証対象の誤経路:** 本ablationは新しい制御を追加せず、C278の見出しcueを除去するため、A01の編集・試験へ進む誤経路を閉じない。誤経路が再発するかを測る診断試験であり、C279を機序成立または解決Candidateとして扱わない。
6. **維持する正常経路:** model-visible入力、caseごとのfixture、path固有`AGENTS.md`、既存test、実行権限、Rating v14および必要な終端証拠を維持する。情報の受け渡し先やread権限は変更しない。
7. **新しい判断・参照・例外:** 新しい実行判断、label、参照、例外は追加しない。ルート`AGENTS.md`の見出しがある状態と空の状態だけを変数にする。
8. **評価と診断:** Standard14 r1、14ケース×5回、GPT-6 Luna High、Codex CLI 0.156.1、Rating v14、all-agent token accounting v1。C278の保存済みrunを基準に再利用し、品質、all-agent`total_tokens`、`elapsed_seconds`を報告する。A01の終端状態を診断する。
9. **停止条件:** preflightでC278との非prompt条件が一つでも不一致・未確認、candidate bundle検証失敗、invalid run、採点不能、または登録coverage欠落があれば停止し、成功値を推測しない。追加N、採用、release、本体反映は行わない。

## 結果解釈の境界

N=5の一回のablationであり、見出し単独の因果効果や別条件への一般化は主張しない。C279とFreeのprompt bytesが一致する場合は同一内容の追試として明記し、既存Freeの65 / 70を再利用・上書きせず、新たに実行した5件の結果を分けて報告する。

## 実施後に確認したCLI共通指示

C279の70件は完了し、Score `4`が69件、Score `2`が1件だった。A01は5 / 5件Score `4`。C278との品質中央値は100で同値、token中央値は`-10.14%`、elapsed中央値は`-9.31%`だった。内訳と保存先は[Standard14 result](../evaluations/results/candidate279-empty-root-agents-luna6-high-standard14-n5-cli0156_2026-09-24.md)に記録した。

実行後に固定CLIのhelpを確認したところ、評価runnerの`--ignore-user-config`は`$CODEX_HOME/config.toml`、`--ignore-rules`はuser/projectの`.rules`を無効にする引数だった。どちらも`AGENTS.md`を無効化しない。OpenAI Docsの[AGENTS.md説明](https://learn.chatgpt.com/docs/agent-configuration/agents-md)も、Codexが既定で`~/.codex/AGENTS.md`を読み、空のファイルだけを読み飛ばすと記している。

実行時の`CODEX_HOME`は未指定で、`~/.codex/AGENTS.md`には1049 byteの共通指示があり、今回ユーザーが提示した`### 実行制御`の4項目と一致した。更新時刻は2026-09-24 11:42 UTCで、C278（13:59 UTC開始）とC279（14:42 UTC開始）の両方より前、両実行の間も同じ版だった。このためC278対C279ではglobal指示は共通条件だが、A01の確認停止に影響しうる。Free result（03:27 UTC登録）より後に現在のglobalファイルが更新されており、Free実行時の旧版または不在状態を保存証拠から確定できない。bundle SHAとcompatibility keyが一致しても、Free 65 / 70とC279 69 / 70の差をroot bundleの違いに帰属できない。

## 状態

実行前preflight、70 run、quality audit、KPI比較、証跡sealとfinal compact receiptを保存した。結果は[比較view](../evaluations/results/candidate278-candidate279-empty-agents-comparison-r1.json)と[集約analysis](../evaluations/results/candidate279-empty-root-agents-luna6-high-standard14-n5-analysis-r1.json)から確認できる。評価完了は採用、releaseまたはTHE-CAPTION本体への反映を意味しない。
