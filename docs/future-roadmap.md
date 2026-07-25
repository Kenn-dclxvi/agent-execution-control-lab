# 今後の使い方と発展方針

このリポジトリは、プロンプト文面の良し悪しを感覚的に決める場所ではなく、AIエージェントの実行制御が成果品質、token、最終結果までの時間、実行経路へ与える影響を再現可能に測る実験基盤として使う。改善対象は文章量そのものではなく、worker起動、context継承、model再入、read、validation、停止、result bindingなどの実行上の判断点である。

この文書は恒久的な方針を扱う。現在未完了の個別項目（label監査の再測定、`P3`削除candidate、A01 variation、未解決riskなど）は[`research-backlog.md`](research-backlog.md)へ集約する。

### 基本的な改善サイクル

1. 現行のtarget repository ref、prompt identity、model、Agent環境、TaskSpec、permission、fixture、evaluation set、rating contract、反復条件を固定する。
2. 保存済みtraceから、一つの誤経路または余剰経路を選ぶ。将来起こりそうという推測だけで新しい制御を追加しない。
3. 既存のTaskSpec、repository authority、repository stateでは防げない理由と、残す最短正常経路を定義する。
4. 一つのcandidateで一つのpredicateだけを追加、置換、削除する。prompt変更と評価条件変更を同じ比較単位へ混ぜない。
5. まず対象control pathのtargeted試験を行い、成果品質と狙った実行経路の変化を確認する。成立した場合だけ標準評価と継続反復へ進む。
6. 3 KPIの`quality_score`、all-agent `total_tokens`、`elapsed_seconds`を保存する。tool call、model step、worker routing、context継承、失敗traceはdiagnosticとして確認し、KPIを増やさない。
7. 評価結果、採用、release、本体反映を別のgateとして記録する。評価基盤はwinnerまたは採用可否を出さない。

### 評価setの役割と育て方

標準評価setは、既存制御の回帰とcandidate間の互換比較に使う固定基準とする。tuningに使ったcaseを同じrevisionのheld-out evidenceとして扱わず、caseの入力、fixture、採点条件を変更する場合は既存revisionを上書きしない。

新しいcaseまたはvariationを追加する根拠は、既存setでは識別できない失敗が保存traceで見つかった場合、または新しいcontrol pathを既存caseで観測できない場合に限定する。caseは単に難しくするのではなく、競合する失敗仮説を分離できるように設計する。

個別caseのvariation設計は、この方針に沿った未完了項目として[`research-backlog.md`](research-backlog.md)へ置く（現在はA01の3択variationが該当する）。

低頻度の誤経路は少数反復で不在を証明しない。targeted試験でfixtureと採点を確認した後、必要な反復数と継続Batchを固定し、発生条件、選択値、理由分類、影響範囲を保存する。

### modelとruntime更新時の使い方

model、reasoning設定、Agent、CLI、memory、tool protocol、runtimeが変わる場合は新しいprofile revisionとして評価する。異なるmodelまたはruntimeのresultを同一compatibility comparisonへ混ぜず、それぞれの条件内でcontrol-free、現行prompt、candidateの差を測る。

この反復により、model能力の向上で自然に不要になった制御、引き続き効率や安全へ寄与する制御、新しいruntimeでは逆にcostを増やす制御を区別する。制御の必要性をmodel世代の印象で判断せず、同じcase familyと保存traceで更新する。

### prompt制御からruntime制御への発展

安定して効果が確認された機械的な制御は、自然言語promptへ永久に積み増すのではなく、型付きTaskSpec、permission gate、scheduler、validation DAG、artifact revision、producer identity、result validity、terminal stateなどのruntime機構へ移す候補とする。

移行時は、prompt-only条件、runtime強制条件、control-free条件を同じ評価setで比較する。runtimeへ移した結果、品質を維持したままprompt読解cost、model step、再read、再試行を減らせた場合に限り、prompt側の重複predicateを削除する。promptは実行境界の宣言へ寄せ、機械的に強制できる状態遷移はruntimeへ寄せる。

### 採用判断の考え方

有限回の試験で将来の挙動を100%保証することを採用条件にしない。残余riskは、観測頻度だけでなく、実利用での影響、検出可能性、回復可能性、不可逆操作の別gate、運用上の確認手段と合わせて扱う。

採用判断では、互換条件、score分布、3 KPI、case別結果、実行経路diagnostic、未解決risk、運用上の検出・回復手段、rollback identityを一つのevidence packageとして確認する。大きな効率改善と低頻度で回復可能な誤経路が共存する場合も、評価上の状態を変更せず、人が用途と運用条件に基づいて別途判断する。
