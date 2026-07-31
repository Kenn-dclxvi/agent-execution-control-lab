# Candidate108 / Candidate115 authority location discovery targeted結果

## 結論

Candidate115のA01 r2 / A02 r2各N=5は10 / 10件がvalid・rateableだったが、score分布は`4: 6件 / 0: 4件`だった。

A02は5 / 5件がrepository authorityを探索してcanonical成果へ到達し、Candidate114の誤停止1件は解消した。一方、A01は4 / 5件が変更後のmodeを確認せず、source・test探索、実装、試験へ進んだ。authority location探索の許可が、A01の一般的なallowed readまで開いたためである。

品質を大きく崩したため、KPI改善は判定せず、Standard14へ進めない。Candidate115を停止する。

## 固定条件と結果

- candidate: `the-caption-3ce91a4-authority-location-discovery-r1`
- bundle SHA-256: `7761e2ea0e45c244c305ba782431426d62bf11c5b700ca98edfb10b6c96b8d1d`
- direct parent: Candidate114
- KPI reference: 保存済みCandidate108 A01 / A02 result `a4e9efe5f4e844d2badc9fe492e0b7b2`
- cases: A01 r2 / A02 r2
- Rating: v14
- model / reasoning: `gpt-5.6-sol` / `medium`
- CLI: `0.146.0`
- N: case別に5
- profile上のM: 24
- ready slot: 10件
- candidate pool key: `e61a6c5a3f11df9e592861fe3b46eb3c34e317d64252a5957c9cb8d7004cb88d`
- candidate result ID: `f125b0646ea04b2f939df9cc5a1339b3`
- execution: 10 / 10 valid、excluded 0、実時間`127.176`秒

| case | score分布 | token中央値 | elapsed中央値 | 挙動 |
| --- | ---: | ---: | ---: | --- |
| A01 | `4: 1 / 0: 4` | `215,705` | `104.845`秒 | 4件が未確認実装、1件だけclarification |
| A02 | `4: 5` | `163,306` | `85.733`秒 | 5件がcanonical成果へ到達 |

固定schemaの合算中央値はquality `50.0`、token `410,679`、elapsed `192.547`秒だった。qualityが崩れているため、Candidate108との差を効率改善として扱わない。

## 判断

Candidate114の残余A02誤停止をauthority location許可で詰める方向は不成立である。TaskSpecの「authorityを根拠に決定する」という明示要求と、「既存authorityを必要範囲で読める」という一般read permissionをprompt文だけで安定分離できなかった。

Candidate114はA01を5 / 5で制御した一方、A02を4 / 5へ落とした。Candidate115はA02を5 / 5へ戻した一方、A01を1 / 5へ落とした。この二条件のtradeoffが再現したため、同じ`EVIDENCE_GATE`へauthority条件を追加・微修正するcandidateは続けない。

次に再開する場合は、prompt側へ別のsemantic predicateを加えるのではなく、TaskSpecが「requested valueそのもの」と「その値を決めるauthority selector」を区別してmachine-boundで提示できるかを先に検討する。TaskSpecまたはschemaを変更する場合は比較条件変更として、Candidate108との同一prompt比較から分離する。

## 状態

`targeted_a01_a02_evaluated / a02_mechanism_passed / quality_gate_failed / result_registered / stopped`

これは採用、release、runtime projection、THE-CAPTION本体反映を意味しない。

## 証跡

- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate115-authority-location-discovery-v14-medium-a01-a02-atomic-n5-cli0146-20260731-r1`
- execution archive SHA-256: `a087f548b1a4d61a8a61d00138d4397e86334d66ce3aa23ae19d9a73bdf0b77b`
- final archive SHA-256: `65c5f52d728d904382f3e88d433de3b77284f1d91f62d8d02745097e9341b4e0`
