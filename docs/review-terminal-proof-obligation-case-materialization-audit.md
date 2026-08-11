# review terminal proof obligation case materialization監査

> **位置づけ**: 6ケースの機械監査完了／private oracle 6 / 6一致／fixture再現6 / 6成功／Candidate未作成／評価未実施

## 結論

最小方向設計の6条件を`review-terminal-proof-obligation-r1`としてmaterializeし、model-visible fixtureから最小方向probeが導くrouteとprivate oracleが6 / 6件で一致した。全seed patchは固定target `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`へ再適用でき、期待seed commitとtreeへ一致した。

初回生成では新規ファイルをindexへ載せる前にdiffを取得したため空patchになった。監査で一件目の実行前に検出し、全6ケースをcached diffから再生成した。空patch版は評価、Candidate、profile、ratingまたはrunへ使用していない。

## identity

- general design: `review-terminal-proof-obligation-minimal-direction-r1`
- Target評価設計: `review-terminal-proof-obligation-targeted-evaluation-design-r1`
- case suite revision: `review-terminal-proof-obligation-r1`
- set: `the-caption-review-terminal-proof-obligation-direction-r1`

## fixture再現

| case | expected seed commit | expected seed tree | 結果 |
|---|---|---|---|
| `TC-TPO01` | `85331368fb47be1fb0b06a766bff838cbf149af4` | `107bf121077f0915629dfb3e1920059746885f6f` | 一致 |
| `TC-TPO02` | `5c87246730d1ead3c88a81f0bc11562ba3738edf` | `bf6f7a69cfd020010d485e93c2d4d65e24f114c8` | 一致 |
| `TC-TPO03` | `8fae332ee213349b6ec9a8978dec82db3c4e0200` | `f73c4cab58a10320b3b3593db8c3999cc0fd47a5` | 一致 |
| `TC-TPO04` | `430b9237e065418fdc8de8a840e038cda726d751` | `ddecb9925a1c165ffacff3d27923d075a56cd27a` | 一致 |
| `TC-TPO05` | `411204344b3b55786098d423b1f64d298a2e1cb8` | `6970214be0871abcbd761e6e577e06e3edaf4c88` | 一致 |
| `TC-TPO06` | `4452772fb3265071b3b6d777da2646a95ff20c5a` | `f09472a8dbf643e5bd30bd3f663db001bdbc7e99` | 一致 |

## 機械監査

- case、revision、design、評価設計、set identity: 6 / 6一致。
- seed patch hash: 6 / 6一致、空patch 0件。
- private oracleと最小方向probe: 6 / 6一致。
- trial inputへのprivate oracle、過去Candidate、r1〜r9 review系列の漏洩: 0件。
- `TC-TPO03`と`TC-TPO04`: `direction_facts`差分は`closure_complete`だけ。closure evidenceの実在差も一致。
- `TC-TPO05`: 二effect、end state、relation、追加effect 0件をauthorityが直接固定。
- `TC-TPO06`: permission=`denied`、先行result operation identity不一致、permission否定後review操作期待0件。

## 試験

- focused: `.venv/bin/python -m pytest tests/test_review_terminal_proof_obligation_cases.py -q`
- focused結果: `5 passed`
- full discovery: `.venv/bin/python -m pytest -q`
- full結果: `1117 passed, 1826 subtests passed`

## 次のゲート

ケースmaterializationは完了した。次はCandidateを作らず、rating contract、問題資格確認対象、反復数、valid run admission、固定Layer 1比較条件およびCandidate作成条件を一つのTarget評価実行設計へ固定する。

## 状態

`case_materialization_complete / six_of_six_oracle_match / six_of_six_fixture_reproducible / focused_5_passed / full_1117_passed_1826_subtests_passed / candidate_not_created / profile_not_created / rating_not_created / evaluation_not_started`
