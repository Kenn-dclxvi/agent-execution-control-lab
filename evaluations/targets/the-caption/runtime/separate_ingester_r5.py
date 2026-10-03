"""元のメソッド・テストを保持して実読入口を分離する。"""
import ast

def separate(source, tests):
    tree = ast.parse(source)
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef))
    methods = [n for n in cls.body if isinstance(n, ast.FunctionDef)]
    cut = next(n for n in methods if n.name == '_load_external_assets').lineno - 1
    lines = source.splitlines(keepends=True)
    prefix = ''.join(lines[:cut])
    tail = ''.join(lines[cut:])
    assert 'super(' not in source and '__REV' not in tail
    header = ''.join(lines[:cls.lineno - 1])
    # 既存のメソッドとコメントは改変しない。
    assets = header + 'class _UniversalIngesterAssets:\n' + tail
    main = prefix.replace('class UniversalIngester:', 'from src.domain._universal_ingester_assets import _UniversalIngesterAssets\n\nclass UniversalIngester(_UniversalIngesterAssets):', 1)
    extracted = {}
    for text in [main, assets]:
        c = next(n for n in ast.parse(text).body if isinstance(n, ast.ClassDef))
        for n in c.body:
            if isinstance(n, ast.FunctionDef):
                assert n.name not in extracted
                extracted[n.name] = ast.dump(n, include_attributes=False)
    assert extracted == {n.name: ast.dump(n, include_attributes=False) for n in methods}
    names = [n.name for n in ast.parse(tests).body if isinstance(n, ast.FunctionDef) and n.name.startswith('test_')]
    wrapper = 'from _universal_ingester_cases import (\n' + ''.join('    ' + n + ',\n' for n in names) + ')\n'
    return main, assets, wrapper, tests, names
