from .lexer import *

###############################################################################
#                                                                             #
#  PARSER                                                                     #
#                                                                             #
###############################################################################


class AST(object):
    pass


class BinOp(AST):

    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class UnOp(AST):

    def __init__(self, op, right):
        self.token = self.op = op
        self.right = right

         
class Equal(AST):

    def __init__(self, left, right):
        self.left = left
        self.right = right


class Num(AST):

    def __init__(self, token):
        self.token = token
        self.value = token.value

class Var(AST):

    def __init__(self, token):
        self.token = token
        self.value = token.value


class Function(AST):

    def __init__(self, func, expr):
        self.func = func
        self.expr = expr

        
class Pow(AST):

    def __init__(self, left, right):
        self.left = left
        self.right = right


class LogOp(AST):

    def __init__(self, left, logOp, right):
        self.left = left
        self.right = right
        self.logOp = logOp
        
class Bool(AST):

    def __init__(self, token):
        self.token = token
        self.value = token.value

class Parser(object):

    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        """factor : INTEGER | LPAREN expr RPAREN"""
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type == TRUE:
            self.eat(TRUE)
            return Bool(token)
        elif token.type == FALSE:
            self.eat(FALSE)
            return Bool(token)
        elif token.type == VARIABLE:
            self.eat(VARIABLE)
            return Var(token)
        elif token.type == FUNCTION:                
            self.eat(FUNCTION)
            if(self.current_token.type != LPAREN):
                return Var(token)
            self.eat(LPAREN)
            node = self.dodela()
            if token.value == 'pow':  # pow prima 2 vrednosti
                self.eat(COMMA)
                rnode = self.dodela()
                self.eat(RPAREN)
                return Pow(left=node, right=rnode)
                
            self.eat(RPAREN)
            return Function(func=token , expr=node)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.dodela()
            self.eat(RPAREN)
            return node
        elif token.type == MINUS:
            self.eat(MINUS)
            node = UnOp(op=token, right=self.factor())
            return node
        elif token.type == PLUS:
            self.eat(PLUS)
            node = UnOp(op=token, right=self.factor())
            return node

    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        node = self.factor()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def expr(self):
        """
        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MUL | DIV) factor)*
        factor : INTEGER | LPAREN expr RPAREN
        """
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type in (PLUS, MINUS):
                if token.type == PLUS:
                    self.eat(PLUS)
                elif token.type == MINUS:
                        self.eat(MINUS)

                node = BinOp(left=node, op=token, right=self.term())
        
        return node
    
    
    def logickaOp(self):
        node = self.expr()
        
        if self.current_token.type == LOGOP:
            lop = self.current_token
            self.eat(LOGOP)
            node = LogOp(left=node, logOp=lop, right=self.logickaOp())
            
        return node
        
        
    def dodela(self):
        node = self.logickaOp()
        
        if self.current_token.type == EQUAL:
            self.eat(EQUAL)
            node = Equal(left=node, right=self.dodela())
        
        return node
    
    

    def parse(self):
        node = self.dodela()
        if self.current_token.type != EOF:
            self.error()
        return node
