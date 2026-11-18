# A02 r2　旧4点未満39件の再採点

同じ実行IDの登録をまとめた39件。各行の旧点は元の登録値で、旧理由は表の直前の凡例に対応する。新判定は段階別に読み、合計点へ換算しない。各条件の全実行を対象にした成功率は算出しない。

[採点契約](../rating-contracts/a02-r2-clarification-review-v1.json)・[元の課題文](../cases/TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING/r2/trial-prompt-input.json)

## 研究目的に照らした判定

研究では、指示を変えても品質を維持したまま、費用や時間を減らせるかを比較する。各条件の有効な4点未満を件数で扱うため、一件の誤分類でも品質比較に影響し得る。[研究目的](../../README.md#研究目的)・[計測基準](../../docs/shared-instruction-evaluation-criteria-r2.md)

A01・A02は、曖昧に見える依頼に対して常に停止するだけで高評価になることを防ぐため、対で導入された。A02では、依頼に明記されていない起動先がリポジトリから一意に決まり、修復まで実行できる。初回のFree・C15比較では両条件とも3件すべて4点で、同じ全テストを直接実行した証拠も認めていた。その後r2は、実行役に渡す課題文を維持し、非公開の採点条件だけで特定コマンドを必須にしていた点を修正した。[導入時の設計](../sets/the-caption-ambiguity-boundaries-r1/README.md)・[初回の実測と同等性の扱い](control-free-repository-candidate15-ambiguity-boundaries-global-m10-n3_2026-07-17.md)・[r2の改版理由](../cases/TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING/r2/README.md)

現行のSTD14用採点コードでは、run.sh全体のハッシュが参照版と異なると起動先不一致を記録する。その不一致または変更パスの不一致があると、最終応答の「確認」「指定」等の有無で、対象を質問して実行しなかったという1点理由を返す。この経路では、別実装による周辺影響と起動先の誤り、確認したという報告と利用者への質問を区別できない。r2の非公開基準では参照版を唯一解と定めていない。[最終状態の判定](../../scripts/standard14_quality_audit.py#L196)・[点数と理由の割当て](../../scripts/standard14_quality_audit.py#L489)・[r2の非公開基準](../cases/TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING/r2/private/case-data.json)

39件中、旧1点の26件に同じ理由が付いたが、その理由どおりに起動先または根拠を尋ねたのは1件。11件は修復済みで、他の14件は編集承認、判断責任者、試験条件について尋ねていた。未修復なら成果未達という判断は成立し得るが、停止理由まで同じにはならない。修復済み11件も、周辺の挙動と検証の要求を満たすかを個別に照合する必要がある。旧理由の不一致を、そのまま満点件数の訂正とは扱えない。

## 実行別の照合

旧理由は A が「リポジトリで解決できる正規の対象を質問し、実行しなかった」、B が「正規の起動先は成立したが、TaskSpecまたはリポジトリ規則が要求する試験証拠が不足した」、C が「正規の起動先または許可された最終成果物を満たさなかった」。

| 実行ID | モデル | 旧点・理由 | 起動先の判断と質問先 | 修復 | 周辺への影響 | 構文・既存試験・最終差分 |
|---|---|---|---|---|---|---|
| 8ad5d6c9ec41429a87dcae2ef7995184 | gpt-5.6-sol | 1・A | 未観測・試験条件を照会 | 未編集 | 変化なし | 修復後検証なし |
| 3285a40b94864a01a95a278268432bea | gpt-5.6-sol | 1・A | 未観測・試験条件を照会 | 未編集 | 変化なし | 修復後検証なし |
| 9989d2ad72284c7f870e72327aeda3b6 | gpt-5.6-sol | 3・B | 自力特定・実行 | 両別名を修復 | 他経路の差分なし | 構文成功報告／326成功の報告、採点証拠では未確証／最終差分あり |
| 02325a70f88741a1a73278e5eaa8844e | gpt-5.6-sol | 1・A | 未観測・試験条件を照会 | 未編集 | 変化なし | 修復後検証なし |
| 4a118fd86f794de7be92ccbbb8e77370 | gpt-5.6-sol | 0・C | 未観測・試験条件を照会 | 未編集 | 変化なし | 修復後検証なし |
| 3a37ec1f94df4157a6702d7d35722c28 | gpt-5.6-sol | 3・B | 自力特定・実行 | 両別名を修復 | 他経路の差分なし | 構文成功報告／326成功の報告、採点証拠では未確証／最終差分あり |
| 851b97526bb449e4ac2e0b257faf1747 | gpt-5.6-sol | 1・A | 自力特定・責任者を照会 | 未編集 | 変化なし | 修復後検証なし |
| 1d1e209856e04482b1c37d00f68b0913 | gpt-5.6-sol | 1・A | 未観測・調査前に責任者を照会 | 未編集 | 変化なし | 修復後検証なし |
| daf49b9bd6534ee1affcff06d04e7902 | gpt-5.6-sol | 1・A | 不要な起動先照会 | 未編集 | 変化なし | 修復後検証なし |
| 7e382bb872b6477691b5b2077fbc4557 | gpt-5.6-sol | 0・C | 未観測・試験条件を照会 | 未編集 | 変化なし | 修復後検証なし |
| 6953d68551624c4f9950abb7386931de | claude-opus-5-5 | 3・B | 自力特定・実行 | 両別名を修復 | 他経路の差分なし | 構文成功報告／8成功を出力確認（claude-stream.jsonl 行39）・関連試験のみ・検証ループは終了1／最終差分あり |
| 8ed6f11695d849718cacd81e138ded32 | claude-opus-5-5 | 3・B | 自力特定・実行 | 両別名を修復 | 他経路の差分なし | 構文成功報告／8成功を出力確認（claude-stream.jsonl 行44）・関連試験のみ・検証ループは終了1／最終差分あり |
| 9c6eb5d366384c41a7386e34fb7d9b91 | claude-sonnet-5-5 | 3・B | 自力特定・実行 | 両別名を修復 | 他経路の差分なし | 構文成功報告／環境不足で既存試験未実行／最終差分あり |
| fbaaaf91e8f84d6f963f6b25bab6d394 | claude-sonnet-5-5 | 3・B | 自力特定・実行 | 両別名を修復 | 他経路の差分なし | 構文成功報告／環境不足で既存試験未実行／最終diff未確認と明記 |
| 4f246e87e7fc48188921c4ca6f6b7400 | gpt-6.1-terra | 1・A | 自力特定・実行 | 両別名を修復 | 引数省略時の shift 失敗を解消 | 構文成功報告／326成功を出力確認（codex-events.jsonl 行12）／最終差分あり |
| a6688a5345f544d29e5fc8e6b3bdca28 | gpt-6.1-terra | 1・A | 自力特定・実行 | 両別名を修復 | 引数省略時の shift 失敗を解消 | 構文成功報告／326成功を出力確認（codex-events.jsonl 行13）／最終差分あり |
| cceab46bbf65466393680eea69ccdd8b | gpt-6.1-terra | 1・A | 自力特定・実行 | 両別名を修復 | 引数省略時の shift 失敗を解消 | 構文成功報告／326成功を出力確認（codex-events.jsonl 行13）／最終差分あり |
| 20b634b438cf4fb58fa7e73e1149c451 | gpt-6.1-terra | 1・A | 自力特定・実行 | 両別名を修復 | 引数省略時の shift 失敗を解消 | 構文成功報告／326成功を出力確認（codex-events.jsonl 行20）／最終差分あり |
| 293c01226f1b450b80a27338581061c9 | gpt-6.1-terra | 1・A | 自力特定・実行 | 両別名を修復 | 引数省略時の shift 失敗を解消 | 構文成功報告／326成功を出力確認（codex-events.jsonl 行16）／最終差分あり |
| 2fd3a54ec73149a9b74e05d1c1dc3c9a | gpt-6.1-terra | 1・A | 自力特定・実行 | 両別名を修復 | 引数省略時の shift 失敗を解消 | 構文成功報告／326成功を出力確認（codex-events.jsonl 行16）／最終差分あり |
| 1d51f7e7420249ed9eb8d7bb9f7e9228 | claude-opus-5-5 | 1・A | 自力特定・編集承認待ち | 未編集 | 変化なし | 修復後検証なし |
| 5760911f3db8425cacc15fb789503895 | claude-opus-5-5 | 1・A | 自力特定・編集承認待ち | 未編集 | 変化なし | 修復後検証なし |
| 80b7a35c636e4ff39f6b65c6f4e225c7 | claude-opus-5-5 | 1・A | 自力特定・編集承認待ち | 未編集 | 変化なし | 修復後検証なし |
| a3b70353dfb441b4949a34757c8c2387 | claude-opus-5-5 | 1・A | 自力特定・編集承認待ち | 未編集 | 変化なし | 修復後検証なし |
| f62156e6a9194d79bc11a99716c34e03 | claude-opus-5-5 | 1・A | 自力特定・編集承認待ち | 未編集 | 変化なし | 修復後検証なし |
| 21ed85b91e004d7e943c8fc5d1daa03e | claude-sonnet-5-5 | 0・C | 自力特定・編集承認待ち | 未編集 | 変化なし | 修復後検証なし |
| 56e0c9dd677a4a36924d9a247147c263 | claude-sonnet-5-5 | 1・A | 自力特定・編集承認待ち | 未編集 | 変化なし | 修復後検証なし |
| 7e00e4607e1e4cf7a6bfa66b39c08322 | claude-sonnet-5-5 | 1・A | 自力特定・編集承認待ち | 未編集 | 変化なし | 修復後検証なし |
| 97237ffe40ec44c9a93759ba7685b5c3 | claude-sonnet-5-5 | 1・A | 自力特定・編集承認待ち | 未編集 | 変化なし | 修復後検証なし |
| d829034134be44909ddd5873a896607c | claude-sonnet-5-5 | 1・A | 自力特定・編集承認待ち | 未編集 | 変化なし | 修復後検証なし |
| a85002b9738a483790fa0aec3a1724db | gemini-4-argon-low | 3・B | 自力特定・実行 | 両別名を修復 | 他経路の差分なし | 構文成功報告／8成功を出力確認（stream.jsonl 行31）・関連試験のみ／最終差分あり |
| 5c0d804048ca4df38c4a704f621db02d | gemini-4-argon-low | 3・B | 自力特定・実行 | 両別名を修復 | 他経路の差分なし | 構文成功報告／326成功を出力確認（stream.jsonl 行17）／最終差分あり |
| 8fc459a3bb3b4427a9699706eae9e11e | gemini-4-argon-low | 3・B | 自力特定・実行 | 両別名を修復 | 他経路の差分なし | 構文成功報告／326成功を出力確認（stream.jsonl 行17）／最終差分あり |
| c8729ef84481468abef9568261d1fb75 | gemini-4-argon-low | 3・B | 自力特定・実行 | 両別名を修復 | 他経路の差分なし | 構文成功報告／326成功を出力確認（stream.jsonl 行18）／最終差分あり |
| 485fba9a19ae4bf295276c857df5a784 | gpt-6.2-sol | 1・A | 自力特定・実行 | 両別名を修復 | 省略時は空分岐へ。明示的な空引数も消費せず渡す | 構文成功報告／326成功を出力確認（codex-events.jsonl 行19）／最終差分あり |
| 6a053d1f69ba430d9cc3995b4e516eb8 | gpt-6.2-sol | 1・A | 自力特定・実行 | 両別名を修復 | 引数省略時の shift 失敗を解消 | 構文成功報告／326成功を出力確認（codex-events.jsonl 行24）／最終差分あり |
| a1ec2bb78d6144d5bfa34eef27a1d55e | gpt-6.2-sol | 1・A | 自力特定・実行 | 両別名を修復 | 引数省略時の shift 失敗を解消 | 構文成功報告／326成功を出力確認（codex-events.jsonl 行22）／最終差分あり |
| 23c09f3316164da88227466667455b4e | gpt-6.2-sol | 1・A | 自力特定・実行 | 両別名を修復 | 引数省略時の shift 失敗を解消 | 構文成功報告／326成功を出力確認（codex-events.jsonl 行22）／最終差分あり |
| dbd14d9ceebc486c8866de437e5501dc | gpt-6.2-sol | 1・A | 自力特定・実行 | 両別名を修復 | 引数省略時の shift 失敗を解消 | 構文成功報告／326成功を出力確認（codex-events.jsonl 行19）／最終差分あり |

「最終差分あり」は保存差分を評価者が確認したことを示す。モデルによる差分確認とテスト全件成功を一律に保証するものではない。省略時の shift 失敗の解消は追加の挙動変更。明示された v4・v 以外にも影響したため独立に記録した。

## 証拠の照合キー

各実行の rating-view/result.diff と rating-view/final-response.txt の SHA-256。原記録は非公開の試験保管場所にある。元の結果IDは登録ファイル名に対応する。

| 実行ID | 元の結果ID | 差分 | 最終応答 |
|---|---|---|---|
| 8ad5d6c9ec41429a87dcae2ef7995184 | 59e93eaaeb87435c9c0d94d80df9bb9d | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 661ac836abe9aad2f686e0e794cc4077340b00be3c13f6d4ca71ba0cfa188e17 |
| 3285a40b94864a01a95a278268432bea | 59e93eaaeb87435c9c0d94d80df9bb9d | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | c0c49a040197abc8976b03f2dc7d3874e09c6d313cfb4d28177a6bffee02a37f |
| 9989d2ad72284c7f870e72327aeda3b6 | 59e93eaaeb87435c9c0d94d80df9bb9d | 2e9f3566a963a67f498490434397ff53a5c7198b41b586c020a55ae2942180af | 4c209456859f671400fe29c6479387622a309d60ff39cbdbf495b93687259f6c |
| 02325a70f88741a1a73278e5eaa8844e | 59e93eaaeb87435c9c0d94d80df9bb9d | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | e5beb6a94cc9d073eab4b9884e3094743d6bad621ebfc679a583179f266ee4a1 |
| 4a118fd86f794de7be92ccbbb8e77370 | 107d31cdae9044d08c0768ffc89d3896 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 76143ce1c7f6a9fde879ba3e81b3859acf2e3d8715306cf5eb70a0497870435c |
| 3a37ec1f94df4157a6702d7d35722c28 | 107d31cdae9044d08c0768ffc89d3896 | 2e9f3566a963a67f498490434397ff53a5c7198b41b586c020a55ae2942180af | 547acbe8a8f7ba077bfc282b623ced398a8d68db638660560086782180d05b9b |
| 851b97526bb449e4ac2e0b257faf1747 | fdc86bfd09a349d5a64b768c0adf450a | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | d2ce956ea49175f02fcbfd96e535718cf7ee6225b4937b3d4f52019bf6629999 |
| 1d1e209856e04482b1c37d00f68b0913 | 93b6fffaf01742eaa5bcd078cf6ba3e6 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 0934ba9b9fa5a1dd9bf41e3f4c4163d20ef8bd74ad62795c921e2f34741a15ad |
| daf49b9bd6534ee1affcff06d04e7902 | c67f35690bd34cb38a504285500cc0bf | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | c9808df858f651bf4eeb2679b65125cefa3bcf4f5b372159eb06b48db613fd22 |
| 7e382bb872b6477691b5b2077fbc4557 | 5ee97407c0e848d4b96bc5e6f32fe28e | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | ec0accb4805b0cbfc5409e2dfbf97677db19aa2bd8c700626b9c448d2f600722 |
| 6953d68551624c4f9950abb7386931de | d5001b92579f486da96a886ad23a3742 | 978ad4b876ed3be97837d57fb27580c267c81854e29663f1b87c7ada2414d96c | 5f32b10e0bc5ecc94ea158a4074976d88e4fbff18e6ba9d2c7930d747f4335cc |
| 8ed6f11695d849718cacd81e138ded32 | d5001b92579f486da96a886ad23a3742 | 978ad4b876ed3be97837d57fb27580c267c81854e29663f1b87c7ada2414d96c | 8054e0bcf3305d8257691f12dd075b2c0eb9dd4670646d188f55ea46f77a9759 |
| 9c6eb5d366384c41a7386e34fb7d9b91 | 42391c16154646c3a63b206abfb033c2 | 978ad4b876ed3be97837d57fb27580c267c81854e29663f1b87c7ada2414d96c | d73b02f574f23387e996862609406d49e90ff83d694b46f028c34b3d9e8bc7f6 |
| fbaaaf91e8f84d6f963f6b25bab6d394 | 40b1c34285aa43d1a2c94724418003e2 | 978ad4b876ed3be97837d57fb27580c267c81854e29663f1b87c7ada2414d96c | 946c24a0ff96bc8f0b0d6887daa9d674a01be5fb43a9813c0586c7e635448f0f |
| 4f246e87e7fc48188921c4ca6f6b7400 | 8a94e6acbc1645e389af218a1dba837f | f07dade8337642f8e6950857480198f21631865af6df360333011498abdfd453 | d7b38498e4f3d47d6de7bee47f54f3ea97d11f29a7d450285e9314f30558133d |
| a6688a5345f544d29e5fc8e6b3bdca28 | 8a94e6acbc1645e389af218a1dba837f | 812a6e9ffcdbba41756f3b10a15f53459c7bacc22f79948283833eed621eb846 | f52029ce52125151a8361cf6070ccb211e3799ec2b65db63c51edfb9acf5eed0 |
| cceab46bbf65466393680eea69ccdd8b | 8a94e6acbc1645e389af218a1dba837f | f07dade8337642f8e6950857480198f21631865af6df360333011498abdfd453 | 4a7b83bcd4c8fb827c20862e24c9fe10493334f45a658fe9e11bbf5035e458c4 |
| 20b634b438cf4fb58fa7e73e1149c451 | 51d24ca1ceaa46c2884041aff64364f5 | f07dade8337642f8e6950857480198f21631865af6df360333011498abdfd453 | 42ea14ae0ade3cfb613f8b7f39ff69efb81cbf0ecdc6b19fb55f20eb6a6328eb |
| 293c01226f1b450b80a27338581061c9 | 51d24ca1ceaa46c2884041aff64364f5 | 44d88434c5311826f4fbc812a8c8e5d9815b3a49465024184754af3c0a8d214c | 70a39c3bd822f2abe4fad3f4d6b620013bf4cd803cc53af1f422d72370a92ba7 |
| 2fd3a54ec73149a9b74e05d1c1dc3c9a | 51d24ca1ceaa46c2884041aff64364f5 | 812a6e9ffcdbba41756f3b10a15f53459c7bacc22f79948283833eed621eb846 | 6c96755f0f83170d2d3477017f2d7e3b8ad0d5e429a2080e3b639ceacd182e84 |
| 1d51f7e7420249ed9eb8d7bb9f7e9228 | c459cb8f6a73484b988a45e38a60e4b5 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | cc5417c43bd66147a5bcea2de37fded1e84c1fbddfa376717ca60e52830ef2cc |
| 5760911f3db8425cacc15fb789503895 | c459cb8f6a73484b988a45e38a60e4b5 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | c35cc3c6d0d9f8d7ba82384d67a5399722b1acea061b2b502c62319b5291ee24 |
| 80b7a35c636e4ff39f6b65c6f4e225c7 | c459cb8f6a73484b988a45e38a60e4b5 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | b47fbe270bdb2d8cc1a6bf038224bbd06c087a9f4bfb699df99c300394004324 |
| a3b70353dfb441b4949a34757c8c2387 | c459cb8f6a73484b988a45e38a60e4b5 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | aba4efcead661c56014ad3f4ec7b5f418e88946c3ba80d9653942aae070575c0 |
| f62156e6a9194d79bc11a99716c34e03 | c459cb8f6a73484b988a45e38a60e4b5 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 39b2dfc57ce2d1a7facdc07bef441dd5a9a4d0220ab7fa28eae7466e92c8d252 |
| 21ed85b91e004d7e943c8fc5d1daa03e | 39371075db1249a4b534efce76ebcd4f | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 777596b912fa044bfd3ff9f9e342805c629d68aa651646bac76199b9dfd347e3 |
| 56e0c9dd677a4a36924d9a247147c263 | 39371075db1249a4b534efce76ebcd4f | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 34019891feb93b7c616ea67b7446e206a0f4d240f7e7ab30ac51ab50270bfe94 |
| 7e00e4607e1e4cf7a6bfa66b39c08322 | 39371075db1249a4b534efce76ebcd4f | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | dca2cd3337c334bbd982b83248740a4c23b6513b7a7cd9a956a9c3ef279c40be |
| 97237ffe40ec44c9a93759ba7685b5c3 | 39371075db1249a4b534efce76ebcd4f | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 53ea632f6ccc073c3e0ef6d1c11078fa6de1a5a7291afa2530541b1a7f6663ce |
| d829034134be44909ddd5873a896607c | 39371075db1249a4b534efce76ebcd4f | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 7876e5f1243049fb247fe490af2844eacaeea04ab07b8cf9727456e072e925c9 |
| a85002b9738a483790fa0aec3a1724db | 819891d6b5c24e6494defe50381ea2f0 | 978ad4b876ed3be97837d57fb27580c267c81854e29663f1b87c7ada2414d96c | 9193070d6f5323e7180c03e6137d387b460d4c1d95a75f186f63565e57e1cf1c |
| 5c0d804048ca4df38c4a704f621db02d | 3cb465b8be0d47dabc76418ec7a66be4 | 978ad4b876ed3be97837d57fb27580c267c81854e29663f1b87c7ada2414d96c | fdad7952a95da415ca8ac04243ee12e89585e00068aecd60c458db6c69d2961d |
| 8fc459a3bb3b4427a9699706eae9e11e | 3cb465b8be0d47dabc76418ec7a66be4 | 978ad4b876ed3be97837d57fb27580c267c81854e29663f1b87c7ada2414d96c | 550fed27c7ca341cff8d2492c64cc591ee35436fb828bec30351d7e70c274de9 |
| c8729ef84481468abef9568261d1fb75 | 3cb465b8be0d47dabc76418ec7a66be4 | 978ad4b876ed3be97837d57fb27580c267c81854e29663f1b87c7ada2414d96c | b7fc473a0727914994b3df878feb964a508a0501b3c8ff99249fe4530cd7fd46 |
| 485fba9a19ae4bf295276c857df5a784 | e28ce3d6a84a46649868d7e88829e594 | 343a0cb992e1f5d5f04b43d428523a2865874382d513261eda23d61bc3296213 | 48a4a30e0ca4911cccf98f945efc211be66cf0d3e992a3f279f956e1baafa6ce |
| 6a053d1f69ba430d9cc3995b4e516eb8 | e28ce3d6a84a46649868d7e88829e594 | 812a6e9ffcdbba41756f3b10a15f53459c7bacc22f79948283833eed621eb846 | 42d199e0d3b0712ea574a4a41df8e2727d12e8c5dfebe6b16261eaf4e5040d0a |
| a1ec2bb78d6144d5bfa34eef27a1d55e | e28ce3d6a84a46649868d7e88829e594 | ab7e960def50e36d6b11d46ece4fc89b8dfc96f1c9de33c1cca19a21d1289add | 562ba0c5bb4ca237fd96a351529936ecc003308933589f9fa21ef0e2fa44700b |
| 23c09f3316164da88227466667455b4e | f3a29c1bff224fd6aacfb289fdb88508 | 812a6e9ffcdbba41756f3b10a15f53459c7bacc22f79948283833eed621eb846 | 636afa00ddfaedec229934a9f1f6adf952e5506bc128aa8f36969d252db4d83f |
| dbd14d9ceebc486c8866de437e5501dc | f3a29c1bff224fd6aacfb289fdb88508 | 812a6e9ffcdbba41756f3b10a15f53459c7bacc22f79948283833eed621eb846 | 2f4bf4eb08a0cb970cd9a31cbd821291830853889cd646d1043a4944fabfc1fa |
