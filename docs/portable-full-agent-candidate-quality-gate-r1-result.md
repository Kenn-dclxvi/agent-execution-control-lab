# Portable full-agent Candidate quality gate r1結果

> [!IMPORTANT]
> **結果**: `valid_14_of_14 / schema_valid_14 / score4_7 / mechanism_passed_7 / quality_failed / c147_reference_not_authorized / adoption_not_decided / release_not_decided / projection_not_authorized`

## 結論

portable full-agent CandidateはCodex CLI 0.146.0、GPT-5.6 Sol、reasoning `medium`、held-out r1全14 Case、N=1で、応答、all-agent一次tokenおよびelapsedを14件すべて欠落なく取得した。ただしscore 4は7 / 14であり、事前に固定した14 / 14のquality gateを通過しなかった。

このため、C147 referenceのProfile、preflightおよび14 runは発行しない。Candidateの存在、7 / 14という品質値またはcontrol-freeからの改善を、効率改善、採用、releaseまたはplatform projectionへ昇格させない。

## 測定値

| 指標 | control-free r4 | portable Candidate r1 | 差 |
| --- | ---: | ---: | ---: |
| 有効result | 14 / 14 | 14 / 14 | 0 |
| score 4 | 5 / 14 | 7 / 14 | +2件 |
| 機序通過 | 5 / 14 | 7 / 14 | +2件 |
| all-agent token中央値 | 12,673.5 | 15,337.5 | +2,664.0（約+21%） |
| elapsed中央値 | 10.431秒 | 11.173秒 | +0.742秒（約+7%） |

Case別ではH01がscore 2から4、H09が1から4へ改善し、残り12件は同じscoreだった。score低下は0件である。token差は全14件で増加し、対応Case差の中央値は+2,565、範囲は+2,305〜+2,811だった。elapsed差は10件で増加、4件で減少し、対応Case差の中央値は+1.374秒だった。

これは0 byte controlへ10,781 byteのkernelを追加したcost診断である。qualityも5 / 14から7 / 14へ変わっているため、品質維持後の効率比較ではない。C147 referenceを未実行のまま、platform非依存再構成が直接の親より効率的か、同等か、退行したかは未判定とする。

## 効率上の読み取り

追加tokenが全Caseで+2.3k〜+2.8kに収まる一方、quality差が現れたのは2 Caseだけだった。現行のfull-agent一枚は、Case固有処理よりも毎runの固定instruction costが支配的である可能性が高い。ただしN=1の対応差だけを安定傾向、因果確定または削除対象の特定には使わない。

いま必要なのは、held-outの失敗内容へ条件を足すことではなく、既存の機能blockごとに固定costと消費するsemantic primitiveを切り分ける診断である。文字数だけを理由にblockを削除せず、同じ意味を維持した統合または表現圧縮の候補を、評価Candidateとは別の管理用診断として作る。

## 次のgate

held-out r1はこのCandidateのquality判定に使用済みであり、本文修正後の同じ系列を再選択する入力には使わない。次は既存のtuning Q01〜Q08と81 primitive対応を使い、`vocabulary / outcome / actor / observation / frontier / completion / validation / recovery`のblock別costと必要効果を診断する。

その診断から新しいcompact Candidateを作る場合は、C147を直接の親とし、保持する81 primitive、統合する責務、消える固定cost、非目標および停止条件を新しいCandidate作成前gateへ固定する。quality評価には、新Candidate本文の固定後に別のheld-out revisionを凍結する。新Candidateがそのquality gateを通過するまで、C147 reference run、N=5、N=20、採用、releaseおよびprojectionへ進まない。
