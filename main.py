from lexer.tokenizer import tokenize

code = """
var
    a, b, c: integer;
    d:real
if
    a+b
then a:=c
"""

for token in tokenize(code):
    print(token)
