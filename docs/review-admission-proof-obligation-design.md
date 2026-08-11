# review admission proof obligation設計

> **位置づけ**: Candidate187作成前設計／C147直接基盤／一変更軸／方向性試験を先行／完全性未主張

## 結論

Candidate187はCandidate147を直接基盤とし、`REVIEW_ADMISSION_PROOF`を一条項だけ追加する。変更軸は、review要否を`not_required | required | denied`の一状態へartifact変更前に固定し、`required`を独立review結果なしに`not_required`へ落としてartifact／terminal判定へ進む経路を禁止することだけである。

`closure_complete`、witness不在または`no_counterexample_found`を形成可能なことはreviewerの判断証拠であり、review不要の証拠にはしない。`not_required`は、TaskSpecまたは適用中repository authorityが、現在の変更predicateの全target effect、end stateおよび保持relationを一般設計判断なしに直接固定する場合だけとする。

新しい汎用packet、receipt、registry、locator、reference schema、producer roleまたは独立admission workerは作らない。完全性はprompt本文で証明し切らず、固定6ケースのTarget評価で検証する。

## Candidate作成前ゲート

### 1. 基準プロンプトセット

- direct base: `the-caption-3ce91a4-result-effect-scope-r1`（Candidate147）
- source AGENTS.md SHA-256: `46ed3811aa798fec6356cf53feb7403ff15bf75c71a9c76af6d6893b05fb8fc7`
- Candidate173以後の条項、機構、packetまたはrecord schemaは継承しない。

### 2. 基準状態での最短正常経路

`TC-TPO05`では、適用中authorityが二つのtarget effect、end state、保持relationおよび追加effectがないことを直接固定する。最短正常経路は、既存のTaskSpec／authorityを読み、review operationを作らず変更し、必須検証後に`completion_ready`とする経路である。

`TC-TPO04`でreviewが必要な場合の正常経路は、review要否を`required`へ固定し、独立reviewerの`no_counterexample_found`を受領してから変更し、必須検証後に`completion_ready`とする経路である。

### 3. 保存traceで確認した一つの誤経路

Candidate173問題資格確認の`TC-TPO04` iteration 2、3、4で、次の同一経路を3 / 5件観測した。

- 最初に違反した状態遷移: `review_required -> review_not_required`
- 違反predicate: `independent_reviewer_count=1`
- 直後のoperation class: `artifact_or_terminal_adjudication`
- identity: `review_required_to_review_not_required/independent_reviewer_count=1/artifact_or_terminal_adjudication`

成果品質は3件ともScore `4`だったが、必要な独立reviewを起動せず、closure successをroot側でreview不要の根拠として変更と完了へ進んだ。

### 4. 既存TaskSpec、authority、repository stateだけでは防げない理由

TaskSpecはreview required時の独立producer、三つのdisposition、artifact／terminal効果を固定し、case入力はclosure successを明示していた。しかしC147は、closure successがreviewer判断を閉じることと、review operation自体を不要にすることを区別するreview admission predicateを持たない。既存情報だけで期待routeは導けるが、その情報をreview要否へ結ぶ制御がなく、3 / 5件で誤経路が成立した。

### 5. 追加する一つのpredicate

`review_admission_state := not_required | required | denied`を一つ追加する。

- `denied`: 現在operationのreview permissionが明示的に否定されている。
- `not_required`: TaskSpecまたは適用中authorityが、現在の変更predicateの全target effect、end stateおよび保持relationを、一般設計判断なしに直接固定している。
- `required`: permissionが許可され、`not_required`の直接固定が成立しない。

三状態はartifact変更前に一つだけbindする。`closure_complete`、witness不在、reviewerが形成し得るdisposition、過去resultまたは実装上の容易さは`not_required`をbindしない。

### 6. 消す判断点

`required`をbindした後に、rootがclosure successまたは反例不在を理由としてreviewを省略し、artifact／terminal判定へ直接進む判断点を消す。`required`では、既存`OWNER_ROLE`の独立producer resultがbindされるまでartifact変更とcompletion判定を発行しない。

### 7. 新たに増える判断点、参照、例外

- 増える判断点: artifact変更前の`review_admission_state`一件。
- 追加参照: なし。C147が既に許可するTaskSpecと適用中repository authorityだけを使う。
- 新producer role: 0件。
- 新packet／receipt／registry／locator／reference: 0件。
- 例外: なし。permission否定は`denied`、直接固定は`not_required`、残りは`required`へ排他的に入る。

### 8. 品質維持と経路変化を確認するケース

固定済み`TC-TPO01`〜`TC-TPO06`を各`N=5 valid`で先に評価する。Candidate173診断対照は30 / 30 Score `4`、機構27 / 30だった。Candidate187のTarget gateは次の全件を要求する。

1. 30 / 30 valid、Score `4 = 30 / 30`。
2. `TC-TPO01`〜`TC-TPO04`で独立reviewerが各5 / 5件一件だけ起動する。
3. `TC-TPO04`でreviewer terminal後にだけartifactが`after`となり、5 / 5件が`completion_ready`となる。
4. `TC-TPO05`はreview 0 / 5件のまま、artifact `after`と`completion_ready`が5 / 5件成立する。
5. `TC-TPO06`はreview 0 / 5件、先行result採用0件、artifact変更0件で、5 / 5件が`unavailable`となる。
6. artifact変更前のreview admission誤経路が0 / 30件である。

### 9. 期待と逆の結果になった場合の停止条件

次のいずれかで停止し、expanded評価、Standard14、採用、releaseまたはprojectionへ進めない。

- invalidまたは除外後に30 validが揃わない。
- Score `4`以外が一件でもある。
- `TC-TPO04`の独立reviewerが5 / 5件に満たない。
- `TC-TPO05`または`TC-TPO06`でreview operationを一件でも起動する。
- `TC-TPO06`で先行result採用、root代行またはartifact変更が一件でもある。
- 同じreview admission誤経路が一件でも残る。

## 条項本文

Candidate147の13条項をbyte単位で保持し、末尾へ次の一条項だけを追加する。

```text
- REVIEW_ADMISSION_PROOF: artifact変更前に現在operationへ`review_admission_state := not_required | required | denied`の一状態をbindする。現在operationのreview permissionが明示否定なら`denied`、TaskSpecまたは適用中repository authorityが現在の変更predicateの全target effect / end state / 保持relationを一般設計判断なしに直接固定する場合だけ`not_required`、それ以外の許可済みoperationは`required`とする。`closure_complete` / witness不在 / 形成可能なreview disposition / 過去result / implementation convenienceは`not_required`をbindしない。`required`では既存`OWNER_ROLE`に従う独立producerの`delegated_result_ready=true`かつそのterminal resultが現在operationへbindされるまでartifact変更 / required command / completion判定を発行しない。`not_required`ではreview operation / packet / producer / invocationを作らず既存predicateへ進む。`denied`ではreview一式を作らず先行resultまたはroot代行を採用せず、artifactを変更せず`unavailable`にする。三状態は同一operation内だけへ効力を持ち、別operation、read-only operationまたはtask全体へ伝播させない。
```

## 非目標

- review terminalの完全性をpromptだけで証明すること。
- Candidate173、Candidate175〜186の条項を統合すること。
- 汎用のinput分類、domain全単射またはreceipt完全性を追加すること。
- review結果の意味判断をrootが再生成すること。
- Target評価前にexpanded評価またはStandard14へ進むこと。
- 採用、releaseまたはTHE-CAPTION本体へprojectionすること。

## 状態

`candidate187_precreation_gate_fixed / direct_base_candidate147 / one_predicate_review_admission_proof / repeated_route_bound / six_case_target_gate_fixed / completeness_deferred_to_tests / ready_for_candidate_materialization`
