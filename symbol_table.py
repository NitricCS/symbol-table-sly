from src.STLexer import STLexer
from src.STParser import STParser

if __name__ == "__main__":
    data = open("./samples/example.cpp").read()
    lexer = STLexer()

    parser = STParser("./symbol_table.log")
    s = lexer.tokenize(data)
    # for tok in s:
    #     print (tok)
    parser.parse(s)