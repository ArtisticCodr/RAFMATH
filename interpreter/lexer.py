# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
import math
FALSE, TRUE, COMMA, LOGOP, FUNCTION, VARIABLE, EQUAL, INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF = (
     'False', 'True','COMMA', 'LOGOP', 'FUNCTION', 'VARIABLE', 'EQUAL', 'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', '(', ')', 'EOF'
)

functions = dir(math)
signs = {'<', '>', '=', '!', '&', '|', '+', '-', '%', '^', '/', '*'}


class Token(object):

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS, '+')
            Token(MUL, '*')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Lexer(object):

    def __init__(self, text):
        # client string input, e.g. "4 + 2 * 3 - 6 / 2"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """Return a (multidigit) integer consumed from the input."""
        result = ''
        b = False
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.') :
            if(self.current_char == '.'):
                b = True
                
            result += self.current_char
            self.advance()
        
        if b == False:
            return int(result)
        else:
            return float(result)
    
    def string(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalpha() or self.current_char.isdigit()):
            result += self.current_char
            self.advance()
        return str(result)
    
    def logOp(self):
        result = ''
        while self.current_char is not None and (self.current_char in signs):
            self.current_char
            if(self.current_char in ('=', '<', '>')):
                result += self.current_char
                self.advance()
                if(self.current_char in ('=', '<', '>')):
                    continue
                else:
                    break
            result += self.current_char
            self.advance()
        return str(result)

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())
            
            if self.current_char.isalpha():
                string = self.string()
                if(string == 'True'):
                    return Token(TRUE, True)
                if(string == 'False'):
                    return Token(FALSE, False)
                if(string.lower() in functions):
                    return Token(FUNCTION, string.lower())
                else:
                    return Token(VARIABLE, string)
                
            if(self.current_char in signs):
                string = self.logOp()
                if(string == '='):
                    return Token(EQUAL, '=')
                
                if string == '+':
                    return Token(PLUS, '+')

                if string == '-':
                    return Token(MINUS, '-')

                if string == '*':
                    return Token(MUL, '*')

                if string == '/':
                    return Token(DIV, '/')
                
                return Token(LOGOP, string)


            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')
            
            if self.current_char == ',':
                self.advance()
                return Token(COMMA, ',')

            self.error()

        return Token(EOF, None)
