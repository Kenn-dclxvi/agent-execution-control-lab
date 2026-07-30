# Candidate96 successful validation result projection設計

## 結論

Candidate96はCandidate81を直接親とし、`VALIDATION_CLOSURE`一規則だけを置換する。全required validationが成功した場合、生成したwrapperは各validationのidentity、exact command、exit codeだけを一度modelへ返し、成功stdout / stderrを返さない。

TaskSpec、repository authority、required validation、評価条件、executor adapterは変更しない。diff / status等のcompletion evidenceを同じwaveへ統合する変更も本Candidateへ混ぜない。

## 作成前gate

1. 基準prompt setはCandidate81 `the-caption-3ce91a4-validation-wrapper-precedence-r1`、bundle SHA-256 `919e2d4c53a487efde9d87ab182ea9b576c082c29ac81eb46fb7a442fb837220`とする。
2. 最短正常経路は、bind済みrequired validationを一つのwrapperから順に個別発行し、全成功resultを一度返してterminalを判断する経路とする。
3. 保存済みC81 Rating v14 Medium標準14 B20では、F01 / F02の8 / 200 runがfull validationを再実行した。raw traceでは長い成功出力後にmachine-bound exit codeを確認できず、同じrequired commandを再発行していた。
4. TaskSpecとrepository authorityはrequired commandを既に固定している。誤経路はcommand成功後のmodel-visible result投影で生じるため、TaskSpec変更では防がない。adapterではなく、modelが生成するvalidation wrapperの返却規則をpromptで制御する。
5. 変更predicateは、`VALIDATION_CLOSURE`のsuccess / non-success result projection一つとする。
6. 消す判断点は、成功stdoutを読んだ後にexit code evidenceの有無を再判断し、同じvalidationを再発行するmodel再入である。
7. 新たに増える判断点は、全required validationがsuccessか否かの一分岐である。これはwrapperが直接観測するexit codeから判定する。
8. 最初の品質確認は既存F02 r1、Rating v14、Medium、`N=5`とする。5 / 5 score `4`、required command evidence 5 / 5、success projection 5 / 5を要求する。
9. score `4`、required command evidence、success projectionのいずれかが5 / 5未満なら停止する。mechanism成立後にC81比でtokenとelapsedがともに高ければF04以降へ進めない。

## 保存traceの境界

対象campaignは[`Candidate81 / Candidate95 Standard14 B20比較`](../evaluations/results/candidate81-candidate95-required-judgment-owner-boundary-v14-medium-standard14-continuous-n5-b20-cli0146_2026-07-30.md)に登録されたC81 campaignである。

- C81 prompt: `the-caption-3ce91a4-validation-wrapper-precedence-r1`
- Codex CLI: `0.146.0`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Rating: v14
- F01 / F02: 各100 run
- full validation再実行: F01 3件、F02 5件

代表traceでは、full gateのpytest成功行を確認できても構造化exit codeがmodel contextへ残らず、同じfull gateを再発行した。これは成果品質の失敗ではなく、成功resultの投影と再入に関するroute診断である。

## Prompt変更

Candidate81の`VALIDATION_CLOSURE`を次の意味へ置換する。

- 全success時は、各validationのidentity、exact command、exit codeだけを一度返す。
- success stdout / stderrはmodelへ返さない。
- nonzero、unavailable、unknown、permission要求では後続を止める。
- 失敗時は完了済みvalidationの識別情報と、該当tool resultを省略せず返す。
- read、search、diff、target探索、変更前調査のoutputは変更しない。

## 非目標

- TaskSpecまたはrequired validation集合の変更
- diff / status等のcompletion evidenceの必須化またはwave統合
- repository read / search / diffへの一律byte cap
- executor adapter、Codex CLI、tool transportの変更
- 評価済み、採用済み、release済み、本体反映済みという主張

## 評価順序

1. bundle構造とC81からの一規則差分を検証する。
2. F02 r1 `N=5`でquality、required command evidence、success projectionを確認する。
3. mechanism gateと品質gateを通過した場合だけ、C81とのKPIを比較する。
4. F04、標準14、B20は別gateとし、F02結果だけで進めない。

## F02評価結果

2026-07-30にCLI `0.146.0`、Rating v14、Medium、各`N=5`でCandidate81と比較した。両promptは5 / 5 score `4`で、Candidate96のtoken中央値は`-11.03%`、elapsed中央値は`-15.78%`だった。

ただし、全5 runでrequired validationの成功stdoutがmodel-visible resultへそのまま返り、success projectionは`0 / 5`だった。狙ったwrapperは生成されず、required commandは直接発行された。事前停止条件に従い、現在状態を`targeted_f02_evaluated / mechanism_gate_failed / stopped`とする。詳細は[`F02 result`](../evaluations/results/candidate81-candidate96-successful-validation-result-projection-v14-medium-f02-n5-cli0146_2026-07-30.md)を正本とする。

### 評価順序の事後訂正

このmechanism gateはCandidate96のtraceだけで判定できた。保存済みCandidate81 B20 traceも存在したため、Candidate81 F02 N=5を先に新規実行する必要はなかった。今後はcandidate-only mechanism gateを先に行い、通過後だけ保存済み互換baselineを照合する。不足するbaselineがある場合もcandidateの不足slotと同じ最大24のcampaign queueへ入れる。
