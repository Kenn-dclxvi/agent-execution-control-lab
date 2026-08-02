# Candidate128 required-effect closure設計

## 結論

Candidate128はCandidate125を直接親とし、root `AGENTS.md`の`RECOVERY`だけを置換する。Candidate127は親として継承せず、保存済みの失敗・成功traceを設計証拠としてだけ使う。変更単位やファイル数ではなく、TaskSpecが要求した効果の充足状態を保持する`required_effects_closed`を一つのpredicateとする。

artifact変更の成功・失敗後に、未充足のrequired effectを失敗したhunkと一緒に消さない。全required effectが適用済み、または開始状態から充足済みと既存evidenceで証明できる場合だけvalidationへ進む。

## Identityと作成前gate

- candidate number: Candidate128
- prompt identity: `the-caption-3ce91a4-required-effect-closure-r1`
- direct parent: `the-caption-3ce91a4-criterion-complete-single-target-continuation-r1`
- changed target: root `AGENTS.md`
- changed rule: `RECOVERY`
- changed axis: required effect closure after artifact change result
- evaluation status: `not_evaluated`
- adoption: `not_decided`
- release: `not_created`
- runtime projection: `not_projected`

## 狭い条件を避けるためのtrace照合

### F02の低Score 2件

Candidate127のF02 N=29では、次の2件がscore `2`だった。

- `352352e56b7b4bdaa0565cf048c2e445`
- `e88c0aad89aa4167bbc97fb49505de39`

両runとも`src/app/v4_engine.py`だけを変更し、`src/domain/collection_history_updater.py`のrequired effectを未充足のままvalidationへ進んだ。focused testは`8 failed, 16 passed`だった。

ここで残った要求は「2ファイルを変更すること」ではない。engineが日付をupdaterへ渡す効果と、updaterがasset class別の日付をfetchへ渡す効果のうち、後者が未充足だったことが問題である。

### F02の成功経路

Candidate95の代表成功trace `19fcada46dc642708a416cc744a8d121`は、両sourceを一つのartifact変更resultで適用し、focused gate `24 passed`、full gate `326 passed, 3 skipped`を得た。Candidate127初段F02 N=5も5 / 5で両source変更を保持した。

Candidate128は一括変更そのものを必須methodにしない。分割・一括のどちらでも、両required effectが閉じることだけを要求する。

### F04の成功経路

Candidate127のF04 N=5は5 / 5がscore `4`だった。`hasAuditKey`は未充足だったため変更し、`colSpan`は開始状態ですでに要求を満たしていたため、失敗した不要hunkを捨てても全required effectが閉じた。

したがって「失敗した変更単位を常に残す」という制御にはしない。開始前evidenceで充足済みと証明できるeffectに対応する変更単位は失効できる。

### F07の成功経路

Candidate127のF07 N=5は5 / 5で`requirements.in`と`requirements.txt`を変更し、score `4`だった。代表trace `40fa1d615a684279a2a141c15532c2b7`は2ファイルのrequired effectを一つのartifact変更resultで閉じた。

Candidate128はファイル数や特定caseをpredicateへ含めない。複数artifactへ分散したrequired effectも同じ条件で扱う。

## 置換する一つのpredicate

`required_effects_closed := TaskSpecの各required effectが、artifact変更resultで適用済み、または初回artifact変更前のadmission済みrepository evidenceで開始状態から充足済みとbind可能`

各artifact変更result後に、TaskSpecから固定した同じrequired effect集合へ状態をbindする。

- true: 既存`VALIDATION_PLAN`へ進む。
- falseかつmachine rework残数あり: 一回を消費し、充足済みeffectを保持して、failure前にcriterion、target、current contentへbind済みの未充足effectだけを発行する。
- falseかつ未充足effectのcurrent contentが未bind、またはrework残数なし: 既存停止条件を維持する。

失敗した変更単位は、未充足effectが依存しない場合だけ失効できる。hunk不一致、invocation failure、別effectからの独立性だけを理由に未充足effectを失効しない。

## 消す判断点と増える判断点

消す判断点は、artifact変更失敗後に「独立した変更単位だから残す」「不一致単位だから捨てる」と変更単位そのものを基準にTaskSpecの要求を縮める判断である。

増える判断点は`required_effects_closed`のtrue / falseだけである。入力はTaskSpec、初回変更前に受領済みのadmission済みrepository evidence、実際のartifact変更resultに限定する。

## 最短正常経路の保持

初回artifact変更で全required effectが閉じた場合は、そのまま既存`VALIDATION_PLAN`へ進む。追加read、再監査、reworkは発生しない。

開始状態ですでに満たされたeffectは、初回変更前の既存evidenceだけで充足済みへbindする。変更不要なeffectを再度変更しない。

## 非目標

- ファイル数、case ID、特定path、特定hunkをpromptへ埋め込むこと
- 全artifact変更を一つのinvocationへ強制すること
- patch tool、atomic apply、executor、Codex CLI、adapter、runtime hookの変更
- machine rework上限を増やすこと
- failure後に追加evidenceを取得すること
- 未観測current contentを推測で補うこと
- Candidate128の採用、release、本体投影

## Targeted evaluation gate

Candidate128だけを先に実行する。model、reasoning、CLI、runtime、permission、rating、fixture、TaskSpec、token accounting、executor条件はCandidate125 compatible条件へ固定し、prompt identityだけを変更する。profileの`max_workers`は`24`へ固定する。

ユーザー指定どおり、いきなりN=20へ進めず、次の順で各N=5を実施する。

1. F02 N=5
2. F04 N=5
3. F07 dependency N=5
4. Standard14 N=5

各段階でscore `3`以下が一件でも出た時点で停止する。

追加mechanism gateは次のとおりとする。

- F02: required source effectを2つとも5 / 5で満たす。
- F02: 未充足updater effectをhunk失敗または独立性だけで失効しない。
- F04: `hasAuditKey`を5 / 5で満たし、開始状態で充足済みの`colSpan`を変更しない。
- F07: dependency pairのrequired effectを2つとも5 / 5で満たす。
- 全case: failure後の追加read 0件、machine rework上限超過0件。

初段N=5は一般的安定性の証明ではない。C95とC127はいずれもN=5通過後の追加反復で低頻度failureを観測しているため、N=5通過後も採用判断へ進めない。
