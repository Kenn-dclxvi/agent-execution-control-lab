# Candidate200後 C147直接基盤review入力分割設計

## 結論

次CandidateはCandidate147を直接親とし、変更前reviewへ必要な有限観測を`root_projection`と`reviewer_observation`へ重複なく全件分割する。Candidate200で成立したprojected source閉鎖とexact reviewer read setを保持し、必要入力を閉じ過ぎた失敗だけを除く。

## 基準と非目標

- 直接親: Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`
- 反例証拠: Candidate200のrequired reviewer欠落14件とpacket投影不足3件
- 非目標: Candidate200のprompt機構継承、closed source再読、rootによるreview judgement、Standard14実行、採用、release、projection

## 正常経路

1. 開始identityをTaskSpecどおり確認する。
2. C147の変更前evidenceで一つの変更predicateをbindする。
3. 明示reviewが適用される場合、review criterionを閉じる`required_review_input_manifest`を固定する。
4. manifest全entryを`root_projection`または`reviewer_observation`へ一意に割り当てる。
5. rootは前者だけを取得し、値とprovenanceをpacketへ投影する。後者は読まない。
6. reviewerは後者のexact targetだけを直接観測し、projected sourceを読まない。
7. reviewerのterminal resultをidentity、sender、観測、result kindへbindし、対応変更だけへ効果を適用する。

## 変更するpredicateと責任

`START_BOUNDARY`と`PRECHANGE_REVIEW`をC147へ追加し、`EVIDENCE_GATE`の変更直結遷移だけを条件分岐へ置換する。`PRECHANGE_REVIEW`では次を一つの分離不能な閉包として固定する。

- applicability、permission、operation identity、producer、criterion、result kind、consumer
- `required_review_input_manifest`
- `projection_input_set`と`reviewer_observation_read_set`の排他的かつ完全な分割
- projection completeness、value/provenance投影、forbidden input除外
- reviewerに対するprojected source閉鎖、exact read、mixed read禁止
- judgement、result admission、対応変更だけへのresult effect

分割だけを別Candidateへすると、read閉鎖またはresult admissionのない中間状態ができるため分離しない。

## 事前反例

| 状態 | 期待 |
|---|---|
| manifest entryが未割当て | reviewerも変更も発行せず`unavailable` |
| 同一entryが両ownerへ重複 | reviewerも変更も発行せず`unavailable` |
| root projection entryのvalueまたはprovenance欠落 | reviewerも変更も発行せず`unavailable` |
| rootがreviewer observation targetを先読み | result admission不成立 |
| reviewerがprojected sourceを部分read | result admission不成立 |
| exact targetとclosed sourceのmixed read | invocation全体をinadmissible |
| forbidden inputがpacketへ混入 | reviewerを起動しない |
| descriptor固定targetがmissing | reviewer自身のnon-value observationとして扱う |

## 評価と停止

最初の挙動評価はADR9 r2全9ケース各5件、合計45件に固定する。Score 4が45 / 45、reviewer cardinality、input partition、projection completeness、exact read、result admission、result effect、開始identity、required command、forbidden input境界が全件一致した場合だけ次段階を検討する。一件でも不一致ならresultを保持して停止し、Standard14へ進めない。

`M2_complete / c147_direct_base / finite_input_partition / projected_source_closed / ADR9_first_gate / Standard14_not_started`
