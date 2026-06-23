TOKEN_ENTERO = 1
TOKEN_DECIMAL = 2
TOKEN_CADENA = 3
CHIQA = 4
JANI = 5
TOKEN_ID = 6
LURAYANA = 7
TUKUYANA = 8
WAKICHANA = 9
UNTAYANA = 10
KUTICHANA = 11
JISA = 12
JANIWA = 13
TUKUYA_JISA = 14
KUTIÑA = 15
TUKUYA_KUTIÑA = 16

SUMA = 17
RESTA = 18
MULT = 19
DIV = 20
MAYOR = 21
MENOR = 22
IGUAL_IGUAL = 23
DIFERENTE = 24
MAYOR_IGUAL = 25
MENOR_IGUAL = 26
IGUAL = 27
PAR_IZQ = 28
PAR_DER = 29
COMA = 30
COMILLA = 31

PALABRAS_RESERVADAS = {
    "chiqa": CHIQA,
    "jani": JANI,
    "lurayaña": LURAYANA,
    "tukuyaña": TUKUYANA,
    "wakichaña": WAKICHANA,
    "uñtayaña": UNTAYANA,
    "kutichaña": KUTICHANA,
    "jisa": JISA,
    "janiwa": JANIWA,
    "tukuya_jisa": TUKUYA_JISA,
    "kutiña": KUTIÑA,
    "tukuya_kutiña": TUKUYA_KUTIÑA
}

SIMBOLOS = {
    "+": SUMA,
    "-": RESTA,
    "*": MULT,
    "/": DIV,
    ">": MAYOR,
    "<": MENOR,
    "==": IGUAL_IGUAL,
    "!=": DIFERENTE,
    ">=": MAYOR_IGUAL,
    "<=": MENOR_IGUAL,
    "=": IGUAL,
    "(": PAR_IZQ,
    ")": PAR_DER,
    ",": COMA,
    '"': COMILLA
}

NOMBRE_TOKEN = {}

for palabra, codigo_tok in PALABRAS_RESERVADAS.items():
    NOMBRE_TOKEN[codigo_tok] = f"'{palabra}'"

for simbolo, codigo_tok in SIMBOLOS.items():
    NOMBRE_TOKEN[codigo_tok] = f"'{simbolo}'"

NOMBRE_TOKEN[TOKEN_ENTERO] = "un número entero"
NOMBRE_TOKEN[TOKEN_DECIMAL] = "un número decimal"
NOMBRE_TOKEN[TOKEN_CADENA] = "una cadena de texto"
NOMBRE_TOKEN[TOKEN_ID] = "un identificador"

def nombre_token(codigo_tok):
    """Devuelve la representación literal de un código de token."""
    return NOMBRE_TOKEN.get(codigo_tok, f"token desconocido ({codigo_tok})")

def describir_token(token):
    """
    Describe un token concreto (tupla) de forma literal,
    útil para mostrar 'se encontró ...' en los errores.
    """
    codigo_tok, lexema, _linea, _columna = token

    if codigo_tok == TOKEN_ID:
        return f"el identificador '{lexema}'"

    if codigo_tok == TOKEN_ENTERO:
        return f"el número entero '{lexema}'"

    if codigo_tok == TOKEN_DECIMAL:
        return f"el número decimal '{lexema}'"

    if codigo_tok == TOKEN_CADENA:
        return f"la cadena \"{lexema}\""

    return f"'{lexema}'"

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
    linea = 1
    columna = 1

    while i < len(codigo):

        c = codigo[i]

        if c in [' ', '\t', '\r']:
            i += 1
            columna += 1
            continue

        if c == '\n':
            i += 1
            linea += 1
            columna = 1
            continue

        if c == '"':

            col_inicio = columna

            tokens.append((COMILLA, '"', linea, columna))

            i += 1
            columna += 1

            lexema = ""

            while i < len(codigo):

                if codigo[i] == '\\' and i + 1 < len(codigo):

                    if codigo[i + 1] == '"':
                        lexema += '"'
                        i += 2
                        columna += 2
                        continue

                if codigo[i] == '"':
                    break

                if codigo[i] == '\n':
                    raise Exception(
                        f"Error léxico en línea {linea}, "
                        f"columna {col_inicio}: cadena sin cerrar"
                    )

                lexema += codigo[i]
                i += 1
                columna += 1

            if i >= len(codigo):
                raise Exception(
                    f"Error léxico en línea {linea}, "
                    f"columna {col_inicio}: cadena sin cerrar"
                )

            tokens.append((TOKEN_CADENA, lexema, linea, col_inicio))

            tokens.append((COMILLA, '"', linea, columna))

            i += 1
            columna += 1

            continue

        if es_digito(c):

            col_inicio = columna
            lexema = ""

            while i < len(codigo) and es_digito(codigo[i]):
                lexema += codigo[i]
                i += 1
                columna += 1

            if i < len(codigo) and (es_letra(codigo[i]) or codigo[i] == '_'):

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
                    columna += 1

                raise Exception(
                    f"Error léxico en línea {linea}, "
                    f"columna {col_inicio}: identificador inválido "
                    f"'{lexema}'. No puede comenzar con un número."
                )

            if i < len(codigo) and codigo[i] == '.':

                lexema += '.'
                i += 1
                columna += 1

                if i >= len(codigo) or not es_digito(codigo[i]):
                    raise Exception(
                        f"Error léxico en línea {linea}, "
                        f"columna {col_inicio}: decimal inválido '{lexema}'"
                    )

                while i < len(codigo) and es_digito(codigo[i]):
                    lexema += codigo[i]
                    i += 1
                    columna += 1

                if i < len(codigo) and codigo[i] == '.':
                    raise Exception(
                        f"Error léxico en línea {linea}, "
                        f"columna {col_inicio}: número mal formado '{lexema}.'"
                    )

                tokens.append((TOKEN_DECIMAL, lexema, linea, col_inicio))

            else:
                tokens.append((TOKEN_ENTERO, lexema, linea, col_inicio))

            continue

        if es_letra(c):

            col_inicio = columna
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
                columna += 1

            if lexema in PALABRAS_RESERVADAS:

                tokens.append(
                    (
                        PALABRAS_RESERVADAS[lexema],
                        lexema,
                        linea,
                        col_inicio
                    )
                )

            else:

                tokens.append(
                    (
                        TOKEN_ID,
                        lexema,
                        linea,
                        col_inicio
                    )
                )

            continue

        if i + 1 < len(codigo):

            doble = codigo[i:i + 2]

            if doble in ["==", "!=", ">=", "<="]:

                tokens.append(
                    (
                        SIMBOLOS[doble],
                        doble,
                        linea,
                        columna
                    )
                )

                i += 2
                columna += 2

                continue

        if c in SIMBOLOS:

            tokens.append(
                (
                    SIMBOLOS[c],
                    c,
                    linea,
                    columna
                )
            )

            i += 1
            columna += 1

            continue

        raise Exception(
            f"Error léxico en línea {linea}, "
            f"columna {columna}: símbolo no reconocido '{c}'"
        )

    return tokens

class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def actual(self):

        if self.pos < len(self.tokens):
            return self.tokens[self.pos]

        return None

    def consumir(self, token_esperado):

        token = self.actual()

        if token is None:
            raise Exception(
                f"Error sintáctico: se esperaba {nombre_token(token_esperado)} "
                f"y se encontró el fin del archivo"
            )

        if token[0] != token_esperado:

            raise Exception(
                f"Error sintáctico en línea {token[2]}, "
                f"columna {token[3]}: se esperaba "
                f"{nombre_token(token_esperado)} y se encontró "
                f"{describir_token(token)}"
            )

        self.pos += 1

    def programa(self):

        if self.actual() is None:
            raise Exception("Error sintáctico: el programa está vacío")

        while self.actual() is not None:
            self.funcion()

    def funcion(self):

        self.consumir(LURAYANA)
        self.consumir(TOKEN_ID)
        self.consumir(PAR_IZQ)

        self.params()

        self.consumir(PAR_DER)

        self.cuerpo()

        self.consumir(TUKUYANA)

    def params(self):

        if self.actual() and self.actual()[0] == TOKEN_ID:

            self.consumir(TOKEN_ID)

            while self.actual() and self.actual()[0] == COMA:

                self.consumir(COMA)
                self.consumir(TOKEN_ID)

    def cuerpo(self):

        while self.actual() and self.actual()[0] in [
            WAKICHANA,
            UNTAYANA,
            KUTICHANA,
            JISA,
            KUTIÑA
        ]:
            self.sentencia()

    def sentencia(self):

        token = self.actual()[0]

        if token == WAKICHANA:
            self.declaracion()

        elif token == UNTAYANA:
            self.impresion()

        elif token == KUTICHANA:
            self.retorno()

        elif token == JISA:
            self.si()

        elif token == KUTIÑA:
            self.ciclo()

        else:

            actual = self.actual()

            raise Exception(
                f"Error sintáctico en línea {actual[2]}, "
                f"columna {actual[3]}: se encontró {describir_token(actual)} "
                f"donde se esperaba el inicio de una sentencia válida "
                f"(declaración, impresión, retorno, condicional o ciclo)"
            )

    def declaracion(self):

        self.consumir(WAKICHANA)
        self.consumir(TOKEN_ID)
        self.consumir(IGUAL)
        self.expresion()

    def impresion(self):

        self.consumir(UNTAYANA)
        self.expresion()

    def retorno(self):

        self.consumir(KUTICHANA)
        self.expresion()

    def si(self):

        self.consumir(JISA)

        self.consumir(PAR_IZQ)

        self.condicion()

        self.consumir(PAR_DER)

        self.cuerpo()

        if self.actual() and self.actual()[0] == JANIWA:

            self.consumir(JANIWA)

            self.cuerpo()

        self.consumir(TUKUYA_JISA)

    def ciclo(self):

        self.consumir(KUTIÑA)

        self.consumir(PAR_IZQ)

        self.condicion()

        self.consumir(PAR_DER)

        self.cuerpo()

        self.consumir(TUKUYA_KUTIÑA)

    def condicion(self):

        self.expresion()

        token = self.actual()

        if token is None:
            raise Exception(
                "Error sintáctico: se esperaba un operador relacional "
                "(>, <, ==, !=, >=, <=) y se encontró el fin del archivo"
            )

        if token[0] not in [
            MAYOR,
            MENOR,
            IGUAL_IGUAL,
            DIFERENTE,
            MAYOR_IGUAL,
            MENOR_IGUAL
        ]:

            raise Exception(
                f"Error sintáctico en línea {token[2]}, "
                f"columna {token[3]}: se esperaba un operador relacional "
                f"(>, <, ==, !=, >=, <=) y se encontró {describir_token(token)}"
            )

        self.pos += 1

        self.expresion()

    def expresion(self):

        self.termino()

        while self.actual() and self.actual()[0] in [SUMA, RESTA]:

            self.pos += 1

            self.termino()

    def termino(self):

        self.factor()

        while self.actual() and self.actual()[0] in [MULT, DIV]:

            self.pos += 1

            self.factor()

    def factor(self):

        token = self.actual()

        if token is None:

            raise Exception(
                "Error sintáctico: la expresión está incompleta, "
                "se encontró el fin del archivo"
            )

        if token[0] in [
            TOKEN_ENTERO,
            TOKEN_DECIMAL,
            TOKEN_ID
        ]:

            self.pos += 1

        elif token[0] == COMILLA:
            self.consumir(COMILLA)
            self.consumir(TOKEN_CADENA)
            self.consumir(COMILLA)
        elif token[0] == PAR_IZQ:
            self.consumir(PAR_IZQ)
            self.expresion()
            self.consumir(PAR_DER)
        elif token[0] in [CHIQA, JANI]:
            self.pos += 1
        else:

            raise Exception(
                f"Error sintáctico en línea {token[2]}, "
                f"columna {token[3]}: se esperaba un valor "
                f"(número, identificador, cadena, '(' o chiqa/jani) "
                f"y se encontró {describir_token(token)}"
            )

if __name__ == "__main__":

    codigo = '''
lurayaña contar()
    wakichaña i = 10
    kutiña (i <= 5)
        uñtayaña i
        wakichaña i = i + 1
        jisa (i > 5)
            uñtayaña "hola"
        tukuya_jisa
    tukuya_kutiña
tukuyaña
'''
    try:
        tokens = analizador_lexico(codigo)
        print("TOKENS ENCONTRADOS:\n")
        for token in tokens:
            print(token)
        parser = Parser(tokens)
        parser.programa()
        if parser.pos != len(tokens):
            token = tokens[parser.pos]
            raise Exception(
                f"Error sintáctico en línea {token[2]}, "
                f"columna {token[3]}: se encontró {describir_token(token)} "
                f"de forma inesperada; se esperaba el inicio de una nueva "
                f"función ('lurayaña') o el fin del archivo"
            )
        print("\nANÁLISIS SINTÁCTICO CORRECTO")
    except Exception as e:
        print("\nERROR DETECTADO:")
        print(e)