# Candidate90 tool output ingress boundary設計

## 結論

Candidate90は投影済み基準Candidate81を直接親とし、TaskSpec、Evaluation set、fixture、oracle、required validation、rating、executor、model、reasoning、M / Nを変更しない。変更軸は、toolのraw outputがmodel contextへ入る前に、次の判断に必要な観測値へ限定する`OUTPUT_INGRESS`一つである。

効果測定は既存caseを各`N=5`で行う。F02とF04のtargeted gateを先に通し、その後だけ通常の標準14項目各`N=5`へ進む。新しいTaskSpecまたは公開・本番確認caseは作成しない。

## 作成前gate

1. 基準prompt setは`the-caption-3ce91a4-validation-wrapper-precedence-r1`（Candidate81）である。
2. 基準の最短正常経路は、TaskSpecを固定し、必要なrepository evidenceを取得し、変更後にrequired validationを一つのclosure waveで実行し、全result受領後に一度だけterminalを判断する経路である。
3. 2026-07-29のTHE-CAPTION実タスクtraceでは、公開・本番確認開始時点で1 model step当たりのinputが約20万tokenへ達し、その後約15回のmodel reentryがあった。公開・本番確認相当区間は`3,051,212` tokenで、うちcached inputは`3,011,840`だった。
4. このtraceの問題はrequired command数ではなく、前段でmodel-visibleになった広い検索、diff、test、GitHub応答等を含むcontext全体が後続stepで再入力されたことである。
5. C81の`VALIDATION_CLOSURE`はrequired validationのmodel reentryを抑えるが、各tool resultのmodel-visible量を制約しない。既存TaskSpec、repository authority、repository stateだけでもoutput ingress量は固定されない。
6. Candidate7 / Candidate8はcommandまたはphase間のresult形式を指定したが、同一親contextへ入る前のraw tool outputを遮断せず、F02単回観測でtoken削減を示さなかった。Candidate40はoperation / result identity境界であり、F10のtool callとtokenを減らさなかった。
7. 追加する一つのpredicateは`OUTPUT_INGRESS`である。raw stdout / stderrを受領してから要約するのではなく、invocation内でrepository外の一時fileへ保存し、modelへ返すresultを先に限定する。
8. 新たに増える判断点は、完全出力自体が成果または直接判定材料か、次predicateに必要なobservation fieldsは何か、non-success時にどの範囲を追加取得するかである。
9. token推定、required evidence削減、command省略、TaskSpec変更、context reset、Worker必須化、executor変更、THE-CAPTION本体変更は行わない。

## Prompt変更

Candidate81のroot `AGENTS.md`へ`OUTPUT_INGRESS`だけを追加する。他の11 label本文は変更しない。

- 検索はpath / pattern / fieldを発行元で絞る。広い結果を取得後にtruncateして探索漏れを隠さない。
- 完全出力自体が成果、TaskSpec-required evidence、source / diffの直接判定材料でないcommandは、stdout / stderrをrepository外の一時fileへ保存する。
- modelへ返すsuccess resultはcommand identity、exit code、必要な観測値、一時evidence pathに限定し、4096 bytes以下とする。
- non-successは原因に直接関係するexcerptを8192 bytes以下で返す。追加診断が必要な場合だけ、一時fileの必要範囲を次invocationで読む。
- target commandのexit code、required evidence、fail-stopは維持する。`head`等をtarget commandへpipeして成功扱いを変えない。
- raw outputがmodelへ一度入った後の要約は、このpredicateの成立として数えない。

## 評価順と停止条件

1. 保存済みC81とCandidate90を、既存F02 r1、Rating v14、Medium、各`N=5`で比較する。
2. Candidate90が5 / 5 score `4`、required command evidence欠落0、取得時projection成立5 / 5、token中央値がC81未満、elapsed中央値がC81比`+10%`以下ならF04へ進む。
3. 同じ条件で既存F04 r2を各`N=5`で比較し、同じgateを適用する。
4. 両case通過時だけ、既存`the-caption-standard14-r1`の14項目をRating v14、Medium、global queue `M=24`、各`N=5`で実行する。
5. 標準14ではquality、all-agent token、elapsedの3 KPIを記録する。採用判断の目安は70 / 70 score `4`、token中央値C81比`-10%`以上、elapsed中央値C81比`+5%`以下とする。未達でも測定resultは保持し、採用、release、本体反映へ進めない。

取得時projection成立はraw traceから診断する。commandの完全出力を一時fileへ保存する前にmodel-visible resultへ出したrun、required evidenceを欠落させたrun、success resultが4096 bytesを超えたrunは不成立とする。tool output bytesとmodel stepは診断値であり、3 KPIへ追加しない。

## 測定限界

標準14にはGitHub公開、merge後同期、本番dry-run / apply確認を含まない。この試験は既存coding taskでtool output ingressを抑える一般効果を測るものであり、実タスクで観測した公開後44%を直接再現する試験ではない。そこを直接測るには別TaskSpecが必要だが、本系列では作成しない。

## 状態境界

設計、candidate bundle、profile作成時点は`draft / not_evaluated`だった。後続の[`F02 N=5 result`](../evaluations/results/candidate81-candidate90-tool-output-ingress-boundary-v14-medium-f02-n5_2026-07-29.md)は5 / 5 score `4`だったが、取得時projectionが0 / 5、C81比token中央値`+5.35%`、elapsed中央値`+23.31%`だった。事前停止条件に従う現在状態は`targeted_f02_evaluated / stopped`であり、F04、標準14、採用、release、THE-CAPTION本体反映は未実施である。
