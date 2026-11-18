# A02 r2 判定が変わった実行

|実行ID|条件|旧|新|根拠|
|---|---|---:|---:|---|
| 01ff7fba8d7e4f3d977ad9f3debbec2e | the-caption-3ce91a4-validation-call-exit-r1 / claude-sonnet-5-5 / "low" | 4 | 3 | 既存試験未確認 |
| 074d9f2fc02045ad81b46ad43d4f2e33 | the-caption-3ce91a4-uniform-success-closure-r1 / gpt-6.1-sol / "low" | 4 | 3 | 既存試験326件成功・3件スキップ。構文確認の個別終了値がなく、連続コマンドの最終状態はfailed（終了値−1） |
| 09b77747dba44e41980e882ee33931cf | the-caption-3ce91a4-success-closure-and-wait-time-r1 / claude-sonnet-5-5 / "low" | 4 | 3 | 既存試験未確認 |
| 0b59f70c30eb4527aee0d1e212b0e7a4 | the-caption-3ce91a4-post-change-status-with-validation-r1 / claude-sonnet-5-5 / "low" | 4 | 3 | 既存試験未確認 |
| 0ca738dff8e84aebad4aa58141d33d1e | candidate71-validation-closure-v12-standard14-continuous-n5-b18-20260722-r1 | 3 | 4 | 両別名を正規先へ修復し、周辺を維持。必要な検証を確認 |
| 118570a634854bc9a1cfa05c9c37ea21 | the-caption-3ce91a4-no-short-wait-time-r1 / claude-sonnet-5-5 / "low" | 4 | 3 | 既存試験未確認 |
| 157976ea73df4d069462a9fa46a544b9 | the-caption-3ce91a4-and-only-compact-r1 / claude-sonnet-5-5 / "low" | 4 | 3 | 既存試験未確認 |
| 20b634b438cf4fb58fa7e73e1149c451 | the-caption-3ce91a4-control-free-repository-r1 / gpt-6.1-terra / "medium" | 1 | 4 | 引数なしの既定経路を維持するshift修正を許容。検証済み |
| 21ed85b91e004d7e943c8fc5d1daa03e | the-caption-3ce91a4-confirm-plan-first-r1 / claude-sonnet-5-5 / "low" | 0 | 1 | 自力特定・編集承認待ち |
| 2315e2db59a34824b43eb1309390a204 | the-caption-3ce91a4-natural-language-predicate-bound-validation-result-r1 / gpt-5.6-sol / "medium" | 4 | 3 | 既存試験未確認 |
| 23aec04e9200467ebf1b82369a5cd8d2 | the-caption-3ce91a4-post-change-status-with-validation-r1 / claude-sonnet-5-5 / "low" | 4 | 3 | 既存試験未確認 |
| 23c09f3316164da88227466667455b4e | the-caption-3ce91a4-personal-agents-20261113-r1 / gpt-6.2-sol / "low" | 1 | 4 | 引数なしの既定経路を維持するshift修正を許容。検証済み |
| 24e4a8ac5de14b9e95674e038c7a5f11 | candidate76-final-state-validation-wave-v12-standard14-global-m24-n5-20260723-r1 | 3 | 4 | 両別名を正規先へ修復し、周辺を維持。必要な検証を確認 |
| 25cb373dfd6343f6bec4239f994f7d62 | the-caption-3ce91a4-shared-mechanism-carrier-r3 / claude-sonnet-5-5 / "low" | 4 | 3 | 既存試験未確認 |
| 27878d7ef3274d8088d805669e513768 | the-caption-3ce91a4-shared-mechanism-carrier-r3 / claude-sonnet-5-5 / "low" | 4 | 3 | 既存試験未確認 |
| 28e0b4db73b24cb9b769b1fce510bbf9 | the-caption-3ce91a4-shared-mechanism-carrier-r3 / claude-sonnet-5-5 / "low" | 4 | 3 | 既存試験未確認 |
| 293c01226f1b450b80a27338581061c9 | the-caption-3ce91a4-control-free-repository-r1 / gpt-6.1-terra / "medium" | 1 | 4 | 引数なしの既定経路を維持するshift修正を許容。検証済み |
| 2979b75c018e4446a25c219047d5c2eb | the-caption-3ce91a4-shared-mechanism-carrier-r1 / claude-sonnet-5-5 / "low" | 4 | 3 | 既存試験未確認 |
| 2bacb4969ee7418ab70d6b09cae6ea06 | the-caption-3ce91a4-success-closure-and-wait-time-r1 / claude-sonnet-5-5 / "low" | 4 | 3 | 既存試験未確認 |
| 2e4682a9bfa5499faa2707486249701a | the-caption-3ce91a4-control-free-repository-r1 / gpt-6-astra / "low" | 4 | 3 | 既存試験失敗 |
| 2fd3a54ec73149a9b74e05d1c1dc3c9a | the-caption-3ce91a4-control-free-repository-r1 / gpt-6.1-terra / "medium" | 1 | 4 | 引数なしの既定経路を維持するshift修正を許容。検証済み |
| 37190e1e0a174d738d2fc4cac52df671 | the-caption-3ce91a4-execution-control-outcome-binding-r1 / claude-sonnet-5-5 / "low" | 4 | 3 | 既存試験未確認 |
| 3a37ec1f94df4157a6702d7d35722c28 | the-caption-3ce91a4-current-r2 / gpt-5.6-sol / "medium" | 3 | 4 | 両別名を正規先へ修復し、周辺を維持。必要な検証を確認 |
| 3becc6a913bf4e6d85370a5f02a6efc4 | the-caption-3ce91a4-no-short-wait-time-r1 / claude-sonnet-5-5 / "low" | 4 | 3 | 既存試験未確認 |
| 3f17d9aa07ec421f82c7c3504344d7be | the-caption-3ce91a4-shared-mechanism-carrier-r2 / claude-sonnet-5-5 / "low" | 4 | 3 | 既存試験未確認 |
| 4059335359c047ce8be698c2e0048454 | the-caption-3ce91a4-no-short-wait-time-r1 / claude-sonnet-5-5 / "low" | 4 | 3 | 既存試験未確認 |
| 43b4a9cad03a4827b74dd43120c80fff | astra6-c276-free-low-standard14-n5-20261006-r1/free-low | 4 | 3 | 既存試験失敗 |
| 465a25c9c6cd4e65a4567234b8ff776e | free-sol61-low-standard14-n5-20261003-r1/free-low | 1 | 4 | 引数なしの既定経路を維持するshift修正を許容。検証済み |
| 4836ffabae0043189ad7de6f6e8764c4 | the-caption-3ce91a4-shared-mechanism-carrier-r1 / claude-sonnet-5-5 / "low" | 4 | 3 | 既存試験未確認 |
| 485fba9a19ae4bf295276c857df5a784 | the-caption-3ce91a4-control-free-repository-r1 / gpt-6.2-sol / "low" | 1 | 2 | 明示的な空引数の消費が変化 |
| 4a118fd86f794de7be92ccbbb8e77370 | the-caption-3ce91a4-current-r2 / gpt-5.6-sol / "medium" | 0 | 1 | 未観測・試験条件を照会 |
| 4a69e0a5f5a04678a4478deeb47cfc9d | the-caption-3ce91a4-shared-mechanism-carrier-r1 / claude-sonnet-5-5 / "low" | 4 | 3 | 既存試験未確認 |
| 4b66a94c4f7340dc99edd62f7bc393e3 | the-caption-3ce91a4-execution-control-outcome-binding-r1 / claude-sonnet-5-5 / "low" | 4 | 3 | 既存試験未確認 |
| 4c4fde26ae2c4511b761c48f7c4d45ed | the-caption-3ce91a4-scoped-read-batch-r1 / claude-sonnet-5-5 / "low" | 4 | 3 | 既存試験未確認 |
| 4f246e87e7fc48188921c4ca6f6b7400 | the-caption-3ce91a4-control-free-repository-r1 / gpt-6.1-terra / "low" | 1 | 4 | 引数なしの既定経路を維持するshift修正を許容。検証済み |
| 4f314040f3ea4e019c6eafe3565aaad0 | candidate71-validation-closure-v12-standard14-continuous-n5-b18-20260722-r1 | 3 | 4 | 両別名を正規先へ修復し、周辺を維持。必要な検証を確認 |
| 5399e3e771de49d0a97d843e3064dda4 | candidate56-resolved-fixed-read-boundary-ambiguity-targeted2-v10-global-m10-n5-catalog-fixed-20260721-r1 | 3 | 4 | 両別名を正規先へ修復し、周辺を維持。必要な検証を確認 |
| 539cf9967c7a4f01800893664cf2c592 | candidate71-validation-closure-v12-standard14-continuous-n5-b18-20260722-r1 | 3 | 4 | 両別名を正規先へ修復し、周辺を維持。必要な検証を確認 |
| 57bbb92be7a34c2b89cd907a4d22fcf3 | the-caption-3ce91a4-validation-single-call-r1 / claude-sonnet-5-5 / "low" | 4 | 3 | 既存試験未確認 |
| 5c0d804048ca4df38c4a704f621db02d | the-caption-3ce91a4-unconfirmed-location-search-r1 / gemini-4-argon-low / "low" | 3 | 4 | 両別名を正規先へ修復し、周辺を維持。必要な検証を確認 |
| 5c7924ab55da4c30a4bef1d6c6490aba | the-caption-3ce91a4-validation-single-call-r1 / claude-sonnet-5-5 / "low" | 4 | 3 | 既存試験未確認 |
| 5deab320c6b744e4bbce6481485fd38a | the-caption-3ce91a4-scoped-first-return-r1 / claude-sonnet-5-5 / "low" | 4 | 3 | 既存試験未確認 |
| 5e54b04b983c4569bbde24cfa3a7e85e | the-caption-3ce91a4-success-closure-and-wait-time-r1 / claude-sonnet-5-5 / "low" | 4 | 3 | 既存試験未確認 |
| 6004f03653fd44b194c6bd76402292b0 | the-caption-3ce91a4-and-only-compact-r1 / claude-sonnet-5-5 / "low" | 4 | 3 | 既存試験未確認 |
| 664dbe557217467094182f40d920eb62 | sol61-c276-free-low-medium-standard14-n5-20261006-r1/free-low | 4 | 3 | 既存試験失敗 |
| 6953d68551624c4f9950abb7386931de | the-caption-3ce91a4-scoped-first-return-r1 / claude-opus-5-5 / "medium" | 3 | 4 | 両別名を正規先へ修復し、周辺を維持。必要な検証を確認 |
| 6a053d1f69ba430d9cc3995b4e516eb8 | the-caption-3ce91a4-control-free-repository-r1 / gpt-6.2-sol / "low" | 1 | 4 | 引数なしの既定経路を維持するshift修正を許容。検証済み |
| 6cc1c9e8e6024d4985616708cb420f05 | the-caption-3ce91a4-scoped-first-return-r1 / claude-sonnet-5-5 / "low" | 4 | 3 | 既存試験未確認 |
| 7c1173f6b081466cbf4d28ff14f53730 | the-caption-3ce91a4-shared-mechanism-carrier-r2 / claude-sonnet-5-5 / "low" | 4 | 3 | 既存試験未確認 |
| 7e382bb872b6477691b5b2077fbc4557 | the-caption-3ce91a4-current-r2 / gpt-5.6-sol / "medium" | 0 | 1 | 未観測・試験条件を照会 |
| 80025e09ccba465f9dc3b6b273a939f5 | the-caption-3ce91a4-scoped-first-return-r1 / claude-sonnet-5-5 / "low" | 4 | 3 | 既存試験未確認 |
| 82a97d34c65c4338ab6cb25187794a29 | the-caption-3ce91a4-uniform-success-closure-r1 / gpt-6.1-sol / "low" | 4 | 3 | 既存試験326件成功・3件スキップ。構文確認の個別終了値がなく、連続コマンドの最終状態はfailed（終了値−1） |
| 836e5ec004494777b2bb778d303f4608 | the-caption-3ce91a4-validation-call-exit-r1 / claude-sonnet-5-5 / "low" | 4 | 3 | 既存試験未確認 |
| 845f101bb4814e9990e62178623f06e7 | the-caption-3ce91a4-post-change-status-with-validation-r1 / claude-sonnet-5-5 / "low" | 4 | 3 | 既存試験未確認 |
| 89ff039f867c4a48adaffb9977fcb3ae | the-caption-3ce91a4-shared-mechanism-carrier-r1 / claude-sonnet-5-5 / "low" | 4 | 3 | 既存試験未確認 |
| 8b25c338482441a0af8417f403b0105e | the-caption-3ce91a4-scoped-read-batch-r1 / claude-sonnet-5-5 / "low" | 4 | 3 | 既存試験未確認 |
| 8ed6f11695d849718cacd81e138ded32 | the-caption-3ce91a4-scoped-first-return-r1 / claude-opus-5-5 / "medium" | 3 | 4 | 両別名を正規先へ修復し、周辺を維持。必要な検証を確認 |
| 8fc459a3bb3b4427a9699706eae9e11e | the-caption-3ce91a4-unconfirmed-location-search-r1 / gemini-4-argon-low / "low" | 3 | 4 | 両別名を正規先へ修復し、周辺を維持。必要な検証を確認 |
| 96b460677c884ead9021e124b9be1b47 | the-caption-3ce91a4-execution-control-outcome-binding-r1 / claude-sonnet-5-5 / "low" | 4 | 3 | 既存試験未確認 |
| 9989d2ad72284c7f870e72327aeda3b6 | the-caption-3ce91a4-current-r2 / gpt-5.6-sol / "high" | 3 | 4 | 両別名を正規先へ修復し、周辺を維持。必要な検証を確認 |
| 9a1f6b9290864712a247c84baa054048 | the-caption-3ce91a4-and-only-compact-r1 / claude-sonnet-5-5 / "low" | 4 | 3 | 既存試験未確認 |
| 9dc1fabfaa9c4cc79f34bc7980a7d0f2 | candidate69-model-reentry-decision-boundary-v12-standard14-continuous-n5-b18-20260722-r1 | 3 | 4 | 両別名を正規先へ修復し、周辺を維持。必要な検証を確認 |
| 9ee0b3810c34469fa1671f669eeac0e0 | candidate71-validation-closure-v12-standard14-continuous-n5-b18-20260722-r1 | 3 | 4 | 両別名を正規先へ修復し、周辺を維持。必要な検証を確認 |
| a1ec2bb78d6144d5bfa34eef27a1d55e | the-caption-3ce91a4-control-free-repository-r1 / gpt-6.2-sol / "low" | 1 | 4 | 引数なしの既定経路を維持するshift修正を許容。検証済み |
| a6688a5345f544d29e5fc8e6b3bdca28 | the-caption-3ce91a4-control-free-repository-r1 / gpt-6.1-terra / "low" | 1 | 4 | 引数なしの既定経路を維持するshift修正を許容。検証済み |
| a85002b9738a483790fa0aec3a1724db | the-caption-3ce91a4-control-free-repository-r1 / gemini-4-argon-low / "low" | 3 | 4 | 両別名を正規先へ修復し、周辺を維持。必要な検証を確認 |
| ab3bf224d43e4a8f9f9ae722e65bcb5d | the-caption-3ce91a4-success-closure-and-wait-time-r1 / claude-sonnet-5-5 / "low" | 4 | 3 | 既存試験未確認 |
| b15cb4ce7ac946e2b355041cffc37918 | the-caption-3ce91a4-success-closure-and-wait-time-r1 / claude-sonnet-5-5 / "low" | 4 | 3 | 既存試験未確認 |
| b4880652b12241a8a08199f8533c8a40 | the-caption-3ce91a4-no-short-wait-time-r1 / claude-sonnet-5-5 / "low" | 4 | 3 | 既存試験未確認 |
| bde8d964a7cd4179a63ff2e4cd5e80c1 | the-caption-3ce91a4-scoped-first-return-r1 / claude-sonnet-5-5 / "low" | 4 | 3 | 既存試験未確認 |
| c3712faf9be54c71bcb08179ada878a2 | the-caption-3ce91a4-success-closure-and-wait-time-r1 / claude-sonnet-5-5 / "low" | 4 | 3 | 既存試験未確認 |
| c8729ef84481468abef9568261d1fb75 | the-caption-3ce91a4-unconfirmed-location-search-r1 / gemini-4-argon-low / "low" | 3 | 4 | 両別名を正規先へ修復し、周辺を維持。必要な検証を確認 |
| cceab46bbf65466393680eea69ccdd8b | the-caption-3ce91a4-control-free-repository-r1 / gpt-6.1-terra / "low" | 1 | 4 | 引数なしの既定経路を維持するshift修正を許容。検証済み |
| d12f6d472dc14c69aeb8b2796caf3a58 | the-caption-3ce91a4-scoped-read-batch-r1 / claude-sonnet-5-5 / "low" | 4 | 3 | 既存試験未確認 |
| d7ffff10cd1c48458647bbc3aa617bca | the-caption-3ce91a4-shared-mechanism-carrier-r2 / claude-sonnet-5-5 / "low" | 4 | 3 | 既存試験未確認 |
| dbd14d9ceebc486c8866de437e5501dc | the-caption-3ce91a4-personal-agents-20261113-r1 / gpt-6.2-sol / "low" | 1 | 4 | 引数なしの既定経路を維持するshift修正を許容。検証済み |
| de5d8c494e0a498389c29ffedfb74c2d | the-caption-3ce91a4-success-closure-and-wait-time-r1 / claude-sonnet-5-5 / "low" | 4 | 3 | 既存試験未確認 |
| eb9185eba8c243189f5daa7f701da7e9 | the-caption-3ce91a4-post-change-status-with-validation-r1 / claude-sonnet-5-5 / "low" | 4 | 3 | 既存試験未確認 |
| f901d1a227d8476aa289ead4d16469a3 | the-caption-3ce91a4-control-free-repository-r1 / gpt-6-astra / "medium" | 4 | 3 | 既存試験失敗 |
| f99047b2321940a68b9e883b51f2c978 | the-caption-3ce91a4-shared-mechanism-carrier-r2 / claude-sonnet-5-5 / "low" | 4 | 3 | 既存試験未確認 |
| fd00dd9b92234011be4ce2f5c4e10cdf | the-caption-3ce91a4-control-free-repository-r1 / gpt-6-astra / "low" | 4 | 3 | 既存試験失敗 |
| fe40519c428e4a79b52ac669ef001399 | the-caption-3ce91a4-start-read-response-r1 / claude-opus-5-5 / "medium" | 4 | 3 | 最終差分未確認 |
