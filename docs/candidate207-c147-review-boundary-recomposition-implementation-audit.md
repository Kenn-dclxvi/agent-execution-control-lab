# Candidate207 C147 review境界再構成 実装監査

## 結論

Candidate207は`ADR9_completed / quality_passed / mechanism_failed / stopped`である。Candidate147を直接複製し、root `AGENTS.md`だけへ作成前監査で固定したreview境界接続を実装した。非root 18 target、symlinkおよび`DECISION_BOUNDARY`を含むC147の非変更条項は維持したが、ADR9でpacket反例成立後のdirect readを12 / 20件抑止できなかった。

## identity

- prompt identity: `the-caption-3ce91a4-c147-review-boundary-recomposition-r1`
- direct base: `the-caption-3ce91a4-result-effect-scope-r1`
- bundle SHA-256: `b37800172decfd0b44e161bbb69fe36a3bb24d7271d68e946966f09014516bed`
- root `AGENTS.md` SHA-256: `f3a4bcf98de95344ff468e9ba494c659904d1fd87998928a0bf920a4b56f6e90`
- root `AGENTS.md` Git blob: `7607a727b42fc5397aa6925b2a3e43989e460252`
- changed target: `AGENTS.md`だけ

## 実装対応

| C147制御群 | 実装した差分 |
| --- | --- |
| `PRODUCER` | `producer_execution_required(operation)`へapplicabilityとpermissionの条件付きbindingを追加 |
| `OWNER_ROLE` | 上記predicateがtrueの場合だけ明示producerを起動 |
| `CONTEXT` | review packetの許可・禁止membershipとmanifest descriptor / reviewer observation所有権を追加 |
| `TERMINAL` | projected counterexampleと三review terminal certificateを追加 |
| `EVIDENCE_GATE` | packet上counterexample成立を否定条件にしたdirect observation consumerとreview result dependencyを既存`implementation_bound`へ追加 |
| `REVIEW_BOUNDARY` | supplied boundary recordだけからreview requirement stateをbindする一predicate群を追加 |

## C147保持監査

- target数はC147とC207で19件ずつである。
- manifest entryが異なるtargetはroot `AGENTS.md`一件だけである。
- `SPEC`、`ROOT`、`INDEPENDENCE`、`DECISION_BOUNDARY`、`VALIDATION_CLOSURE`、`VALIDATION_PLAN`、`METHOD`、`RECOVERY`はC147と逐語一致する。
- `CLAUDE.md`およびpath-local `CLAUDE.md`のsymlink構造はC147と同一である。
- Candidate名、case ID、fixture path、期待terminal、Scoreはroot制御本文に含めていない。
- `admitted_evidence_current`、台帳構築、projection receipt、acknowledgement、revision loop、review result kind別operationは含めていない。

## 構造診断値

| prompt | 文字数 | UTF-8 bytes | top-level条項 |
| --- | ---: | ---: | ---: |
| C147 | 7,090 | 10,772 | 13 |
| C207 | 10,290 | 15,024 | 14 |
| 差 | +3,200 | +4,252 | +1 |

文字数減少または増加を合否条件にしない。C206比では本文量を減らしたが、削減自体を効率改善とは扱わず、review非適用経路の実測負担をStandard14の3 KPIと保存traceで判定する。

## 評価境界

ADR9 r2 N=5はC147保存N=50 poolから再選択したN=5 resultを比較基準にし、prompt identity以外の互換条件が一致した後に不足45件を発行した。45 / 45 Score 4だったが機序gateが不通過だったため、Standard14を開始せず停止した。詳細は[評価結果](../evaluations/results/candidate207-c147-review-boundary-recomposition-adr9-r2-n5_2026-08-13.md)を参照する。

## 静的検証結果

- Candidate207集中テスト: `28 passed, 226 subtests passed`
- profile index生成後の索引集中テスト: `11 passed`
- Candidate207 profile・結果記録後の最終全テスト: `1288 passed, 1874 subtests passed`
- 最初の全テストで検出した二件は、同じ作業ツリーですでに追加済みだったCandidate206 N=20 profileが索引未生成だったことによる。正規generatorで索引を再生成し、最終全テストで解消した。

## 一次参照

- [本文案・作成前監査](candidate207-c147-review-boundary-recomposition-draft.md)
- [保存trace事前反証](candidate207-c147-review-boundary-recomposition-direction-review.md)
- [検証計画](candidate207-c147-review-boundary-recomposition-plan.md)
