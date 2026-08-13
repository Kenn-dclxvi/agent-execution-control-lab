# Candidate216 packet construction projection 実装監査

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
| Candidate | Candidate216 |
| prompt identity | `the-caption-3ce91a4-packet-construction-projection-r1` |
| direct base | `the-caption-3ce91a4-result-effect-scope-r1`（Candidate147） |
| storage format | `instruction-suffixed/v1` |
| bundle SHA-256 | `77a0f660d7066bee128785814517a7899d18086e0c0617b9bc90feebe3995eb6` |
| root `AGENTS.md` SHA-256 | `cb982be26e32e926398d67aaa69ae28f89dd79d9958117edd0663168408b4378` |
| changed target | `AGENTS.md`だけ |
| 評価状態 | `quality_failed / mechanism_failed / stopped` |

## 実装範囲

Candidate147のfull bundleを直接基盤とし、root `AGENTS.md`だけを変更した。manifestの19 targetのうち、`AGENTS.md`以外の18 targetはCandidate147と同一である。

変更は次の一つの構造provenance軸である。

1. artifact変更前reviewへ、packet constructionと同じoperationでliteral data dependencyの一意なstructural path / range / subtreeをprojection receiptとしてmaterializeする境界を追加した。
2. 元readがwhole-containerでも一意なprojectionを保持し、曖昧、複数origin、要約、変換または出所不明の場合だけcontainer fallbackへ戻した。
3. projectionと同一・祖先・子孫・重複するreadを閉じ、固定非重複regionは既存のterminal disposition effect predicateが成立する場合だけ許可した。

## 持ち込まなかった制御

- case別のfield / scope / observation対応
- value equalityまたは意味からのsource推定
- 成功runのtool順、read順または判断順
- executor、adapter、runtime hookまたは外部wrapper変更
- Candidate215をprompt親とする系譜

Candidate215は、必要非重複routeが成立した13 readと、projection identityが揺れた失敗9 runの保存証拠だけに使った。

## 静的検証

- `verify_bundle()`が成功した。
- manifestのbundle SHA-256再計算値が一致した。
- Candidate147との差分targetは`AGENTS.md`だけだった。
- 非変更targetは18件だった。
- root本文にcase identity、固定path、固定field / scope / observation identityまたは期待dispositionを含めていない。
- construction-time projection materialization、whole-read selector非依存、一意でない場合だけのfallback、value / meaning inference禁止を固定した。
- bundle identity snapshotへCandidate216を追記した。

## 評価結果

ADR9 r2全9ケースN=5は45 / 45 valid、Score `4 / 1 = 44 / 1`だった。projection重複read、packet caseの誤paired readおよびroot prereadは各0件だった。一方、ADR06の1件が期待terminalから外れ、ADR07 / ADR09では不要なdesign-container readが14回、7 runに残った。品質・機序とも不通過のため停止し、Standard14を開始していない。

## 参照

- [Candidate216作成前設計](candidate216-packet-construction-projection-design.md)
- [Candidate216方向監査](candidate216-packet-construction-projection-direction-audit.md)
- [Candidate216 manifest](../prompts/candidates/the-caption-3ce91a4-packet-construction-projection-r1/manifest.json)
- [Candidate147 manifest](../prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1/manifest.json)
- [Candidate216 ADR9結果](../evaluations/results/candidate216-packet-construction-projection-adr9-r2-n5_2026-08-14.md)
