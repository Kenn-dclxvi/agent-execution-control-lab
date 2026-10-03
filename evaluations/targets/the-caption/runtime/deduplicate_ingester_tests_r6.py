"""テストの準備処理を共通化し、展開後のAST一致を確認する。"""
import ast
import copy

PATHS = '''funds_csv = tmp_path / "funds.csv"
external_json = tmp_path / "external_assets.json"
history_dir = tmp_path / "history"
history_dir.mkdir()
'''
HELPERS = '''

def _case_paths(tmp_path):
    funds_csv = tmp_path / "funds.csv"
    external_json = tmp_path / "external_assets.json"
    history_dir = tmp_path / "history"
    history_dir.mkdir()
    return funds_csv, external_json, history_dir


def _utf8(path, content):
    path.write_text(content, encoding="utf-8")


def _new_ingester(funds_csv, external_json, history_dir, **kwargs):
    return UniversalIngester(funds_csv_path=str(funds_csv), external_assets_path=str(external_json), history_dir=str(history_dir), **kwargs)
'''

def deduplicate(source):
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))
    def span(node):
        # AST columns are UTF-8 byte offsets.
        start = offsets[node.lineno - 1] + len(lines[node.lineno - 1].encode()[:node.col_offset].decode())
        end = offsets[node.end_lineno - 1] + len(lines[node.end_lineno - 1].encode()[:node.end_col_offset].decode())
        return start, end
    def dump(node):
        return ast.dump(node, include_attributes=False)
    pattern = ast.parse(PATHS).body
    edits = []
    counts = {'path_blocks': 0, 'utf8_calls': 0, 'ingester_calls': 0}
    for fn in tree.body:
        if not isinstance(fn, ast.FunctionDef):
            continue
        for i in range(len(fn.body) - 3):
            nodes = fn.body[i:i+4]
            if [dump(n) for n in nodes] == [dump(n) for n in pattern]:
                a, _ = span(nodes[0]); _, b = span(nodes[-1])
                edits.append((a, b, 'funds_csv, external_json, history_dir = _case_paths(tmp_path)'))
                counts['path_blocks'] += 1
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Attribute) and node.func.attr == 'write_text' and len(node.args) == 1 and len(node.keywords) == 1 and node.keywords[0].arg == 'encoding' and isinstance(node.keywords[0].value, ast.Constant) and node.keywords[0].value.value == 'utf-8':
            a, b = span(node)
            edits.append((a, b, '_utf8(' + ast.unparse(node.func.value) + ', ' + ast.unparse(node.args[0]) + ')'))
            counts['utf8_calls'] += 1
        elif isinstance(node.func, ast.Name) and node.func.id == 'UniversalIngester' and not node.args and len(node.keywords) >= 3:
            expected = ast.parse('UniversalIngester(funds_csv_path=str(funds_csv), external_assets_path=str(external_json), history_dir=str(history_dir))', mode='eval').body
            if [dump(k) for k in node.keywords[:3]] == [dump(k) for k in expected.keywords] and all(k.arg is not None for k in node.keywords[3:]):
                a, b = span(node)
                extra = ''.join(', ' + k.arg + '=' + ast.unparse(k.value) for k in node.keywords[3:])
                edits.append((a, b, '_new_ingester(funds_csv, external_json, history_dir' + extra + ')'))
                counts['ingester_calls'] += 1
    edits.sort()
    assert all(edits[i][1] <= edits[i+1][0] for i in range(len(edits)-1))
    result = source
    for a, b, text in reversed(edits):
        result = result[:a] + text + result[b:]
    result += HELPERS
    class Expand(ast.NodeTransformer):
        def visit_Assign(self, node):
            if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and node.value.func.id == '_case_paths':
                assert dump(node.targets[0]) == dump(ast.parse('funds_csv, external_json, history_dir = 0').body[0].targets[0])
                assert len(node.value.args) == 1 and dump(node.value.args[0]) == dump(ast.Name(id='tmp_path', ctx=ast.Load()))
                return copy.deepcopy(pattern)
            return self.generic_visit(node)
        def visit_Call(self, node):
            node = self.generic_visit(node)
            if isinstance(node.func, ast.Name) and node.func.id == '_utf8':
                assert len(node.args) == 2 and not node.keywords
                return ast.Call(func=ast.Attribute(value=node.args[0], attr='write_text', ctx=ast.Load()), args=[node.args[1]], keywords=[ast.keyword(arg='encoding', value=ast.Constant(value='utf-8'))])
            if isinstance(node.func, ast.Name) and node.func.id == '_new_ingester':
                assert len(node.args) == 3
                names = ['funds_csv_path', 'external_assets_path', 'history_dir']
                keywords = [ast.keyword(arg=n, value=ast.Call(func=ast.Name(id='str', ctx=ast.Load()), args=[v], keywords=[])) for n,v in zip(names,node.args)]
                return ast.Call(func=ast.Name(id='UniversalIngester', ctx=ast.Load()), args=[], keywords=keywords+node.keywords)
            return node
    expanded = ast.parse(result)
    expanded.body = expanded.body[:-3]
    expanded = Expand().visit(expanded)
    assert dump(expanded) == dump(tree)
    return result, counts
