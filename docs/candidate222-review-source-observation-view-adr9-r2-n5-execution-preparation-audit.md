# Candidate222 ADR9 r2 N=5 実行準備監査

## 結論

Candidate210保存result `9ac8eb53cf79463f9c7ae446c61b625a`とCandidate147保存Layer 1へbindした。Candidate222の空poolに対する`plan-missing --desired-count 5`は9ケース各5件、合計45件だけを発行対象へ固定した。

prompt identity以外のcase、fixture、TaskSpec、oracle、rating、model、reasoning、Agent/runtime/CLI、permission、executor、target commit / treeおよびtoken accountingはCandidate221の固定ADR9 r2条件と一致した。comparison preflightは`ready`、発行前状態は`authorized_45 / issued_0`である。

最初のatomic plan生成は、参照したCandidate221 templateのprompt identityがCandidate222 poolと一致せず停止した。続く最初のrunner起動も、templateの実行用prompt bundle参照がCandidate221のままだったためadapterがmodel起動前に全件を拒否した。どちらもpreflight上の評価slot発行数は0件である。失敗rootは保持し、新しい`r2` rootで9 templateの`binding.prompt_set_identity`、`parameters.bundle_sha256`および`parameters.prompt_bundle`だけをCandidate222へ置換した。これら3項目以外がCandidate221 templateと一致することを確認してから再生成した。

## identity

- Candidate: `the-caption-3ce91a4-review-source-observation-view-r1`
- bundle SHA-256: `6ccb9fa020e65898e5a445d37db1338fa75cc917116fd09a6e87fc48d0dcdfad`
- profile: `candidate222-review-source-observation-view-adr9-r2-medium-m24-n5-cli0146-r1`
- profile SHA-256: `3af1268b6b7df052d0af3a6b199af9a63ae63488208e09b105292cac527f4bbc`
- reference result: `9ac8eb53cf79463f9c7ae446c61b625a`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- atomic pool key: `337fc0883baac9f76dc449eb610e88f17fe5686dfac798bc69f924a0b4b3bfa7`
- comparison key: `e57ff13335daac3e76c8755cb32214bb62ad5f83a9742d756631e51876066938`
- global plan SHA-256: `4f05a1556c6c942484b5e203ab7a2d578d979647fd2f00c4224f984ede38a093`
- dispatch plan SHA-256: `b35fdf87e10dc6912b591876cd5a9823c503935e92371940ae05537a7939077b`
- comparison preflight SHA-256: `b14f5c491c7341c702df7d5ea536ee06a86b34132e7e53684e54fd3b8356fa72`
- execution root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate222-review-source-observation-view-adr9-r2-n5-20260814-r2`

目的は試験成功ではなく、必要reviewがrootへのreviewer-owned value配送なしで完遂されるかを観察することである。一件でも誤配送、必要review欠落、必要値欠落、root補完またはresult effect不一致があれば有効runを保持して停止し、repair rerun、ADR9 N=20、Standard14、採用、releaseおよびprojectionへ進めない。
