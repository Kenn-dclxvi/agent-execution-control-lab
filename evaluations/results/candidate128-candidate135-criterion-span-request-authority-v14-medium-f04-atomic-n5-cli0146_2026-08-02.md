# Candidate128 / Candidate135 F04 targeted result

## 結論

Candidate135のF04 N=5はscore `4 / 2 = 4 / 1`だった。score `2`が1件出たためCandidate135を停止し、追加24件、F02、F07、Standard14、Candidate136へ進めない。

criterion外のTaskSpec fieldから検索語を混ぜる現象は0 / 5件だった。この点では、Candidate134の2 / 5件からrequest source boundaryを分離できた。一方、criterion由来の全3 lexemeをcontinuation resultの先頭へ置くmechanismは3 / 5件に留まった。

低Score 1件は必要contentを全targetから取得済みだった。それでも変更hunk（patchで置き換える局所的なまとまり）の既存文字列を正しく構成できず、初回変更と許可されたreworkがともに原子的に失敗した。変更が0件のためNode validationへ進まずscore `2`となった。これはrequest authorityやreference definition不足ではなく、Point 5のchange constructionが独立して残ることを示す。

## 固定条件

- candidate: `the-caption-3ce91a4-criterion-span-request-authority-r1`
- parent: `the-caption-3ce91a4-required-effect-closure-r1`
- bundle SHA-256: `191b5fab2f42226f5b2199bce10300eff366d0260c35265ea42379a4f7c1fe87`
- case: `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY/r2`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Codex CLI / Python: `0.146.0` / `3.14.5`
- N / M: `5` / `24`
- pool: `f5f0d4aa8fb0b611b94908d54f5491483ba79a5f47757c43c6818e61ebd74cb4`
- compatibility key: `1a3b75ac2311cda9630a15db6ee0ab8c3d8e51bb46d4c63c44954fc5a958c24a`
- selection: `37a1be3eb4714d52bbfc246a88b1fe7a`
- analysis: `c2b3cf5219de474081f49314a5ef3fda`
- registered result: `8742d40fe3e94ab6bffc78afb108ed62`
- excluded attempt: 0

比較前に保存済みF04 reference result `cea34faab78149119808da7c59628955`を一意にbindした。prompt以外のEvaluation set、case、fixture、TaskSpec、rating、model、reasoning、Agent/runtime/CLI、permission、executor挙動、token accountingを機械照合し、preflightが5 slotを承認した後だけ発行した。

## 結果

| iteration | run | score | criterion-span経路 | artifact変更 | validation |
| ---: | --- | ---: | --- | --- | --- |
| 1 | `4e125e81d0f446099fe8685ac5101cc7` | 4 | 全3 lexemeを先頭取得後、全量 | `hasAuditKey`一行 | 3 / 3成功 |
| 2 | `18c199966ac84cf79d2fbaa316120557` | 2 | 2 / 3 lexeme取得後、全量 | hunk不一致で変更なし | 0 / 3、変更失敗で停止 |
| 3 | `58bda13af0264d76b602c7a3f833c76f` | 4 | continuation先頭で全3 lexeme、その後全量 | `hasAuditKey`一行 | 3 / 3成功 |
| 4 | `e26c0ed063d247f896de44abd9074380` | 4 | lexeme検索を使わず全量 | `hasAuditKey`一行 | 3 / 3成功 |
| 5 | `4db7793fc96e4f66a3b40edd42a276c1` | 4 | 全3 lexemeを先頭取得後、全量 | `hasAuditKey`一行 | 3 / 3成功 |

5件中央値はquality `100.000`、token `158,790`、elapsed `87.664`秒だった。停止条件へ到達したため、効率改善や採用の判断には使わない。

## source boundaryの実測

F04のcriterion由来lexemeは`audit_match_key`、`Audit Key`、`colSpan`である。全5件で、constraints、allowed path、validation、temporary output、recoveryなど他field由来の語を検索集合へ混ぜなかった。Candidate134で2 / 5件あったcriterion外lexeme混入は、このN=5では0件だった。

ただし、全3 lexemeをcontinuation resultの先頭へ置いたのは3 / 5件だった。iteration 2は`colSpan`を検索集合へ入れなかった。iteration 4はlexeme検索自体を使わず全量を読んだ。したがって、入力authorityの限定は観測上機能したが、lexeme-first手順を安定して強制したとはいえない。

全量取得は5 / 5件だった。Candidate135では全量fallbackを診断値として許可しているため、それ自体をmechanism失敗には数えない。別target、repository-wide search、二回目のcontinuationは0 / 5件だった。

## Score 2の切り分け

iteration 2は初回readで`const hasAuditKey = true;`を含む1〜260行を取得した。continuationでは`audit_match_key`と`Audit Key`の一致周辺に続き、261行目以降も取得した。つまり、変更に必要な上流定義、header、row cell、空表示cellはmodel-visibleだった。

agentは`hasAuditKey`をdata依存へ変更し、空表示の`colSpan`を同じ条件へ結び付ける方針を確定した。しかし、空表示cellを含む変更hunkの既存文字列が実ファイルと一致せず、patch全体が適用されなかった。許可された`machine_rework_max=1`でも同じ未充足effectへ小さいhunkを試したが、再び適用されなかった。fail-stopに従い追加read、別手段、validationを行わず終了した。

したがって、C134のScore 3で問題だった「上流定義が見えていない」はこのrunでは起きていない。必要contentが見えていても、そのcontentから正しい変更hunkを組み立てる処理は別の失敗点である。request source boundaryとchange constructionは両立可能な別制御として扱う必要がある。

## 汎用性の解釈

今回確認できたのはF04固有語の成功ではなく、構造上の二点である。

1. `task_kind_goal_and_done_condition`内のcriterion spanだけを検索語authorityにすると、他field由来語の混入を抑えられる可能性がある。
2. 検索語authorityを正しく限定しても、取得contentから変更hunkを構成する完全性は保証されない。

ただし実測caseはTypeScript / JSXの単一target implementation 1件だけである。Python、shell、declarative config、複数target、review、proseへの一般化は未検証であり、Candidate135の停止後に推測でpass扱いしない。

## 状態

`targeted_f04_n5_evaluated / quality_gate_failed / mechanism_gate_failed / score_2_1_of_5 / criterion_external_lexeme_0_of_5 / complete_criterion_lexeme_first_3_of_5 / full_content_5_of_5 / change_hunk_failure_1_of_5 / result_registered / stopped`

## 結論表

| gate | 期待 | 実測 | 判定 |
| --- | ---: | ---: | --- |
| valid / rateable | 5 / 5 | 5 / 5 | pass |
| score `4` | 5 / 5 | 4 / 5 | fail / stop |
| score `3`以下 | 0 / 5 | 1 / 5 | fail / stop |
| criterion外lexeme混入 | 0 / 5 | 0 / 5 | pass |
| 全criterion lexemeをcontinuation先頭へ配置 | 5 / 5 | 3 / 5 | fail |
| criterion direct content | 5 / 5 | 5 / 5 | pass |
| 全target content | 診断値 | 5 / 5 | diagnostic |
| 二回目continuation / 別target / repository-wide | 0 / 5 | 0 / 5 | pass |
| 必要変更と3 validation完備 | 5 / 5 | 4 / 5 | fail |
