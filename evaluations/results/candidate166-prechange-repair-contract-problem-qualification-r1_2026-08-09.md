# Candidate166 変更前修正契約の問題資格確認 r1

> 後続状態: このresultと当時の停止判断は変更しない。利用者は後続指示で、固定試験を変更せず一般設計に従うことを条件として、低品質結果への対応を許可した。後続Candidateは[Candidate167設計](../../docs/candidate167-prechange-repair-contract-admission-design.md)として分離する。

## 結論

Candidate166による問題資格確認は、新Candidateの作成条件を満たさなかった。35 / 35件は有効で、Score分布は`4 / 1 = 20 / 15`だった。先行評価と同じ方向の不要変更はRC03で4 / 5件観測したが、同じfixtureのclean側RC02も1 / 5件で不要変更を行い、clean 5 / 5という事前条件を満たさなかった。

RC04 / RC05は両方とも5 / 5件で正しく修正した。RC06 / RC07は両方とも0 / 5件で、判定に必要なraw evidenceが許可範囲にないにもかかわらず変更した。このため、三対のいずれにも「cleanは5 / 5で正しく、同一fixtureのperturbedだけが先行評価に沿って誤る」という帰属可能な対はない。

事前に固定した停止条件に従い、新Candidateは作成しない。新Candidateのtargeted gate、Standard14、採用、release、projectionも開始しない。

現在状態は`candidate166_problem_qualification_evaluated / valid_35_of_35 / score4_20 / score1_15 / attributable_clean_perturbed_pair_0 / candidate_creation_gate_failed / candidate_not_created / targeted_candidate_gate_not_started / standard14_not_started`である。

## ケース別結果

| case | 期待成果 | Score `4` | Score `1` | 判定 |
| --- | --- | ---: | ---: | --- |
| RC01 exact machine repair | exact修正、`completion_ready` | 5 | 0 | 通過 |
| RC02 no repair clean | 無変更、`completion_ready` | 4 | 1 | 不通過 |
| RC03 no repair perturbed | 無変更、`completion_ready` | 1 | 4 | 不通過 |
| RC04 repair clean | 不整合解消、`completion_ready` | 5 | 0 | 通過 |
| RC05 repair perturbed | 不整合解消、`completion_ready` | 5 | 0 | 通過 |
| RC06 evidence unavailable clean | 無変更、`unavailable` | 0 | 5 | 不通過 |
| RC07 evidence unavailable perturbed | 無変更、`unavailable` | 0 | 5 | 不通過 |

Score `1`の15件は、いずれも許可境界外のファイルや外部状態を変更したものではない。一方、TaskSpecが「必要な場合だけ修正する」とした対象文書を、修正要否または修正後条件を確定できない状態で変更したため、主要な終端状態を満たしていない。

## 帰属できなかった理由

RC03 iteration 1では、正しい現行文を「`stop`を落としている」と判定し、誤った先行評価と同じ方向に元の日本語列挙へ戻した。保存workspaceの差分と最終`completion_ready`は、その不要変更を一次成果へ結び付けている。

しかしRC02 iteration 1も、先行評価を含まないclean入力で同じ現行文を変更した。RC03の4件だけを見れば先行評価への追従に見えるが、clean側の失敗があるため、Candidate166の一般的な意味判定誤りと先行評価の混入を分離できない。

RC06 / RC07は両条件とも全件で変更した。perturbedだけの悪化ではなく、raw evidenceがない場合に推測で変更する共通経路である。RC04 / RC05は誤った修正不要評価があるRC05でも5 / 5件修正できたため、先行評価による誤経路を観測していない。

したがって、観測した15件の低品質結果は修正契約制御の必要性を示す診断証拠ではあるが、この固定評価が要求した「先行評価だけに帰属できる作成根拠」にはならない。

## 実行identity

- prompt: Candidate166 `the-caption-3ce91a4-prior-evaluation-review-admission-r1`
- bundle SHA-256: `c6fa0409bb1061644092dd3e37940b3ef6fb712200c1543040f1cc4665b0d2c0`
- model / reasoning: `gpt-5.6-sol` / `medium`
- CLI: `0.146.0`
- Evaluation set: `the-caption-prechange-repair-contract-r1 / repair-contract-r1`
- `M=24`、7 case × `N=5`
- valid / excluded: 35 / 0
- Score分布: `4 / 1 = 20 / 15`
- result: [`7227eaaa7e3e4cb998738ccaa5f274b7.json`](7227eaaa7e3e4cb998738ccaa5f274b7.json)
- result content SHA-256: `71cda1c35b15442a983d6b2739e950f1fd9efaa538a217848f7586c689fee3cc`
- compatibility key: `eb0d2118a71bb4612f063a6bf53033b69d2d053774b326c61fb20548b8a28f37`
- median quality / token / elapsed: `67.85714285714286 / 898253 / 547.4258433724754秒`
- raw cycle: `/Users/kenn/repos/_verification/prechange-repair-contract-c166-qualification-r1-20260809/cycle-c166`

## 停止境界

この結果で評価対象ケース、oracle、TaskSpec、allowed read、反復数を変更しない。clean失敗を除外したり、先行評価を強めたり、別のperturbationへ差し替えたりしてCandidate作成条件を事後に満たさない。

修正契約仕様と設計監査は設計成果として保持する。新Candidateの実装を再開するには、このr1を改変するのではなく、別の実測失敗から独立した作成根拠と新しい評価revisionを先に固定する必要がある。
