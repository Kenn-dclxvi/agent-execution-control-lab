# Candidate112 evidence admission scheduling boundary設計

## 結論

Candidate112はCandidate108を直接親とし、`EVIDENCE_GATE`一規則だけを置換する。

証拠identityを開くadmissionと、開いたinvocationをいつ発行するかというschedulingを分離する。現在許可済みで、一つのresultが他の未発行invocationを変え得ない場合は、既存の`DECISION_BOUNDARY`に従い分割しない。先行resultが次のevidence identityの開放条件になる場合だけ、modelへ戻って次を判断する。

## Identityと状態

- candidate number: Candidate112
- prompt identity: `the-caption-3ce91a4-evidence-admission-scheduling-boundary-r1`
- direct parent: `the-caption-3ce91a4-validation-ticket-terminal-closure-r1`
- changed target: root `AGENTS.md`
- changed predicate: `EVIDENCE_GATE`の置換
- bundle SHA-256: `0a543a6439d73bfe76ad47daf28507b4b5d731bf9b22d4749edf12f2586ae56e`
- evaluation status: `targeted_a01_a02_f01_evaluated / quality_gate_passed / aggregate_cost_tradeoff / evidence_scheduling_not_demonstrated / stopped`
- release: `not_created`
- runtime projection: `not_projected`

## 作成前gate

1. 基準prompt setはCandidate108とする。
2. 最短正常経路は、TaskSpecと適用中authorityから現在許可済みのevidence identityを確定し、相互にdecision boundaryを持たないinvocationを分割せず発行し、全result受領後に一度だけ次を判断する経路とする。
3. 保存済み誤経路はCandidate108 Standard14のA01 iteration 1とする。開始identity、target source、関連test検索、test読取り、authority検索を5回のevidence tool callへ分け、Candidate107の同一selection iterationよりmodel stepが4回、tokenが`93,220`多かった。
4. Candidate108の70 runは全件score `4`だったが、C107比でmodel stepとtool callがそれぞれ`+37`だった。wait増加は20回で、残る17回は証拠取得等の別tool callだった。token増分`1,176,155`の99.7%はinput tokenである。
5. C104の証拠admission自体はC98比のStandard14でtoken中央値`-6.48%`、elapsed中央値`-9.77%`だった。したがってdefault denyと追加identityの開放条件は削除しない。
6. 置換するpredicateは`EVIDENCE_GATE`一つとする。admissionはidentityの許可だけを決め、許可済みinvocationの順序とmodel return boundaryを作らない。
7. 消す判断点は、現在許可済みで相互非依存のevidence invocationを一件ずつmodelへ戻して発行する分岐である。
8. 新しいlabel、allowlist、case固有path、tool名、読取り回数、token上限、時間閾値は追加しない。schedulingは既存の`DECISION_BOUNDARY`を再利用する。
9. 初回評価はA01 r2、A02 r2、F01 r3の各N=5とする。A01で停止品質、A02でrepository authorityからの値解決、F01で変更とrequired validationを確認する。
10. 15 / 15件のscore `4`と、許可外evidence 0件を必須とする。同時に、現在許可済みでdecision boundaryのないevidence invocation間のmodel return、model step、tool call、3 KPIをCandidate108の保存済み互換resultと比較する。
11. 品質またはadmissionが1件でも崩れた場合は停止する。非依存invocationの分割が減らない、またはquality同値でtokenとelapsedの両方が低下しない場合もStandard14へ進めない。

## 変更する規則

```text
EVIDENCE_GATE: 変更前のevidence identityのadmissionはdefault denyとし、最初はTaskSpecから直接決まるevidence identityだけを許可する。requested outcome valueが一意なrepository authorityへ委ねられている場合はそのidentityを許可する。admission自体はinvocationの順序やmodel return boundaryを作らない。現在許可済みでdecision boundaryのないinvocationは分割しない。追加identityは許可済みresultが明示する具体的不足または矛盾にbindする場合だけ許可する。
```

実際のbundleでは、C104から維持する許可identityと追加開放条件を省略せず記載する。

## 非目標

- 再入またはwait回数の直接制御
- validation wrapper、outer yield、executorの変更
- 新しいevidence allowlistまたはcase固有の証拠列挙
- TaskSpec、Evaluation set、fixture、rating、model、reasoning、CLI、permissionの変更
- 採用、release、runtime projection、THE-CAPTION本体反映

## 初回試験

- cases: A01 r2 / A02 r2 / F01 r3
- Rating: v14
- model / reasoning: `gpt-5.6-sol` / `medium`
- CLI: `0.146.0`
- repetition: 各`N=5`
- profile上の並列上限: `M=24`
- ready slot: 15件
- direct reference: Candidate108の保存済み同case atomic N=5

初回gateを通過する前にStandard14 profileを作らない。

## 評価結果

初回試験は15 / 15件がscore `4`だった。一方、Candidate108比でtool callとmodel stepが各`+16`件となり、合算中央値もtoken`+3.53%`、elapsed`-3.10%`のtradeoffだった。事前停止条件に従いStandard14へ進めない。詳細は[`Candidate112 targeted結果`](../evaluations/results/candidate108-candidate112-evidence-admission-scheduling-boundary-v14-medium-a01-a02-f01-atomic-n5-cli0146_2026-07-31.md)を正本とする。
