# Results

control-free資格確認の正本は[`portable-semantic-control-free-heldout-r1-n1-qualification-r4.json`](portable-semantic-control-free-heldout-r1-n1-qualification-r4.json)である。14 Caseすべてでschema適合応答、all-agent一次tokenおよびelapsedを取得し、測定成立gateを通過した。score 4と機序通過は各5/14だが、qualificationでは記述値であり合否条件ではない。

このresultはcontrol-freeの比較基準を固定するもので、portable kernelの効果、採用、releaseまたはruntime projectionを意味しない。生応答と実行証跡はrepository外へ保持する。

portable full-agent Candidateの正本は[`portable-semantic-c147-portable-full-agent-heldout-r1-n1-qualification-r1.json`](portable-semantic-c147-portable-full-agent-heldout-r1-n1-qualification-r1.json)である。14/14件がvalid、score 4は7/14でquality gate不通過となった。C147 referenceは未発行で、効率比較、N拡張、採用、releaseおよびprojectionへ進めない。

後続のC147 reference先行資格確認の正本は[`portable-semantic-c147-full-agent-reference-heldout-r1-n1-qualification-r1.json`](portable-semantic-c147-full-agent-reference-heldout-r1-n1-qualification-r1.json)である。14 / 14 validだがScore 4は6 / 14であり、semantic held-out r1はC147同等性テストとして資格なしとなった。portable r1の7 / 14をC147機能再現率へ使わず、既存resultは未資格set上の履歴値として保持する。

transition projectionのC147校正は、[`r2`](portable-semantic-c147-reference-transition-calibration-r2-n1-qualification-r1.json)、[`r3`](portable-semantic-c147-reference-transition-calibration-r3-n1-qualification-r1.json)、[`r4`](portable-semantic-c147-reference-transition-calibration-r4-n1-qualification-r1.json)の順にappend-onlyで保持する。Score 4は12 / 14、13 / 14、14 / 14と推移し、r4だけが全14件のreference contract gateを通過した。いずれも既知Caseによる校正であり、portable比較resultではない。

独立heldout r2の[`C147 result`](portable-semantic-c147-reference-heldout-r2-n1-qualification-r1.json)はLayer 1のfrontier authority不一致により12 / 14となったため、portableを発行せず設計不適格として保存する。

修正版heldout r3では[`C147 reference`](portable-semantic-c147-reference-heldout-r3-n1-qualification-r1.json)と[`portable full-agent r1`](portable-semantic-c147-portable-full-agent-heldout-r3-n1-qualification-r1.json)がともに14 / 14 Score 4・機序成立となった。N=1対応比較ではportableのtoken中央値が26増え、elapsed中央値が0.260秒減った。cost改善は未判定で、採用、release、projectionは未決定である。

同条件のN=5拡張は[`C147 reference`](portable-semantic-c147-reference-heldout-r3-n5-qualification-r1.json)と[`portable full-agent r1`](portable-semantic-c147-portable-full-agent-heldout-r3-n5-qualification-r1.json)へappend-onlyで登録した。C147は69 / 70、portableは70 / 70でScore 4・機序成立となった。portableはtoken合計が2,322増え、elapsed合計が24.812秒減った。採用、release、projectionは未決定である。

N=20拡張は[`C147 reference`](portable-semantic-c147-reference-heldout-r3-n20-qualification-r1.json)と[`portable full-agent r1`](portable-semantic-c147-portable-full-agent-heldout-r3-n20-qualification-r1.json)へappend-onlyで登録した。C147は275 / 280、portableは280 / 280でScore 4・機序成立となった。portableはtoken合計が10,195増え、elapsed合計が56.230秒減った。採用、release、projectionは未決定である。
