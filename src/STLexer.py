# Lexer (Tokenizer) for Symbol Table
#
# Kirill Borisov, 108144

from sly import Lexer

class STLexer(Lexer):
    tokens = {
        IF_KW, FOR_KW, CONST_STR, CONST_NUMBER, PLUS_OP, MINUS_OP, MULTIPLY_OP,
        DIVIDE_OP, LP, LCB, RP, RCB, EQUAL_OP, MORE_OP, LESS_OP,ASSIGNMENT_OP, SEMICOLON,
        IDENTIFIER, VOID_KW, INT_KW, FLOAT_KW, COMMA,
    }

    ignore = ' \t'

    IF_KW = r'if'
    FOR_KW = r'for'
    CONST_STR = r'".*?"|\'.*?\''
    CONST_NUMBER = r'\d+'

    PLUS_OP = r'\+'
    MINUS_OP = r'\-'
    MULTIPLY_OP = r'\*'
    DIVIDE_OP = r'\/'
    LP = r'\('
    LCB = r'\{'
    RP = r'\)'
    RCB = r'\}'

    VOID_KW = r'void'
    FLOAT_KW = r'float'
    INT_KW = r'int'

    EQUAL_OP = r'=='
    MORE_OP = r'>'
    LESS_OP = r'<'
    ASSIGNMENT_OP = r'='
    COMMA = r','
    SEMICOLON = r';'
    IDENTIFIER = r'[a-zA-Z_]\w*'

    variable_tokens = [
        'IDENTIFIER',
        'CONST_STR',
        'CONST_NUMBER',
    ]

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)