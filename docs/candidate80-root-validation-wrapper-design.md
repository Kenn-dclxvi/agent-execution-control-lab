# Candidate80 root validation wrapper設計記録

## 結論

Candidate80はCandidate71を直接sourceとする。Candidate71の11 labelを維持し、`VALIDATION_CLOSURE`一行だけを置換する。

同一課題に対するprompt-onlyの動作安定化を目的とし、root producerが完全にbind済みのrequired validationを1回のcustom exec wrapper内から列挙順の個別`exec_command`として発行する方法をpromptへ直接固定する。adapter、TaskSpec、command evidence protocol、caseは変更しない。

## Candidate作成前gate

1. 基準prompt setは`the-caption-3ce91a4-validation-closure-r1`（Candidate71）とする。最短正常経路は、artifact変更後に完全なrequired-validation集合をbindし、root producerが一つのwrapper内で各commandを個別実行し、nonzeroで後続を止め、完了済み全resultを一度だけmodelへ返す経路である。
2. 保存済みCandidate71、Rating v13、Medium、F04のprotocol v1 `N=10`では、1-step closureは5 / 10だった。同じpromptへroot ordered wrapperをmodel-visibleに指定したprotocol v2では10 / 10だった。
3. Candidate71は個別invocationを同一model stepから発行すると定めるが、rootが一つのcustom wrapper内で順序実行する方法を固定しない。Candidate79は`dependency order`と先行success条件を抽象predicateへ追加したが、1-step closureは0 / 5だった。
4. 置換する一つのpredicateは、`validation_set_ready=true ∧ producer=root`の場合、1回のcustom exec wrapper内から全required validationをbind順の個別`exec_command`として発行し、各exit codeをwrapper内で確認することである。nonzeroまたはunavailableなら後続を発行しない。
5. このpredicateが消す判断点は、required command間で次commandの発行方法を再選択するmodel判断である。各commandの個別invocation、個別exit、fail-stop、全result一括返却は維持する。
6. 新しいlabelは増やさない。増えるのはroot producer時のwrapper方法だけである。shell compound command、case名、固定command列、worker起動、adapter変更は追加しない。
7. 成果品質はCandidate71とCandidate80をRating v13、Medium、F04 r2、各`N=10`の互換条件で確認する。両条件とも10 / 10 valid・rateable・score `4`、required validation欠落0、protocol違反0、zero driftを必須とする。
8. 主判定は1-step closure率とする。Candidate80の10 / 10を成功条件とする。token、elapsed、tool call、message数は診断として記録するが、prompt安定性の合否条件にしない。
9. 1-step closureが10 / 10未満、score `4`未満、required validation欠落、protocol違反、順序違反、workspace driftのいずれかがあれば停止する。Candidate80へ補助predicateを追加せず、同じ課題のprompt安定化成功を主張しない。

九項目を定義済みであるため、Candidate80のbundle、C71 / C80互換profile、構造testを作成できる。

## 変更境界

- direct source: Candidate71
- 置換: root `AGENTS.md`の`VALIDATION_CLOSURE`一行
- 非変更: 残り18 target、TaskSpec、case、rating、permission、executor parameter、command evidence protocol v1、THE-CAPTION runtime
- evaluation scope: F04 r2、Medium、各`N=10`のprompt安定性試験だけ
- adoption / release / runtime projection: 未実施

## Candidate状態

- candidate number: Candidate80
- prompt identity: `the-caption-3ce91a4-root-validation-wrapper-r1`
- evaluation status: [`targeted_evaluated / stopped`](../evaluations/results/candidate71-candidate80-root-validation-wrapper-v13-medium-f04-n10_2026-07-26.md)
- state: `stopped`
- observed result: 1-step closureはCandidate71の5 / 10に対して9 / 10。品質は両条件とも10 / 10 score `4`。strict gateの10 / 10未達により停止。

## Evidence

- [Candidate71設計](candidate71-validation-closure-design.md)
- [Candidate79結果](../evaluations/results/candidate71-candidate79-ordered-validation-wave-v13-medium-f04-n5_2026-07-26.md)
- [command protocol v1 / v2診断](../evaluations/results/candidate71-command-protocol-v1-v2-v13-medium-f04-n10_2026-07-26.md)
- [Candidate80対象試験結果](../evaluations/results/candidate71-candidate80-root-validation-wrapper-v13-medium-f04-n10_2026-07-26.md)
- [Prompt制御の検討原則](prompt-control-design-principles.md)
