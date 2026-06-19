ENTERO = 1
DECIMAL = 2
CADENA = 3
CHIQA = 4
JANI = 5
ID = 6
LURAYANA = 7
TUKUYANA = 8
WAKICHANA = 9
UNTAYANA = 10
KUTICHANA = 11
JISA = 12
JANIWA = 13
TUKUYA_JISA = 14
KUTINA = 15
TUKUYA_KUTINA = 16
OP_SUMA = 17
OP_RESTA = 18
OP_MUL = 19
OP_DIV = 20
OP_MAYOR = 21
OP_MENOR = 22
OP_IGUAL = 23
OP_DISTINTO = 24
OP_MAYOR_IG = 25
OP_MENOR_IG = 26
ASIG = 27
PAR_ABRE = 28
PAR_CIERRA = 29
COMA = 30

def start(tokens):
    i, error = programa(tokens, 0)

    if error != '':
        return error

    if i != len(tokens):
        return f"Error sintáctico: token inesperado {tokens[i]} en la posición {i}"

    return "VÁLIDO"
def es_inicio_sentencia(token):
    return token in (
        WAKICHANA,
        ID,
        UNTAYANA,
        JISA,
        KUTINA,
        KUTICHANA
    )

# programa = funcion { funcion }

def programa(tokens, i):

    if i >= len(tokens):
        return i, "Se esperaba una función"

    while i < len(tokens):

        i, error = funcion(tokens, i)

        if error != '':
            return i, error

    return i, ''
def funcion(tokens, i):
    if i >= len(tokens) or tokens[i] != LURAYANA:
        return i, "Se esperaba 'lurayaña'"
    i += 1
    if i >= len(tokens) or tokens[i] != ID:
        return i, "Se esperaba un identificador"
    i += 1
    if i >= len(tokens) or tokens[i] != PAR_ABRE:
        return i, "Se esperaba '('"
    i += 1
    i, error = params(tokens, i)
    if error != '':
        return i, error
    if i >= len(tokens) or tokens[i] != PAR_CIERRA:
        return i, "Se esperaba ')'"
    i += 1
    i, error = cuerpo(tokens, i, [TUKUYANA])
    if error != '':
        return i, error
    if i >= len(tokens) or tokens[i] != TUKUYANA:
        return i, "Se esperaba 'tukuyaña'"
    i += 1
    return i, ''
def params(tokens, i):
    if i < len(tokens) and tokens[i] == ID:
        i += 1
        while i < len(tokens) and tokens[i] == COMA:
            i += 1
            if i >= len(tokens) or tokens[i] != ID:
                return i, "Se esperaba un identificador"
            i += 1
    return i, ''
def cuerpo(tokens, i, fin):
    while i < len(tokens):
        if tokens[i] in fin:
            return i, ''
        if not es_inicio_sentencia(tokens[i]):
            return i, "Se esperaba una sentencia"

        i, error = sentencia(tokens, i)

        if error != '':
            return i, error

    return i, "Fin inesperado del programa"
def sentencia(tokens, i):
    if tokens[i] == WAKICHANA:
        return declaracion(tokens, i)
    if tokens[i] == ID:
        return asignacion(tokens, i)
    if tokens[i] == UNTAYANA:
        return impresion(tokens, i)
    if tokens[i] == JISA:
        return condicional(tokens, i)
    if tokens[i] == KUTINA:
        return bucle(tokens, i)
    if tokens[i] == KUTICHANA:
        return retorno(tokens, i)

    return i, "Sentencia inválida"

def declaracion(tokens, i):
    i += 1
    if i >= len(tokens) or tokens[i] != ID:
        return i, "Se esperaba un identificador"
    i += 1
    if i >= len(tokens) or tokens[i] != ASIG:
        return i, "Se esperaba '='"
    i += 1
    return comparacion(tokens, i)
def asignacion(tokens, i):
    i += 1
    if i >= len(tokens) or tokens[i] != ASIG:
        return i, "Se esperaba '='"
    i += 1
    return comparacion(tokens, i)
def impresion(tokens, i):
    i += 1
    return comparacion(tokens, i)
def retorno(tokens, i):
    i += 1
    return comparacion(tokens, i)

def condicional(tokens, i):
    i += 1
    if i >= len(tokens) or tokens[i] != PAR_ABRE:
        return i, "Se esperaba '('"
    i += 1
    i, error = comparacion(tokens, i)
    if error != '':
        return i, error
    if i >= len(tokens) or tokens[i] != PAR_CIERRA:
        return i, "Se esperaba ')'"
    i += 1
    i, error = cuerpo(tokens, i, [JANIWA, TUKUYA_JISA])
    if error != '':
        return i, error
    if i < len(tokens) and tokens[i] == JANIWA:
        i += 1
        if i < len(tokens) and tokens[i] == JISA:
            i, error = condicional(tokens, i)
        else:
            i, error = cuerpo(tokens, i, [TUKUYA_JISA])
        if error != '':
            return i, error
    if i >= len(tokens) or tokens[i] != TUKUYA_JISA:
        return i, "Se esperaba 'tukuya_jisa'"
    i += 1
    return i, ''
def bucle(tokens, i):
    i += 1
    if i >= len(tokens) or tokens[i] != PAR_ABRE:
        return i, "Se esperaba '('"
    i += 1
    i, error = comparacion(tokens, i)
    if error != '':
        return i, error
    if i >= len(tokens) or tokens[i] != PAR_CIERRA:
        return i, "Se esperaba ')'"
    i += 1
    i, error = cuerpo(tokens, i, [TUKUYA_KUTINA])
    if error != '':
        return i, error
    if i >= len(tokens) or tokens[i] != TUKUYA_KUTINA:
        return i, "Se esperaba 'tukuya_kutiña'"
    i += 1
    return i, ''
def comparacion(tokens, i):
    i, error = expresion(tokens, i)
    if error != '':
        return i, error
    if i < len(tokens) and tokens[i] in (
        OP_MAYOR,
        OP_MENOR,
        OP_IGUAL,
        OP_DISTINTO,
        OP_MAYOR_IG,
        OP_MENOR_IG
    ):
        i += 1
        return expresion(tokens, i)
    return i, ''
def expresion(tokens, i):
    i, error = termino(tokens, i)
    if error != '':
        return i, error
    while i < len(tokens) and tokens[i] in (OP_SUMA, OP_RESTA):
        i += 1
        i, error = termino(tokens, i)
        if error != '':
            return i, error
    return i, ''
def termino(tokens, i):
    i, error = factor(tokens, i)
    if error != '':
        return i, error
    while i < len(tokens) and tokens[i] in (OP_MUL, OP_DIV):
        i += 1
        i, error = factor(tokens, i)
        if error != '':
            return i, error
    return i, ''
def factor(tokens, i):
    if i >= len(tokens):
        return i, "Se esperaba un valor"
    if tokens[i] in (
        ENTERO,
        DECIMAL,
        CADENA,
        CHIQA,
        JANI,
        ID
    ):
        return i + 1, ''
    if tokens[i] == PAR_ABRE:
        i += 1
        i, error = comparacion(tokens, i)
        if error != '':
            return i, error
        if i >= len(tokens) or tokens[i] != PAR_CIERRA:
            return i, "Se esperaba ')'"
        i += 1
        return i, ''
    return i, "Se esperaba un valor"
vector = [
    7, 6, 28, 6, 30, 6, 29,
    9, 6, 27, 1,
     28, 6, 25, 1, 29,
    10, 3,
    14,
    11, 6,
    8
]

print(start(vector))
'''lurayaña suma(a,b)
    wakichaña x = 10

    jisa (x >= 5)
        uñtayaña "hola"
    tukuya_jisa

    kutichaña x
tukuyaña'''