# Portable full-agent kernel直接比較設計

> [!IMPORTANT]
> **状態**: `candidate_precreation_gate_fixed / direct_parent_c147 / measurement_control_r4_reused / c147_reference_bundle_registered / portable_candidate_bundle_registered / candidate_issued_14 / candidate_valid_14 / candidate_score4_7 / quality_failed / c147_reference_not_authorized / root_only_out_of_scope`

> [!NOTE]
> この状態はCandidate-first順序で実施した当時の記録である。後続監査で、semantic set自体をC147 referenceで先に資格確認する必要があると訂正した。C147は14 / 14 validだがScore 4が6 / 14となったため、現在は[`C147 reference先行資格確認r1結果`](portable-semantic-c147-reference-qualification-r1-result.md)を正とし、held-out r1をportable同等性比較へ使わない。

## 結論

portable full-agent kernelの効率は、control-freeとの絶対差ではなく、C147の既存full-agent一枚との直接比較で判定する。control-free r4は14 Caseすべてでschema、all-agent一次tokenおよびelapsedを取得できることを証明した測定基盤であり、品質はscore 4が5 / 14なので、品質維持後のcost比較基準にはしない。

直接の意味上の親は`the-caption-3ce91a4-result-effect-scope-r1`（Candidate147）である。比較用referenceは同identityの既存full-agent `AGENTS.md`一枚、比較対象はC147の81 primitiveをplatform非依存語へ再構成したfull-agent draft一枚とする。root-only、他platformへの配置、本文短縮および機能削除を同じ比較へ入れない。

## identityと役割

| 役割 | identity | bytes / SHA-256 | この比較での扱い |
| --- | --- | --- | --- |
| 測定成立control | `portable-semantic-a544769-control-free-r1` | 0 / `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | r4 resultを再利用し、再実行しない |
| 直接の親・効率reference | `the-caption-3ce91a4-result-effect-scope-r1` | 10,772 / `46ed3811aa798fec6356cf53feb7403ff15bf75c71a9c76af6d6893b05fb8fc7` | semantic targetへ別prompt identityとして登録してN=1を測る |
| portable比較対象 | full-agent draft。登録時に新しいtarget固有prompt identityを付与する | 10,781 / `3d3733a4ec0bb531a5be8eb53922e92fafe37b479b6190d24a8176ae452805e3` | 本文bytesを変更せずCandidate化してN=1を測る |

control-freeの失敗runはportable Candidateの親ではない。追加制御がない場合の反例であり、C147 referenceは意味保持と効率を比較する直接の親である。C204以降のportable/review Candidateも親にせず、成功したtool順、判断順またはreview固有条件を取り込まない。

## 保存済み反例と維持経路

control-free r4の正式resultで、14件中9件に次の問題経路を観測した。

| Case | 実際の問題経路 | portable本文で閉じるpermissionまたはdependency |
| --- | --- | --- |
| H01 | 未固定required outcomeの確認だけでなく、未開始operationを`unavailable`へ移した | outcome bindingとoperation stateを分離し、未固定値のclarificationだけを許可する |
| H03〜H05 | 許可済みconsumer、独立operationまたはprovenance不一致resultの効果範囲を誤った | observation consumer、result locality、actor result admissionを一意にbindする |
| H09〜H11 | 個別validation resultと集約operationを混同し、失敗後の後続または偽terminalを許した | validation plan、個別result admission、最初のnon-successで閉じる発行frontierを分ける |
| H13〜H14 | environment failureをterminal扱いし、許可されたexact recovery pairと禁止method substitutionを区別できなかった | recovery allowanceを同一operationのenvironment-only repairと同じrequired invocationへ限定する |

これらは文面から推測した失敗ではなく、[`control-free qualification r4`](../evaluations/targets/portable-instruction-semantic-conformance/results/portable-semantic-control-free-heldout-r1-n1-qualification-r4.json)の保存済み応答に対する固定graderの診断である。

H02、H06〜H08およびH12で成立した、bound outcomeを再確認せずactionへ進む経路、独立frontierの全件発行、能力欠落時のsubset発行禁止、同じnonterminal invocationの継続は維持する。Candidate本文へ成功時のtool順やmodel stepを転記せず、既存のoperation permission、dependency、result effectおよびterminalの意味だけを保持する。

## allowed delta

このCandidateは、一つの分離不能な再構成目的だけを扱う。

- C147の81 primitiveを削除または追加せず、platform名に依存しない`operation / actor / observation / frontier / validation / recovery`へ再表現する。
- 管理上は共通componentと`multi-actor` capability blockへ分ける。
- modelへ配送する成果物はcomponent参照を要求しない自己完結した一枚の`AGENTS.md`にする。
- C147で一つに結合していたactor binding、actor input、result admissionおよびcoordinator境界を、同じ正常経路を維持したまま依存関係で分ける。

許可しない差分は、primitiveの意味削除、Case別の正解route、tool順、product固有adapter、TaskSpec wrapper、case、oracle、rating、schema transport、token accounting、model、reasoning、permissionおよび実行方法の変更である。THE-CAPTION固有のtarget identity、repository layout、release状態および後続Candidateのreview条件は継承しない。

## 新しく増えるcostと対象外影響

portable draftはC147 referenceより9 bytes大きい。この静的差をcost退行または改善とは判定しない。新しい語彙定義とactor capability境界を理解するcostが増える可能性と、platform固有語の解釈や責務重複を減らす可能性を、all-agent `total_tokens`と`elapsed_seconds`で測る。

multi-actor能力がないsurfaceを`unavailable`へ閉じるroot-only本文は別Candidateとする。今回のfull-agent本文からworker条項を削る方法、両capability blockを同居させる方法、他platformのsurface bindingを同時に評価する方法は採らない。

## 比較条件と順序

1. C147 referenceとportable full-agent Candidateを、それぞれtarget固有の自己完結したprompt bundleとして登録する。
2. portable Candidateだけに、control-free r4と同じtarget、held-out r1、TaskSpec wrapper、oracle、rating、Codex CLI 0.146.0、GPT-5.6 Sol、reasoning `medium`、permission、instruction isolation、schema transport r3、token accounting v2およびelapsed境界をbindしたProfileを作る。
3. portable Candidateのprompt identity以外がcontrol-free r4と完全一致することをpreflight receiptで証明し、14 Case N=1を実行する。どのslotもpreflight前に発行しない。
4. portable Candidateが14 / 14 score 4を満たした場合だけ、同じ条件のC147 reference Profileと比較preflightを作り、不足するreference 14 Case N=1を実行する。Candidateがquality gateを通らなければreference Profileとrunを発行しない。control-freeは再実行しない。
5. 両方の全resultを受領してから、Case別quality、all-agent tokenおよびelapsedを対応づける。

## 判定と停止条件

- portable Candidateのpreflight不一致、未固定field、prompt bundle driftまたはruntime driftが一件でもあれば、Candidate slotを発行しない。後段のC147 referenceにも同じ独立preflightを要求する。
- schema不適合、一次token欠落、elapsed欠落または採点不能が一件でもあれば、その条件を`invalid`としてN拡張しない。
- portable Candidateにscore 4未満が一件でもあれば`quality_failed`としてN拡張しない。機序診断だけを独立した停止条件にしない。
- C147 referenceにscore 4未満があれば、portable Candidate自体のqualityは記録できるが、品質維持後の効率比較は`comparison_reference_not_qualified`として判定しない。
- 両条件が14 / 14 score 4の場合だけcost方向を判定する。portable Candidateのall-agent token中央値とelapsed中央値がともにC147 referenceより小さい場合だけ`cost_improvement_direction`とする。一方でも同値または増加ならN=5へ自動拡張しない。
- N=1の方向を安定傾向とは呼ばない。N=5は別の事前確認票で許可し、N=20はN=5の品質維持と両KPI減少を確認した後にだけ別途計画する。
- 評価成立、品質通過、cost方向、採用、releaseおよび各platformへのprojectionを別状態として保持する。

## 次のアーティファクト単位

本文を変更せず、C147 reference bundleとportable full-agent Candidate bundleをsemantic targetへ登録した。portable Candidateは14 / 14 validだったがscore 4は7 / 14でquality gateを通過しなかった。したがってreference Profile、比較preflightおよびslotは作成せず、直接の効率比較を未判定のまま停止する。詳細は[`quality gate r1結果`](portable-full-agent-candidate-quality-gate-r1-result.md)を正本とする。
