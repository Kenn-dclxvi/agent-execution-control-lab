# Candidate144 required outcome / validation method boundary設計

## 結論

Candidate144はCandidate143を直接親とし、validation readinessの一変更軸だけを置換する。

TaskSpecまたはcommand evidence protocolが要求するvalidation predicate、順序、個別pass条件、stop条件がbind済みなら、TaskSpec未指定のexact commandはmissing validation identityとして追加探索しない。既に受領したTaskSpec、適用中instruction、target evidenceの範囲からexecution methodとして選び、validation実行票の発行時にcommandへbindする。

Candidate143のrequired outcome全体の`implementation_bound`、変更前evidence admission、artifact変更開始条件、recoveryは変更しない。

## Identity

- candidate number: Candidate144
- prompt identity: `the-caption-3ce91a4-required-outcome-validation-method-boundary-r1`
- direct parent: `the-caption-3ce91a4-required-outcome-implementation-bind-r1`（Candidate143）
- changed target: root `AGENTS.md`
- changed axis: `validation_predicate_ready`によるvalidation predicate / exact command method境界
- evaluation status: `six_case_n5_evaluated / quality_gate_passed / mechanism_gate_failed / stopped`
- adoption / release / runtime projection: `not_decided / not_created / not_projected`

## 作成前gate

1. Candidate143のF02 / F04 / F07各N=100は300 / 300件がscore `4`で、required outcome全体のimplementation bindは対象3経路のstability gateを通過した。この変更前境界を親として固定する。
2. Candidate143 Standard14 N=5は70 / 70 score `4`だが、C125比でtoken中央値`+24.98%`、elapsed中央値`+17.30%`だった。
3. 保存traceでは、C143はC125と同じ45 file changeに対してcommandが450件から620件へ増えた。増加は成果量ではなく、変更前確認と変更後validation method探索の細分化にある。
4. 今回は変更後分岐だけを扱う。変更前evidenceの一括取得、command数、read数、bytes、token上限は変更しない。
5. Candidate119はCandidate118上で同じvalidation境界を置換し、A02の変更後method探索を4 / 5件から0 / 5件、token中央値を`226,321`から`149,154`へ下げた。
6. Candidate119は同時にimplementation bind後・変更前command再入を1 / 5件発生させたため停止した。Candidate144はCandidate119を親にせず、対象N=100を通過したCandidate143の`implementation_bound`を保持した上でvalidation境界だけを再検証する。
7. TaskSpecまたはcommand evidence protocolがexact commandを明示する場合、そのcommandは従来どおりrequired validationとしてbindする。抽象predicateへの読み替えや別methodへの置換を禁止する。
8. A01 / A02 / F01は変更軸の再現と明示command保持を測る。F02 / F04 / F07 dependencyはCandidate143の複数target、単一target、pair経路の非回帰を測る。
9. 初回は6 case各N=5、M=24とする。一件でもscore `3`以下またはmechanism欠落があれば停止し、Standard14へ進めない。

## 置換する境界

```text
validation_predicate_ready :=
  artifact変更完了
  ∧ TaskSpec-required validationの
    predicate / order / individual pass condition / stop conditionが全件bind済み
  ∧ TaskSpecまたはcommand evidence protocolが
    exact commandを明示したvalidationだけcommandがbind済み
```

`validation_predicate_ready=true`でexact commandがTaskSpec未指定なら、その未固定状態をrepository evidenceの開放条件にしない。既存のmodel-visible evidenceからmethodを選び、validation実行票発行時にcommandへbindする。

この境界は「検証を省略する」制御ではない。何を合格とするかは事前に固定し、具体的にどのcommandで判定するかだけを実行methodとして遅延bindする。

## 汎用性

predicateとmethodの分離はpytest固有ではない。

- 「shell syntaxが成立する」を`bash -n`等で判定する場合
- 「schemaが読み込める」を既存projectのtest runnerで判定する場合
- 「生成物が整合する」をbuildまたはstatic checkerで判定する場合
- 「変更差分が構文上clean」をVCSのdiff checkerで判定する場合

TaskSpecが具体commandを明示すれば、そのcommandがpredicateの一部になる。明示しなければ、同じpredicateを判定できるmethodをpermission内で選ぶ。この区別はtool名やrepository pathに依存しない。

## 初回評価gate

| gate | 期待 |
| --- | ---: |
| valid / rateable | 30 / 30 |
| score `4` | 30 / 30 |
| score `3`以下 | 0 |
| A01 clarification停止、変更・testなし | 5 / 5 |
| A02 canonical成果 | 5 / 5 |
| A02 implementation bind後・変更前command再入 | 0 / 5 |
| A02 artifact変更後・最初のvalidation前method探索 | 0 / 5 |
| F01明示required command完備 | 5 / 5 |
| F02両source変更 | 5 / 5 |
| F04単一target必要変更 | 5 / 5 |
| F07 dependency pair完備 | 5 / 5 |

## Cost判定

- 直接対象A02のCandidate143 token中央値は`235,359`である。Candidate144がこれを下回るかを変更軸のcost effectとして測る。
- 同一互換条件のCandidate125 A02 token中央値は`141,143`である。これは最終目標であり、初回N=5で未達でもquality / mechanism成立と分離する。
- Standard14全体のC125目標はtoken中央値`1,401,225`、elapsed中央値`846.377秒`である。初回targeted結果だけから到達を主張しない。

## 非目標

- Candidate143の`implementation_bound`変更
- 変更前evidence operationの一括化または取得量制御
- validation省略、required command置換、pass条件緩和
- command数、read数、bytes、token、elapsedのprompt内上限
- executor、CLI、runtime hook、wrapper、rating contractの変更
- Standard14、採用、release、本体反映の先行実施

## 初回試験

- cases: A01 r2 / A02 r2 / F01 r3 / F02 r1 / F04 r2 / F07 dependency r1
- Rating: v14
- model / reasoning: `gpt-5.6-sol` / `medium`
- CLI / Python: `0.146.0` / `3.14.5`
- repetition / configured M: 各`N=5` / `24`
- direct reference: Candidate143同case atomic run
- prompt以外の互換条件: Candidate143と完全一致

Candidate143の既存runは再実行しない。Candidate144の不足30 slotだけを発行する。全gate通過時だけ、次の比較または追加試験を別判断する。

## 評価結果

6 case各N=5は30 / 30がscore `4`だった。ただしA02でimplementation bind後・変更前command再入が1 / 5件、artifact変更後・最初のvalidation前method探索が1 / 5件発生し、事前mechanism gateを満たさなかった。

A02 token中央値はCandidate143比`-23.50%`だったが、C125目標比では`+27.56%`だった。6 case合計はtoken`-8.88%`、elapsed`+9.26%`で混在した。Candidate144は停止し、Standard14へ進めない。詳細は[比較結果](../evaluations/results/candidate143-candidate144-required-outcome-validation-method-boundary-v14-medium-a01-a02-f01-f02-f04-f07-atomic-n5-cli0146_2026-08-02.md)を正本とする。
