# Candidate177 result invalidation locality 設計

## 目的

実行上まとめられた複数の観測について、一件の失敗が、意味上は独立して成立した別の判断証拠まで失効させる経路を閉じる。失敗の影響範囲をcommand、wrapper、workerまたはinvocationの外形ではなく、predicateが依存するevidence unitへbindする。

## 作成前ゲート

1. 基準prompt setは`the-caption-3ce91a4-decision-premise-counterexample-r1`（Candidate176）とする。
2. 基準状態の最短正常経路は、producerが反例を支える各観測へ独立したsuccess receiptを持ち、具体的反例を確定し、無関係な後続manifest欠落で失効させず`counterexample_found`を返し、rootが現designをrejectする経路である。
3. 保存済み誤経路はCandidate176 ADR05 N=50 run `79302c5e76874014bbcdf8f5d3304031`である。reviewerは反例を支える4観測を得たが、無関係なmissing targetを同じshell commandへ`&&`で束ね、aggregate exit code `2`のまま前半をsuccess receiptとして報告した。rootはresultを受理できず、期待する`blocked`ではなく`unavailable`となった。
4. Candidate176は確定済み反例を無関係なmissingで失効させない意味規則を持つが、複数のevidence identityを一つのaggregate statusへ統合できる条件と、失敗が無効化できる意味範囲を固定していない。このため既存TaskSpec、repository authority、repository stateだけでは実行上の集約が意味上の独立性を潰す経路を防げない。
5. 変更軸は`result locality` predicate一件とする。既存の「失敗resultは、そのresultが入力を変えたpredicateだけを失効できる」を、evidence unit、predicate dependency、result invalidation scope、safe aggregation、確定済みpredicateの局所的失効へ置き換える。
6. このpredicateは、executorがcommandやworkerの外形を根拠に、独立した成功観測と失敗観測を一括して成功または失敗へ読み替える判断点を消す。
7. 新たに増える判断点は、複数resultを一つのinvocationへ集約する前の`result_aggregation_safe`判定一件である。個別identity・status・receiptを保持する集約、または実行前に一つのevidence unit identityと一つのsuccess conditionへbindされた不可分観測だけを許可する。
8. 品質維持の確認対象は、直接失敗を観測したADR05、隣接するADR06・ADR07、独立producer過剰起動を監視するStandard14 F02とする。targeted評価前はexpanded評価へ進めない。
9. 期待と逆の結果として、個別receiptを保持した有効な集約まで禁止する、確定前の必要観測を打ち切る、失敗したchild resultをsuccessへ補完する、rootがproducerの証拠を再構成する、または既存4ケースのterminal・情報封鎖・producer機序が変わる場合は停止する。

## 一般predicate

`evidence_unit_identity := predicate identity / observationまたはresult identity / target / success condition / input snapshot identity`とする。

`evidence_dependency(predicate) := 当該predicateを確定するadmissible supportとして必要なevidence unit identityの集合`とする。

`result_invalidation_scope(result) := 当該resultが直接観測を試み、そのstatusがadmissible supportの成立可否を変え得るevidence unit identity、または当該resultがtargetもしくはinput snapshotを直接変更したevidence unit identityと、それらへ依存するpredicateの集合`とする。

`result_aggregation_safe := 発行前に、全child resultのidentity / status / receiptを独立生成するresult envelope contractへbind済み ∨ 発行前から一つのevidence unit identity / 一つのsuccess condition / 一つのresult_invalidation_scopeへbindされた不可分観測だけを一つのstatusにする`とする。

command、wrapper、worker、sessionまたはinvocationへ複数resultを入れること自体は許可するが、その外形だけでevidence unit identity、statusまたはinvalidation scopeを統合しない。`result_aggregation_safe=false`のresultを単一aggregate statusへ束ねて発行しない。aggregateがnon-successでも個別successを示すadmissible receiptは保持し、個別receiptがないpartial outputを元producer、rootまたはその他の主体がadmissibleなsuccess receiptへ昇格させない。

predicateがadmissible supportで`satisfied`または`unsatisfied`へ確定した後は、そのsupportのevidence unit identityを直接失効させるresultだけが状態を変更できる。artifact変更またはfailed / unavailable resultは`result_invalidation_scope`内だけを失効させ、別predicateまたは無関係なsupportへ伝播させない。

## 既存制御との接続

- `EVIDENCE_GATE`へ一般predicateを置き、変更前探索、review、validation、recoveryを含む全lifecycleへ適用する。
- `DESIGN_ADMISSION`の反例優先順位とresult admissionは変更しない。reviewerが使うmanifest observationも一般predicateのevidence unitになる。
- `DECISION_BOUNDARY`の同一model step発行は維持する。同一model stepでもchild result identityとreceiptを分離すればよく、tool call回数や逐次model stepを要求しない。
- `VALIDATION_CLOSURE`の一wrapper内個別commandは、各command resultを個別に保持するため許可される。
- rootはproducerが返さなかった個別statusやreceiptをaggregate outputから再生成しない。

## 非目標

- 特定case、fixture、manifest targetまたはshell commandへの分岐
- 一観測一tool callの強制
- 全evidenceの逐次実行
- Candidate176の反例定義、review要否、permission、producer binding、semantic projectionまたはroot result admissionの変更
- 採用、releaseまたはTHE-CAPTION本体へのprojection

## 状態

- design: `complete`
- adversarial_review: `no_counterexample_found`
- implementation: `complete`
- evaluation: `adr05_n20_quality_passed_mechanism_failed`
- adoption: `not_decided`
