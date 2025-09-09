from tokens import TOKEN
from colorama import init, Fore

class Lexico:
    def __init__(self, arqFonte):
        self.arqFonte = arqFonte
        self.fonte = self.arqFonte.read()
        self.tamFonte = len(self.fonte)
        self.indiceFonte = 0
        self.tokenLido = None
        self.linha = 1
        self.coluna = 0

    def fimDoArquivo(self):
        return self.indiceFonte >= self.tamFonte

    def getChar(self):
        if self.fimDoArquivo():
            return '\0'
        car = self.fonte[self.indiceFonte]
        self.indiceFonte += 1
        if car == '\n':
            self.linha += 1
            self.coluna = 0
        else:
            self.coluna += 1
        return car

    def unGetChar(self, simbolo):
        if simbolo == '\n':
            self.linha -= 1
        if self.indiceFonte > 0:
            self.indiceFonte -= 1
        self.coluna -= 1

    def imprimirToken(self, tokenCorrente):
        (token, lexema, linha, coluna) = tokenCorrente
        msg = TOKEN.msg(token)
        print(Fore.GREEN + '(tk = ' + Fore.BLUE + str(msg) + Fore.GREEN + ' lex = ' + Fore.YELLOW + str(
            lexema) + Fore.GREEN + ' lin = ' + Fore.RESET + str(linha) + Fore.GREEN + ' col = ' + Fore.RESET + str(coluna))
    def getToken(self):
        estado = 1
        simbolo = self.getChar()
        lexema = ''

        while(True):
            lin = self.linha
            col = self.coluna
            if estado == 1:

                #ignora comentario
                if simbolo == "/":
                    simbolo = self.getChar()
                    if simbolo != "/":
                        self.unGetChar(simbolo)
                        return TOKEN.divide, "/", lin, col
                    else:
                        simbolo = self.getChar()
                        while (simbolo != "\n"):
                            simbolo = self.getChar()

                # ignora espaco e quebra de linha
                elif simbolo == " " or simbolo == "\n":
                    simbolo = self.getChar()
                    continue

                #palavras
                elif simbolo.isalpha():
                    estado = 2

                #numeros
                elif simbolo.isdigit():
                    estado = 3

                #strings
                elif simbolo == '"':
                    estado = 4

                elif simbolo == "=":
                    return TOKEN.igual, "=", lin, col
                elif simbolo == "{":
                    return TOKEN.abreChave, "{", lin, col
                elif simbolo == "}":
                    return TOKEN.fechaChave, "}", lin, col
                elif simbolo == "(":
                    return TOKEN.abreParenteses, "(", lin, col
                elif simbolo == ")":
                    return TOKEN.fechaParenteses, ")", lin, col
                elif simbolo == ',':
                    return TOKEN.virgula, ",", lin, col
                elif simbolo == ";":
                    return TOKEN.pontoVirgula, ";", lin, col
                elif simbolo == ".":
                    return TOKEN.pontofinal, ".", lin, col

                elif simbolo == "+":
                    return TOKEN.mais, "+", lin, col
                elif simbolo == "-":
                    return TOKEN.menos, "-", lin, col
                elif simbolo == "*":
                    return TOKEN.vezes, "*", lin, col
                elif simbolo == "%":
                    return TOKEN.porcentagem, "%", lin, col
                elif simbolo == ">":
                    return TOKEN.maior, ">", lin, col
                elif simbolo == "<":
                    return TOKEN.menor, "<", lin, col

                elif simbolo == "\0":
                    return TOKEN.fimarquivo, "<eof>", lin, col
                else:
                    lexema += simbolo
                    return TOKEN.erro, lexema, lin, col

            elif estado == 2:
                estado = 1
                palavra = simbolo
                while True:
                    simbolo = self.getChar()
                    if simbolo == ".":
                        pass
                    elif(not simbolo.isalnum()):
                        self.unGetChar(simbolo)
                        break
                    palavra += simbolo

                if palavra == "inicio":
                    return TOKEN.inicio, palavra, lin, col
                if palavra == "fim.":
                    return TOKEN.fim, palavra, lin, col

                if palavra == "if":
                    return TOKEN.IF, palavra, lin, col
                if palavra == "else":
                    return TOKEN.ELSE, palavra, lin, col

                if palavra == "leia":
                    return TOKEN.leia, palavra, lin, col
                if palavra == "escreva":
                    return TOKEN.escreva, palavra, lin, col

                elif palavra == "and":
                    return TOKEN.AND, palavra, lin, col
                elif palavra == "or":
                    return TOKEN.OR, palavra, lin, col
                elif palavra == "not":
                    return TOKEN.NOT, palavra, lin, col

                else:
                    return TOKEN.ident, palavra, lin, col

            elif estado == 3:
                estado = 1
                numero = simbolo
                while True:
                    simbolo = self.getChar()
                    if (not simbolo.isdigit()):
                        break
                    numero += simbolo

                self.unGetChar(simbolo)
                return TOKEN.num, numero, lin, col

            elif estado == 4:
                estado = 1
                string = ''
                simbolo = self.getChar()
                while simbolo != '"':
                    string += simbolo
                    simbolo = self.getChar()

                return TOKEN.string, string, lin, col

if __name__ == '__main__':
    init()
    with open("example.toy", "r") as arqFonte:
        lexico = Lexico(arqFonte)
        token = lexico.getToken()
        while token[0] != TOKEN.fimarquivo:
            lexico.imprimirToken(token)
            token = lexico.getToken()
        lexico.imprimirToken(token)