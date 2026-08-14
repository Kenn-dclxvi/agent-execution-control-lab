# Candidate221 ADR9 r2 N=5 実行準備監査

## 結論

Candidate210保存result `9ac8eb53cf79463f9c7ae446c61b625a`とCandidate147保存Layer 1へbindした。Candidate221の空poolに対する`plan-missing --desired-count 5`は9ケース各5件、合計45件だけを発行対象へ固定した。

prompt identity以外のcase、fixture、TaskSpec、rating、model、reasoning、Agent/runtime/CLI、permission、executor、target commit / treeおよびtoken accountingは基準resultと一致した。comparison preflightは`ready`、発行前状態は`authorized_45 / issued_0`である。

## identity

- Candidate: `the-caption-3ce91a4-review-source-authority-closure-r1`
- bundle SHA-256: `4e40da5f16466226a053b5bcc5efa31c5600219f4117a8bc0635c3c5a0196562`
- profile: `candidate221-review-source-authority-closure-adr9-r2-medium-m24-n5-cli0146-r1`
- profile SHA-256: `d6daf5895bbad6fca58ac2f8ba3c9bfd8a1d2586e004d59105a6f1c39182f16c`
- reference result: `9ac8eb53cf79463f9c7ae446c61b625a`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- atomic pool key: `10c5e3fe8608a212b504aa87ea29906aa85a31ccbf00f2960e4ea67c46f08006`
- comparison key: `e57ff13335daac3e76c8755cb32214bb62ad5f83a9742d756631e51876066938`
- global plan SHA-256: `d7b763e31dabb8375a5466911aba4ea95d4c87a07d781a1376ae09139fd1eed4`
- dispatch plan SHA-256: `8b6238c23f9ca83eb75cf041ea6e719e8d2fae7ddb6493db8145ac1e735a50e6`
- comparison preflight SHA-256: `34e637215b2e081ff2581678461bb205a21d43f9a61f31973270bc905ad7b1f2`
- execution root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate221-review-source-authority-closure-adr9-r2-n5-20260814-r1`

一件でも品質または機序gateを外れた場合は有効runを保持して停止し、repair rerun、ADR9 N=20、Standard14、採用、releaseおよびprojectionへ進めない。
