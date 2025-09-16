import Lexico
import tokens

class sintatico:
    def __init__(self,  lexico):
        self.lexico = lexico
        self.lexico.tokenLido = self.lexico.getToken()

    def consome(self, tokenAtual):
        (token, lexema, linha, coluna) = self.lexico.tokenLido
        if tokenAtual == token:
            self.lexico.tokenLido = self.lexico.getToken()
        else:
            msgTokenLido = tokens.TOKEN.msg(token)
            msgTokenAtual = tokens.TOKEN.msg(tokenAtual)
            if token == tokens.TOKEN.erro:
                msg = lexema
            else:
                msg = msgTokenLido
            print(f'Era esperado {msgTokenAtual} mas veio {msg}')
            raise Exception

    def prog(self):
        # Prog -> inicio Coms fim.
        self.consome(tokens.TOKEN.inicio)
        self.coms()
        self.consome(tokens.TOKEN.fim)
        self.consome(tokens.TOKEN.pontofinal)
        self.consome(tokens.TOKEN.fimarquivo)

    def coms(self):
        # Coms -> LAMBDA | Com Coms
        # Conjunto de tokens que podem iniciar um comando
        primeiros_com = {
            tokens.TOKEN.leia,
            tokens.TOKEN.escreva,
            tokens.TOKEN.IF,
            tokens.TOKEN.ident,
            tokens.TOKEN.abreChave,
        }

        (token, lexema, linha, coluna) = self.lexico.tokenLido
        if token in primeiros_com:
            self.com()  # Consome um comando
            self.coms()  # Continua a lista
        else:
            # LAMBDA: não faz nada
            return

    def com(self):
        # <com> -> <atrib> | <if> | <ler> | < escrever > | < bloco >
        (token, lexema, linha, coluna) = self.lexico.tokenLido

        if token == tokens.TOKEN.leia:
            self.ler()
        elif token == tokens.TOKEN.escreva:
            self.escrever()
        elif token == tokens.TOKEN.IF:
            self.IF()
        elif token == tokens.TOKEN.ident:
            self.atrib()
        elif token == tokens.TOKEN.abreChave:
            self.bloco()
        else:
            msg = tokens.TOKEN.msg(token)
            print(f'Comando inesperado: {msg} na linha {linha}, coluna {coluna}')
            raise Exception

    def ler(self):
        # Ler -> leia ( string, ident ) ;
        self.consome(tokens.TOKEN.leia)
        self.consome(tokens.TOKEN.abreParenteses)
        self.consome(tokens.TOKEN.string)
        self.consome(tokens.TOKEN.virgula)
        self.consome(tokens.TOKEN.ident)
        self.consome(tokens.TOKEN.fechaParenteses)
        self.consome(tokens.TOKEN.pontoVirgula)



    def escrever(self):
        # Escrever -> escreva ( string RestoEscrever
        self.consome(tokens.TOKEN.escreva)
        self.consome(tokens.TOKEN.abreParenteses)
        self.consome(tokens.TOKEN.string)
        self.restoEscrever()

    def restoEscrever(self):
        # RestoEscrever -> , ident ) ; | ) ;
        (token, lexema, linha, coluna) = self.lexico.tokenLido

        if token == tokens.TOKEN.virgula:
            self.consome(tokens.TOKEN.virgula)
            self.consome(tokens.TOKEN.ident)
            self.consome(tokens.TOKEN.fechaParenteses)
            self.consome(tokens.TOKEN.pontoVirgula)

        elif token == tokens.TOKEN.fechaParenteses:
            self.consome(tokens.TOKEN.fechaParenteses)
            self.consome(tokens.TOKEN.pontoVirgula)

        else:
            msg = tokens.TOKEN.msg(token)
            print(f'Erro em restoEscrever: esperado vírgula ou fechaParenteses, mas veio {msg}')
            raise Exception

    def IF(self):
        # If -> if ( Exp ) Com RestoIf
        self.consome(tokens.TOKEN.IF)
        self.consome(tokens.TOKEN.abreParenteses)
        self.exp()
        self.consome(tokens.TOKEN.fechaParenteses)
        self.com()
        self.restoIF()


    def restoIF(self):
        # RestoIf -> LAMBDA | else Com
        (token, lexema, linha, coluna) = self.lexico.tokenLido

        if token == tokens.TOKEN.ELSE:
            self.consome(tokens.TOKEN.ELSE)
            self.com()
        else:
            # LAMBDA: não faz nada
            return

    def bloco(self):
        # Bloco -> { Coms }
        self.consome(tokens.TOKEN.abreChave)
        self.coms()
        self.consome(tokens.TOKEN.fechaChave)

    def atrib(self):
        # Atrib -> ident = Exp ;
        self.consome(tokens.TOKEN.ident)
        self.consome(tokens.TOKEN.igual)
        self.exp()
        self.consome(tokens.TOKEN.pontoVirgula)

    def exp(self):
        # Exp -> Nao RestoExp
        self.nao()
        self.restoExp()

    def restoExp(self):
        # RestoExp -> LAMBDA | and Nao RestoExp | or Nao RestoExp
        (token, lexema, linha, coluna) = self.lexico.tokenLido

        if token == tokens.TOKEN.AND:
            self.consome(tokens.TOKEN.AND)
            self.nao()
            self.restoExp()

        elif token == tokens.TOKEN.OR:
            self.consome(tokens.TOKEN.OR)
            self.nao()
            self.restoExp()

        else:
            # LAMBDA: não faz nada
            return

    def nao(self):
        # Nao -> not Nao | Rel
        (token, lexema, linha, coluna) = self.lexico.tokenLido

        if token == tokens.TOKEN.NOT:
            self.consome(tokens.TOKEN.NOT)
            self.nao()
        else:
            self.rel()

    def rel(self):
        # Rel -> Soma RestoRel
        self.soma()
        self.restoRel()

    def restoRel(self):
        # RestoRel -> LAMBDA | opRel Soma
        (token, lexema, linha, coluna) = self.lexico.tokenLido

        if token in {
            tokens.TOKEN.menor,
            tokens.TOKEN.maior,
            tokens.TOKEN.igual
        }:
            self.consome(token)
            self.soma()
        else:
            # LAMBDA: não faz nada
            return


    def soma(self):
        # Soma -> Mult RestoSoma
        self.mult()
        self.restoSoma()

    def restoSoma(self):
        # RestoSoma -> LAMBDA | + Mult RestoSoma | - Mult RestoSoma
        (token, lexema, linha, coluna) = self.lexico.tokenLido

        if token == tokens.TOKEN.mais:
            self.consome(tokens.TOKEN.mais)
            self.mult()
            self.restoSoma()

        elif token == tokens.TOKEN.menos:
            self.consome(tokens.TOKEN.menos)
            self.mult()
            self.restoSoma()

        else:
            # LAMBDA: não faz nada
            return

    def mult(self):
        # Mult -> Uno RestoMult
        self.uno()
        self.restoMult()

    def restoMult(self):
        # RestoMult -> LAMBDA | * Uno RestoMult | / Uno RestoMult | % Uno RestoMult
        (token, lexema, linha, coluna) = self.lexico.tokenLido

        if token == tokens.TOKEN.vezes:
            self.consome(tokens.TOKEN.vezes)
            self.uno()
            self.restoMult()

        elif token == tokens.TOKEN.divide:
            self.consome(tokens.TOKEN.divide)
            self.uno()
            self.restoMult()

        elif token == tokens.TOKEN.porcentagem:
            self.consome(tokens.TOKEN.porcentagem)
            self.uno()
            self.restoMult()

    def uno(self):
        # Uno -> + Uno | - Uno | Folha
        (token, lexema, linha, coluna) = self.lexico.tokenLido

        if token == tokens.TOKEN.mais:
            self.consome(tokens.TOKEN.mais)
            self.uno()

        elif token == tokens.TOKEN.menos:
            self.consome(tokens.TOKEN.menos)
            self.uno()

        else:
            self.folha()

    def folha(self):
        # <folha> -> num | ident | ( <exp>)
        (token, lexema, linha, coluna) = self.lexico.tokenLido

        if token == tokens.TOKEN.num:
            salva = lexema
            self.consome(tokens.TOKEN.num)
            return salva

        elif token == tokens.TOKEN.ident:
            salva = lexema
            self.consome(tokens.TOKEN.ident)
            return salva

        elif token == tokens.TOKEN.abreParenteses:
            self.consome(tokens.TOKEN.abreParenteses)
            salva = self.exp()
            self.consome(tokens.TOKEN.fechaParenteses)
            return '(' + salva + ')'

        else:
            msg = tokens.TOKEN.msg(token)
            print(f'Erro em folha: era esperado num | ident | "(" mas veio {msg} (linha {linha}, coluna {coluna})')
            raise Exception