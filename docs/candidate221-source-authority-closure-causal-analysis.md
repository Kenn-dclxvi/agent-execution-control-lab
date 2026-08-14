# Candidate221 source authority closure 原因分析

## 状態

- `analysis_completed`
- `candidate221_quality_failed`
- `candidate221_mechanism_failed`
- `candidate221_not_adopted`
- `next_candidate_redesign_required`

## 分析対象

Candidate221で解こうとした課題は、Candidate214実行時の消費・admission監査で成立した二つの局所閉鎖を維持しながら、同Candidateが遮断した必要なreviewer観測だけを回復できるかである。

Candidate214の当時の監査は、packet作成元sourceのreviewer再readとrootによるreviewer-owned値のadmissionを0件と判定した。一方で、packetへ実際に投影した範囲ではなくsource container全体を閉じたため、ADR03、ADR05およびADR06の4 runでcurrent inventory membershipまたはconsumer contractをreviewerが観測できず、期待`blocked`が`unavailable`になった。後続のdelivery境界監査で、初回whole-source result自体はrootへ配送されていたことが判明している。

したがって課題は、readの必要性を正しく判断させることではない。source取得前に、次の値と経路を相互に重ならない形で固定することである。

- rootがreviewer packetを構築するために取得できる値と、そのcarrier
- reviewerが直接観測する値と、そのread authority
- root自身のoperationに必要な値と、そのobservable output
- いずれへも一意に固定できない場合の`unavailable`への停止

## Candidate221で検証した仮説

Candidate221はCandidate147を直接基盤とし、TaskSpecが列挙するpacket permissionとfinite evidence manifestから、次の三集合をrepository evidence発行前に分離できると仮定した。

1. packetへ投影できるtarget
2. root-owned operationのtarget
3. reviewerが直接観測するtarget

この仮説が成立するなら、rootはpacket構築に必要なexact regionだけを取得し、reviewerはpacketへ運べないmanifest上のexact targetだけを直接観測できる。whole-source resultが複数ownerの値を含む場合はrootへ返せないため、Candidate214で観測したreviewer-sideの局所閉鎖を保持しながら過剰遮断だけを解消できるはずだった。

## 実行結果

ADR9 r2 N=5は45 / 45 valid、除外0件で完了した。Score 4は29 / 45、期待terminal一致は29 / 45、成果物境界一致は42 / 45、required command一致は12 / 15だった。

機序では、ADR03からADR06の20 / 20 runでrootがreviewer-owned targetを先行取得し、同じ20 / 20 runでmixed-owner resultを受領した。必要なreviewer direct observationは7 / 20、ADR03からADR06の期待terminal一致も7 / 20だった。source authorityを含む全機序の通過は16 / 45にとどまった。

一方、review不要時のreviewer起動とmanifest外readはともに0件で、forbidden canary deliveryも0件だった。これらは局所的な成立として保持するが、root whole-source routeの再開を相殺しない。

## 原因

失敗経路は次のとおりである。

```text
TaskSpecのpacket permissionとmanifest targetを参照する
  -> whole design containerをroot operationの合法なtargetへ分類する
  -> root whole-source readを発行する
  -> reviewer-owned inventory / contractsを含むresultをrootが受領する
```

Candidate221は三集合を定義したが、各repository targetがどの集合に属するかを、発行前に機械的なauthorityで固定しなかった。モデルはwhole design containerを`root_operation_set`へ含めることができ、その分類に基づくwhole-source readもCandidate本文へ準拠した操作として構成できた。

したがって、失敗原因はownerや集合の記述不足ではない。禁止対象を合法な集合へ再分類できるpermission edgeが残っていたことである。これは、C218のownership、C219のconsumer ticket、C220のobservable output closureと同じく、read authorityの成立をモデル自身の意味判断へ委ねた構造である。

## 得られた知見

### model-visibleであることはcarrierを固定しない

TaskSpecから値またはtargetを確認できること、finite manifestにtargetが記載されること、repository readが一般に許可されることは、その値をpacketへ運べること、rootが受領できること、reviewerが直接読むことのいずれも単独では決めない。

### packet構築権限とsource取得権限は別である

rootがreviewer packetを構築する責任を持っていても、その責任からpacketの元source全体を取得する権限は導けない。packetへ運べる値とrootへ返せるobservable outputが閉じていなければ、正しいpacket構築目的でもmixed-owner resultを取得できる。

### 集合を増やしてもtarget帰属が自己判断なら経路は閉じない

producer別の集合名、owner、ticketまたはoutput closureを追加しても、modelがtargetを集合へ割り当て直せるなら、禁止対象を合法なoperation targetへ含められる。静的に集合が排他的に見えることは、実行時のpermission closureを証明しない。

### 受領後の無視または非admissionでは遅い

reviewer-owned値がrootへ配送された時点で経路閉鎖は不成立である。rootがその値を判断に使わないこと、resultを非admissionにすること、後から不要部分を捨てることは、先行取得の修復にならない。

### 局所改善と核心機序を相殺しない

不要reviewer起動0件、manifest外read 0件、forbidden canary delivery 0件は個別の観測として有効である。しかし、事前にzero-toleranceとしたroot reviewer-owned prereadが20 / 20で再発したため、Candidate221の品質、KPIまたは局所改善を採用根拠へ昇格しない。

### 静的方向監査は動的な強制可能性を代替しない

作成前監査ではTaskSpecのpacket permissionとmanifest targetから必要carrierを一意化できると判断した。実行結果は、target帰属自体がmodel-side classificationとして残ることを示した。Candidate作成前の意味上の排他性と、保存trace上の失敗operationが実行不能であることを別々に確認する必要がある。

## 現行frontierへの反映

Candidate221はCandidate214で観測したreviewer-sideの局所閉鎖を保持できなかったため、次Candidateの親にしない。Candidate221と同じ三集合または自己分類条件へlabelや確認順を追加した案も作成しない。

現行frontierで保持できるのは、Candidate214で実証したpacket構築後のreviewer再read閉鎖と別containerの必要観測である。root初回deliveryは未閉鎖であるため、次の設計へ進む前に、少なくとも次を一次アーティファクトとmodel-visible inputから固定する必要がある。

1. invocationがrootへ返せる正確なobservable output。
2. outputを受領できるproducerと、packetへ運べる値の対応。
3. reviewer-owned値を含むwhole-container requestを、目的または必要性に関係なく違法にするauthority境界。
4. その境界を閉じた後も、ADR03、ADR05およびADR06の必要値がreviewerへ到達する合法なcarrier。
5. target帰属をmodelの読後分類、owner宣言、ticketまたは処理順へ委ねないこと。

これらを固定できない設計案は`prompt_control_not_demonstrated / candidate_not_created`として棄却する。ただし、問題全体の検討終了とは扱わない。owner、read対象の粒度、packet構築およびrootへ返るoutputの構造を再分解し、Candidate214のreviewer-side局所境界を維持しながら初回deliveryも閉じる別案の検討へ戻る。

## 後続のdelivery境界監査による限定

この文書でいうCandidate214の二つの経路閉鎖は、Candidate214実行時に固定した消費・admission監査の範囲を指す。後続のseal済みrollout再監査では、Candidate214でもrootがreview開始前に`design-admission.json`全体を受領しており、ADR03からADR06の20 / 20 runでpacket配送禁止のinventoryとcontractsがroot outputに含まれていたことを確認した。

したがって現在は、Candidate214からpacket構築後のreviewer再read閉鎖と別containerの必要観測だけを保持し、root初回whole-source deliveryまで閉じたとは扱わない。次のfrontierは、reviewer readを後から開く条件ではなく、最初のsource取得からroot projectionとreviewer direct observationを別carrierへ固定する`source bootstrap projection`である。詳しくは[`review carrier bootstrap authority監査`](review-carrier-bootstrap-authority-audit.md)を参照する。

## 状態境界

この分析はCandidate221の評価結果を変更しない。Candidate221は`quality_failed / mechanism_failed / stopped`であり、ADR9 N=20、Standard14、採用、releaseおよびprojectionは未実施のままである。局所的に成立した観測も、Candidate221の採用または一般的効果を意味しない。

## 一次参照

- [Candidate221 ADR9 r2 N=5結果](../evaluations/results/candidate221-review-source-authority-closure-adr9-r2-n5_2026-08-14.md)
- [Candidate221品質監査](../evaluations/results/candidate221-review-source-authority-closure-adr9-r2-n5-quality-audit-r1.json)
- [Candidate221機序監査](../evaluations/results/candidate221-review-source-authority-closure-adr9-r2-n5-mechanism-audit-r1.json)
- [Candidate221作成前設計](candidate221-review-source-authority-closure-design.md)
- [Candidate221方向監査](candidate221-review-source-authority-closure-direction-audit.md)
- [Candidate214経路閉鎖の再制御方針](candidate214-route-closure-recontrol-direction.md)
- [Prompt制御の検討原則](prompt-control-design-principles.md)
- [review carrier bootstrap authority監査](review-carrier-bootstrap-authority-audit.md)
