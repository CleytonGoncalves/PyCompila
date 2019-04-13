from typing import Sequence, Optional

from lexer import Token, TokenType


class SyntacticParser:
    code: Optional[str]  # Usado para gerar mensagens de erro mais úteis
    tokens: Sequence[Token]
    curr_token_pos: int
    curr_token: Optional[Token]
    valid: bool

    def __init__(self, tokens: Sequence[Token], code: str = None) -> None:
        self.code = code
        self.tokens = tokens
        self.curr_token_pos = 0
        self.curr_token = tokens[0]
        self.valid = True

    def parse(self) -> bool:
        self.z()
        return self.valid

    def next_token(self) -> None:
        self.curr_token_pos += 1
        if self.curr_token_pos >= len(self.tokens):
            self.curr_token = None
        else:
            self.curr_token = self.tokens[self.curr_token_pos]

    def raise_error(self, *expected_types) -> None:
        self.valid = False
        expected_str = ' | '.join(str(exp_type) for exp_type in expected_types)

        raise Exception(self.format_error(expected_str))

    def format_error(self, expected_str: str):
        error_msg = \
            f"\n\tExpected Token Type(s): {expected_str}" \
                f"\n\tFound: {self.curr_token.token_type}"

        if self.code is not None:
            line_num = self.curr_token.line
            code_split = self.code.splitlines()

            code_context = ""
            if len(code_split) >= 4:
                code_context += f"{'':>3}{code_split[line_num - 2]}\n"  # Linha anterior ao erro
            if len(code_split) >= 1:
                code_context += f">{'':>2}{code_split[line_num - 1]}\n"  # Linha do erro
            if len(code_split) > line_num:
                code_context += f"{'':>3}{code_split[line_num]}\n"  # Linha próxima ao erro

            error_msg += f"\n\tLine: {self.curr_token.line}, starting column: {self.curr_token.column}" \
                f"\n\n\tContext:\n\t{code_context}"

            return error_msg

    def is_type(self, expected_token_type: TokenType, error_on_fail: bool = False) -> bool:
        if self.curr_token is not None and self.curr_token.token_type == expected_token_type:
            self.next_token()
            return True

        if error_on_fail:
            self.raise_error(expected_token_type)
        return False

    def z(self) -> None:
        """
        Z ::= I S
        """
        self.i()
        self.s()

    def i(self) -> None:
        """
        I ::= 'var' D
        """
        if self.is_type(TokenType.KEYWORD_VAR, error_on_fail=True):
            self.d()

    def d(self) -> None:
        """
        D ::= L ':' K O
        """
        self.l()
        if self.is_type(TokenType.COLON, error_on_fail=True):
            self.k()
            self.o()

    def l(self) -> None:
        """
        L ::= 'id' X
        """
        if self.is_type(TokenType.IDENTIFIER, error_on_fail=True):
            self.x()

    def x(self) -> None:
        """
        X ::= (',' L)?
        """
        if self.is_type(TokenType.COMMA):
            self.l()

    def k(self) -> None:
        """
        K ::= 'integer'  |  'real'
        """
        if self.is_type(TokenType.KEYWORD_INTEGER) or self.is_type(TokenType.KEYWORD_REAL):
            pass
        else:
            self.raise_error(TokenType.KEYWORD_INTEGER, TokenType.KEYWORD_REAL)

    def o(self) -> None:
        """
        O ::= (';' D)?
        """
        if self.is_type(TokenType.SEMI_COLON):
            self.d()

    def s(self) -> None:
        """
        S ::= 'id' ':=' E | 'if' E 'then' S
        """
        if self.is_type(TokenType.IDENTIFIER):
            if self.is_type(TokenType.ASSIGNMENT, error_on_fail=True):
                self.e()
        elif self.is_type(TokenType.KEYWORD_IF):
            self.e()
            if self.is_type(TokenType.KEYWORD_THEN, error_on_fail=True):
                self.s()
        else:
            self.raise_error(TokenType.IDENTIFIER, TokenType.KEYWORD_IF)

    def e(self) -> None:
        """
        E ::= T R
        """
        self.t()
        self.r()

    def r(self) -> None:
        """
        R ::= ('+' T R)?
        """
        if self.is_type(TokenType.ADD_OPERATOR):
            self.t()
            self.r()

    def t(self) -> None:
        """
        T ::= 'id'
        """
        self.is_type(TokenType.IDENTIFIER, error_on_fail=True)


def parse(tokens: Sequence[Token], code: str = None):
    return SyntacticParser(tokens, code).parse()
