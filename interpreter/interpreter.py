from .lexer import*
import math
variables = {}
logOperators = {'+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '>>=', '<<=', '<', '>', '==', '<=', '>=', '!='}

###############################################################################
#                                                                             #
#  INTERPRETER                                                                #
#                                                                             #
###############################################################################


class NodeVisitor(object):

    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class Interpreter(NodeVisitor):
    
    def __init__(self, parser):
        self.parser = parser

    def visit_BinOp(self, node):
        levo = self.visit(node.left)
        desno = self.visit(node.right)
        
        if node.op.type == PLUS:
            return levo + desno
        elif node.op.type == MINUS:
            return levo - desno
        elif node.op.type == MUL:
            return levo * desno
        elif node.op.type == DIV:
            if isinstance(levo, int) and isinstance(desno, int):
                return int(levo/desno)
            return levo / desno
        
    def visit_UnOp(self, node):        
        if node.op.type == PLUS:
            return self.visit(node.right)
        elif node.op.type == MINUS:
            return 0 - self.visit(node.right)
        elif node.op.type == MUL:
            return 1 * self.visit(node.right)
        elif node.op.type == DIV:
            return 1 / self.visit(node.right)
    
    def visit_LogOp(self, node):
        global variables
        if(node.logOp.value not in logOperators):
            self.error()


        if(node.logOp.value == '+='):            
            val = self.isVariable(node.right)   
            variables[node.left.value] += val
            
            return variables[node.left.value]
        if(node.logOp.value == '-='):            
            val = self.isVariable(node.right)   
            variables[node.left.value] -= val
            
            return variables[node.left.value]
        if(node.logOp.value == '*='):            
            val = self.isVariable(node.right)   
            variables[node.left.value] *= val
            
            return variables[node.left.value]
        if(node.logOp.value == '/='):            
            val = self.isVariable(node.right)   
            variables[node.left.value] /= val
            
            return variables[node.left.value]
        if(node.logOp.value == '%='):
            val = self.isVariable(node.right)   
            variables[node.left.value] %= val
            
            return variables[node.left.value]
        if(node.logOp.value == '&='):
            val = self.isVariable(node.right)   
            variables[node.left.value] &= val
            
            return variables[node.left.value]
        if(node.logOp.value == '|='):
            val = self.isVariable(node.right)   
            variables[node.left.value] |= val
            
            return variables[node.left.value]
        if(node.logOp.value == '^='):
            val = self.isVariable(node.right)   
            variables[node.left.value] ^= val
            
            return variables[node.left.value]
        if(node.logOp.value == '>>='):
            val = self.isVariable(node.right)   
            variables[node.left.value] >>= val
            
            return variables[node.left.value]
        if(node.logOp.value == '<<='):
            val = self.isVariable(node.right)   
            variables[node.left.value] <<= val
            
            return variables[node.left.value]
        
        iskaz = True
        while(hasattr(node, 'left') and hasattr(node, 'right') and hasattr(node, 'logOp')):
            desni = node.right
            if(hasattr(desni, 'left') and hasattr(desni, 'logOp')):
                desni= desni.left
            
            valL = self.isVariable(node.left)
            valR = self.isVariable(desni)
            if(node.logOp.value == '<'):
                iskaz = valL < valR 
            if(node.logOp.value == '>'):
                iskaz = valL > valR
            if(node.logOp.value == '=='):
                iskaz = valL == valR
            if(node.logOp.value == '<='):
                iskaz = valL <= valR
            if(node.logOp.value == '>='):
                iskaz = valL >= valR
            if(node.logOp.value == '!='):
                iskaz = valL != valR

            if(iskaz == False):
                return iskaz
            
            node = node.right
            
        return iskaz
    
    def visit_Equal(self, node):
        global variables  
        
        if(isinstance(node.left.value, int)):
            self.error()     
        
        val = self.isVariable(node.right)
        variables[node.left.value] = val
        return val
    
    def visit_Function(self, node):
        func = getattr(math, node.func.value)
        return func(self.visit(node.expr))
    
    def visit_Pow(self, node):
        return math.pow(self.visit(node.left), self.visit(node.right))

    def visit_Num(self, node):
        return node.value
    
    def visit_Bool(self, node):
        return node.value
    
    def visit_Var(self, node):
        global variables
        
        if(node.value in variables):
            return variables[node.value]
        
        return node.value

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)
    
    def isVariable(self, n):
        val = self.visit(n)
        
        if(isinstance(val,str)):
            self.error()
        
        if(val in variables):
                val = variables[val]
        return val

