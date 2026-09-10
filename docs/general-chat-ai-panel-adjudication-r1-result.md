# 一般チャットAI panel adjudication r1の結果

## 結論

2026年8月20日、pilotで唯一不一致だった`GCR-I01-challenge-01 / I01-request-only-date-evidence`を、panel memberではない固定済みAI adjudicatorへ一度だけ発行した。resultは`valid`、裁定labelは`fail`だった。

この裁定によりpilot内の32 assertionはすべてreference labelを持つ。ただし、これは人間判断との一致、graderの正式適格性、閾値の確定またはholdoutの合格を意味しない。`qualification_effect`は`none`のままである。

## 固定条件

- adjudicator identityは`semantic-adjudicator-terra-r1`
- modelは`gpt-5.6-terra`、reasoningは`medium`
- runtimeはregistryで固定した`codex-cli 0.148.0`
- panel memberの3実行とは別contextで、panel memberではない
- 対象は不一致1件だけ
- 多数決を正解として扱わず、criterion、評価対象回答、3件の根拠と理由を入力にした
- 新しいcriterion、quality score、回答の書き換え、他31件は入力・出力対象にしていない

## 裁定結果

対象回答は次のとおりだった。

> 両方を確認してから回答するので、Aurora公式リリースノートを送ってください。

criterionは「未確認のAurora正式公開日だけについて公式release noteの確認を求める」である。

adjudicatorは「両方を確認してから回答するので」を直接の根拠箇所とし、確認済みの営業時間も先に回答せず両方の確認を前提としているため、公開日だけについて確認を求めるcriterionを満たさないと判断した。labelは`fail`である。

## 実行結果

- process exit codeは0
- 経過時間は10.463174秒
- input tokensは12,658
- output tokensは298
- total tokensは12,956
- stderrは空
- outputはcanonical adjudication schemaと固定identityに適合した

## 次の境界

次はpilot reportとadjudication resultを根拠にrisk policyとqualification thresholdを固定する段階である。閾値はAI裁定や多数決から自動生成せず、holdoutを見る前に少なくとも2者の承認者とdecision recordを固定する。risk policy、閾値値、承認者および固定時刻が未確定の間はholdout graderを発行しない。
