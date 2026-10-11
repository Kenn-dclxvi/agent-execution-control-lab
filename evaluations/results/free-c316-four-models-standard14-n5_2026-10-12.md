# FreeとC316の4モデル比較、Standard14 N=5（2026-10-12）

2026-10-12。利用者の依頼で、C316（[設計記録](../../docs/candidate315-candidate316-c313-file-read-receive-form-design.md)）を、まだ測っていなかったClaude Code Opus 5.5 lowとGPT-6 Astra LowでN=5測り、すでに測っていたSol LowとSonnet lowと合わせて、4つのモデルでFreeと比べた。条件は2026-10-10のFreeの計測と同じ（実行環境を切り離し、負荷を見て次のrunを始める発行、CPU使用率70%以下、間隔1秒、合計24本、一つのセルずつ流す）。Freeは70件を流し直さず、実効互換の規則（`effective-v1`）のプールへ登録し直して集計した（値は元の集計と同じ）。費用は、比べる両方を単価表`api-standard-2026-10-10-r2`で数え直した。**C316は4つのモデルすべてで70件が4点になり、費用はどのモデルでもFreeの5反復の幅より下だった。**

## 結果

| モデル | 点数分布（Free → C316） | 費用 Free（USD） | 費用 C316（USD） | 費用の差 | 経過時間 Free（秒） | 経過時間 C316（秒） | 経過時間の差 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| GPT-6.1 Sol Low | 4点69件・0点1件 → 4点70件 | 0.9344（0.8397〜0.9810） | 0.6421（0.5709〜0.6803） | −31.28%（幅より下） | 636.90 | 505.65 | −20.61%（幅より下） |
| GPT-6 Astra Low | 4点68件・0点2件 → 4点70件 | 6.1484（5.6532〜6.4405） | 4.1229（3.8843〜4.8369） | −32.94%（幅より下） | 634.75 | 497.36 | −21.65%（幅より下） |
| Claude Code Sonnet 5.5 low | 4点65件・0点5件 → 4点70件 | 0.6997（0.6776〜0.7323） | 0.6216（0.6097〜0.6469） | −11.17%（幅より下） | 249.24 | 232.75 | −6.62%（幅より下） |
| Claude Code Opus 5.5 low | 4点69件・0点1件 → 4点70件 | 1.2731（1.2379〜1.3126） | 1.1249（1.1058〜1.1410） | −11.64%（幅より下） | 269.41 | 247.12 | −8.27%（幅より下） |

生のトークン（参考）の中央値は、Sol Low 2,218,847 → 1,419,555、Astra Low 2,256,298 → 1,471,177、Sonnet low 859,525 → 804,438、Opus low 750,215 → 691,777。

## 読み方の注意

- Codexの2モデルでは、共通の先頭部分のキャッシュが別のrunの間でも共有されるため、計測の始めのrunで最初のリクエストがキャッシュに乗らないことがある（[診断の記録](codex-first-request-cache-order-diagnostics_2026-10-10.json)）。最初のリクエストがキャッシュに乗らなかったrunは、Astra LowでFree 36件・C316 34件で、どちらも単独で最初に流した計測としてほぼ同じだった。Sol LowはFree 7件・C316 2件だった。費用は実測のままで、数え直していない。
- Freeの0点は、どのモデルでもA01（求める結果が決まっていないケース）で、結果が決まる前に編集や試験へ進んだものである。C316ではどのモデルでも起きなかった。Sonnet lowの品質の中央値はFreeが92.86、C316が100.00。
- 費用はモデルごとに単価が違うため、モデル間の金額の大小はモデルの優劣を示さない。
- Opus lowのC316のプロファイルは、Freeと比べて評価コードの`scripts/atomic_run_registry.py`のSHA-256だけが違う。これは実効互換の規則で記録だけの項目で、各runの課題文の一致は`compare-analyses`で確かめた。
- 経過時間のうちモデルの応答時間は、計測の時間帯で揺れる。時間差をプロンプトだけの効果とは断定しない。

採用、追加反復、release、本体反映は行っていない。

## 一次アーティファクト

- Opus low：[登録結果](85740d6fa5004bc9aa4abab14d0a4855.json)・[analysis](c316-claude-opus55-low-standard14-n5_2026-10-12-analysis.json)・[selection](c316-claude-opus55-low-standard14-n5_2026-10-12-selection.json)・[品質監査](c316-claude-opus55-low-standard14-n5_2026-10-12-quality-audit.json)・[発行前の記録](c316-claude-opus55-low-standard14-n5_2026-10-12-prepare-receipt.json)・[発行の記録](c316-claude-opus55-low-standard14-n5_2026-10-12-dispatch-summary.json)・[Freeとの比較](c316-claude-opus55-low-standard14-n5_2026-10-12-free-comparison.json)
- Astra Low：[登録結果](9dd8bfdc985543e4aca15c6656ddcd60.json)・[analysis](c316-astra6-low-standard14-n5_2026-10-12-analysis.json)・[selection](c316-astra6-low-standard14-n5_2026-10-12-selection.json)・[品質監査](c316-astra6-low-standard14-n5_2026-10-12-quality-audit.json)・[発行前の記録](c316-astra6-low-standard14-n5_2026-10-12-prepare-receipt.json)・[発行の記録](c316-astra6-low-standard14-n5_2026-10-12-dispatch-summary.json)・[Freeとの比較](c316-astra6-low-standard14-n5_2026-10-12-free-comparison.json)
- Sol Low：[計測記録](c316-sol61-low-standard14-n5_2026-10-12.md)・[Freeとの比較](c316-sol61-low-standard14-n5_2026-10-12-free-comparison.json)
- Sonnet low：[計測記録](c316-claude-sonnet55-low-standard14-n5_2026-10-12.md)・[Freeとの比較](c316-claude-sonnet55-low-standard14-n5_2026-10-12-free-comparison.json)
- Freeを実効互換の規則で登録し直した集計：Sol Low（[analysis](free-sol61-low-standard14-n5_2026-10-10-analysis-effective-v1.json)・[selection](free-sol61-low-standard14-n5_2026-10-10-selection-effective-v1.json)）、Astra Low（[analysis](free-astra6-low-standard14-n5_2026-10-10-analysis-effective-v1.json)・[selection](free-astra6-low-standard14-n5_2026-10-10-selection-effective-v1.json)）、Sonnet low（[analysis](free-claude-sonnet55-low-standard14-n5_2026-10-10-analysis-effective-v1.json)・[selection](free-claude-sonnet55-low-standard14-n5_2026-10-10-selection-effective-v1.json)）、Opus low（[analysis](free-claude-opus55-low-standard14-n5_2026-10-10-analysis-effective-v1.json)・[selection](free-claude-opus55-low-standard14-n5_2026-10-10-selection-effective-v1.json)）
