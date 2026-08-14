# Candidate224 review source exclusive authority 方向監査

## 状態

- `direction_review_completed`
- `direction_failed_after_dynamic_observation`
- `candidate_creation_authorized`
- `ADR9_r2_completed_stopped`

## 結論

Candidate224の設計方向は、C214の過剰遮断を条件付きreadで緩める案ではない。pre-review sourceを一般repository evidence authorityから外し、root projectionとreviewer observationを排他的なsource access operationへ置き換える。これにより、一般`target artifact`権限からroot whole-source readへ到達する辺を削除し、同じcontainer内のpacket非配送manifest targetはreviewer固有carrierとして残す。

作成前の静的方向監査では通過とした。ただし後述の動的結果により、経路閉鎖としては反証済みである。

## 誤経路監査

| 誤経路 | 設計上の扱い |
|---|---|
| rootがpacket構築を理由にsource全体を取得 | pre-review sourceを一般`EVIDENCE_GATE`から除外し、root projection operation以外に権限を与えない |
| whole outputを受領して必要値だけpacket化 | observable outputが有限projectionへ閉じないため発行不可 |
| rootがreviewer observation targetを先読み | targetのresult recipientがreviewerへ固定され、root projectionとの重複も禁止 |
| reviewerがpacket sourceを別selectorで再取得 | root projectionとの同一・祖先・子孫・重複targetをreviewer setから除外 |
| reviewerがsource container全体を取得 | exact manifest targetではなくancestorを含むため発行不可 |
| 同じcontainer内の必要値まで一律遮断 | container一致を禁止条件にせず、projectionとの構造重複だけを閉じる |
| 将来の変更やvalidationでpre-review root authorityを開く | review terminal前は別operationのauthorityを伝播させない |

## C215からC223を親にしない理由

- C215からC220の必要性、operand、ownership、ticketまたはobservable outputの自己分類を継承しない。
- C221とC222の追加viewは一般`EVIDENCE_GATE`と併存した。Candidate224はview名を追加せず、pre-review sourceのauthorityを一般operationから除外する。
- C223のscope別carrier contractと変更済み評価入力を使用しない。

## 正常経路への影響

- review不要時はreviewerを作らない。
- permission deniedではartifact変更へ進まない。
- packetに許可された値はroot projectionとして取得できる。
- packetと重ならないmanifest exact targetはreviewerが直接取得できる。
- reviewer-owned terminal resultだけがresult admissionと対応変更へ接続する。

必要値の取得をcontainer一致で禁止しないため、C214の同一container過剰遮断を再導入しない。

## 評価境界

後続評価を行う場合は、Candidate214と同じADR9 r2全9ケース、TaskSpec、fixture、oracle、rating、model、runtime、permissionおよびexecutor条件をそのまま使う。新しいcase revision、TaskSpec revision、scope mappingまたはmissing evidenceを作成しない。

## 動的結果

変更していないADR9 r2では、必要reviewerは30 / 30で起動したが、必要な判断結果は28 / 30に留まった。packet case 20 / 20でroot reviewer-owned prereadとmixed-owner admissionが残り、reviewer direct observationは9 / 20だった。

したがって、作成時に想定した排他的source authorityは動的経路閉鎖として反証された。同じsource containerからroot packet literalとreviewer observationを分離するprompt上のoperation定義は、rootへwholeまたはmixed-owner outputを返すread能力を実行不能にしなかった。固定ADR9 r2とprompt-onlyの範囲では、C214の閉鎖を弱めず正常carrierを開く次Candidateは作成しない。

- [Candidate224 ADR9 r2 N=5結果](../evaluations/results/candidate224-review-source-exclusive-authority-adr9-r2-n5_2026-08-14.md)
