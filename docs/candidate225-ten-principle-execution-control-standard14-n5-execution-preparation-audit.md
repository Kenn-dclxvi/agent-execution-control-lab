# Candidate225 10原則実行制御 Standard14 N=5実行準備監査

## 結論

保存済みCandidate147 Standard14 N=5 result `f7baeadc5bd44399ac13cc0e0a8aff48`と保存Layer 1へbindした。Candidate225のprompt identity以外の互換条件は一致し、比較前receiptは`ready`、承認70件、発行0件である。

## 発行前固定

- Evaluation set: `the-caption-standard14-r1` r1、14ケース。
- N: 各ケース5件、合計70 run。
- model / reasoning: `gpt-5.6-sol / medium`。
- runtime: Codex CLI 0.146.0、Python 3.14.5。
- target: commit `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`、tree `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`。
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`。
- permission: `workspace-write / never`。
- configured M: 24。
- token accounting: all-agent v1。
- compatibility key: `cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561`。
- Candidate225 bundle SHA-256: `50d5c742bbf2c983aaa4bf084dfabd810025a023523376323258c124f479613a`。

`seed-pool`はCandidate147のStandard14 pool `2a0816816b146f2083f9d2507e2ac485ecaecf62269e834495347f5bc2be99e5`からCandidate225の空pool `9a57fbacefb23042a087460b07d1b43d249e3613711b139fa6291754dac9448c`を作成した。`plan-missing --desired-count 5`は14ケースすべてを既存0件、不足各5件、合計70件へ固定した。

初回準備先では、比較元Layer 1に既存receiptを含むpathを指定したためwrite-once衝突を検出し、旧Candidate templateのprompt identity不一致も検出した。いずれもpreflight前で、評価slotは0件のままである。新しい`cycle-r2`ではreceiptを含まない保存Layer 1だけをmaterializeし、templateのfixture、TaskSpec、rating、runtime、permissionおよびexecutor条件を変えず、prompt identity、bundle hash、bundle pathだけをCandidate225へ置換した。

`prepare-comparison-layer1`、`prepare_atomic_plan.py`、`preflight-comparison`、`verify-comparison-preflight`はすべて成功した。最終receiptはprofile SHA-256 `5d2f93c45b958831995f2bb08ac010e930d56595ef41e50fb8e097fc16df2c27`、global plan SHA-256 `8d7649b44e416c89a759d1f064b43b073f37bf5162d880e334d3bf72c63f8952`、承認70件、発行0件を固定する。

## 現在状態

この監査が固定したreceiptから70件を発行し、70 / 70 validかつrateable、70 / 70 Score `4`で完了した。発行後の結果は[Candidate225 Standard14 N=5](../evaluations/results/candidate225-ten-principle-execution-control-standard14-n5_2026-08-14.md)へ分離して記録する。

`preflight_completed / authorized_70 / issued_70 / registered_result_89c3babd670c461f8b075e7c9a329248`
