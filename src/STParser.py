from sly import Parser
from src.STLexer import STLexer
from src.STLogger import STLogger

class STParser(Parser):
    tokens = STLexer.tokens
    symbol_table = [[]]

    def __init__ (self, log_path):
        self.logger = STLogger(log_path)

    @_('{ declarations statements functions }')
    def program(self, p):
        self.logger.save_scope(self.symbol_table.pop())
        self.logger.make_log()

    @_('{ func_decl open_scope internal_decl body close_scope }')
    def functions(self, p):
        return p.body
    @_('')
    def open_scope(self, p):
        self.symbol_table.append([])
    @_('')
    def close_scope(self, p):
        self.logger.save_scope(self.symbol_table.pop())

    @_('LCB { declarations statements } RCB')
    def body(self, p):
        pass

    @_('{ declaration SEMICOLON }')
    def declarations(self, p):
        pass
    
    @_('LP { declaration } RP')
    def internal_decl(self, p):
        pass
    
    @_('vartype IDENTIFIER [ { COMMA IDENTIFIER } ]')
    def declaration(self, p):
        ids = self.get_args(p[1], p[2])
        for id in ids:
            self.insert( (id, p.lineno) )
    
    @_('VOID_KW IDENTIFIER')
    def func_decl(self, p):
        self.insert ( (p.IDENTIFIER, p.lineno) )

    @_('{ statement [ SEMICOLON ] }')
    def statements(self, p):
        pass
    
    @_('IF_KW LP IDENTIFIER rel_op IDENTIFIER RP open_scope body close_scope')
    def statement(self, p):
        self.lookup(p.IDENTIFIER0, p.lineno)
        self.lookup(p.IDENTIFIER1, p.lineno)
    
    @_('FOR_KW open_scope LP statement SEMICOLON statement SEMICOLON statement close_scope RP body',
       'FOR_KW open_scope LP declaration SEMICOLON statement SEMICOLON statement close_scope RP body')
    def statement(self, p):
        pass

    @_('IDENTIFIER ASSIGNMENT_OP CONST_NUMBER')
    def statement(self, p):
        self.lookup(p.IDENTIFIER, p.lineno)
    
    @_('IDENTIFIER ASSIGNMENT_OP IDENTIFIER')
    def statement(self, p):
        self.lookup(p.IDENTIFIER0, p.lineno)
        self.lookup(p.IDENTIFIER1, p.lineno)

    @_('IDENTIFIER ASSIGNMENT_OP CONST_NUMBER bin_op CONST_NUMBER')
    def statement(self, p):
        self.lookup(p.IDENTIFIER, p.lineno)

    @_('IDENTIFIER ASSIGNMENT_OP IDENTIFIER bin_op CONST_NUMBER',
       'IDENTIFIER ASSIGNMENT_OP CONST_NUMBER bin_op IDENTIFIER')
    def statement(self, p):
        self.lookup(p.IDENTIFIER0, p.lineno)
        self.lookup(p.IDENTIFIER1, p.lineno)

    @_('IDENTIFIER ASSIGNMENT_OP IDENTIFIER bin_op IDENTIFIER')
    def statement(self, p):
        self.lookup(p.IDENTIFIER0, p.lineno)
        self.lookup(p.IDENTIFIER1, p.lineno)
        self.lookup(p.IDENTIFIER2, p.lineno)
    
    @_('IDENTIFIER LP [ args ] RP')
    def statement(self, p):
        self.lookup(p.IDENTIFIER, p.lineno)

    @_('IDENTIFIER [ { COMMA IDENTIFIER } ]')
    def args(self, p):
        args = self.get_args(p[0], p[1])
        for arg in args:
            self.lookup(arg, p.lineno)
    
    @_('PLUS_OP', 'MINUS_OP', 'MULTIPLY_OP', 'DIVIDE_OP')
    def bin_op(self, p):
        pass

    @_('EQUAL_OP', 'MORE_OP', 'LESS_OP')
    def rel_op(self, p):
        pass

    @_('INT_KW', 'FLOAT_KW')
    def vartype(self, p):
        pass

    def get_args(self, mandatory, optional: list):
        args = [mandatory]
        for arg in optional:
            if (arg):
                for var in arg:
                    args.append(var[1])
        return args

    def insert(self, variable):
        last = len(self.symbol_table) - 1
        if self.is_in_current_scope(variable[0], last):
            self.logger.log_insertion_error(variable[0], variable[1])
        else:
            self.symbol_table[last].append(variable)

    def is_in_current_scope(self, variable, last_index):
        current_scope = self.symbol_table[last_index]
        for symbol in current_scope:
            if variable in symbol:
                    return True

    def lookup(self, variable, lineno):
        for scope in reversed(self.symbol_table):
            for symbol in scope:
                if variable in symbol:
                    self.logger.log_reference(variable, lineno, symbol[1])
                    return True
        self.logger.log_error(variable, lineno)
        return False