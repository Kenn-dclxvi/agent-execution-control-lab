## 4. Units スナップショット仕様

### 4.1 ファイル仕様

1. 保存先:
   `data/current/collection_units_YYYYMMDD.json`
2. `schema_version`:
   `market_units_snapshot.v1`
3. `snapshot_type`:
   `FULL_SNAPSHOT`
4. `captured_at`:
   timezone 付き ISO 8601、JST で記録する。
   例: `2026-05-21T19:30:00+09:00`

### 4.2 必須トップレベル項目

1. `schema_version`
2. `snapshot_type`
3. `target_date`
4. `captured_at`
5. `source.ssot_a_path`
6. `source.ssot_a_sha256`
7. `items[]`

`source.ssot_a_path` は正本 SSOT A のパスを示す。値は原則 `data/collection/market_units.csv` とする。

### 4.3 必須 `items[]` 項目

1. `asset_key`
2. `name`
3. `asset_class`
4. `currency`
5. `units`
6. `source_symbol`
7. `audit_match_key`
8. `csv_url`

`units` は文字列で保存する。これは小数・桁数・CSV 上の表現を不用意に丸めないためである。

### 4.4 任意 `items[]` 項目

1. `enabled`

`enabled` は将来互換フィールドとする。CSV 生成時に付与する場合の既定値は `true` とする。v1 の ledger 計算では `enabled=false` を特別扱いせず、計算対象から除外しない。検証時も `enabled` の有無は必須条件にしない。

---


## 5. asset_key 生成仕様

`asset_key` は snapshot 内の安定識別子であり、重複判定と再計算時の資産対応に使う。

生成優先順:

1. `audit_match_key` が空でなければ `audit_match_key`
2. `source_symbol` が空でなければ `${asset_class}:${currency}:${source_symbol}`
3. それ以外は `${asset_class}:${currency}:${name}`

正規化ルール:

1. `asset_class` と `currency` は `trim` 後に uppercase する。
2. `name`、`source_symbol`、`audit_match_key` は `trim` のみ行う。
3. 空文字は未設定として扱う。
4. 重複判定は上記正規化後の `asset_key` で行う。

注意:

1. `name` を含む fallback key は、表示名変更で履歴が割れる可能性がある。
2. 安定性が必要な資産では `audit_match_key` を明示することを推奨する。
3. FX helper row、COMMODITIES、JP_STOCK、US_STOCK、MUTUAL_FUNDS は同一ルールで扱う。

---


## 6. Ledger 入力元記録仕様

### 6.1 `ssot_a_path` の意味

`ShadowLedger.ssot_a_path` は canonical SSOT A の正本パスを示す。

値は常に以下とする。

```text
data/collection/market_units.csv
```

`ssot_a_path` には、実際に採用した snapshot ファイルパスを入れない。

### 6.2 `units_source` の追加

実際に Units 入力として採用したソースは、`ShadowLedger` のトップレベルに新設する `units_source` へ記録する。

既存 ledger 読み込み互換のため、schema 上の `units_source` は Optional とする。ただし、新規生成する ledger では必須出力とする。

```json
{
  "ssot_a_path": "data/collection/market_units.csv",
  "units_source": {
    "type": "SNAPSHOT",
    "path": "data/current/collection_units_20260521.json",
    "snapshot_target_date": "2026-05-21"
  }
}
```

`units_source` フィールド:

1. `type`: `"SNAPSHOT"` または `"LIVE_CSV"`
2. `path`: 実際に読んだファイルパス
3. `snapshot_target_date`: snapshot 採用時のみ設定する

LIVE_CSV 採用時の例:

```json
{
  "ssot_a_path": "data/collection/market_units.csv",
  "units_source": {
    "type": "LIVE_CSV",
    "path": "data/collection/market_units.csv"
  }
}
```

---


## 7. Units 解決モード仕様

### 7.1 起動インターフェース

`UniversalIngester.build_shadow_ledger()` は `units_mode` を受け取る。

```python
build_shadow_ledger(target_date: Optional[str] = None, units_mode: str = "daily")
```

許容値:

1. `daily`
2. `strict`

`recompute`、`audit`、`backfill` 相当の処理は `strict` を指定する。CLI や専用スクリプトで別名を設ける場合も、domain 層では `strict` に正規化する。

### 7.2 daily mode

日次運用では可用性を優先する。

1. 対象日の snapshot が存在し、検証に通れば snapshot を採用する。
2. snapshot 欠損時は `market_units.csv` を採用する。
3. snapshot 不正時は `[Guard]` warning を出し、`market_units.csv` へフォールバックする。
4. フォールバックした場合も `units_source.type = "LIVE_CSV"` として記録する。

### 7.3 strict mode

再計算・監査・バックフィルでは `strict` を使い、再現性を優先する。

1. snapshot が存在し、検証に通れば snapshot を必ず採用する。
2. snapshot 不正時は blocking とし、live CSV へ黙って切り替えない。
3. snapshot 欠損時に live CSV を使うには、明示オプションを必要とする。
4. 明示オプションで live CSV を使った場合も、`units_source.type = "LIVE_CSV"` として記録する。

---


## 8. スナップショット検証ルール

有効判定条件:

1. `schema_version = "market_units_snapshot.v1"`
2. `snapshot_type = "FULL_SNAPSHOT"`
3. `target_date` が要求日付と一致する。
4. `items` が空でない。
5. 全 `items` の `units` が数値として解釈可能である。
6. 正規化後の `asset_key` が重複しない。
7. 必須項目が欠損していない。

検証失敗時の扱いはモードに従う。

---


## 14. 受け入れ条件

### 14.2 日次実行

1. snapshot 存在時は snapshot Units を採用する。
2. snapshot 欠損・不正時は warning を出し、live CSV で処理完走する。
3. ledger には `ssot_a_path` と `units_source` がそれぞれ正しい意味で記録される。

### 14.3 再計算・監査

1. `strict` 指定時、snapshot が存在する日付では snapshot を必ず採用する。
2. snapshot 不正時に live CSV へ黙って切り替わらない。
3. live CSV を使う場合は明示オプションが必要である。
4. 同一 `target_date`・同一 snapshot 入力で deterministic な Units 入力になる。

## 15. テスト要件

1. Unit テスト:
   - snapshot 採用パス
   - daily mode の snapshot 欠損 fallback
   - daily mode の snapshot 不正 fallback
   - strict mode の snapshot 不正 blocking
   - `asset_key` 生成・重複判定
   - `units_source` 記録
