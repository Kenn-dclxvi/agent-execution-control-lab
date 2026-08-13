# Candidate204 portable execution core 実装監査

> [!IMPORTANT]
> **状態**: `candidate204_created / M4_static_verification_passed / not_evaluated / adoption_not_decided / release_not_created / projection_not_performed`

## 結論

Candidate204 `the-caption-3ce91a4-portable-execution-core-r1`を、Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`の直接child full bundleとして作成した。

変更targetはroot `AGENTS.md`一件だけである。C147の13条項をM2で固定した12責任へ全置換し、Review responsibility、Codex固有field名、API名、待機identity、会話継承指定およびcommand配送方式を本文から外した。他の18 targetはCandidate147 release snapshotと同一bytesであり、`prompts/review.md`は0バイトのまま保持する。

bundleの存在は、評価済み、採用済み、release済みまたはprojection済みを意味しない。

## Identity

- candidate number: Candidate204
- prompt identity: `the-caption-3ce91a4-portable-execution-core-r1`
- direct semantic parent: `the-caption-3ce91a4-result-effect-scope-r1`（Candidate147）
- source full bundle: `the-caption-3ce91a4-result-effect-scope-release-r1`
- bundle SHA-256: `d9c90d877e97479d95e5be51306111b221dd7e53c5c921e14599fb39df1faf5e`
- changed target: `AGENTS.md`
- unchanged target count: 18
- evaluation status: `not_evaluated`

Candidate190〜Candidate203は保存trace上の反例だけを供給し、親子関係、条項またはReview responsibilityを継承しない。

## 実装した12責任

1. `OUTCOME`
2. `PRODUCER`
3. `INPUT`
4. `INVOCATION`
5. `RESULT_ADMISSION`
6. `RESULT_EFFECT`
7. `IMPLEMENTATION`
8. `COMPLETION`
9. `VALIDATION_PLAN`
10. `VALIDATION_CLOSURE`
11. `METHOD`
12. `RECOVERY`

候補本文は[`M2設計`](c147-review-free-portable-core-design.md)の`PORTABLE_CORE`範囲と逐語一致する。M2修正後のmethod resultとpredicate resultの分離も反映済みである。

## C147からの差

| 項目 | C147 release | Candidate204 | 差 |
|---|---:|---:|---:|
| root本文bytes | 10,772 | 6,346 | `-4,426`（`-41.09%`） |
| 制御条項 | 13 | 12 | `-1` |
| changed target | - | 1 | `AGENTS.md`だけ |
| Review用prompt | 0 bytes | 0 bytes | 変更なし |

M3で計測した6,314 bytesはMarkdown marker間のcore本文だけである。Candidate bundleの6,346 bytesは見出しと改行を含む実ファイル値なので、同じ測定値ではない。

## 本文から除外した表面語

Candidate204のroot本文には、次を含めない。

- `review`
- `Codex`
- `root` / `worker`
- `fork_turns`
- `FINAL_ANSWER`
- `runtime_spawn_result`
- `custom exec` / `exec_command`
- `cell ID`
- `model step` / `modelへ戻らず`
- `environment_recovery_max`

意味として必要なinput sufficiency、producer provenance、nonterminal continuation、individual validation closureおよびrecovery authorityは、特定表面語を使わず12責任へ保持する。

## 変更していないもの

- Standard14 case、fixture、TaskSpec、rating contract。
- model、reasoning、permission、実行環境、executor behavior、token accounting。
- root以外の18 bundle target。
- Candidate147のrelease、evaluation result、adoption、projection state。
- Candidate203以前のbundle、profile、result。

## M4静的検証

次を全件successにする。

1. manifestを再計算してbundle identityが一致する。
2. M2のportable core範囲とCandidate204 root本文が逐語一致する。
3. 12 labelが一回ずつ順番通りに存在する。
4. 禁止表面語がroot本文に0件である。
5. C147 releaseとの差が`AGENTS.md`一件だけである。
6. `prompts/review.md`が0バイトである。
7. `git diff --check`が通過する。

7項目はすべて通過した。設計文書とCandidateの静的testは9 / 9 passed、`git diff --check`も通過した。

## 次のgate

M4通過後、M3で固定したF01 / F02 / F03各N=5の[評価設計](candidate204-portable-execution-core-f01-f02-f03-n5-evaluation-design.md)とprofileを作成した。比較前receiptが`ready`になるまでは評価slotを発行しない。targeted qualityまたはportable mechanismが一件でも不通過ならStandard14へ進めない。

## 参照

- [`c147-review-free-portable-core-causal-reclassification.md`](c147-review-free-portable-core-causal-reclassification.md)
- [`c147-review-free-portable-core-design.md`](c147-review-free-portable-core-design.md)
- [`c147-review-free-portable-core-direction-audit.md`](c147-review-free-portable-core-direction-audit.md)
- [`Candidate204 manifest`](../prompts/candidates/the-caption-3ce91a4-portable-execution-core-r1/manifest.json)
