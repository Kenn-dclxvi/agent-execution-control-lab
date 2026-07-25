# click rating contracts

target instance `click`のquality rating contractを置く。**未作成である。**

rating contractは`boundary_rules`と`case_quality_rules`をcase ID単位で内包するためinstance固有であり、`the-caption`側のcontractを流用しない。作成時は`scripts/evaluation_loop.py`の`SUPPORTED_QUALITY_RATINGS`へ登録し、`target.json`の`current_rating_contract`へ設定する。
