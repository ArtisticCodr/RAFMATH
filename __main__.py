from interpreter.lexer import Lexer
from interpreter.parser import Parser
from interpreter.interpreter import Interpreter


def main():    
    while True:
        try:
            text = input('rafmath: ')
        except (EOFError, KeyboardInterrupt):
            break
        if not text:
            continue

        if(text.lower() == 'exit'):
            break

        try:
            lexer = Lexer(text) 
            parser = Parser(lexer)
            interpreter = Interpreter(parser)
            result = interpreter.interpret()
        
            if isinstance(result, int):
                print(result)
            if isinstance(result, float):
                result *= 1000
                result = int(result)
                result = result / 1000;
                print (result)
        except:
            print('ERROR')
            pass


if __name__ == '__main__':
    main()
