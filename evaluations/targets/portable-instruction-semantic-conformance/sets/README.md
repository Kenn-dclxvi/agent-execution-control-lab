# Evaluation sets

登録済みheld-out setは[`heldout-r1/set.json`](heldout-r1/set.json)である。ただしC147 referenceが6 / 14だったため、C147同等性またはportable再現率の評価には使わない。

既知14 Caseを使うC147契約校正setは、[`reference-calibration-r2`](reference-calibration-r2/set.json)、[`reference-calibration-r3`](reference-calibration-r3/set.json)、[`reference-calibration-r4`](reference-calibration-r4/set.json)としてrevisionごとに固定する。これらはportable Candidateのheld-outではなく、r4だけがC147 14 / 14 gateを通過した。

独立setは[`heldout-r2`](heldout-r2/set.json)をLayer 1設計不適格の履歴として保持し、frontier authorityを修正した[`heldout-r3`](heldout-r3/set.json)を現行比較setとする。
