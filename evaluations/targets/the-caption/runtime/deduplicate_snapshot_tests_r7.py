"""snapshotテストの共通準備を短縮し、展開後ASTを照合する。"""
import ast
import copy

SETUP = '''market_units_csv = tmp_path / "market_units.csv"
snapshot_dir = tmp_path / "current"
snapshot_dir.mkdir()
_write_market_units(market_units_csv)
'''
HELPERS = '''

def _snapshot_case(tmp_path):
    market_units_csv = tmp_path / "market_units.csv"
    snapshot_dir = tmp_path / "current"
    snapshot_dir.mkdir()
    _write_market_units(market_units_csv)
    return market_units_csv, snapshot_dir


def _case_ledger(tmp_path, market_units_csv, snapshot_dir, **kwargs):
    return _ingester(tmp_path, market_units_csv, snapshot_dir).build_shadow_ledger("2026-04-20", **kwargs)
'''

def deduplicate(source):
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))
    def span(n):
        a = offsets[n.lineno-1] + len(lines[n.lineno-1].encode()[:n.col_offset].decode())
        b = offsets[n.end_lineno-1] + len(lines[n.end_lineno-1].encode()[:n.end_col_offset].decode())
        return a,b
    def dump(n):
        return ast.dump(n, include_attributes=False)
    pattern = ast.parse(SETUP).body
    expected = ast.parse('_ingester(tmp_path, market_units_csv, snapshot_dir).build_shadow_ledger("2026-04-20")', mode='eval').body
    edits = []
    counts = {'setup_blocks':0,'ledger_calls':0}
    for fn in tree.body:
        if not isinstance(fn, ast.FunctionDef):
            continue
        for i in range(len(fn.body)-3):
            nodes = fn.body[i:i+4]
            if [dump(n) for n in nodes] == [dump(n) for n in pattern]:
                a,_ = span(nodes[0]);_,b = span(nodes[-1])
                edits.append((a,b,'market_units_csv, snapshot_dir = _snapshot_case(tmp_path)'))
                counts['setup_blocks'] += 1
    for n in ast.walk(tree):
        if isinstance(n,ast.Call) and dump(n.func)==dump(expected.func) and [dump(v) for v in n.args]==[dump(v) for v in expected.args] and all(k.arg is not None for k in n.keywords):
            a,b=span(n)
            extra=''.join(', '+k.arg+'='+ast.unparse(k.value) for k in n.keywords)
            edits.append((a,b,'_case_ledger(tmp_path, market_units_csv, snapshot_dir'+extra+')'))
            counts['ledger_calls']+=1
    edits.sort()
    assert all(edits[i][1]<=edits[i+1][0] for i in range(len(edits)-1))
    out=source
    for a,b,text in reversed(edits):
        out=out[:a]+text+out[b:]
    out+=HELPERS
    class Expand(ast.NodeTransformer):
        def visit_Assign(self,n):
            if isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='_snapshot_case':
                assert dump(n.targets[0])==dump(ast.parse('market_units_csv, snapshot_dir = 0').body[0].targets[0])
                assert len(n.value.args)==1 and isinstance(n.value.args[0],ast.Name) and n.value.args[0].id=='tmp_path'
                return copy.deepcopy(pattern)
            return self.generic_visit(n)
        def visit_Call(self,n):
            n=self.generic_visit(n)
            if isinstance(n.func,ast.Name) and n.func.id=='_case_ledger':
                assert [dump(v) for v in n.args]==[dump(v) for v in expected.func.value.args]
                result=copy.deepcopy(expected);result.keywords=n.keywords
                return result
            return n
    expanded=ast.parse(out);expanded.body=expanded.body[:-2];expanded=Expand().visit(expanded)
    assert dump(expanded)==dump(tree)
    return out,counts
