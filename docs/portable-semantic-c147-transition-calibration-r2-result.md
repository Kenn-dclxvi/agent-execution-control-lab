# C147 transition contract r2校正結果

> [!IMPORTANT]
> **状態**: `completed / valid_14_of_14 / score4_12_of_14 / contract_inconsistency_detected / heldout_r2_not_created / portable_prompt_unchanged`

## 結論

C147 referenceを既知14 Caseへ発行した結果、全14件が有効だったが、Score 4と機序成立は12 / 14だった。この値をC147の意味制御限界とは判定しない。外れた2件はr2 wrapperと固定oracleの間に、次の評価契約上の矛盾または不足があるためである。

- `PIC-H04`: oracleは`res-a`の明示effect scopeにある`op-a2`の失効を要求する。一方、r2 wrapperは`predicate_state=satisfied`を一律に失効対象外としており、同じ応答を禁止していた。
- `PIC-H13`: oracleは、bound済みrequired outcomeを満たす唯一のrecoveryがallowance未固定で拒否された状態を`unavailable`へ閉じる。一方、r2 wrapperはこの必要経路と単なるdenied decoyの区別を定義していなかった。

したがって、新しい未使用heldoutは作成せず、r2 resultを契約診断として保存する。r3ではCase、oracle、C147、response schemaを変更せず、この2つの意味境界だけを共通wrapperで明確化して再校正する。

## 計測結果

- valid: 14 / 14
- schema valid: 14 / 14
- Score 4: 12 / 14
- mechanism passed: 12 / 14
- Score 3: `PIC-H04`, `PIC-H13`
- token: min 15,356 / median 15,618 / max 16,011
- elapsed: min 9.800秒 / median 11.701秒 / max 18.281秒

## 停止境界

- r2を同じrevisionのまま修正または再発行しない。
- r2の12 / 14をportable Candidateとの比較値にしない。
- r3校正が14 / 14 Score 4になるまで、新しいheldoutとportable評価を発行しない。
- portable promptは変更しない。
