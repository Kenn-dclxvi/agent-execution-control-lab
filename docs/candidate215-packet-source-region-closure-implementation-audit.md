# Candidate215 packet source region closure 実装監査

## 状態

- `candidate_created`
- `static_verification_passed`
- `ADR9_evaluated`
- `quality_failed`
- `mechanism_failed`
- `stopped`
- `adoption_not_decided`
- `release_not_created`
- `projection_not_performed`

## Candidate identity

| 項目 | 値 |
|---|---|
| Candidate | Candidate215 |
| prompt identity | `the-caption-3ce91a4-packet-source-region-closure-r1` |
| direct base | `the-caption-3ce91a4-result-effect-scope-r1`（Candidate147） |
| storage format | `instruction-suffixed/v1` |
| bundle SHA-256 | `da08a220485f0e48fe38165ec379ae52c60a0cbef9b225b92fc3edb7ff855a4f` |
| root `AGENTS.md` SHA-256 | `e7bec542866056734dcd3c556ab19ee22c80a742b50e47983004a558a207fd8c` |
| changed target | `AGENTS.md`だけ |
| 評価状態 | `quality_failed / mechanism_failed / stopped` |

## 実装範囲

Candidate147のfull bundleを直接複製し、root `AGENTS.md`だけを変更した。manifestの19 targetのうち、`AGENTS.md`以外の18 targetはCandidate147と同一である。

root本文は10,772 bytesから16,372 bytesとなり、差分は+5,600 bytesである。変更は次の二点だけである。

1. `EVIDENCE_GATE`の`implementation_bound`後を、review不要時のartifact変更とreview必要時の`PRECHANGE_REVIEW`へ分岐した。
2. `PRECHANGE_REVIEW`を追加し、packet construction receiptにfixed source regionを保持し、同一containerでもfixed non-overlap regionを必要時に許可し、region不明時だけcontainer fallbackで閉じた。

Candidate147のほかの12条項は逐語で保持した。

## 閉じる辺と維持する辺

```text
packet source region
  -/-> 同一 / 祖先 / 子孫 / 重複regionの再read

same container + fixed non-overlap region + disposition-changing result
  --> reviewer direct observation

same container + region unknown
  -/-> reviewer read
```

意味、field名、scope名またはcase名はpermission判断に使わない。

## 持ち込まなかった制御

- Candidate214のcontainer一律閉鎖
- case別のinventory / contract対応
- 成功runのtool順または判断順
- Candidate200 / Candidate202のrouting tableや手順
- executor、adapterまたはruntime変更

Candidate214は保存traceの反例と正常経路だけに使い、prompt親にはしていない。

## 静的検証

- `verify_bundle()`が成功した。
- manifestのbundle SHA-256再計算値が一致した。
- Candidate147との差分targetは`AGENTS.md`だけだった。
- 非変更targetは18件だった。
- root本文にcase identity、固定path、固定field / scope / observation identityまたは期待dispositionを含めていない。
- fixed regionの保持、non-overlap許可、region未知fallback、manifest-to-receipt禁止を本文へ固定した。
- bundle identity snapshotへCandidate215を追記した。

## 評価結果

ADR9 r2全9ケースN=5は45 / 45 valid、Score `4 / 1 = 41 / 4`だった。投影元regionの重複またはwhole-container readとroot prereadは各0件で、同一container内の必要非重複region readは13回、9 runで成立した。一方、packet構築時の投影regionが一貫してreceiptへ固定されず4件が期待terminalから外れ、ADR07 / ADR09では不要な非重複region readも7回、4 runに残った。品質・機序とも不通過のため停止し、Standard14を開始していない。

## 参照

- [Candidate215作成前設計](candidate215-packet-source-region-closure-design.md)
- [Candidate215方向監査](candidate215-packet-source-region-closure-direction-audit.md)
- [Candidate215 manifest](../prompts/candidates/the-caption-3ce91a4-packet-source-region-closure-r1/manifest.json)
- [Candidate147 manifest](../prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1/manifest.json)
- [Candidate215 ADR9結果](../evaluations/results/candidate215-packet-source-region-closure-adr9-r2-n5_2026-08-14.md)
