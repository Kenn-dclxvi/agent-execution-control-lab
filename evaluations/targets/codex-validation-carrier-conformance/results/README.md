# Results

write-once resultの索引を置く。control-free N=1 qualificationは[`codex-validation-carrier-control-free-heldout-r1-n1-qualification-r1.json`](codex-validation-carrier-control-free-heldout-r1-n1-qualification-r1.json)へ登録した。6件すべてvalidで3 KPIを取得し、quality分布はScore 4が4件、Score 2が1件、Score 1が1件、mechanismはpass 1件、fail 5件である。これは測定系のqualificationでありformal comparisonではない。

P002 candidate-only N=1は[`codex-validation-carrier-p002-heldout-r1-n1-candidate-gate-r1.json`](codex-validation-carrier-p002-heldout-r1-n1-candidate-gate-r1.json)へ登録した。6件すべてvalid、Score 4、mechanism passでcandidate-only gateを通過した。P001とのpaired resultはまだなく、効率差は未判定である。

VCC6 P001/P002 N=5は[`vcc6-p001-p002-n5-comparison-r1.json`](vcc6-p001-p002-n5-comparison-r1.json)へ登録した。60件すべてvalidで、P002は30 / 30件がScore 4、tokens合計はP001比9.47%減、elapsed合計は10.72%増となった。両cost減少を要求する事前gateは不通過であり、Standard14へは進まない。

共通runnerでfresh実行したVCC6 P001/P002/P003 N=1は[`vcc6-p001-p002-p003-shared-runner-n1-result-r1.json`](vcc6-p001-p002-p003-shared-runner-n1-result-r1.json)へ登録した。18件すべてvalidかつScore 4で、mechanismはP001が2 / 6、P002とP003が6 / 6である。P003のtokens合計はP001比29.97%、P002比10.39%少なく、elapsed合計はP001比19.22%、P002比5.64%多い。N=1の安定傾向は主張しない。

P004 candidate-only VCC6 N=1は[`vcc6-p004-shared-runner-n1-candidate-gate-r1.json`](vcc6-p004-shared-runner-n1-candidate-gate-r1.json)へ登録した。6件すべてvalidだが、H06がScore 1・mechanism failureとなり、分布はScore 4が5件、Score 1が1件である。品質停止条件によりN=5を許可せず、効率改善を判定しない。

P005 candidate-only VCC6 N=1は[`vcc6-p005-shared-runner-n1-candidate-gate-r1.json`](vcc6-p005-shared-runner-n1-candidate-gate-r1.json)へ登録した。6件すべてvalid、Score 4、mechanism passである。H06のraw outer outputは342 bytes、forbidden substringは0件となった。N=5を実施できるが、N=1から効率差または安定傾向は主張しない。

P001・P003・P005のfresh VCC6 N=5は[`vcc6-p001-p003-p005-shared-runner-n5-comparison-r1.json`](vcc6-p001-p003-p005-shared-runner-n5-comparison-r1.json)へ登録した。90件すべてvalidで、P005は30 / 30件Score 4・mechanism passである。P003比はtokens 1.44%、elapsed 5.72%減だが、P001比はtokens 14.50%減、elapsed 18.40%増となった。直接親に対する両cost減少gateは不通過であり、Standard14へ進まない。
