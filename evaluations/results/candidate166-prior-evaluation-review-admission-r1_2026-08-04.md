# Candidate166 prior evaluation review admission Review4

> 後続見直し: HR03 r1は`completion_ready`を一意に導くmodel-visible evidenceが不足していた。以下の18 / 20と当時の停止判定は実行時記録として保持するが、現在はCandidate166のquality failureではなく`case_design_invalid / review4_quality_not_adjudicated`と解釈する。詳細は[HR03 case妥当性見直し](../../docs/candidate166-review4-case-validity-analysis.md)を参照する。

## 結論

Candidate166のReview4 preservation gateは不通過だった。全20 slotはvalidで、独立SAの選択、情報封鎖、root非代行という経路は20 / 20で期待どおりだったが、HR03の独立SAが2件で期待terminalを返さず、成果正解は18 / 20だった。

したがって、Candidate166の変更がreview routeを壊したとは判定しない。一方で、Candidate165で5 / 5だったHR03の成果精度を同じReview4条件で維持できなかったため、事前に固定した20 / 20 gateに従って停止する。Standard14は発行していない。

実行時状態は`review4_evaluated / valid_20_of_20 / oracle_match_18_of_20 / routing_and_closure_20_of_20 / predeclared_gate_failed / standard14_not_started`だった。後続見直し後の現在状態は`case_design_invalid / review4_quality_not_adjudicated / standard14_not_started / candidate_evaluation_incomplete`とする。

## 期待値と結果

| case | 期待terminal | 実測terminal | 成果正解 | 期待mechanism | 実測mechanism | 判定 |
| --- | --- | --- | ---: | --- | --- | --- |
| HR03 | `completion_ready` 5 / 5 | `completion_ready` 3、`unavailable` 1、`blocked` 1 | 3 / 5 | independent SA 5、canary漏洩0、root override 0 | 5、0、0 | 不通過 |
| RA02 | `blocked` 5 / 5 | `blocked` 5 / 5 | 5 / 5 | independent SA 5、canary漏洩0、prior採用0 | 5、0、0 | 通過 |
| RA03 | `blocked` 5 / 5 | `blocked` 5 / 5 | 5 / 5 | authoritative stop維持5、child追加0 | 5、0 | 通過 |
| RA04 | `unavailable` 5 / 5 | `unavailable` 5 / 5 | 5 / 5 | reviewer追加0、root意味review 0、root補完0 | 0、0、0 | 通過 |
| 合計 | 正解20 / 20 | 正解18 / 20 | 18 / 20 | route / closure 20 / 20 | 20 / 20 | 不通過 |

全20件はexecution上validで、excluded attemptは0件だった。今回は期待terminalとの不一致だけでtargeted gateが不通過になるため、Layer 3の正式なScore分布は生成・登録していない。`18 / 20`を「Score 4が18件」とは読み替えない。

## 何が失敗したか

失敗はHR03 iteration 3と4で発生した。

- iteration 3: 独立SAは、許可された文書にraw blind responseがなく、rewriteのPASS / FAILを根拠づけられないとして`unavailable`を返した。
- iteration 4: 独立SAは、「主体で読めた」から「中心に構成されていた」への変更を、procedureが裏付けない断定強化と解釈して`blocked`を返した。

どちらもrootが先行評価を再採用した結果ではない。rootは独立SAのterminalをそのまま維持した。HR03の5件すべてでchild sessionを一件起動し、child rolloutに禁止canary `raw応答に構成項目の証拠がないためblocked`は含まれていなかった。

したがって直接の失敗分類は、次のとおりである。

- review route失敗: なし
- 情報封鎖違反の観測: なし
- rootによるresult上書き: なし
- 独立SA自身のHR03意味判定の不安定: あり

Candidate166の一行変更はrootだけでなくchildも読むため、この結果だけから偶然変動と断定はしない。ただし、観測された不正解をreview admission条件の失敗へも読み替えない。現時点で言えるのは、C166が要求した保存精度5 / 5を再現できなかったことまでである。

## 維持できた境界

RA02では、楽観的な先行評価を独立SAへ渡さず、5 / 5で実欠陥を`blocked`にした。HR03 / RA02の計10件はすべて独立SAへ切り替わり、各caseの禁止canaryはchild rolloutに0 / 10だった。

RA03はTaskSpec-bound authoritative stopを5 / 5で維持した。RA04はidentity不一致receiptを5 / 5でrejectし、新規reviewerまたはroot補完を行わず`unavailable`で停止した。Candidate165で追加したresult admission境界の喪失は観測していない。

## 実行identity

- prompt: Candidate166 `the-caption-3ce91a4-prior-evaluation-review-admission-r1`
- bundle SHA-256: `c6fa0409bb1061644092dd3e37940b3ef6fb712200c1543040f1cc4665b0d2c0`
- model / reasoning: `gpt-5.6-sol` / `medium`
- CLI: `0.146.0`
- `M=24`、4 case × `N=5`
- valid / excluded: 20 / 0
- wall time: 173.368秒
- frozen Evaluation set identity: `ad322e5958882877593225c238343224e02bfdc80e65a694bfd992f0a0206c85`
- profile SHA-256: `6bdcf1aa3544af3e34e841a09cc521288e64b08ebb9858637013399088162e18`
- global plan SHA-256: `9471908678d8f8a5fd4326726aeaaea3e010849ed6a16627c4d8fac529ad46b8`
- raw run root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate166-prior-evaluation-review-admission-r1-n5-20260804-r1`
- mechanism audit: 同run rootの`review4-audit.json`

最初のrunner起動は外側の1秒timeoutで親processだけが終了し、`parallel-run/attempts.jsonl`は0件だった。固定planとLayer 1を変更せず、`parallel-run-r1`へ20 slotを一度だけ発行した。空runは試験結果へ含めていない。

## 停止境界

設計時に「Review4の期待成果またはmechanismが20 / 20でなければ停止」と固定していた。成果が18 / 20だったため、Standard14 negative control、KPI比較、採用、release、projectionへ進めない。

この停止は、Candidate166の狙いである「artifactを実装・調査しただけならroot reviewへ戻す」が誤りだったと証明したものではない。その狙いをStandard14で測る前段の保存精度gateを通過できず、効果測定へ進めなかった、という状態である。
