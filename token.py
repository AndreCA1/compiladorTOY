from enum import IntEnum

class TOKEN(IntEnum):
    fim = 0
    fimarquivo = 1
    erro = 2

    inicio = 3
    leia = 4
    escreva = 5
    IF = 6
    ELSE = 7

    ident = 8
    string = 9
    num = 10

    abreChave = 11
    fechaChave = 12
    abreParenteses = 13
    fechaParenteses = 14
    pontoVirgula = 15
    virgula = 16
    pontofinal = 17

    igual = 18
    AND = 19
    OR = 20
    NOT = 21

    mais = 22
    menos = 23
    vezes = 24
    divide = 25
    porcentagem = 26

    @classmethod
    def msg(cls, token):
        nomes = {
            0: 'end',
            1: '<eof>',
            2: 'erro',
            3: 'begin',
            4: 'read',
            5: 'print',
            6: 'if',
            7: 'else',
            8: 'ident',
            9: 'string',
            10: 'numero',

            11: '{',
            12: '}',
            13: '(',
            14: ')',
            15: ';',
            16: ',',
            17: '.',
            18: '=',

            19: 'and',
            20: 'or',
            21: 'not',

            22: '+',
            23: '-',
            24: '*',
            25: '/',
            26: '%'
        }
        return nomes[token]

    @classmethod
    def reservada(cls, lexema):
        reservadas = {
            'if': TOKEN.IF,
            'end': TOKEN.fim,
            'else': TOKEN.ELSE,
            'read': TOKEN.leia,
            'print': TOKEN.escreva,
            'and': TOKEN.AND,
            'or': TOKEN.OR,
            'not': TOKEN.NOT
        }
        if lexema in reservadas:
            return reservadas[lexema]
        else:
            return TOKEN.ident
