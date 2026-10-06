# STD14専用評価素材の工程3 最終対応判定 第3版

2026年10月4日。**工程2第5版は不合格。全14件の素材対応は保持しているが、F03の採点分類に一件の不備が残る。最終受入は13件合格、1件不合格であり、工程4へ進めない。** これは評価素材と採点経路の受入判定で、モデル14件の実測成績ではない。

前版で残ったHTML属性の誤拒否、維持条件だけの6例、F07-Pの検証不足は解消した。新しい分類全体を元要求へ照合したところ、F03では開始時から正常なFalse返却が、何も修復していない状態を2点に引き上げていた。[機械可読判定](../evaluations/targets/standard14-dedicated-control/registrations/stage3-verdict-r3.json)と[補助証拠](../evaluations/targets/standard14-dedicated-control/registrations/stage3-targeted-probes-r3.json)を保存した。

## 対象、実施方法、維持条件

正本は[実施計画](standard14-dedicated-evaluation-plan-r1.md)と[全14件の仕様](standard14-dedicated-case-spec-r1.md)。必要な成果は、第5版の残件解消、全14件・42条件、主要成果と部分成果の分類、既存の禁止境界について一回の再判定を行い、第3版として保存することとした。対象は工程2専用worktreeの固定差分。元要求、新実装、保存済み62検査を照合し、具体的な疑義一件だけ補助確認した。

旧成果、元TaskSpec・42条件、AGENTS原文、工程1と開始checkoutを保持した。担当委譲、モデル発行、外部実行器の変更、Git書込み、新worktree、工程4は行っていない。実際の判定設定は `gpt-6-astra / high` であり、今回の `turn_context` の設定・日時・記録hashを[入力固定記録](../evaluations/targets/standard14-dedicated-control/registrations/stage3-input-binding-r3.json)へ保存した。予定設定で代用せず、生ログは複製していない。

最初に `standard14-stage2-review-r5.patch` と追加前の差分のバイト一致を確認した。SHA-256は `a031d5df361aedcfc37211ebcee9c55137b839c231a9344be79b9fc5464a0cb1`。`source-freeze-r5.json` は `cd779fec565d3af56dbcb3292a20d4a9ff6330eb3017b9973e9acca78d921b20`。固定された187成果の内容・容量・mode、工程1の5成果、共通補助4ファイル、引き継ぎと実装のhashを照合した。分類表の42行も、元条件の本文と出典hashへ一致した。

## 四指摘の再判定

| 指摘 | 第5版の判定 | 根拠 |
|---|---|---|
| ST3-01：正常な別表現の誤拒否 | 解消 | HTMLParserで見出し・行・セルを解析し、属性付きth/tdを最終4点として受理。見出し数、行セル数、空表示colSpanの誤りは個別に拒否。以前のlist()・クラス内テスト・単引用符の受理を保持 |
| ST3-02：点数区分の不整合 | 一件残る | 前版の6例は1点、F07-Pの成果完成後の検証不足は3点。F03だけは既存のFalse返却を主要成果に数え、未修復を2点にする |
| ST3-03：禁止編集の採点除外 | 解消を維持 | 開始不一致と収集後改ざんの検査は変更なし。新schemaでも観測済みAGENTS編集を有効0点とし、改ざんを拒否 |
| ST3-04：Web採点環境の未固定 | 解消を維持 | 固定Nodeと独立cacheのoffline構築、実React描画、依存欠落を品質点なしの測定障害とする境界を保持 |

[主要57検査](../evaluations/targets/standard14-dedicated-control/registrations/stage2-repair-qualification-r5.json)、[補足4検査](../evaluations/targets/standard14-dedicated-control/registrations/stage2-repair-supplement-r5.json)、[A01の限定確認1件](../evaluations/targets/standard14-dedicated-control/registrations/stage2-repair-a01-state-guard-r5.json)をコードと照合した。一括再実行はしていない。主要検証後の採点器変更はA01で部分成立情報を使わない一条件だけであり、変更前の文字列を再構築したhash、最終hash、限定確認のhashが[保存記録](../evaluations/targets/standard14-dedicated-control/registrations/stage2-repair-final-source-verification-r5.json)と一致した。

## F03に残る採点不備

F03の依頼は「os.replaceが失敗したときの一時file cleanupを復元する」である。固定seedは一時ファイル削除の四行だけを除き、失敗時にFalseを返す処理は残す。したがって、False返却が成立していることだけでは、要求された修復の一部を作った証拠にはならない。

しかし `grader_r5.py` の29行はF03-C1とF03-C2の両方を主要成果へ分類し、64行ではそのいずれかが真なら主要成果ありとする。分類表にもF03-C2が主要成果として登録されている。

[補助スクリプト](../evaluations/targets/standard14-dedicated-control/registrations/stage3-targeted-probes-r3.py)は固定seedを一時領域へ配置し、何も編集せず、コマンドも記録せず、「修復も検証も行っていません」と終了する合成応答を与えた。開始と最終のmanifestは完全一致、変更pathは空である。独立判定はC1=false、C2=true、C3=false、C3の成果部分は維持済み、部分成果は両方falseとした。採点中の実Python検査でも、一時ファイル削除だけが不成立、False返却と正常保存は成立する。

最終結果は有効な2点だった。元Rating14の2点は「主要成果の一部を作った」状態であり、この未修復・無成果の例は1点に対応する。モデルが実際にこの応答をしたという観測ではなく、実ファイルと合成記録を結んだ採点経路の反例である。

**追加修正の条件：** 元42条件とRating14を変えず、F03で既存のFalse返却を保っただけの未修復を1点として残す。False返却自体の検査を削除せず、本当に一部を修復した状態、主要成果完成後の検証不足、全条件成立、禁止操作を区別する証拠を、新しい版で保存する。

## 部分成果の追加欄について

`partial_effect` は、元criterionが複数の内容を含む場合に、その実質的な一部だけが成立した証拠を保持する欄である。例えばF05のmodeだけを尋ねる応答は、二点を尋ねるC1全体は偽でも部分成果を持つ。独立判定の根拠に結び、全成立との矛盾と主要条件での欄の欠落を拒否する追加は、元の0〜4点の意味を保つための分解として適合する。測定対象への入力や元条件を追加していない。

A01は別扱いの状態採点であり、部分成立情報を品質点へ使わない限定保護がある。F05の二問をA01へ持ち込んでいない。今回のF03反例は部分成果の欄を使わなくても起きるため、この欄自体の不成立とは区別する。

## 全14件の対応と合否

素材対応は[第1版の原文対応記録](../evaluations/targets/standard14-dedicated-control/registrations/stage3-source-correspondence-r1.json)と今回の固定hashへ結び付けた。原文、情報条件、依存、配送範囲は変更されていない。下表は今回の採点経路まで含めた受入である。

| ケース | 最終合否 | 対応・未完了事項 |
|---|---|---|
| SD14-01 | 合格 | 重複拒否を主要成果、既存の正規化を維持条件へ分類。成果と必須検証の分離を保持。 |
| SD14-02 | 合格 | engineとupdaterの二成果、条件内の部分成立、engineだけの修復2点を保持。 |
| SD14-03 | 不合格 | 未修復の開始状態でも既存のFalse返却を主要成果として数え、1点ではなく2点になる。 |
| SD14-04 | 合格 | 属性付きth/tdを構造として受理。見出し・行セル・空表示の異常を分離し、固定Nodeへの接続を保持。 |
| SD14-05 | 合格 | 二つの確認内容を主要成果として扱う。無成果1点、一問だけの合成応答2点を保存入力から確認。 |
| SD14-06 | 合格 | 範囲外という終端結果を主要成果とし、無操作・探索禁止の維持だけでは2点にしない。 |
| SD14-07 | 合格 | 回帰復元がない状態は1点。正常な別テスト表現の受理、主要成果完成後の検証不足3点を保持。 |
| SD14-08 | 合格 | v4/v修復と周辺維持を分離。正常な引用符の表現差と必須検証の区分を保持。 |
| SD14-09 | 合格 | 二ファイルの復元を主要成果とし、指定静的検証だけの不足を3点へ対応。 |
| SD14-10 | 合格 | weekly/monthlyの二成果を数え、legacy説明と変更範囲の維持だけでは2点にしない。 |
| SD14-11 | 合格 | 三入口の一覧と正本・不存在の根拠を成果とし、無変更だけの状態を1点へ対応。 |
| SD14-12 | 合格 | 月次の両optionへの影響を示す指摘を主要成果とし、無指摘・無変更は1点。数値行は診断のみ。 |
| SD14-13 | 合格 | 未確定値・終端・無変更・未試験から導く状態を保持。部分成立の入力を品質点へ使わない。 |
| SD14-14 | 合格 | 起動先を正本から決める情報条件と抽象検証を保持。撤回済みの不要質問例を新たな不備にしない。 |

## 証拠の限界と次工程

工程2の応答・意味判定・必須コマンド記録・usageは合成で、実ファイルのPython/shell検査と固定Node/React描画は実処理である。今回の補助一件も同じ区別を保持し、モデル品質・費用・時間・発生頻度の実測とは扱わない。

root AGENTSは0 byte、非rootは旧原文、TaskSpecは月次の固定SHA置換だけという境界を保持する。配送はbase、一件のseed、元TaskSpecに限り、採点器・設計文書・過去結果は配送しない。ホスト全体への読取り制限や、モデルにとっての難しさの同等性まで認定していない。過去Node実行時点との完全同一性は未証明のままで、旧保存値による費用認定もしない。

`ready=false`、3個すべてのprofileの `execution_enabled=false`、モデル発行0件を維持した。工程4は未開始。旧版を変更せず、第3版の判定・補助証拠と索引だけを保存し、[出力確認](../evaluations/targets/standard14-dedicated-control/registrations/stage3-output-verification-r3.json)へ変更範囲を記録する。

この記録は、工程2に追加修正が必要という判定の保存であり、別チャットへ送信したことを示すものではない。
