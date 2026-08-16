# Candidate263 Candidate254結果影響範囲の依存関係閉鎖設計

## 結論

Candidate263はCandidate254 `the-caption-3ce91a4-independent-check-same-model-step-r1`を直接の親とする。Candidate254の`DECISION_BOUNDARY`にある一般文を、先行結果が影響しない後続作業を待機対象にできない依存関係へ置き換える。Candidate254のその他の本文は同一byteで保持する。

Candidate147は、結果の停止効果を作業の種類ごとに限定した過去の比較証拠としてだけ参照する。Candidate261とCandidate262は対象を取り違えた診断結果であり、本文、親関係、評価結果を継承しない。

置換後の文は次のとおりとする。

> `result_effect_scope`は、受領resultが後続operationの対象、許可、方法または停止条件を変え得る未発行operationの種類だけを含む。後続operationを先行resultの待機対象にできるのは、その種類が`result_effect_scope`に含まれる場合だけとする。含まれない既知の相互非依存operationは分割せず同一model stepから発行し、全result受領後に一度だけ次を判断する。

ここで`result_effect_scope`は、受け取る結果によって実際に変わり得る後続作業の種類の集合である。「待機対象にできない」とは、先行結果を受け取ることを、影響しない読み取りや確認を開始する条件にしてはいけないという意味である。

## Candidate作成前の検討gate

### 1. 比較基準と最短正常経路

- 直接の親: Candidate254。
- 最短正常経路: TaskSpecで許可済みの開始確認と、その結果で対象、許可、方法、停止条件が変わらない必要readを同じAI判断から発行する。共同resultを受領した後に変更し、必須検証を終えて一度だけ完了を判断する。
- 結果でreadの対象または許可が変わり得る場合は、先にその結果を受領してからreadを決める正常経路を保持する。

### 2. 保存済みtraceで確認した問題経路

Candidate254 Standard14 N=20のF03では、開始確認の結果が必要readの対象または許可を変えないのに、開始確認だけのresultをAIへ返した後、別のAI判断からreadを発行した実行が6 / 20件あった。この分離は一件あたり約一回分のAI再判断を増やし、N=5の二件では19,748 tokenと19,139 tokenの純増に対応した。

### 3. 問題経路を許す依存関係

Candidate254の一般文は、影響しない複数確認を同一model stepから発行する行動を示すが、後続作業を先行resultの待機対象にできる条件を、作業の種類との包含関係として固定していない。開始確認専用の後続文は保持するが、一般文の対象を「複数の確認」という呼び方へ限定せず、readを含む後続operation全体の待機permissionへ接続する。

TaskSpec、repository authorityおよびrepository stateは、開始時点で必要readを許可できるが、許可済みreadを先行resultの待機対象にできるかどうかまでは定めない。この依存関係は操作発行時にモデルから見えるため、promptの境界として扱う。

### 4. 変更する条件と責任範囲

- 変更target: root `AGENTS.md`だけ。
- 変更箇所: `DECISION_BOUNDARY`の最初の一般文一文を三文へ置換する。
- 追加する関係: `result_effect_scope`に含まれない後続operationを、先行resultの待機対象へ置けない。
- 保持する範囲: 用語説明、`SPEC`、`PRODUCER`、`TERMINAL`、`CONTEXT`、`EVIDENCE_GATE`、`OWNER_ROLE`、`ROOT`、`INDEPENDENCE`、開始確認専用の`DECISION_BOUNDARY`、`VALIDATION_CLOSURE`、`VALIDATION_PLAN`、`METHOD`、`RECOVERY`をCandidate254と同一byteで保持する。

### 5. 実行できなくなる問題経路

先行resultが後続readの対象、許可、方法、停止条件を変え得ない場合、そのreadは`result_effect_scope`へ入らない。したがって、モデルが判断順を変えても、先行resultの受領をそのread開始の条件にする経路はpromptに適合しない。

特定のcommand、toolの呼び出し方、read範囲、待ち時間またはwrapper構成は固定しない。

### 6. 維持する正常経路

- TaskSpecがdrift時にreadを禁じる場合は、readを結果受領後へ置ける。
- 先行resultでread対象またはpermissionが変わり得る場合は、readを結果受領後へ置ける。
- F10 entrypoint inventoryでpath-local `AGENTS.md`の内容が配下readの対象またはpermissionを変え得る場合は、規則を先に受領する経路を維持する。
- 必要情報の保持者と受け渡しはCandidate254から変更しない。新しいworker、packet、repository readまたは出力を増やさない。

### 7. 新しく増える判断と対象外影響

新しい作業手順は増やさない。既にCandidate254が判断に使う対象、許可、方法、停止条件と、後続operationの種類との対応だけを待機permissionへ接続する。

増えるmodel-visible本文は、置換前後のbyte差として固定する。F10の必要な分離が欠落した場合は過剰遮断であり、品質Scoreが維持されても停止する。

### 8. 評価ケースと比較単位

最初はCandidate263だけを次の二ケース各N=5で評価する。

- `TC-F03-ATOMIC-CONTEXT-CLEANUP` r2: 対象経路。開始確認と結果非依存readの分離件数を確認する。
- `TC-F10-ENTRYPOINT-INVENTORY-REVIEW` r1: 正常経路の保持。path-local instructionの結果で配下readの対象またはpermissionが変わり得る場合の必要な分離を確認する。

品質は10 / 10件がvalidかつ採点可能で、個別にScore `4`であることを要求する。機序は品質と分離して記録し、品質再現性との相関が100％と確認されていないため、単独で全件成立を品質合否へ読み替えない。

Candidateだけの品質と対象経路を確認した後に限り、保存済みCandidate254の互換resultを基準として、同じ二ケース各N=5のtokenと経過時間を比較する。Candidate147は補助比較に限り、Candidate263の直接基準にしない。

### 9. 停止条件

- 一件でもinvalid、採点不能またはScore `3`以下なら停止する。
- F10で必要なinstruction先行確認を省き、許可または対象が未確定の配下readを先行発行した場合は停止する。
- F03で分離が残った場合は、結果を保持して原因を監査する。機序と品質の相関が100％ではないため、その一件だけを理由に品質結果を無効化しないが、追加NまたはStandard14へ自動で進めない。
- Candidate254比でtokenまたは経過時間の一方でも増え、その増加を品質または必要な正常経路と対応づけられない場合は`unjustified_cost_regression`として停止する。
- targeted gateを通過しても、Standard14、採用、release、projectionは別判断とする。

## 非目標

- Candidate254をCandidate147へ戻すこと。
- Candidate261またはCandidate262を親、継承元、採用根拠にすること。
- 完了前返却を減らすため、待ち秒数、command構成またはwrapperを指示すること。
- 成功runのtool順、read範囲、呼び出し回数を実行手順へ変えること。
- Candidate254の他の制御群を同時に圧縮すること。

## 現在状態

後続のF03・F10 entrypoint各N=5は10 / 10件がScore `4`だったが、F03の分離はCandidate254と同じ2 / 5件、F10の必要な依存関係も同じ3 / 5件だった。二ケース合算tokenはCandidate254比`-1.97%`、経過時間は`+19.29%`である。詳細は[評価結果](../evaluations/results/candidate263-result-effect-dependency-closure-f03-f10-entrypoint-n5_2026-08-16.md)へ固定する。

現在状態は`candidate_created / direct_parent_candidate254 / targeted_n5_completed / quality_passed / mechanism_failed / unjustified_cost_regression / stopped / standard14_not_started / adoption_not_approved / release_not_created / projection_not_performed`とする。
