# Candidate200後 review入力分割方向review

## 結論

設計方向はCandidate実装へ進める。blocking counterexampleは0件である。許可はC147直接childの作成と静的検証までであり、評価スロット発行には別の評価設計とcomparison preflightを必要とする。

## 確認結果

- Candidate200の17件を、review入力ownerの未分割という一原因で全件説明できる。
- `root_projection`と`reviewer_observation`は同一観測identityを共有せず、全required inputを被覆する。
- rootは投影entryの値取得だけを行い、review judgementを代行しない。
- reviewerは自分に割り当てられたexact targetだけを読み、projected sourceを再読しない。
- missing targetを起動前不足にせずreviewer observation resultへ残すため、ADR09の`unavailable`経路を閉ざさない。
- forbidden inputをowner分割前に除外し、packetへkey、value、要約、存在状態のいずれも配送しない。

## 退けた方向

- Candidate200を直接親にする: 失敗機構を継承するため不採用。
- reviewerへ`design-admission.json`の再読を許す: Candidate199の禁止input漏洩を戻すため不採用。
- rootが全観測を読み、要約だけ渡す: reviewer-owned observationをrootが代行するため不採用。
- 入力不足時にrootが補完して再dispatchする: 同一subjectのterminal review再開と責任混同を作るため不採用。

`M3_passed / blocking_counterexample_0 / candidate_implementation_allowed / evaluation_not_authorized`
