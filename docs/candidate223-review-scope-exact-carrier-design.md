# Candidate223 review scope exact carrier 設計

## 状態

- `creation_gate_fixed`
- `candidate_creation_authorized`
- `evaluation_completed_failed_stopped`
- direct base: `Candidate147`
- evaluation input: `ADR9 r4`

## 結論

Candidate223は、C214で実証したreviewer側の経路閉鎖を不変条件として保ち、packet構築前のbootstrapだけをsource外のscope別exact carrierへ置き換える。

後続の固定ADR9 r4では、root deliveryとscope外readの閉鎖は成立したが、TaskSpecのscope-to-observation対応にsource内manifestへ存在しないobservation identityを含めたため、必要review 2件が開始前に停止した。本書の以下の内容は作成前に固定した設計として保持し、成立済みCandidateとして再利用しない。

閉じる辺は二つである。

```text
packetを作るためにroot valueが必要
  -> 同じcontainerのwhole-source outputもrootへ返せる

reviewに使い得るmanifest targetである
  -> 現在のrequired review scopeに不要でもreviewerへ返せる
```

sourceを読む前に、TaskSpecが`required review scope -> packet observation / reviewer direct observation`を一意に固定する。rootとreviewerは対応表へ列挙されたexact structural targetだけを、それぞれのrecipientへ受領できる。対応表にないmanifest target、container、ancestor、複数recipientの共同outputおよび受領後の選別は許可しない。

## direct baseと非継承

- direct prompt baseは`the-caption-3ce91a4-result-effect-scope-r1`（Candidate147）である。
- Candidate214の本文は継承しない。同Candidateで成立したreviewer側閉鎖を設計上の不変条件として再構成する。
- Candidate215からCandidate222までは失敗経路の証拠であり、prompt parentではない。
- Candidate222の`observation view`、Candidate221の集合分類、ticket、ownership宣言および成功runのread順を継承しない。

## Candidate作成前の検討gate

1. 必要reviewの完遂を目的とし、試験通過を目的にしない。
2. 最短正常経路は、rootがpacket用projectionだけを受領し、reviewerが当該scopeへ固定されたpacket非配送projectionだけを直接観測し、reviewer-owned terminal resultを返す経路である。
3. C214はreviewer側の閉鎖を示したが、root whole-source受領と正常carrier欠落を残した。
4. Candidate222はsource外carrierなしのconceptual viewで、ADR03からADR06の20 / 20件にmixed-owner root admissionを残した。
5. source外carrierの先行実験はroot配送を45 / 45件でexact projectionへ閉じたが、全scope共通のtarget和集合を許可したため、不要なdirect readと1件のreview未完遂を残した。
6. Candidate223はtarget和集合を作らない。required review scopeごとに必要命題とcarrierをsource外で固定し、対応表にないtargetを禁止する。
7. ADR03からADR06のreviewer direct carrierはinventoryとcontractsだけ、ADR07とADR09はpaired scopeだけ、review不要またはpermission deniedでは空集合とする。
8. missing targetを追加して期待terminalへ合わせない。成功runのtool順または判断順も義務化しない。
9. root whole-source、root reviewer-owned delivery、reviewerのscope外direct read、必要review欠落、root補完またはresult effect不一致はzero toleranceとする。
10. scope別carrierをsource読取前に一意に固定できない場合は、閉鎖を弱めず`candidate_not_created`とする。

## 変更する責務

Candidate147へ次の二条項を追加する。

- `PRECHANGE_REVIEW`: review要否、独立producer、packet、terminal support、result admissionおよび変更effect。
- `REVIEW_SCOPE_CARRIER`: source外のscope-to-observation対応、recipient別exact deliveryおよび未列挙targetのdefault deny。

## 評価境界

- Evaluation set: `the-caption-preimplementation-adversarial-design-review-r4`
- TaskSpec source: `preimplementation-adversarial-design-review-targeted-evaluation-design-r13`
- case revision: 全件`adversarial-design-review-r4`
- direct prompt base: Candidate147
- model / runtime / permission / rating / executor条件: ADR9 r2と同一
- 各case N=5、合計45件

品質、必要review完遂、root配送境界、reviewer配送境界およびresult effectを独立に判定する。一件でも不一致なら有効runを保持して停止し、ADR9 N=20、Standard14、採用、releaseまたはprojectionへ進めない。

## 非目標

- runtime、tool adapter、executorまたは外部wrapperの変更
- missing evidenceの追加
- case固有の期待結果またはselectorのCandidate本文への埋込み
- 採用、releaseまたは本体projection
