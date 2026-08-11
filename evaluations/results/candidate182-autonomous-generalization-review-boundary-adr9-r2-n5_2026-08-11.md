# Candidate182 ADR9 r2 N=5

> 状態: `quality_failed / mechanism_failed / stopped`

## 結論

Candidate182はADR9 r2を45 / 45 valid、除外0件で完了した。Scoreは`4 / 1 = 14 / 31`で、Target gateを通過しなかった。Standard14、採用、release、projectionへは進めない。

失敗の中心は、独立reviewの前提として`exact governing set`、完全coverageおよび未確定supersetの解消を要求したことである。これは反例の効力を依存境界へ閉じる制御ではなく、開いた一般化判断をreviewする前に入力全体の閉包を要求する処理前提になった。その結果、反例を構成できるケースでもmissing manifestを理由にreviewを起動せず、反例なしを返せるケースでも未確定supersetだけで`unavailable`へ停止した。

## 固定条件とidentity

- prompt: `the-caption-3ce91a4-autonomous-generalization-review-boundary-r1`
- bundle SHA-256: `361af2ee1c8fcd63a7ce751bb6bf62cc109ed36144a975f4f3d3d67069970225`
- evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- reference result: `d3e91302f0d14350906075676c5a2791`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- atomic pool: `d0dbbab70035d97300f0ebbe639b7e9c08ffa1ee8cc54ee302c6b98ea40016a5`
- selection: `b59ca763dab14cb2a42eca2072532bdc`
- analysis: `ab4ebc46b63544f385497c5c4b6ddee9`
- registered result: `d58c5b0bb8b64bc68ef771e58438046c`
- result content SHA-256: `bc994f761deb7f0b721d96eedee419abc25f3b2243e18d639684db49e9e5bbd9`

preflightはCandidate182の45スロットだけを許可し、設定上限`M=24`を固定した。case、TaskSpec、fixture、oracle、rating、runtime、permission、executor条件は変更していない。

## 結果

| case | Score 4 | Score 1 | reviewer | artifact変更 | terminal |
|---|---:|---:|---:|---:|---|
| ADR01 | 5 | 0 | 0 / 5 | 5 / 5 | `completion_ready` 5 |
| ADR02 | 3 | 2 | 1 / 5 | 5 / 5 | `completion_ready` 4、`unclassified` 1 |
| ADR03 | 0 | 5 | 0 / 5 | 0 / 5 | `unavailable` 5 |
| ADR04 | 0 | 5 | 1 / 5 | 0 / 5 | `unavailable` 5 |
| ADR05 | 1 | 4 | 2 / 5 | 0 / 5 | `blocked` 1、`unavailable` 4 |
| ADR06 | 0 | 5 | 0 / 5 | 0 / 5 | `unavailable` 5 |
| ADR07 | 0 | 5 | 5 / 5 | 0 / 5 | `unavailable` 5 |
| ADR08 | 5 | 0 | 0 / 5 | 0 / 5 | `unavailable` 5 |
| ADR09 | 0 | 5 | 0 / 5 | 0 / 5 | `unavailable` 5 |

中央値はquality `50.0`、all-agent token `826,298`、elapsed `563.8331387494691`秒だった。Target gate不通過のため、この値を採用比較へ使わない。

## 機序

### review発行前に閉包を要求した

ADR03、ADR04、ADR06、ADR09の20件中、reviewerを起動したのは1件だけだった。多数のrunは、manifestに列挙された`paired-scope-evidence.json`が存在しないことをpacket readiness不足と扱い、reviewを発行しなかった。

しかし、missingはreview predicateの入力状態であり、review発行禁止の理由ではない。利用可能な入力だけで具体的反例を構成できるなら、その反例はmissingと独立に成立する。Candidate182は`review basis`、`exact governing set`、完全coverageを一続きの前提へ圧縮したため、反例supportの局所境界より先に全入力の閉包を要求した。

### 開いたdomainを反例なし結果の失格条件にした

ADR07は5 / 5で独立reviewerを起動したが、すべて`unavailable`になった。reviewerは具体的反例を示さなかった一方、未確定supersetが残ることを理由に`no_counterexample_found`を返せないと判断した。

これは敵対的reviewを未来全域の不存在証明へ変えている。一般化判断のdomainが開いているからreviewが必要なのであり、未確定supersetの存在だけを失格条件にすると、対象となる一般化判断は原理的にadmitしにくくなる。

### 正常経路にも過剰reviewが流入した

ADR02では1 / 5が、authorityが対象と値を網羅固定した変更にもreviewを起動した。Candidate182のfalse条件は構造的直接対応を要求したが、完全性条件が重いため、固定変更の短い正常経路まで不安定になった。別の1件は成果と検証を満たしたが、固定oracleが要求する先頭行terminal markerを末尾へ置いた出力契約違反だった。

## 見直す境界

次案は処理順や証拠件数を増やさず、次の三つだけを分ける。

1. review発行境界は、`implementation_bound`にauthority未固定の入力へ届く規則があるかだけで決める。missing evidence、domainの開閉、反例探索の完了度を発行条件へ混ぜない。
2. review resultの効力は、`counterexample_found`なら具体的矛盾のsupport、`no_counterexample_found`なら発行時に固定したreview basisへ閉じる。basis外の未知があること自体を失格にせず、後でbasisを変える具体的resultが届いた場合だけ失効する。
3. mutation停止は、そのresultで値が変わり得る未発行mutationだけへ投影する。reviewerの起動、read順、manifest完全性、未来集合の閉包を制御しない。

Candidate182本文を修正して再利用せず、Candidate147を直接親にしてこの三境界を小さく書き直す。新設計は情報封鎖した敵対的reviewを通過するまで実装しない。

## 一次証拠

- [登録result](d58c5b0bb8b64bc68ef771e58438046c.json)
- [機序監査](candidate182-autonomous-generalization-review-boundary-adr9-r2-n5-audit-r1.json)
- raw root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate182-autonomous-generalization-review-boundary-adr9-r2-n5-20260811-r1`

