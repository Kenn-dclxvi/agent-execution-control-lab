# Prompt bundles

登録済みprompt bundleは次の三つである。

- 測定成立control: [`baselines/portable-semantic-a544769-control-free-r1/`](baselines/portable-semantic-a544769-control-free-r1/)
- 直接の親・効率reference: [`baselines/portable-semantic-c147-full-agent-reference-r1/`](baselines/portable-semantic-c147-full-agent-reference-r1/)
- portable full-agent Candidate: [`candidates/portable-semantic-c147-portable-full-agent-r1/`](candidates/portable-semantic-c147-portable-full-agent-r1/)

portable Candidateのmanifestはimmutableな作成時状態`registered_not_evaluated`を保持する。後続の正式resultは14 / 14 valid、7 / 14 score 4でquality gate不通過である。reference Profileとrunは作成しない。root-onlyは別Candidate作成前gateが未固定であり、target固有bundleへ登録していない。

両bundleのmanifest、contentおよびCandidate composition bindingは[`full-agent-bundle-registration-r1.json`](full-agent-bundle-registration-r1.json)へ固定する。componentは管理sourceに留め、実行時には各bundleの`AGENTS.md`一枚だけを配送する。
