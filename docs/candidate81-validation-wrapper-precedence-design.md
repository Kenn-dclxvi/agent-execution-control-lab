# Candidate81 validation wrapper precedence設計記録

## 結論

Candidate81はCandidate71を直接sourceとする。Candidate71の11 labelを維持し、`VALIDATION_CLOSURE`一行だけを置換する。

同一課題に対するprompt-onlyの動作安定化を目的とする。root producerのrequired validationについて、TaskSpecまたはcommand evidence protocolの「順に」「1 commandずつ個別」を、1回のcustom exec wrapper内における発行順と個別invocationの指定として解釈する。command間でresultをmodelへ返し、別custom tool callで次commandを発行する意味ではないと固定する。

## Candidate作成前gate

1. 基準prompt setは`the-caption-3ce91a4-validation-closure-r1`（Candidate71）とする。最短正常経路は、artifact変更後に完全なrequired-validation集合をbindし、root producerが一つのwrapper内で各commandを個別実行し、nonzeroで後続を止め、完了済み全resultを一度だけmodelへ返す経路である。
2. 保存済みCandidate80、Rating v13、Medium、F04、protocol v1 `N=10`では1-step closureが9 / 10だった。失敗したiteration 5は「指定順」「まず依存関係」と記述し、`npm ci`、lint、buildを3回のトップレベルcustom tool callへ分割した。
3. Candidate80はroot wrapper方法を固定したが、後段のTaskSpecとcommand evidence protocol v1にある「順に」「1 commandずつ個別」とwrapper方法の関係を定義しなかった。そのため、各command resultをmodelへ返してから次を発行する逐次解釈を排除できなかった。
4. 置換する一つのpredicateは、`validation_set_ready=true ∧ producer=root`の場合、「順に」「個別」をwrapper内の発行順・invocation単位として解釈し、command間のmodel再入を禁止することである。全required validationは1回のcustom exec wrapper内からbind順の個別`exec_command`として発行する。
5. このpredicateが消す判断点は、後段の「順に」「個別」をwrapper内部実行またはトップレベル逐次実行のどちらへ対応付けるかというmodel判断である。個別invocation、個別exit、fail-stop、全result一括返却は維持する。
6. 新しいlabel、case固有command、TaskSpec、adapter、protocol revisionは増やさない。増えるのは後段表現に対する解釈規則である。promptがTaskSpecとprotocolの語句へ依存する点は新しいriskとして残る。
7. 成果品質はCandidate71とCandidate81をRating v13、Medium、F04 r2、command protocol v1、各`N=10`の互換条件で確認する。両条件とも10 / 10 valid・rateable・score `4`、required validation欠落0、protocol違反0、zero driftを必須とする。
8. 主判定は1-step closure率とする。Candidate81の10 / 10を成功条件とする。token、elapsed、tool call、message数は診断として記録するが、prompt安定性の合否条件にしない。
9. 1-step closureが10 / 10未満、score `4`未満、required validation欠落、protocol違反、順序違反、workspace driftのいずれかがあれば停止する。Candidate81へ補助predicateを追加せず、同じ課題のprompt安定化成功を主張しない。

九項目を定義済みであるため、Candidate81のbundle、C71 / C81互換profile、構造testを作成できる。

## 変更境界

- direct source: Candidate71
- 置換: root `AGENTS.md`の`VALIDATION_CLOSURE`一行
- 非変更: 残り18 target、TaskSpec、case、rating、permission、executor parameter、command evidence protocol v1、THE-CAPTION runtime
- evaluation scope: F04 r2、Medium、各`N=10`のprompt安定性試験だけ
- adoption / release / runtime projection: 未実施

## Candidate状態

- candidate number: Candidate81
- prompt identity: `the-caption-3ce91a4-validation-wrapper-precedence-r1`
- evaluation status: [`standard14_evaluated / quality_gate_passed / prompt_stability_gate_passed`](../evaluations/results/candidate71-candidate81-validation-wrapper-precedence-v13-medium-standard14-n5_2026-07-26.md)
- state: `standard14_evaluated`
- targeted result: 1-step closureはCandidate71の5 / 10に対して10 / 10。品質は両条件とも10 / 10 score `4`。required command欠落、protocol違反、順序違反、workspace driftは0件。
- standard14 result: 70 / 70 score `4`。複数required command caseの1-step closureはCandidate71の30 / 35に対して35 / 35。差はF04の0 / 5から5 / 5。

## Evidence

- [Candidate71設計](candidate71-validation-closure-design.md)
- [Candidate80結果](../evaluations/results/candidate71-candidate80-root-validation-wrapper-v13-medium-f04-n10_2026-07-26.md)
- [Candidate81対象試験結果](../evaluations/results/candidate71-candidate81-validation-wrapper-precedence-v13-medium-f04-n10_2026-07-26.md)
- [Candidate81標準14項目結果](../evaluations/results/candidate71-candidate81-validation-wrapper-precedence-v13-medium-standard14-n5_2026-07-26.md)
- [command protocol v1 / v2診断](../evaluations/results/candidate71-command-protocol-v1-v2-v13-medium-f04-n10_2026-07-26.md)
- [Prompt制御の検討原則](prompt-control-design-principles.md)
