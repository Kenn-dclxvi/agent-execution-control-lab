# Candidate131 Point 4 dependency監査

## 結論

Point 4のdependencyについて、新しいCandidateは作成しない。保存済みtraceでは、依存関係を独立したprompt predicateへ固定しなくても、TaskSpecのrequired effect集合とCandidate128の`required_effects_closed`で成果欠落を閉じられている。

Candidate131 F04 iteration 1の下流3式変更もrequired outcomeとvalidationを満たした。共通上流一か所を変更した他4件より品質が低い事実はなく、tokenとelapsedの実測にも不利益を確認できない。保守性の推測だけで上流一か所の変更を全taskへ強制しない。

## 対象と用語

dependencyは、あるeffectの成立が別の値、effect、artifactに依存する関係を指す。変更ファイル数、hunk数、同じ名前の出現数とは区別する。

監査対象は次の保存済み互換traceである。

- Candidate127 F02 N=29のscore `2` 2件
- Candidate128 F02 / F04 / F07各N=5
- Candidate131 F04 N=5

## F02: 明示dependency graphなしで両effectを閉じる

F02 TaskSpecは次を別criterionとして列挙する。

- engineがprimary refreshとselective retryで日本側target dateとUS market trading dateを渡す
- updaterがasset class別に正しいdateをend dateへ使う

二つのeffect間のdependency graphは別artifactとして要求していない。Candidate127の低Score 2件はengine effectだけを適用し、updater effectを未充足のままvalidationへ進んだ。

Candidate128はdependency graphを追加せず、同じrequired effect集合をartifact変更後に再判定した。F02 5 / 5件で両source effectが閉じ、engineだけの部分成果は0 / 5だった。したがって、この保存失敗は「dependencyを明示しなかったこと」より「未充足effectを完了集合から落としたこと」で説明でき、Point 3の既存closureが直接対応している。

## F07: pairはTaskSpec自体が固定

F07 TaskSpecは`requirements.in`のdirect constraintと`requirements.txt`のcompiled pin provenanceをpaired invariantとして明示し、片方だけの修正で完了扱いにしないと定める。

Candidate128は5 / 5件で2ファイルのrequired pairを閉じ、partial pairは0 / 5だった。ここへ別のglobal dependency predicateを重ねると、TaskSpecで固定済みの関係を再分類する判断が増える。

## F04: 上流一か所と下流三か所は両方有効

Candidate131は5 / 5件がscore `4`だった。

- 4件: 共通の`hasAuditKey`定義を一行変更
- 1件: header、row、`colSpan`へ同じdata predicateを直接適用

下流3式を変更したiteration 1はtoken `96,001`、elapsed `84.026`秒だった。他4件のtokenは`122,658`から`153,534`、elapsedは`85.633`から`92.058`秒であり、iteration 1は5件中token最小、elapsed最小だった。N=5の記述値であり方式間の優劣を一般化しないが、少なくとも下流変更へbindできる実害は確認できない。

TaskSpecはdata-dependentな表示挙動と列数一致を要求するが、共通変数の再利用をrequired outcomeにしていない。上流一か所への変更を強制すると、成果条件ではなくimplementation methodをglobal promptへ追加することになる。

## 既存制御との重複

- `SPEC`: required outcomeとcriterion集合を固定する。
- `EVIDENCE_GATE`: criterionを判定できるcontentを取得する。Candidate131はPoint 2のanchor経路を追加した。
- `RECOVERY.required_effects_closed`: artifact変更後も全required effectの状態を保持する。
- TaskSpec: F07のようにdependency自体がrequired outcomeなら、そのpairを直接固定する。

この組合せで、保存trace上のdependency由来に見える部分成果を閉じている。新しいdependency graph、上流／下流分類、共有symbol優先、hunk groupingは追加しない。

## 再開条件

次のいずれかを同じ互換条件の保存traceで観測した場合だけ、Point 4を再開する。

1. 全required effectがclosedと判定されたのに、effect間の依存不整合でquality scoreが`3`以下になる。
2. TaskSpecでdependencyがrequired outcomeなのに、片側だけを適用してvalidationまたは完了報告へ進む。
3. 複数の有効implementationの一方に、事前固定したcostまたは保守性gateの失敗が再現する。

現在は該当しない。次はPoint 5のchange constructionを、C125のstale preimage失敗、C126 / C129の抑止とfalse stop、C131のevidence coverage成立後の状態に分けて監査する。
