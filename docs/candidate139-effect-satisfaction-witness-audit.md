# Candidate139 effect satisfaction witness監査

## 結論

Candidate139 F02の部分変更を生んだ一次原因は、target数の数え方ではない。`effect_prechange_state(effect)=satisfied`を、required behaviorの接続まで確認せず、関連helperの存在だけでbindしたことである。その誤判定によりupdater側effectとownerが未解決集合から消え、後段の`single_change_target_ready`が実質的に一targetとして扱われた。

次の一軸は、TaskSpec required effectが主張する関係全体を直接観測できた場合だけ`satisfied`へbindする`effect_satisfaction_witness`である。criterionが値の伝播、呼出し、分岐、順序、対関係を要求する場合、helper、symbol、literal、片側artifactの存在だけを充足証拠にしない。

## 比較条件

Candidate128とCandidate139のF02は、次が一致している。

- target repository ref: commit `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`、tree `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- F02 fixture digest: `d97bc408f4039cb02cce46d7d4427875516d2c991427d81066b1f61404f14e66`
- compatibility key: `1a160baf02c918304673639cae670d6d9bad5d235e33e965d641f60fef339d93`
- model / reasoning / CLI: `gpt-5.6-sol` / `medium` / `0.146.0`
- TaskSpec、rating、permission、executor behavior

workspaceのfixture commit SHAは実行ごとに異なるが、比較対象のrepository ref、fixture content identity、comparison conditionは一致している。

## 成功挙動と失敗挙動の差

### Candidate128

F02 N=5は5 / 5 score `4`だった。全runが次の二つを未充足と認識した。

1. primary refreshが`target_date`と`us_market_date`を渡していない。
2. updaterが日付選択用の引数とhelperを持つが、解決したend dateをmarket history取得へ渡していない。

全runが`src/app/v4_engine.py`と`src/domain/collection_history_updater.py`を変更し、focused gateは24件、full gateは326件成功・3件skipだった。

### Candidate139

F02 N=5のうち三件はengineだけを変更し、focused gateが16件成功・8件失敗した。

保存contentには次が同時に存在した。

```python
def _resolve_market_end_date(...):
    ...

def _fetch_asset(...):
    ...
    self._fetch_market_history(asset)
```

`_resolve_market_end_date`は存在する。しかし`_fetch_asset`はそのresultを使わず、`_fetch_market_history`へ`end_date`を渡していない。したがってF02-C2のbehaviorは未充足である。

低Score三件はこの状態を次のいずれかへ読み替えた。

- updater側の日付選択は既に実装済み。
- updater側はrequired focused validationの直接判定対象として閉じられる。
- 初回変更は観測済みのprimary refreshだけでよい。

この判断は、helperの存在とrequired behaviorの成立を混同している。

## 出力量仮説の判定

Candidate128の初回readは各fileを260行または320行へboundedし、resultは46,318文字だった。Candidate139の低Score三件は全file読取を選び、resultは55,367文字、55,524文字、64,363文字だった。一件は最終報告で出力上限によるcontent欠落を明示している。

ただし、三件の保存resultには`_fetch_asset`、`_resolve_market_end_date`、`yf.download`、日付境界testがmodel-visible contentとして存在した。したがって出力量増加は誤判定を起こしやすくした可能性はあるが、三件共通の一次原因ではない。少なくとも二件は、必要な接続欠落を直接観測できる状態で充足済みと判断した。

## 既存制御との重複

### Candidate128

`required_effects_closed`は、変更後もTaskSpecから固定した同じrequired effect集合を保持する。しかし開始状態から充足済みとbindする証拠の完全性は定義していない。誤った`satisfied` bind自体は防げない。

### Candidate136

`effect_prechange_state`はeffectを`satisfied / unsatisfied / unobserved`へ分け、未充足effectだけを変更する。これはF04で既に正しい`colSpan`を再変更しないために必要だった。

一方、`admission済みprechange contentがrequired outcomeを満たす`という定義には、criterionが主張する関係のどこまでを観測すべきかがない。C139 F02ではこの空白が、未接続helperを`satisfied`へ上げる余地になった。

### Candidate139

`single_change_target_ready`はTaskSpec上の単一target domainを定義している。しかし`continuation_effect_change_ready`の判断時には、先行するeffect分類で残った変更だけが強く参照された。したがって下流guardをさらに重ねても、上流の誤った`satisfied` bindを直さない限り同じ縮退が起こり得る。

## 次の一軸

次Candidateでは、`effect_prechange_state(effect)=satisfied`の証拠条件だけを次へ置換する。

```text
effect_satisfaction_witness(effect) :=
  admission済みprechange contentが
  TaskSpec required effectに明示された
  value / call / data flow / branch / order / pair relationの全memberと接続を
  current content上で直接示す
```

```text
effect_prechange_state(effect) :=
  effect_satisfaction_witness(effect)があるならsatisfied
  ∨ current contentがrequired relationの不成立を直接示すならunsatisfied
  ∨ それ以外はunobserved
```

次を`satisfied`の証拠にしない。

- helper、symbol、literal、fileの存在だけ
- relationの片側だけ
- validationが後で判定できるという予定
- 他effectの成功
- TaskSpecにないimplementation methodの推測

新しいread、別target、validation、rework、executor制御は追加しない。現在観測済みのcontentをどう三値bindするかだけを変更する。

## 汎用性

この軸はF02やPython固有ではない。

| required effectの形 | satisfied witness |
| --- | --- |
| 値の伝播 | producer valueがrequired consumerへ渡る接続 |
| 条件付き表示 | required conditionからrequired output branchまでの接続 |
| failure cleanup | failure branchからcleanupとterminal resultまでの接続 |
| dependency pair | 両memberとTaskSpec明示の隣接・provenance関係 |
| command / routing | input routeからrequired entrypointまでのmapping |
| test artifact復元 | required assertionと対象behavior呼出しの同一test内接続 |

Standard14外でも、未使用helper、dead branch、未接続config、片側だけ更新されたschema、宣言だけ存在するdependencyなどに同じ判定を適用できる。言語、path、case ID、特定symbolには依存しない。

## 次の評価gate

Candidateを作る場合はCandidate139を直接親とし、初回はF02 / F04 / F07各N=5、M=24とする。

- F02: 未接続helperを`satisfied`へbindしない。engineだけの部分変更0 / 5。
- F04: 実際に接続済みの`colSpan`は`satisfied`として保持し、`hasAuditKey`だけを変更する。
- F07: direct constraintとcompiled provenanceのpair relationを両方維持する。
- score `3`以下が一件でも出たら停止する。

## 結論表

| 論点 | 判定 |
| --- | --- |
| TaskSpec target集合の欠落 | 主因ではない |
| helperの存在をbehavior成立へ読み替え | 三件共通の主因 |
| 出力量増加 | 一件で明示、増悪要因の可能性あり、共通主因ではない |
| C128 closureとの重複 | effect集合保持は既存、satisfied witness完全性は未解決 |
| 次の一軸 | `effect_satisfaction_witness` |
| 新しいCandidate | まだ作成しない |
