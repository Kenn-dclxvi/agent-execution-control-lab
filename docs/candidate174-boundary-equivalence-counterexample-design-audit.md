# Candidate174 境界同値instance設計の敵対的監査

## 結論

一般修正を必要とする具体的反例を確認したため、Candidate174設計をrejectした。prompt bundle、profile、Target評価resultは作成しない。

## 監査対象

- `docs/preimplementation-information-sealed-adversarial-design-review-spec.md`
- `docs/preimplementation-adversarial-design-review-targeted-evaluation-design.md`
- `docs/candidate174-boundary-equivalence-counterexample-design.md`

監査では、fixture名、case ID、期待terminalを設計根拠にせず、一般入力での偽陽性と偽陰性を優先して確認した。

## 具体的反例

設計案は、一般設計が境界判断へ使うものとして固定した属性から`boundary_relevant_signature`を作り、二instanceのsignatureが完全一致し、contractまたはauthorityに区別根拠がなければ反例を成立させる。

しかし、一般設計が正当な区別属性を見落としている場合、その属性はsignatureへ入らない。さらに、contractまたはauthorityが許容される全区別属性を閉じていなければ、現在読めた範囲に記載がないことから不存在を導けない。

具体的には、選択済み`consumer-a`と除外された`consumer-d`で、観測済みの`contract_identity=sync-v1`、`schema=v1`、`stop_capable=true`が一致していても、別の適用authorityに`lifecycle=managed | external`があり、stop適用を`managed`だけに許す場合がある。そのauthorityが未観測、manifestでmissing、または許可scope外なら、二instanceを同値とする根拠は不足している。正しい結果は`unavailable`であり、`counterexample_found`ではない。

この設計案では同値反例をmanifest不足より先に確定できるため、正当な区別を一般設計の反例として誤検出する。

## 一般修正条件

同値反例を安全に使うには、次の全条件が必要である。

- 先行固定contractまたはauthorityが、対象boundaryで許される全区別属性またはpredicateを限定列挙している。
- その閉じた属性集合とprovenanceが一般設計より前に固定されている。
- 比較する両instanceの全属性値が許可済みsuccess receiptへ結び付いている。
- 明示的なsame-treatment predicate、または閉じた全区別属性の一致が、一般設計による異なる扱いと直接矛盾する。
- 区別domainの閉包または関連receiptが不足する場合は`unavailable`とする。

この条件は、contract名、open境界、未観測instanceの可能性だけから反例を作らないCandidate173の制約を維持する。

## 固定Targetとの不整合

ADR03、ADR04、ADR06のmodel-visible入力には、選択・適用されたinstanceと除外されたinstance、および同じcontractラベルがある。一方で、そのcontractが同じ扱いを要求する規範predicate、または扱いを区別できる属性domainの閉包は固定されていない。

したがって、一般修正条件を守るCandidateはこれらを`counterexample_found`へ一意に結び付けられない。反対に、同じcontractラベルだけで反例を成立させるCandidateは、上の具体的反例で偽陽性になる。ADR07に除外instanceがないことだけでは、この一般入力上の欠陥は解消しない。

これはCandidateの判定境界だけでは閉じられず、Target評価の入力資格に不足があることを示す。固定試験へ合わせるためのCandidate実装は行わず、試験を改訂する場合は新revisionとしてsame-treatment predicateまたは区別属性domainの閉包を追加し、Candidate実装前に独立資格監査を行う必要がある。

## 状態

- Candidate174 prompt: `not_created`
- Target評価: `not_started`
- Standard14: `not_started`
- adoption / release / runtime projection: `not_decided / not_created / not_projected`
