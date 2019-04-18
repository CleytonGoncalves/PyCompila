from lexer import tokenize
from sy_parser import parse

filename = "source.txt"

with open(filename) as f:
    source_code = f.read().rstrip()

print("Lexical Analysis:")
tokens = None
try:
    tokens = tokenize(source_code)
    print("\n".join(str(token) for token in tokens), end="\n\n")
except Exception as e:
    print("\tFailed.")
    print(e)

if tokens is None:
    exit(1)

print("Syntactic Analysis:")
try:
    parse(tokens, source_code)
    print("\tSuccess!")
except Exception as e:
    print("\tFailed.")
    print(e)
