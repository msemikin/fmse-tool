class ParsingError(Exception):
    pass


class UnexpectedEndOfInputError(ParsingError):
    def __init__(self):
        super(ParsingError, self).__init__("Unexpected end of input")


class InputSyntaxError(ParsingError):
    def __init__(self, description):
        super(ParsingError, self).__init__("Syntax error in input: " + str(description))
