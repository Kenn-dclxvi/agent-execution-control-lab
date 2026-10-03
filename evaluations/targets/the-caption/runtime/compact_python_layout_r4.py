"""判断情報を保持してPythonの空白と改行だけを短縮する。"""
import ast
import io
import tokenize

def compact(source):
    pairs = []
    depth = 0
    previous = None
    for token in tokenize.generate_tokens(io.StringIO(source).readline):
        kind, value = token.type, token.string
        if kind == tokenize.INDENT:
            depth += 1
            value = ' ' * depth
        elif kind == tokenize.DEDENT:
            depth -= 1
        elif kind == tokenize.NL and previous != tokenize.COMMENT:
            continue
        pairs.append((kind, value))
        previous = kind
    output = tokenize.untokenize(pairs)
    assert ast.dump(ast.parse(source), include_attributes=False) == ast.dump(ast.parse(output), include_attributes=False)
    def significant(text):
        excluded = {tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT}
        return [(t.type, t.string) for t in tokenize.generate_tokens(io.StringIO(text).readline) if t.type not in excluded]
    assert significant(source) == significant(output)
    return output
