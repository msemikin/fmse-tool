import unittest
from fmse_tool.parsing.tokenizer import lexer


class TokenizerTest(unittest.TestCase):
    def test_works(self):
        formula = "E ['foo bar' U 'foo']"
        lexer.input(formula)
        while True:
            tok = lexer.token()
            if not tok:
                break  # No more input
            print(tok)


if __name__ == '__main__':
    unittest.main()
