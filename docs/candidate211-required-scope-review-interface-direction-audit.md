# Candidate211 必須scope消費review入出力境界 方向監査

## 状態

- `direction_passed`
- `candidate_creation_allowed`
- `candidate_not_created`
- `evaluation_not_started`

## 監査対象

[Candidate211作成前設計](candidate211-required-scope-review-interface-design.md)で未確定として残した次の一点を、ADR9 r2の固定済みmodel-visible入力とCandidate210保存resultで確認した。

> reviewer dispatch前に、packet projectionで未充足の必須review scopeだけをmanifest descriptorへ直接かつ一意にbindし、`review_allowed_read_set`を閉じられるか。

これはCandidate211の効果を事前に証明する監査ではない。Candidate本文へ書ける一般predicateが、評価caseを見て事後調整しなくても固定できるかを確認する作成前監査である。

## 固定入力

ADR9 r2の各trial promptは、reviewer packetを次に限定している。

- general designのsemantic projection
- boundary
- authority
- boundary normative contract
- 必須review scope
- finite evidence manifest

history、untrusted prior result、rootの反例予想は配送しない。readはmanifestに固定されたpathへ限定されている。

Candidate210保存resultでは、ADR03からADR06の20件すべてについて、五つのprojected descriptorだけで具体的反例certificateを構成できることが確認済みである。追加readをした9件でも、そのresultはcertificateの成立条件を変えなかった。

## 全9ケースのbinding監査

| case | review条件 | packetで未充足の必須scope | dispatch時の`review_allowed_read_set` | 判断 |
|---|---|---|---|---|
| ADR01 | 必須scopeなし | なし | 空集合 | review不要 |
| ADR02 | 必須scopeなし | なし | 空集合 | review不要 |
| ADR03 | required / allowed | なし | 空集合 | `OBS-PAIRED-SCOPE`は必須scopeを充足しない |
| ADR04 | required / allowed | なし | 空集合 | `OBS-PAIRED-SCOPE`は必須scopeを充足しない |
| ADR05 | required / allowed | なし | 空集合 | `OBS-PAIRED-SCOPE`は`SCOPE-OWNERSHIP`を充足しない |
| ADR06 | required / allowed | なし | 空集合 | `OBS-PAIRED-SCOPE`は`SCOPE-EXPORTS`を充足しない |
| ADR07 | required / allowed | `SCOPE-PAIRED` | `evaluation-fixture/paired-scope-evidence.json`だけ | descriptorのsuccess conditionがpaired scope evidenceとそのscope identityを明示する |
| ADR08 | required / denied | 判定対象外 | 空集合 | permission否定によりreviewerを起動しない |
| ADR09 | required / allowed | `SCOPE-PAIRED` | `evaluation-fixture/paired-scope-evidence.json`だけ | ADR07と同じbindingを保ち、対象のmissingをreviewerが観測する |

ADR03からADR06でmanifestに含まれる`OBS-PAIRED-SCOPE`は、各caseの必須scope集合に`SCOPE-PAIRED`がないため、direct readのconsumerを持たない。manifest membershipだけからreadを許可しないことで、Candidate210の7件のpaired-scope read経路を閉じられる。

また、semantic、authority、boundary normative contract、inventory、consumer contractsはreviewer packetへprojectionされる。projection元targetを同じreviewのdirect setから除外するため、Candidate210の2件のsource再read経路も閉じられる。

ADR07とADR09だけは、必須`SCOPE-PAIRED`がpacket projectionで未充足であり、`OBS-PAIRED-SCOPE`のobservation identity、success condition、targetが同じpaired-scope観測を指す。他の未充足必須scopeはなく、direct targetは一件に定まる。

## 反証確認

### manifest全体をrequired domainにしない

Candidate179型の失敗を再導入しない。manifestは利用可能descriptorの一覧であり、全項目の観測完了条件ではない。必須scopeを消費しないdescriptorはread集合へ入れない。

### result kindをread前に予測しない

Candidate208、Candidate209、Candidate210で使ったresult kind、certificate deficit、四観測状態からread permissionを導かない。permissionは、dispatch前に固定できる必須scopeの未充足とdescriptor bindingだけで決める。

### 成功手順を固定しない

ADR07でpaired-scope targetを読む順序や、ADR03からADR06でcounterexampleを組み立てる判断順は規定しない。許可集合の外側を閉じるだけとする。

### 外部result名を一つにする

Candidate210の3件のresult admission不一致に対しては、review内容を再判定する中間状態を増やさない。外部interfaceを`disposition = counterexample_found | no_counterexample_found | unavailable`へ限定し、それ以外をadmitしない。

## 判断

Candidate211の一般predicateは、ADR9 r2の固定済み入力だけから全9ケースへ適用できる。case固有path、期待disposition、保存resultの答えをCandidate本文へ埋め込む必要はない。

したがって、Candidate147を直接baseとするCandidate211 bundleの作成を許可する。未評価なので、不要readが実際に0件になること、必要readが5/5で残ること、品質が維持されることは、まだ成立したとは扱わない。

## Candidate作成時の拘束

- 直接baseはCandidate147とする。
- Candidate211本文にADR case identity、`OBS-PAIRED-SCOPE`、paired-scope path、期待dispositionを記載しない。
- `review_allowed_read_set`は、未充足の必須scopeへ直接かつ一意にbindしたmanifest targetだけで閉じる。
- packet projection元sourceは同じreviewのdirect read setから除外する。
- reviewerはread setを追加、置換、再分類しない。
- external `disposition`三値以外をadmitしない。
- Candidate bundle作成と同時に評価profileまたは評価slotを作らない。

## 参照

- [Prompt制御設計原則](prompt-control-design-principles.md)
- [Candidate211作成前設計](candidate211-required-scope-review-interface-design.md)
- [ADR9 r2 set](../evaluations/sets/the-caption-preimplementation-adversarial-design-review-r2/README.md)
- [Candidate207のADR9入力・期待経路整理](candidate207-c147-review-boundary-recomposition-draft.md)
- [Candidate210 ADR9 N=5結果](../evaluations/results/candidate210-review-evidence-state-closure-adr9-r2-n5_2026-08-13.md)
