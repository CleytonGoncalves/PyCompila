from lexer import tokenize
from sy_parser import parse

code1 = """
var
    a, b, c: integer;
    d:real
if a+b then a:=c
"""

print("Lexical Analysis:")
tokens = None
try:
    tokens = tokenize(code1)
    print("\n".join(str(token) for token in tokens), end="\n\n")
except Exception as e:
    print("\tFailed.")
    print(e)

if tokens is None:
    exit(1)

print("Syntactic Analysis:")
try:
    parse(tokens, code1)
    print("\tSuccess!")
except Exception as e:
    print("\tFailed.")
    print(e)
