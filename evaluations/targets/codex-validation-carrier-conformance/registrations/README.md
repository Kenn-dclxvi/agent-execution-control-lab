# Registrations

heldout r1のsource、rating、runtime実装およびcontrol-free qualification resultのappend-only bindingは[`heldout-r1-runtime-registration-r1.json`](heldout-r1-runtime-registration-r1.json)を正とする。

`target.json`を遡及変更せず、P002 bundle bindingは[`p002-composition-binding-r1.json`](p002-composition-binding-r1.json)、candidate-only gate通過とpaired N=5許可は[`p002-candidate-gate-registration-r1.json`](p002-candidate-gate-registration-r1.json)へ追記した。VCC6 P001/P002 N=5のcost gate不通過とStandard14非許可は[`vcc6-p001-p002-n5-comparison-registration-r1.json`](vcc6-p001-p002-n5-comparison-registration-r1.json)を正とする。

P002後続でもVCC6を変更せずprompt identityだけを変える比較規則は[`vcc6-fixed-benchmark-policy-r1.json`](vcc6-fixed-benchmark-policy-r1.json)を正とする。これは既存source freezeまたはresultを変更せず、blind性と固定benchmark内の比較可能性を分離するappend-only policyである。
