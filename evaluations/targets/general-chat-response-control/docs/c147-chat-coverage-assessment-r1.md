# C147チャット向けcoverage評価 r1

## 結論

現在の`general-chat-response-control`系列は、C147の知見を満たす統合チャットプロンプトとしては未成立である。

`RequiredValueCarrier r1`が通過したのは、単発・外部toolなし・分担なしの固定8 Caseにおける局所評価である。保存済みresultはこの局所効果の有効な証拠として保持するが、C147の13制御を網羅したこと、統合Candidateが成立したこと、採用可能になったことの証拠には使わない。

現在状態を次へ固定する。

```text
measurement_qualified
local_slice_passed
c147_chat_coverage_incomplete
integrated_candidate_not_created
overall_evaluation_not_started
adoption_not_eligible
release_not_created
projection_not_authorized
```

## 判定対象

C147原文は[`the-caption-3ce91a4-result-effect-scope-r1`](../../../../prompts/releases/the-caption-3ce91a4-result-effect-scope-release-r1/files/AGENTS.md.txt)の13制御とする。現在のチャット評価は、[`runtime capability`](../contracts/codex-cli-0.146.0-chat-semantic-r1.json)により一回応答、外部toolなし、multi-agentなしへ限定されている。

評価時にモデルへ渡した制御は、0 byte baselineまたは3文のCandidateだけではない。[`TaskSpec wrapper`](../contracts/task-spec-wrapper-r1.txt)が、質問、根拠要求、受領済み根拠、独立論点および自然な本文に関する共通制御を持つ。したがって、既存resultからCandidate本文単体の総合能力を主張しない。

## 対応表

| C147制御 | チャット向けrequired effect | 現在の直接評価 | 現在判定 |
| --- | --- | --- | --- |
| `SPEC` | 利用者だけが決められる未確定値だけを質問し、任された表現・手段は自律的に選ぶ | `GCR-Q01`は利用者所有値の質問を扱う。成果値とmethod choiceの対向Caseはない | `partial` |
| `PRODUCER` | 同じ判断または結果生成を複数担当へ重複発行しない | multi-agent無効 | `uncovered` |
| `TERMINAL` | 必要な回答、tool resultまたは担当resultが欠けた状態を完了で補わない | 一回応答の話題完了だけを扱う。nonterminal invocationはない | `partial` |
| `CONTEXT` | 担当へ判定可能な必要十分情報だけを渡し、無関係な全履歴を渡さない | worker packetなし | `uncovered` |
| `EVIDENCE_GATE` | 回答を変え得る根拠だけを取得し、十分な受領済み根拠を再取得しない | `GCR-E01/E02`は静的な根拠選択を扱う。実tool、追加read、state invalidationはない | `partial` |
| `OWNER_ROLE` | 情報や判断の所有者名と実行担当を混同しない | 分担なし | `uncovered` |
| `ROOT` | 他担当のpredicateまたはresultをrootが再生成して補わない | 分担なし | `uncovered` |
| `INDEPENDENCE` | 一つの不足や失敗で独立した話題を止めない | `GCR-I01/P01`で応答レベルの部分回答を扱う | `partial` |
| `DECISION_BOUNDARY` | 受領resultの影響範囲だけを止め、相互非依存の後続を維持する | `GCR-I01/P01`で話題の影響範囲だけを扱う。tool発行境界はない | `partial` |
| `VALIDATION_CLOSURE` | 必要確認を固定単位で発行し、失敗時だけ後続を止め、結果受領後に一度だけ完了判断する | validation invocationなし | `uncovered` |
| `VALIDATION_PLAN` | 完了に必要な確認を開始前に固定し、成功後の追加確認を発行しない | validation planなし | `uncovered` |
| `METHOD` | 利用者が指定した手段だけを固定し、未指定手段は目的を変えず許可範囲で選ぶ | method choiceの対向Caseなし | `uncovered` |
| `RECOVERY` | environment-only failureを内容失敗と分け、同じ目的へ復旧する | failureとrecoveryを含む会話なし | `uncovered` |

`RequiredValueCarrier r1`は、C147の13項目を置き換える14番目の総合制御ではない。baselineで観測した「保持必須値を回答へ運ばず、その値に依存する話題を完了する」一経路だけを閉じる局所差分であり、現在判定は`local_slice_passed`である。

## 既存resultの扱い

- [`ChatControlFree N=1 r4`](../results/chat-control-free-core-r1-n1-qualification-r4.json)は測定成立の証拠とする。
- [`ChatControlFree baseline N=5`](../results/chat-control-free-core-r1-n5-baseline-r1.json)は固定8 Caseのbaseline観測とする。
- [`RequiredValueCarrier core N=5`](../results/required-value-carrier-core-r1-n5-r1.json)と[`targeted N=20`](../results/required-value-carrier-core-r1-q02-n20-r1.json)は局所差分と既存7 Caseの保持結果とする。
- いずれもC147チャット版のcoverage pass、統合Candidate、採用、releaseまたはprojectionへ昇格させない。
- write-once result、当時のscoreおよび当時の局所gate名は変更しない。現在解釈は本書とREADMEで追加する。

## coverage gate

統合Candidateを作成する前に、少なくとも次の能力領域を別々の対向Caseへ固定する。

1. 単発応答: `SPEC`、応答レベルの`TERMINAL`、保持必須値、自然な利用者向け本文。
2. tool利用: `EVIDENCE_GATE`、`DECISION_BOUNDARY`、`METHOD`、tool resultを含む`TERMINAL`、`RECOVERY`。
3. 分担: `PRODUCER`、`CONTEXT`、`OWNER_ROLE`、`ROOT`、producer単位の`INDEPENDENCE`。
4. 複数段階の完了: `VALIDATION_PLAN`、`VALIDATION_CLOSURE`、途中resultと最終resultの区別。

各領域では、必要な正常経路と閉じる失敗経路を先に固定する。Case、oracle、runtime capability、model-visible inputおよび合格条件がそろう前に、統合Candidateを作成または評価しない。

## 次の許可範囲

coverage architectureは[`C147チャット向けcoverage architecture r1`](../../../../docs/general-chat-c147-coverage-architecture-r1.md)へ固定した。既存の一回応答targetを維持し、実tool、分担、途中result、継続、validationおよびrecoveryを観測する`general-chat-agentic-control`を別targetとして登録できるかを先に設計する。

次に許可するのは同targetの登録前設計であり、既存Candidateへの制御文追加、既存resultの再解釈、target descriptor作成、Case freeze、評価slot、総合N拡張、採用、releaseまたはprojectionではない。
