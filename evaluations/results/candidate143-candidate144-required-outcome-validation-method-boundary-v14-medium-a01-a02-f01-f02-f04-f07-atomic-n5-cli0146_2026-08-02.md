# Candidate143 / Candidate144 6 case N=5比較結果

## 結論

Candidate144のA01 / A02 / F01 / F02 / F04 / F07 dependency各N=5は、30 / 30がscore `4`だった。score `3`以下、excluded attempt、controller errorは0件である。

ただし、事前に固定したmechanism gateは通過しなかった。A02では、implementation bind後・artifact変更前のcommand再入が1 / 5件、artifact変更後・最初のvalidation前のmethod探索が1 / 5件発生した。Candidate144はquality合格、mechanism失敗として停止し、Standard14へ進めない。

A02のtoken中央値はCandidate143の`235,359`から`180,039`へ`23.50%`減った。一方、C125の目標`141,143`には`27.56%`届かない。6 case合計のtoken中央値は`8.88%`減ったが、elapsed中央値は`9.26%`増えた。cost改善だけでmechanism失敗を上書きしない。

## 固定条件

- candidate: `the-caption-3ce91a4-required-outcome-validation-method-boundary-r1`
- direct parent: `the-caption-3ce91a4-required-outcome-implementation-bind-r1`（Candidate143）
- bundle SHA-256: `2030d81d0d8a5392399c2d0f367029a4905931d67b58e0df8777003d07723b98`
- cases: A01 r2、A02 r2、F01 r3、F02 r1、F04 r2、F07 dependency r1
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Codex CLI / Python: `0.146.0` / `3.14.5`
- N / configured M: `5` / `24`
- newly issued: 30
- valid / rateable / excluded: `30 / 30 / 0`
- reference result: `49ced962f26e41fa93a02e6957c91785`
- candidate pool: `dc7d17f58dee6528d60d3c8b0c524fb63a40f3d24db9a69352d903556234f52b`
- selection: `f12c480cace142019d27d49baefd0b6b`
- analysis: `215a75df4050467eba4163f891a8599c`
- registered result: `d1990367ad6f4b9098b27ce867f98c85`
- selection comparison key: `a111d96064a392ea0d2cd4fb9bb443af55b7c08d2eb78ce6678d0340f3eeabda`
- registered compatibility key: `438d2d35fcea9a7300969c308f794f56cd7d8e03f2ce54b894b447acb5eaf95c`
- execution archive SHA-256: `68cc1fb2ced9c4c583c2c283d5e4f37f8b0b89443ab01b4e031827c3755fdd3f`

比較元はCandidate143 Standard14の保存済みatomic runから、今回と同じ6 caseを各5件選択して構成した。Candidate143は再実行していない。preflightでは6 caseのcoverage、fixture、TaskSpec、rating、model、reasoning、runtime、permission、executor挙動、token accountingが一致し、prompt identityだけが異なることを機械確認した。

## Qualityと成果挙動

A01は5 / 5でclarification停止し、artifact変更とtest実行を行わなかった。A02は5 / 5で`run.sh`のcanonical V4 routingだけを修正した。F01は5 / 5で明示required commandを完備した。

Candidate143の安定経路を確認するF02 / F04 / F07 dependencyも各5 / 5でscore `4`だった。F02はengineとupdaterの両sourceを変更し、F04は単一targetの必要変更を行い、F07は`requirements.in`と`requirements.txt`のpairを揃えた。

したがって、Candidate144のvalidation境界は、初回N=5ではrequired commandやC143の成果挙動を壊していない。ただし、これはmechanism gateの通過を意味しない。

## A02 mechanism分析

`implementation bind後・変更前command再入`とは、何をどこへ変更するかを確定した後に、artifact変更以外のcommandへ戻る挙動である。

run `c161f4c362fc425eaad440214703c417`は、正規entrypointと変更対象の一分岐を確定したと表明した後、README、entrypoint実体、関連testを再度readしてから変更した。よって変更前再入1件と数える。

`変更後method探索`とは、artifactを変更した後、最初のvalidationを始める前に、どのcommandで検証するかを決めるためrepository evidenceを追加取得する挙動である。

run `f695fa86e95f4d29af9800e0021afbfe`は、`run.sh`変更後に`tests/AGENTS.md`と既存routing testを追加readし、その後にvalidation票を確定した。よって変更後method探索1件と数える。

残る4件は変更後に追加探索せず、既に得たevidenceからvalidation票を発行した。つまりCandidate144の境界は優勢な経路を変えた可能性があるが、分岐を閉じ切ってはいない。N=5のgateは0件を要求しているため停止する。

## Cost比較

| 対象 | Candidate143 | Candidate144 | 差 |
| --- | ---: | ---: | ---: |
| A02 token中央値 | 235,359 | 180,039 | -55,320（-23.50%） |
| A02 elapsed中央値 | 101.328秒 | 101.102秒 | -0.226秒（-0.22%） |
| 6 case合計token中央値 | 946,741 | 862,697 | -84,044（-8.88%） |
| 6 case合計elapsed中央値 | 457.454秒 | 499.791秒 | +42.337秒（+9.26%） |

A02 tokenは下がったが、C125 A02中央値`141,143`より`38,896`多い。6 case全体ではtokenとelapsedが逆方向へ動いている。初回N=5から一般的なcost改善は主張しない。

## 解釈

事実として、validation predicateとexact command methodを分離する一軸変更だけでは、変更後method探索を完全には閉じられなかった。また、Candidate143の`implementation_bound`を保持しても、implementation bind後の変更前再入が1件再発した。

この結果は、二つの再入が独立した局所問題ではない可能性を示す。modelは、変更前は「実装根拠が十分か」、変更後は「検証根拠が十分か」を同じrepository evidence admissionとして再解釈している。validation節だけの置換では、その共通境界を制御できない。

次案を作る場合は、再びcommand順序やread回数を追加するのではなく、Candidate143のrequired outcome bindとvalidation predicate bindを、artifact変更を境にした二つの別々の完了状態としてどう表現するかを挙動から再設計する必要がある。Candidate144をStandard14へ広げる根拠はない。

## 状態

`six_case_n5_evaluated / quality_gate_passed / mechanism_gate_failed / prechange_reentry_1_of_5 / postchange_method_search_1_of_5 / cost_mixed / result_registered / stopped / standard14_not_run / adoption_not_decided`

## 結論表

| gate | 実測 | 判定 |
| --- | ---: | --- |
| valid / rateable | 30 / 30 | pass |
| score `4` | 30 / 30 | pass |
| score `3`以下 | 0件 | pass |
| A01 clarification停止、変更・testなし | 5 / 5 | pass |
| A02 canonical成果 | 5 / 5 | pass |
| A02 implementation bind後・変更前command再入 | 1 / 5 | fail |
| A02 artifact変更後・最初のvalidation前method探索 | 1 / 5 | fail |
| F01明示required command完備 | 5 / 5 | pass |
| F02両source変更 | 5 / 5 | pass |
| F04単一target必要変更 | 5 / 5 | pass |
| F07 dependency pair完備 | 5 / 5 | pass |
| A02 token | C143比-23.50%、C125比+27.56% | improved vs C143 / target not met |
| 6 case cost | token -8.88%、elapsed +9.26% | mixed |
| Standard14 | 未実施 | stopped before expansion |
| 採用 / release / 本体反映 | 未判断・未実施 | not decided |
