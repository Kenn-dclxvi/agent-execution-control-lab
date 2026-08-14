# Candidate221 review source authority closure 方向監査

## 状態

- `direction_passed`
- `candidate_creation_allowed`
- `candidate_created`
- `evaluation_completed`
- `direction_assumption_refuted_by_execution`

## 監査結果

ADR9 r2のTaskSpecとfixtureを全9ケース確認した。packet permissionは有限なvalue classを直接列挙し、finite evidence manifestは独立review producerのobservation identityとexact structural targetを固定し、root substitutionを禁止する。C214の4品質失敗で必要だったinventory / contract targetはmanifestへ固定される一方、packet permissionには含まれない。

したがってroot用packet projectionとreviewer direct observationをsource内容の読後分類ではなく、TaskSpecの発行前権限で分けられる。rootはpacket許可targetをexact regionとして取得できるため、whole-source権限を削除してもpacket construction routeは残る。reviewerはpacket非許可かつmanifest固定のexact targetだけを直接観測できるため、C214が遮断したADR03、ADR05、ADR06の必要値へ到達できる。

## 反例監査

| 状態 | 結果 |
|---|---|
| rootがwhole containerをrouting / readiness用に読む | reviewer targetと重なるため禁止 |
| rootがpacket許可targetだけを読む | exact root targetとして許可 |
| reviewerがpacket投影元を別selectorで読む | region overlapにより禁止 |
| reviewerがpacket非許可のmanifest exact targetを読む | exact reviewer targetとして許可 |
| target ownerまたはcarrierが曖昧 | 集合へ追加せず`unavailable` |
| history / untrusted resultを含む共同output | forbidden targetと重なるため禁止 |
| review不要またはpermission denied | reviewer direct authorityを開かない |

`model-visible`、read permission、target artifact、manifest membershipまたは正しい目的だけではproducer権限を作らない。受領後の無視や非admissionでも補わない。成功runのtool順、具体的selectorまたは確認手順は固定していない。

## 判断

作成時には、Candidate214の閉鎖を保持し、必要carrierをTaskSpecのpacket permissionとmanifest targetから発行前に一意化できると判断した。この判断に基づき、Candidate147直接baseのCandidate221作成を許可し、効果はADR9 r2 N=5で判定することにした。

## 実行後の訂正

ADR9 r2 N=5では、ADR03からADR06の20 / 20 runでrootによるreviewer-owned targetの先行取得とmixed-owner admissionが発生した。TaskSpecのpacket permissionとmanifest targetはvalue classを記述していたが、whole design containerを`root_operation_set`へ含める自己分類を実行不能にはしなかった。

したがって「source内容の読後分類ではなくTaskSpecの発行前権限で分けられる」という作成時判断は、静的なCandidate作成可否判断としては用いたが、動的な経路閉鎖として反証された。Candidate221はC214の閉鎖を保持できず、次Candidate作成根拠にはしない。

## 参照

- [Candidate221作成前設計](candidate221-review-source-authority-closure-design.md)
- [Candidate214経路閉鎖の再制御方針](candidate214-route-closure-recontrol-direction.md)
- [Candidate221 ADR9 r2 N=5結果](../evaluations/results/candidate221-review-source-authority-closure-adr9-r2-n5_2026-08-14.md)
