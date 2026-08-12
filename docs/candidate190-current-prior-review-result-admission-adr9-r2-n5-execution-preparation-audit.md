# Candidate190 current/prior review result admission ADR9 r2 N=5実行準備監査

> **結果**: `execution_preparation_passed / thirty_slots_authorized / zero_slots_issued`

## 結論

Candidate190のADR9 r2変更効果6ケース各5件、合計30 slotは発行直前まで準備できた。保存済みCandidate176 atomic runから同じ6ケース30件を参照selectionへ固定し、prompt identity以外の互換条件を`preflight-comparison`で照合した。comparison preflightは`ready`であり、Candidate190の不足30件だけを許可している。

対象はADR03、ADR04、ADR05、ADR06、ADR07およびADR09である。6 template、30 capsule、global plan、resource class、prompt bundle identityおよび固定Layer 1は一致した。templateとcapsuleに過去Candidate identity、Score、期待terminalまたはmechanism predicateは混入していない。評価runはまだ一件も発行していない。

## 基準resultと互換性

- reference source result ID: `d3e91302f0d14350906075676c5a2791`
- reference subset selection ID: `7f27430b6ddf4046b297618c67dba2db`
- reference subset result ID: `01b8c23f5d014a54aad518757005978e`
- compatibility key: `d09c57a94101d4e2682efbf93a44a456a04e9378556859726d58af872edb6152`
- Candidate190 pool key: `d97416cdfd6166855007970e32f1ac15a22339fcd348b453f27efc166af70df3`
- Candidate190既存run: 全6ケース0件
- dispatch: 各ケース不足5件、合計30件
- max workers: `24`

Candidate176のatomic runはCandidate190へ再利用していない。保存済みrun、resultおよびLayer 1は、case、fixture、TaskSpec、rating、model、reasoning、runtime、permissionおよびexecutor条件を照合する基準としてだけ使用する。新規発行対象はCandidate190だけである。

full ADR9 Layer 1のfixtureとset identityをそのまま再利用し、参照selectionと同じ6ケースcoverageだけを`bind-coverage`で固定した。最初にfull 9ケースcoverageを渡した準備は一致gateで停止し、slotを発行していない。その不一致準備物は`cycle-failed-full-coverage`として保持し、current cycleへ混ぜていない。

## 固定identity

- Candidate190 bundle SHA-256: `63d8a79139e2b1e89268455cf997ccf7bd078b37d1bf44e51e0079aa05bfc30c`
- reference selection SHA-256: `c158b5946654386988710ede5d3c226e1088eb6825018662b7643fbf95856696`
- reference profile SHA-256: `04a3688fbd3b832197f8433bdb567564b0fa9402c2b941e37f1fb2dc85c5a3e0`
- dispatch plan SHA-256: `b60806488738b74351ab963301d89b175e589e4cef2fbed692d9e0a0e9b9273d`
- global plan SHA-256: `01f9b11a0b769edb72d4cc9459a35e0e5d1a2c206e40f7781216ed56568e2cd4`
- comparison generation SHA-256: `79db3977a11e95d68c64abc212fb76089f9abc8cbf247997c3b3f9224e7daeaa`
- comparison preflight SHA-256: `3dd207768406beedfde02ea1d86aea9321e5f9a021ce35614e9e87b8e1524e99`
- resource class SHA-256: `86aa0920e9a45248b653ac3c3ac077680012f368b0adfec2e697dd3b4b928c35`
- preparation root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate190-current-prior-review-result-admission-adr9-r2-n5-20260812-r1`

## 境界

これは実行可能性、互換性および入力固定の監査であり、Candidate190のquality、mechanism、prior result runtime経路、Standard14、採用、releaseまたはprojectionの結果ではない。次に許可される操作は、固定global planのCandidate190 30 slotを発行することだけである。発行後にLayer 1、profile、template、capsule、dispatch plan、global planまたはpreflight receiptを変更しない。

## 状態

`execution_preparation_passed / reference_compatibility_verified / candidate190_only_thirty_slots / authorized_thirty / issued_zero / private_boundary_passed / ready_for_execution`

## 後続実行

固定global planは変更せず発行され、30 / 30 valid、除外0件、runner error 0件で完了した。本監査の実行前状態は上書きせず、結果への導線だけを追加する。現在判断は[`Candidate190 ADR9 r2変更効果6ケース N=5`](../evaluations/results/candidate190-current-prior-review-result-admission-adr9-r2-n5_2026-08-12.md)を正本とする。
