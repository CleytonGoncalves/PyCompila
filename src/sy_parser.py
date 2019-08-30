from typing import Sequence, Optional, Dict, List

from lexer import Token, TokenType
from parser_exception import ParserException
from semantic_exception import SemanticException


class SymbolTable:
    table: Dict[str, TokenType]

    def __init__(self) -> None:
        self.table = {}

    def insert(self, token_val: str, token_type: TokenType) -> None:
        self.table[token_val] = token_type

    def lookup(self, token_val: str) -> Optional[TokenType]:
        return self.table.get(token_val)


class Parser:
    tokens: Sequence[Token]  # Lista de tokens recebido do lexer
    curr_token_pos: int  # Posição do token que o parser está trabalhando atualmente
    curr_token: Optional[Token]
    valid: bool  # Resultado do parser

    variable_list: List[str]  # Variáveis sendo declaras
    symbol_table: SymbolTable

    code: Optional[str]  # Código do programa para msgs de erro mais completas

    def __init__(self, tokens: Sequence[Token], code: str = None) -> None:
        self.code = code
        self.tokens = tokens
        self.curr_token_pos = 0
        self.curr_token = tokens[0]
        self.valid = True

        self.variable_list = []
        self.symbol_table = SymbolTable()

    def add_to_var_list(self, name: str) -> None:
        self.variable_list.append(name)

    def assert_vars_type_compatible(self) -> None:
        if len(self.variable_list) <= 1:
            return

        correct_type = self.symbol_table.lookup(self.variable_list[0])
        is_compatible = all(self.symbol_table.lookup(var) == correct_type for var in self.variable_list)
        if not is_compatible:
            self.raise_semantic_error(f"Incompatible variable types: {self.variable_list!r}")

        self.variable_list.clear()

    def add_vars_to_symbol_table(self, var_type: TokenType) -> None:
        for var in self.variable_list:
            if self.symbol_table.lookup(var) is not None:
                self.raise_semantic_error(f"Variable {var!r} already declared")

            self.symbol_table.insert(var, var_type)

        self.variable_list.clear()

    def parse(self) -> bool:
        self.programa()
        return self.valid

    def next_token(self) -> None:
        self.curr_token_pos += 1
        if self.curr_token_pos >= len(self.tokens):
            self.curr_token = None
        else:
            self.curr_token = self.tokens[self.curr_token_pos]

    def get_prev_token(self) -> Token:
        if self.curr_token_pos == 0:
            raise Exception("There's no previous token")

        return self.tokens[self.curr_token_pos - 1]

    def raise_parser_error(self, *expected_types) -> None:
        self.valid = False
        expected_str = ' | '.join(str(exp_type) for exp_type in expected_types)

        raise ParserException(self.format_error(expected_str))

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
            self.raise_parser_error(expected_token_type)
        return False

    def raise_semantic_error(self, msg):
        raise SemanticException(msg)

    ###################
    # Syntactic Rules #
    ###################

    def programa(self) -> None:
        """
        <programa> ::= program ident <corpo> .
        """
        self.is_type(TokenType.KEYWORD_PROGRAM, error_on_fail=True)
        self.is_type(TokenType.IDENTIFIER, error_on_fail=True)
        self.corpo()
        self.is_type(TokenType.SYMBOL_FULL_STOP, error_on_fail=True)

    def corpo(self) -> None:
        """
        <corpo> ::= <dc> begin <comandos> end
        """
        self.dc()
        self.is_type(TokenType.KEYWORD_BEGIN, error_on_fail=True)
        self.comandos()
        self.is_type(TokenType.KEYWORD_END, error_on_fail=True)

    def dc(self) -> None:
        """
        <dc> ::= <dc_v> <mais_dc> | <dc_p> <mais_dc> | λ
        """
        try:
            self.dc_v()
            self.mais_dc()
        except ParserException:
            try:
                self.dc_p()
                self.mais_dc()
            except ParserException:
                pass

    def mais_dc(self) -> None:
        """
        <mais_dc> ::= ; <dc> | λ
        """
        if self.is_type(TokenType.SYMBOL_SEMICOLON):
            self.dc()

    def dc_v(self) -> None:
        """
        <dc_v> ::= var <variaveis> : <tipo_var>
        """
        self.is_type(TokenType.KEYWORD_VAR, error_on_fail=True)
        self.variaveis()
        self.is_type(TokenType.SYMBOL_COLON, error_on_fail=True)
        self.tipo_var()

    def tipo_var(self) -> None:
        """
        <tipo_var> ::= real | integer
        Ação semântica: Adicionar tipo na tabela de símbolo.
        """
        if self.is_type(TokenType.KEYWORD_INTEGER):
            pass
        elif self.is_type(TokenType.KEYWORD_REAL):
            pass
        else:
            self.raise_parser_error(TokenType.KEYWORD_INTEGER, TokenType.KEYWORD_REAL)

    def variaveis(self) -> None:
        """
        variaveis> ::= ident <mais_var>
        Ação semântica: Adicionar identificadores na tabela de símbolo.
        """
        self.is_type(TokenType.IDENTIFIER, error_on_fail=True)
        self.mais_var()

    def mais_var(self) -> None:
        """
        <mais_var> ::= , <variaveis> | λ
        """
        if self.is_type(TokenType.SYMBOL_COMMA):
            self.variaveis()

    def dc_p(self) -> None:
        """
        <dc_p> ::= procedure ident <parametros> <corpo_p>
        Ação semântica: Adiciona procedimentos na tabela de símbolos.
        """
        self.is_type(TokenType.KEYWORD_PROCEDURE, error_on_fail=True)
        self.is_type(TokenType.IDENTIFIER, error_on_fail=True)
        self.parametros()
        self.corpo_p()

    def parametros(self) -> None:
        """
        <parametros> ::= ( <lista_par> ) | λ
        """
        if self.is_type(TokenType.SYMBOL_OPEN_PARENS):
            self.lista_par()
            self.is_type(TokenType.SYMBOL_CLOSE_PARENS, error_on_fail=True)

    def lista_par(self) -> None:
        """
        <lista_par> ::= <variaveis> : <tipo_var> <mais_par>
        """
        self.variaveis()
        self.is_type(TokenType.SYMBOL_COLON, error_on_fail=True)
        self.tipo_var()
        self.mais_par()

    def mais_par(self) -> None:
        """
        <mais_par> ::= ; <lista_par> | λ
        """
        if self.is_type(TokenType.SYMBOL_SEMICOLON):
            self.lista_par()

    def corpo_p(self) -> None:
        """
        <corpo_p> ::= <dc_loc> begin <comandos> end
        """
        self.dc_loc()
        self.is_type(TokenType.KEYWORD_BEGIN, error_on_fail=True)
        self.comandos()
        self.is_type(TokenType.KEYWORD_END, error_on_fail=True)

    def dc_loc(self) -> None:
        """
        <dc_loc> ::= <dc_v> <mais_dcloc> | λ
        """
        try:
            self.dc_v()
            self.mais_dcloc()
        except ParserException:
            pass

    def mais_dcloc(self) -> None:
        """
        <mais_dcloc> ::= ; <dc_loc> | λ
        """
        if self.is_type(TokenType.SYMBOL_SEMICOLON):
            self.dc_loc()

    def lista_arg(self) -> None:
        """
        <lista_arg> ::= ( <argumentos> ) | λ
        """
        if self.is_type(TokenType.SYMBOL_OPEN_PARENS):
            self.argumentos()
            self.is_type(TokenType.SYMBOL_CLOSE_PARENS, error_on_fail=True)

    def argumentos(self) -> None:
        """
        <argumentos> ::= ident <mais_ident>
        """
        self.is_type(TokenType.IDENTIFIER, error_on_fail=True)
        self.mais_ident()

    def mais_ident(self) -> None:
        """
        <mais_ident> ::= ; <argumentos> | λ
        """
        if self.is_type(TokenType.SYMBOL_SEMICOLON):
            self.argumentos()

    def p_falsa(self) -> None:
        """
        <pfalsa> ::= else <comandos> | λ
        """
        if self.is_type(TokenType.KEYWORD_ELSE):
            self.comandos()

    def comandos(self) -> None:
        """
        <comandos> ::= <comando> <mais_comandos>
        """
        self.comando()
        self.mais_comandos()

    def mais_comandos(self) -> None:
        """
        <mais_comandos> ::= ; <comandos> | λ
        """
        if self.is_type(TokenType.SYMBOL_SEMICOLON):
            self.comandos()

    def comando(self) -> None:
        """
        <comando> ::= read(<variaveis>)
            | write(<variaveis>)
            | while <condicao> do <comandos> $
            | if <condicao> then <comandos> <pfalsa> $
            | ident <restoIdent>
        """
        if self.is_type(TokenType.KEYWORD_READ):
            self.is_type(TokenType.SYMBOL_OPEN_PARENS, error_on_fail=True)
            self.variaveis()
            self.is_type(TokenType.SYMBOL_CLOSE_PARENS, error_on_fail=True)
        elif self.is_type(TokenType.KEYWORD_WRITE):
            self.is_type(TokenType.SYMBOL_OPEN_PARENS, error_on_fail=True)
            self.variaveis()
            self.is_type(TokenType.SYMBOL_CLOSE_PARENS, error_on_fail=True)
        elif self.is_type(TokenType.KEYWORD_WHILE):
            self.condicao()
            self.is_type(TokenType.KEYWORD_DO, error_on_fail=True)
            self.comandos()
            self.is_type(TokenType.SYMBOL_DOLLAR, error_on_fail=True)
        elif self.is_type(TokenType.KEYWORD_IF):
            self.condicao()
            self.is_type(TokenType.KEYWORD_THEN, error_on_fail=True)
            self.comandos()
            self.p_falsa()
            self.is_type(TokenType.SYMBOL_DOLLAR, error_on_fail=True)
        elif self.is_type(TokenType.IDENTIFIER, error_on_fail=True):
            self.resto_ident()

    def resto_ident(self) -> None:
        """
        <restoIdent> ::= := <expressao> | <lista_arg>
        Ação semântica: Verificar os tipos das variaveis em atribuições.
        """
        if self.is_type(TokenType.SYMBOL_ASSIGNMENT):
            self.expressao()
        else:
            self.lista_arg()

    def condicao(self) -> None:
        """
        <condicao> ::= <expressao> <relacao> <expressao>
        """
        self.expressao()
        self.relacao()
        self.expressao()

    def relacao(self) -> None:
        """
        <relacao>::= = | <> | >= | <= | > | <
        """
        if self.is_type(TokenType.SYMBOL_EQUALS) or \
                self.is_type(TokenType.SYMBOL_DIFFERENT) or \
                self.is_type(TokenType.SYMBOL_GREATER_EQUAL) or \
                self.is_type(TokenType.SYMBOL_LESS_EQUAL) or \
                self.is_type(TokenType.SYMBOL_GREATER) or \
                self.is_type(TokenType.SYMBOL_LESS, error_on_fail=True):
            pass

    def expressao(self) -> None:
        """
        <expressao> ::= <termo> <outros_termos>
        """
        self.termo()
        self.outros_termos()

    # \\\\\\\\\ Checar essa regra aqui ///////////
    def op_un(self) -> None:
        """
        <op_un> ::= + | - | λ
        """
        if self.is_type(TokenType.SYMBOL_ADD) or \
                self.is_type(TokenType.SYMBOL_SUBTRACT):
            pass

    def outros_termos(self) -> None:
        """
        <outros_termos> ::= <op_ad> <termo> <outros_termos> | λ
        """
        try:
            self.op_ad()
            self.termo()
            self.outros_termos()
        except ParserException:
            pass

    def op_ad(self) -> None:
        """
        <op_ad> ::= + | -
        """
        if self.is_type(TokenType.SYMBOL_ADD) or \
                self.is_type(TokenType.SYMBOL_SUBTRACT, error_on_fail=True):
            pass

    def termo(self) -> None:
        """
        <termo> ::= <op_un> <fator> <mais_fatores>
        """
        self.op_un()
        self.fator()
        self.mais_fatores()

    def mais_fatores(self) -> None:
        """
        <mais_fatores>::= <op_mul> <fator> <mais_fatores> | λ
        """
        try:
            self.op_mul()
            self.fator()
            self.mais_fatores()
        except ParserException:
            pass

    def op_mul(self) -> None:
        """
        <op_mul> ::= * | /
        """
        if self.is_type(TokenType.SYMBOL_MULTIPLICATION) or \
                self.is_type(TokenType.SYMBOL_DIVISION, error_on_fail=True):
            pass

    def fator(self) -> None:
        """
        <fator> ::= ident | numero_int | numero_real | (<expressao>)
        """
        if self.is_type(TokenType.IDENTIFIER) or \
                self.is_type(TokenType.LITERAL_INTEGER) or \
                self.is_type(TokenType.LITERAL_FLOAT):
            pass
        else:
            self.is_type(TokenType.SYMBOL_OPEN_PARENS, error_on_fail=True)
            self.expressao()
            self.is_type(TokenType.SYMBOL_CLOSE_PARENS, error_on_fail=True)


def parse(tokens: Sequence[Token], code: str = None):
    return Parser(tokens, code).parse()
