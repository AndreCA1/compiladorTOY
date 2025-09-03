from token import TOKEN

global linha, coluna

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
        print(f'(tk = {msg} lex = {lexema} lin = {linha} col = {coluna})')

    def getToken(self):
        estado = 1
        simbolo = self.getChar()
        lexema = ''

        self.descartaComentatios()

        lin = self.linha
        col = self.coluna

        while(True):
            if estado == 1:
                if simbolo.isalpha():
                    estado = 2
                elif simbolo.isdigit():
                    estado = 3
                elif simbolo == '"':
                    estado = 4
                elif simbolo == "=":
                    estado = 5

                elif simbolo == "{":
                    return (TOKEN.abreChave, "{", lin, col)
                elif simbolo == "{":
                    return (TOKEN.fechaChave, "}", lin, col)
                elif simbolo == "(":
                    return (TOKEN.abrePar, "(", lin, col)
                elif simbolo == ")":
                    return (TOKEN.fechaPar, ")", lin, col)
                elif simbolo == ',':
                    return (TOKEN.virgula, ",", lin, col)
                elif simbolo == ";":
                    return (TOKEN.pontoVirgula, ";", lin, col)
                elif simbolo == ".":
                    return (TOKEN.pontofinal, ".", lin, col)

                elif simbolo == "+":
                    return (TOKEN.mais, "+", lin, col)
                elif simbolo == "-":
                    return (TOKEN.menos, "-", lin, col)
                elif simbolo == "*":
                    return (TOKEN.vezes, "*", lin, col)
                elif simbolo == "/":
                    return (TOKEN.divide, "/", lin, col)
                elif simbolo == "%":
                    return (TOKEN.porcentagem, "%", lin, col)

                elif simbolo == "\0":
                    return (TOKEN.fimarquivo, "<eof>", lin, col)
                else:
                    lexema += simbolo
                    return (TOKEN.erro, lexema, lin, col)

            elif estado == 2:
                # TODO: verificar lexema
                if simbolo == "opRel":
                    return (TOKEN.opRel, "", lin, col)
                elif simbolo == "and":
                    return (TOKEN.AND, "", lin, col)
                elif simbolo == "or":
                    return (TOKEN.OR, "", lin, col)
                elif simbolo == "not":
                    return (TOKEN.NOT, "", lin, col)


if __name__ == '__main__':
    lexico = Lexico("teste.toy")
    token = lexico.getToken()
    while (token[0] != TOKEN.eof):
        lexico.imprimirToken(token)
        token = lexico.getToken()
    lexico.imprimirToken(token)