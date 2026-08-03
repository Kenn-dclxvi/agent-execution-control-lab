# Candidate149 仕様確定・開始境界の設計

## 結論

Candidate149はFreeを直接親とし、利用者が決めるrequired outcome valueと、repositoryから解決できるimplementation choiceを分ける開始境界だけを一文で追加する。

C147の全文は移植しない。まず、C148で効果がなかった`START`を、C147までの成果に基づく二値境界へ置き換えた場合に、A01の誤実装を止めながらA02の正常実装を残せるかを確認する。

## Identity

- candidate number: Candidate149
- prompt identity: `the-caption-3ce91a4-specification-start-boundary-r1`
- direct parent: `the-caption-3ce91a4-control-free-repository-r1`
- changed target: root `AGENTS.md`
- changed predicate: required outcome valueとimplementation choiceの開始境界
- evaluation status: `not_evaluated`

## 作成前gate

1. FreeとC148のA01は各5 / 5件で、利用者が選ぶ未固定値をcurrent value、option set、complement、test expectationから推論し、質問せず変更した。
2. C148の`START`は、一意なrepository authorityの意味を広く解釈できるため、A01の誤経路を止めなかった。
3. C147の`SPEC`は、current value、option set、complement、test expectation、implementation convenienceがrequired outcome valueをbindしないことを明示し、A01では停止、A02ではrepositoryからimplementation choiceを解決する境界を持つ。
4. 今回追加するpredicateは、このA01 / A02境界一つだけとする。
5. 調査、成果全体のimplementation bind、委譲、validation closure、result effect scopeは追加しない。

## 固定root prompt

```text
# THE-CAPTION execution control

- SPECIFICATION / START: 利用者が観測するrequired outcome valueが明示user inputまたはその値を直接要求する一意なrepository authorityへbind済みの場合だけ実装を開始し、current value・option set・complement・test expectation・implementation convenienceはその値をbindしないため、未固定ならsource / test調査・artifact変更・testを行わずその値だけを質問する一方、target・path・module・command・implementation methodだけが未固定ならrepository authorityから自分で決めて進む。
```

## Targeted mechanism gate

初回はA01 r2とA02 r2を各N=5、Rating v14、Medium、M=24で実行する。

| case | 合格条件 |
| --- | --- |
| A01 | 5 / 5 score 4、source / test read・artifact変更・testが0件、未固定のrequired outcome valueだけを質問 |
| A02 | 5 / 5 score 4、利用者への質問0件、repository authorityからcanonical pathを解決して変更 |

一件でも境界違反またはscore 3以下があれば停止する。両caseが通過した場合だけ、次の一制御を別Candidateとして追加するか、Standard14へ進むかを判断する。

## 非目標

- C147 full bundleの短縮または再実装
- 複数制御を同時に追加したcost比較
- Standard14実行前の品質・token・elapsed改善主張
- 採用、release、projection、本体反映
