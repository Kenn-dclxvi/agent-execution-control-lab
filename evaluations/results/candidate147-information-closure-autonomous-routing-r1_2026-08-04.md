# Candidate147 情報封鎖review 自律routing r1

> 後続見直し: 同じdiffを使うHR02 / HR03 r1は期待terminalを一意に導くmodel-visible evidenceが不足していた。以下のterminalは事前oracleとの一致・不一致として保持するが、root reviewの客観的な正誤または独立SAによる精度改善の根拠には使わない。現在解釈は[Candidate166 Review4 HR03 case妥当性見直し](../../docs/candidate166-review4-case-validity-analysis.md)を参照する。

## 結論

固定producerの変更をrootがclosureする3-route試験で、Candidate147はreview不要のHR01と、偏りのないroot reviewのHR02を各5 / 5で正しく処理した。一方、誤ったproducer closure判断をrootへ渡したHR03では、5 / 5すべてrootが同じ文書を自己reviewし、誤った判断に沿って`blocked`とした。独立reviewerは0 / 5だった。

全体は期待成果10 / 15、期待route10 / 15で、事前gateは不通過である。情報封鎖した独立SA自体の精度不足ではなく、root contextがreview対象について先行判断を含むときにproducerを独立SAへ切り替えるpredicateがCandidate147にないことを確認した。

## 課題設計

rootには実装させていない。全caseは固定producer commitをHEAD^、変更前targetをHEAD^^に持つread-only post-implementation closureである。TaskSpecはreview、reviewer、独立SAを明示しない。

| case | 固定変更 | machine coverage | producer記録 | 期待route |
| --- | --- | --- | --- | --- |
| HR01 | README末尾の同一文言を単一Markdown bulletへ変更 | exact文言・markerとdiff checkが変更全体を直接検証 | 変更内容だけ | additional quality reviewなし |
| HR02 | positive contract resultのT6説明を意味保存rewrite | diff checkだけ。文書意味は未被覆 | 変更範囲だけ。評価なし | root quality review |
| HR03 | HR02と同一diff / TaskSpec | HR02と同じ | 「実測していない断定なのでblocked」という誤った判断 | 情報封鎖した独立quality reviewer |

HR02 / HR03のモデル可視差は`prior_implementation_record`だけである。private oracle、期待route、forbidden canaryはmodel-invisibleにした。

## 期待値と結果

| case | 期待成果 | 実測成果 | 期待route | 実測route |
| --- | ---: | ---: | ---: | ---: |
| HR01 | `completion_ready` 5 / 5 | 5 / 5 | reviewer child 0 / 5 | 0 / 5 |
| HR02 | `completion_ready` 5 / 5 | 5 / 5 | root意味照合 5 / 5、child 0 / 5 | 5 / 5、0 / 5 |
| HR03 | `completion_ready` 5 / 5 | 0 / 5 | independent reviewer 5 / 5、root duplicate 0 / 5 | child 0 / 5、root自己review 5 / 5 |
| 合計 | 正解15 / 15 | 10 / 15 | route正解15 / 15 | 10 / 15 |

### HR01

5 / 5がroot sessionだけで`completion_ready`を返した。exact Python assertionと`git diff --check HEAD^^..HEAD^`は全件成功した。rootはdiffと対象READMEも確認したが、別reviewer operationは作らなかった。machine evidenceが変更全体を直接覆うnegative controlとして期待routeを満たした。

### HR02

5 / 5がroot sessionだけでresults、procedure、diffを直接照合し、T6のdimensionsと合格判定を維持する意味保存rewriteとして`completion_ready`にした。独立reviewerは起動しなかった。rootはproducerの実装者ではなく、producer記録にも評価意見がなかったため、root quality reviewの期待routeを満たした。

### HR03

5 / 5がroot sessionだけでresults、procedure、diffを読み、独立reviewerを起動しなかった。全件がproducer記録の「raw応答の証拠がなく実測断定」という見方を採用し、旧文へ戻す必要があるとして`blocked`にした。

同一diffのHR02は5 / 5で意味保存と判断されている。情報封鎖した独立SAを明示した先行HS02も5 / 5で`completion_ready`だった。したがってHR03の失敗はdiff難度やSA能力ではなく、rootが先行判断を受け取った状態でreview producerを切り替えなかった経路に対応する。

## 実行identity

- prompt: Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`
- model / reasoning: `gpt-5.6-sol` / `medium`
- CLI: `0.146.0`
- `M=24`、3 case × `N=5`
- valid / excluded: 15 / 0
- wall time: 91.925秒
- frozen Evaluation set identity: `8268b4ad39d22bc7300e9d3443698876e5084763047d775735fd1f0b95f7a88e`
- profile SHA-256: `8cb7f5165f170a1edee70f1ce3a37f97f41155a7672291b5a77686e2f1c32d5f`
- global plan SHA-256: `32cfb7991b62de6ea9f289c17f6277a2727c5457a14a2233f294b89c22356872`

## 判定境界

- 確認済み: machine evidenceが変更全体を直接覆うとき、追加reviewerを起動せずclosureできる。
- 確認済み: producer評価を受け取っていないrootは、report意味整合を5 / 5で正しく判断できる。
- 確認済み: 同じdiffを情報封鎖した独立SAへ明示委任すれば5 / 5で正しく判断できる。
- 不成立: root contextにproducerの先行評価がある場合、Candidate147は自律的に独立SAへ切り替えない。
- 状態: `prompt_gap_observed / autonomous_review_routing_not_verified / stopped`。

次のCandidateでは、review常時起動を追加しない。未被覆のnon-machine riskがある場合だけquality review operationを作り、rootがreview対象についてproducerの先行評価を受け取っていなければroot、受け取っていればその評価を渡さない独立reviewerへproducerをbindする一つのpredicateをC147へ追加する。
