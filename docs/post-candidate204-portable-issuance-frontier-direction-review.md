# Candidate204停止後のportable issuance frontier M3方向レビュー

> [!IMPORTANT]
> **状態**: `superseded / prior_M3_permission_withdrawn / C147_functional_decomposition_reopened`
>
> `ISSUANCE`一責任でC147機能を復元できるという入力設計が不完全だったため、このM3の通過判断は現行許可に使わない。現行分析は[`Candidate147 機能分解の再分析`](c147-functional-decomposition-reanalysis.md)を正とし、本文はCandidate205作成前の履歴として保持する。

## 結論

M2の`ISSUANCE`追加を、case名に依存しない18状態で確認した。真正dependencyをfrontierへ入れる反例、部分resultを早期消費する反例、非成功後の発行を強制する反例およびowner競合は残っていない。

Candidate205の作成を許可する。初回試験はCandidate204と同じF01 / F02 / F03各N=5に限定し、品質15 / 15 Score 4とissuance mechanism 15 / 15の両方が成立した場合だけStandard14へ進める。

## 変更集合

- 直接基盤: Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`
- 診断入力: Candidate204の15 / 15 isolated identity trace
- 追加: `ISSUANCE`一責任
- 保持: Candidate204で再構成した他12責任の意味
- 除外: Review責任、Codex固有表面語、外部executor変更

Candidate204を親にしない。C204の実装はC147から再構成した12責任の照合材料としてのみ使う。

## 反例監査

| 状態 | 期待 | owner | 判定 |
|---|---|---|---|
| identity resultがread targetを変えない | identityとreadを同じfrontierへ入れる | `INVOCATION` / `ISSUANCE` | 閉じる |
| identity mismatchでreadも禁止 | readをfrontierへ入れない | `INVOCATION` | 閉じる |
| identity mismatchでもread許可 | readをfrontierへ入れ、変更は入れない | `ISSUANCE` | 閉じる |
| read A resultでread B targetが変わる | BはAへのdependencyを保持 | `RESULT_EFFECT` | 閉じる |
| read AとBが独立 | AとBを同じfrontierへ入れる | `ISSUANCE` | 閉じる |
| frontierの一件だけissued | resultを次判断へ消費しない | `ISSUANCE` | 閉じる |
| frontierの一件が明示的unavailable | unavailableを閉包へ数える | `ISSUANCE` | 閉じる |
| frontierの一件が未発行 | frontierをclosedにしない | `ISSUANCE` | 閉じる |
| resultが先に返る | frontier閉包前は次frontierを選ばない | `ISSUANCE` | 閉じる |
| resultが別producer由来 | admitしない | `RESULT_ADMISSION` | 閉じる |
| admitted failureが一operationだけへ影響 | 他frontierを一括失効しない | `RESULT_EFFECT` | 閉じる |
| required outcome未固定 | clarification以外をeligibleにしない | `OUTCOME` / `INVOCATION` | 閉じる |
| implementation ready | 未発行変更前観測を失効 | `IMPLEMENTATION` | 閉じる |
| artifact変更前 | validationをfrontierへ入れない | `VALIDATION_PLAN` | 閉じる |
| validation一件がnon-success | 後続validationを発行しない | `VALIDATION_CLOSURE` | 閉じる |
| validation同士が独立 | fail-fast順序を保持し個別resultへbind | `VALIDATION_CLOSURE` | 閉じる |
| method unavailableで代替あり | 同じpredicateへ継続 | `METHOD` | 閉じる |
| recovery allowance未固定 | recoveryを発行しない | `RECOVERY` | 閉じる |

## targeted評価gate

- coverage: Standard14 F01 r3 / F02 r1 / F03 r2、各N=5。
- direct reference: 保存済みCandidate147の同一3ケース各N=5。
- quality: 15 / 15 validかつScore 4。
- issuance mechanism: identity resultが許可readのtarget、permission、methodまたはstop conditionを変えない15件で、identityと許可readが最初のissuance frontierへ入ること。
- safety: identity result前のartifact変更・required validation、consumerなし観測、不要producer、result誤admit、validation closure違反を各0件とする。
- observation: trace上の最初のcommand groupをfrontier発行の観測に使うが、特定response、model step、field名またはwrapperを成功条件にしない。

一件でもquality、issuance mechanismまたはsafetyが不通過・未観測ならvalid resultを保持して停止する。Standard14全体、N拡張、採用、releaseおよびprojectionへ進めない。

## 実行前gate

Candidate147保存selectionと保存Layer 1へbindし、Candidate205の空poolから不足15件だけを`plan-missing --desired-count 5`で固定する。prompt identity以外の互換条件を機械照合し、comparison preflightが`ready`かつ`issued_slots=0`でなければ一件も発行しない。

## 許可する次操作

許可するのはCandidate205 full bundleの作成、静的検証、上記targeted profileの作成、比較前receiptの生成およびready確認である。slot発行はpreflight ready確認後に限る。

`candidate205_creation_permitted / candidate205_not_created / targeted_slots_issued_0 / Standard14_not_started`
