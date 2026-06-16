PALABRAS_RESERVADAS = {
    "chiqa": 4,
    "jani": 5,
    "lurayaña": 7,
    "tukuyaña": 8,
    "wakichaña": 9,
    "uñtayaña": 10,
    "kutichaña": 11,
    "jisa": 12,
    "janiwa": 13,
    "tukuya_jisa": 14,
    "kutiña": 15,
    "tukuya_kutiña": 16
}

SIMBOLOS = {
    "+": 17,
    "-": 18,
    "*": 19,
    "/": 20,
    ">": 21,
    "<": 22,
    "==": 23,
    "!=": 24,
    ">=": 25,
    "<=": 26,
    "=": 27,
    "(": 28,
    ")": 29,
    ",": 30,
    '"': 31
}

TOKEN_ENTERO = 1
TOKEN_DECIMAL = 2
TOKEN_CADENA = 3
TOKEN_ID = 6
def es_letra(c):
    return (
        ('a' <= c <= 'z') or
        ('A' <= c <= 'Z') or
        c in "ñÑüÜ"
    )
def es_digito(c):
    return '0' <= c <= '9'
def analizador_lexico(codigo):
    tokens = []
    i = 0
    while i < len(codigo):
        c = codigo[i]
        if c in [' ', '\t', '\n', '\r']:
            i += 1
            continue
        if c == '"':
            tokens.append((SIMBOLOS['"'], '"'))
            i += 1
            lexema = ""
            while i < len(codigo) and codigo[i] != '"':
                lexema += codigo[i]
                i += 1
            if i >= len(codigo):
                raise Exception("Error léxico: cadena sin cerrar")
            tokens.append((TOKEN_CADENA, lexema))
            tokens.append((SIMBOLOS['"'], '"'))
            i += 1
            continue
        if es_digito(c):
            lexema = ""
            while i < len(codigo) and es_digito(codigo[i]):
                lexema += codigo[i]
                i += 1
            if i < len(codigo) and codigo[i] == '.':
                lexema += '.'
                i += 1
                if i >= len(codigo) or not es_digito(codigo[i]):
                    raise Exception(
                        f"Error léxico: decimal inválido '{lexema}'"
                    )
                while i < len(codigo) and es_digito(codigo[i]):
                    lexema += codigo[i]
                    i += 1
                tokens.append((TOKEN_DECIMAL, lexema))
            else:
                tokens.append((TOKEN_ENTERO, lexema))
            continue
        if es_letra(c):
            lexema = ""
            while (
                i < len(codigo)
                and (
                    es_letra(codigo[i])
                    or es_digito(codigo[i])
                    or codigo[i] == '_'
                )
            ):
                lexema += codigo[i]
                i += 1
            if lexema in PALABRAS_RESERVADAS:
                tokens.append(
                    (PALABRAS_RESERVADAS[lexema], lexema)
                )
            else:
                tokens.append((TOKEN_ID, lexema))
            continue
        if i + 1 < len(codigo):
            doble = codigo[i:i + 2]
            if doble in ["==", "!=", ">=", "<="]:
                tokens.append((SIMBOLOS[doble], doble))
                i += 2
                continue
        if c in SIMBOLOS:
            tokens.append((SIMBOLOS[c], c))
            i += 1
            continue
        raise Exception(
            f"Error léxico: símbolo no reconocido '{c}'"
        )
    return tokens
codigo = '''
lurayaña suma(a, b)

    wakichaña resultado = a + b

    jisa (resultado >= 10)
        uñtayaña "Mayor o igual a diez"
    tukuya_jisa

    kutichaña resultado

tukuyaña
'''

tokens = analizador_lexico(codigo)

for token, lexema in tokens:
    print(f"Token: {token:2}   Lexema: {lexema}")