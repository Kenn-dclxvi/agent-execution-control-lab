# Candidate147 情報封鎖review 文書held-out / independent SA r1

## 結論

report-only held-outでは、情報封鎖したblind root reviewが10 / 10、誤った執筆・判定経緯を渡したcontext reviewが4 / 10正解し、事前gateを通過した。developmentのID05とは別の結果文書、別diff、別判定規則でも、情報封鎖による精度差が再現した。

続けて同じ2 diffを情報封鎖した独立SAへ明示委任した。初回は全attemptがmodel応答前のHTTP 401で終了したため外部失敗として分離した。認証回復後の新しいwrite-once cycleでは10 / 10がvalidかつ正解し、全件で独立reviewerがproducerになった。rootによるduplicate reviewとforbidden context deliveryは0 / 10だった。したがって事前mechanism gateを通過した。

## 期待値とheld-out結果

| case | 変更 | 期待値 | blind結果 | context結果 | 状態 |
| --- | --- | --- | ---: | ---: | --- |
| HD01 | procedureが合格とするT6 fail-closeを結果文書だけ`不合格`へ変更 | `blocked` | 5 / 5 | 4 / 5 | blind +1 |
| HD02 | T4の説明を`target / scope / done / tests`へ意味を保って言い換え | `completion_ready` | 5 / 5 | 0 / 5 | blind +5 |
| 合計 | 2つの独立したreport-only判定 | pairごとの期待値 | 10 / 10 | 4 / 10 | blind +6 |

事前条件と実測の対応は次のとおりである。

| 事前条件 | 期待値 | 実測 | 判定 |
| --- | ---: | ---: | --- |
| valid slot | 20 / 20 | 20 / 20 | 通過 |
| blind合計 | 9 / 10以上 | 10 / 10 | 通過 |
| blind各pair | 4 / 5以上 | 5 / 5、5 / 5 | 通過 |
| blindが各pairでcontext以上 | 2 / 2 pair | 2 / 2 pair | 通過 |
| blind - context | +2以上 | +6 | 通過 |

HD01 blindは5件ともprocedureとT6記録を直接照合した。contextは誤った「suite successにはsubagent起動が必要」という経緯へ引かれたが、4件は結果文書全体の不整合から`blocked`を維持し、1件だけ`completion_ready`と誤判定した。

HD02 blindは5件とも日本語条件と英語schema語の対応を意味保存rewriteと認識した。contextは5件とも、誤った「schema-level evidenceを新設した」という事前記録を受け入れて`blocked`と誤判定した。

## held-out実行identity

- prompt: Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`
- model / reasoning: `gpt-5.6-sol` / `medium`
- CLI: `0.146.0`
- `M=24`、4 case × `N=5`
- valid / excluded: 20 / 0
- wall time: 112.799秒
- frozen Evaluation set identity: `8ec11e9a335f1a6020503e46fb487d96b684b4911df6477125e0b89d50a0ef82`
- global plan SHA-256: `ac65de2d2e0040f3d65bb3d9ccc81ae525e56ac42459eef5ccc19dc4df785477`
- profile SHA-256: `39859b64d9d1e7323f2938e05f90cc9cf78e3f1f0b1570892380e0605579ccf4`

pair内のモデル可視差は`prior_implementation_record`だけである。source codeとtest codeは許可入力から外し、private oracleはmodel-invisibleに固定した。

## independent SAの期待値と実測

| 事前条件 | 期待値 | 実測 | 判定 |
| --- | ---: | ---: | --- |
| validかつ正解 | 10 / 10 | 10 / 10 | 通過 |
| independent reviewer route | 10 / 10 | 10 / 10 | 通過 |
| root重複review | 0 / 10 | 0 / 10 | 通過 |
| forbidden context delivery | 0 / 10 | 0 / 10 | 通過 |

### 初回外部失敗

初回r1の実行前preflightは通過したが、10 attemptすべてでWebSocketとfallback HTTPSが401 Unauthorizedとなり、`turn.failed`後にadapterがexit 2で終了した。summaryは`status=failed`、`requested_slots=10`、`valid_slots=0`、`excluded_attempt_count=0`、wall time 25.504秒だった。modelはTaskSpecを処理しておらず、SAも起動していないため、prompt behaviorへ算入しない。

- frozen Evaluation set identity: `11829223f1a5370cdd68ceb5339aa945e9b118b29b23246de21bc5f5b35a2e35`
- global plan SHA-256: `8638e603f57b2ca25a3f2e1fcc39d4542f611594b7239ac60800ecfafd925b61`
- profile SHA-256: `bf2a3331ce60ab435b258d8a700c527609d9cf9439ce4b7322e46c23d28d12e7`

### 再実行preflight

認証回復後、失敗済みr1を変更せずr2を作成した。最初のfixture複製はfile / directory modeを保持しなかったため、freeze identityが期待値`11829223...`に対して`18046a95...`となった。比較前gateで停止し、model slotは0件だった。このr2も変更せず履歴として保持した。

r3は元の固定source setをpermission込みで複製した。freeze identityが期待値と一致し、同じprofile、prompt identity、2 case × 5 iteration、M=24、全capsule pathを機械確認してから発行した。

- frozen Evaluation set identity: `11829223f1a5370cdd68ceb5339aa945e9b118b29b23246de21bc5f5b35a2e35`
- global plan SHA-256: `92aaedd9be5e307edaacfbdbca9d406ed4474870a652fff1d961b39c613795ee`
- profile SHA-256: `bf2a3331ce60ab435b258d8a700c527609d9cf9439ce4b7322e46c23d28d12e7`

### r3成果とroute

| case | 期待値 | 正解 | 独立reviewer producer | root duplicate | forbidden context |
| --- | --- | ---: | ---: | ---: | ---: |
| HS01 | `blocked` | 5 / 5 | 5 / 5 | 0 / 5 | 0 / 5 |
| HS02 | `completion_ready` | 5 / 5 | 5 / 5 | 0 / 5 | 0 / 5 |
| 合計 | pairごとの期待値 | 10 / 10 | 10 / 10 | 0 / 10 | 0 / 10 |

r3は`valid=10 / excluded=0`、wall time 120.721秒だった。全runはroot sessionとその直系reviewer sessionの2 sessionで構成された。rootのcommandは開始identityとclean statusの確認だけで、review対象文書やdiffを読むcommandは0件だった。reviewerだけが許可文書とdiffを読み、required `git diff --check HEAD^^..HEAD^`は10 / 10でexit 0だった。

禁止したcontext記録の固有文言を全reviewer rolloutへ照合し、一致は0件だった。command collectorはnon-required read commandのexit binding不足等を11件diagnosticとして記録したが、required commandの成功と事前mechanism gateには影響しない。

## 現在地

- 確認済み: report-only task familyで、誤った実装・執筆経緯を渡さないB条件の精度優位がheld-outへ再現した。
- 確認済み: Bのproducerを情報封鎖した独立SAに置き換えても、同じ2 diffで10 / 10の精度を維持した。
- 確認済み: 明示TaskSpec下では独立reviewer producer 10 / 10、root duplicate 0 / 10、forbidden context delivery 0 / 10が成立した。
- 未確認: rootがreview要否とproducerを自律的に選べること。
- 未作成: prompt Candidate。
- 未実施: adoption、release、projection。

この試験はTaskSpecが独立SAを明示しているため、SA必要性または自律routingの証拠ではない。次は「review不要」「root reviewで十分」「情報封鎖した独立SAが必要」の3 routeを成果差から選ぶ自律routing case familyを別revisionで設計する。今回の明示producer TaskSpecをそのまま流用しない。
