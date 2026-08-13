# Candidate209 名前付きcertificate欠損境界 実装監査

## 結論

Candidate209はCandidate208を直接基盤とし、root `AGENTS.md`の`TERMINAL`と`EVIDENCE_GATE`だけへ名前付きcertificate欠損と排他的観測依存を実装した。C208の`CONTEXT`、review適用、producer、packet封鎖、result effect、共同発行およびvalidation制御は保持している。

新しいreview順序、model-step barrier、operation、rootによる意味判定、manifest固有例外または評価条件は追加していない。後続のADR9 r2 N=5はScore `4 / 1 = 42 / 3`で品質不通過、機序不通過7件となった。現在状態は`quality_failed / mechanism_failed / stopped`であり、採用、releaseおよびprojectionは未判定である。

## identity

- prompt identity: `the-caption-3ce91a4-named-certificate-deficit-r1`
- direct base: `the-caption-3ce91a4-result-kind-evidence-domain-r1`
- bundle SHA-256: `4790214b24a560cfc34c93decde076cbf033c007ad8fd3f4533203d395c3925b`
- root `AGENTS.md` SHA-256: `19e8c5875e3f4d4c2b67a0f752b8afbdc26cd8cf38ce67d3449e1334734d7d86`
- root `AGENTS.md` Git blob: `59645097cc90e6a5b96b0cfbc145d31d7f19f32b`
- changed target: `AGENTS.md`だけ

## 実装対応

| C208制御群 | C209の置換 |
| --- | --- |
| `TERMINAL` | certificateを7 componentの有限集合として明示し、packetで現在unobservedなcomponentだけを`certificate_deficit`へ入れる。`review_unavailable`には原因observation、欠損component identityおよびobservationだけが同componentをbindできる排他的依存を要求し、missingによる事後生成を禁止した |
| `EVIDENCE_GATE` | 「未解決resultをbind可能」という広いread資格を削除し、manifest observationのsuccess conditionが名前付き欠損componentをbindでき、同じcomponentをbindするmodel-visible inputまたはadmission済みresultがない場合だけconsumerを開く。欠損集合が空なら全manifest observationのconsumerを閉じる |
| `CONTEXT` | 変更なし。manifestは全result共通の実行義務ではなく、projectionを`unobserved`へ戻さないというC208境界を保持 |

両置換は、terminal evidenceとread permissionが同じ排他的依存を消費するため分離不能である。片方だけでは、不要readまたはmissingからの不完全な`unavailable`のいずれかが残る。

## 構造診断値

| prompt | 文字数 | UTF-8 bytes | top-level条項 |
| --- | ---: | ---: | ---: |
| C208 | 10,498 | 15,386 | 14 |
| C209 | 10,898 | 16,018 | 14 |
| 差 | +400 | +632 | 0 |

増分は二つの既存条項へ閉じ、新しいtop-level条項を増やしていない。文字数当たりの価値は未評価であり、実試験前に改善とは判定しない。

## 手順化禁止監査

- certificate判定とmanifest observationを別operationまたは別model stepへ分離していない。
- 「先に」「成立しない場合だけ」「次に」という実行順序を追加していない。
- tool、read順、read回数またはretryを固定していない。
- `TC-ADR05`、`OBS-PAIRED-SCOPE`または特定pathをprompt本文へ入れていない。
- rootの`ROOT`責務を変更せず、Reviewer resultの意味判定、再構成または再採点を追加していない。
- 観測を開かない効果は、名前付き欠損を消費しない観測にconsumerが存在しないpermission境界として表した。

## 静的検証

- Candidate209集中テスト: `4 passed`
- Candidate208・Candidate209集中テスト: `11 passed`
- Candidate209結果記録後の全テスト: `1301 passed, 1876 subtests passed`
- bundle verification: 通過
- 非変更18 target: C208と同一
- 変更条項: `TERMINAL`、`EVIDENCE_GATE`だけ
- `git diff --check`（Candidate209対象path）: 通過

## 未実施

- ADR9累積N=20延長
- Standard14
- KPI比較
- 採用、releaseおよびTHE-CAPTION本体へのprojection

評価条件と停止条件は[作成前設計](candidate209-named-certificate-deficit-design.md)を正本とする。candidate bundleと静的検証の成立は、品質または機序の通過を意味しない。

## 後続のADR9 r2 N=5

45 / 45 valid、Score `4 / 1 = 42 / 3`だった。Score 1はすべて`TC-ADR07`で、反例certificateの欠損が空であることを全manifest consumerのfalseへ直結した結果、`no_counterexample_found`に必要なdirect observationを取得できず`unavailable`へ停止した。機序監査も、反例成立後read 3件、必要read欠落3件、missing未観測での架空success receipt 1件を含む7 runで不通過だった。

詳細は[ADR9結果](../evaluations/results/candidate209-named-certificate-deficit-adr9-r2-n5_2026-08-13.md)を参照する。
