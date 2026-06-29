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
    return NOMBRE_TOKEN.get(codigo_tok, f"token desconocido ({codigo_tok})")


def describir_token(token):
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
    return ('a' <= c <= 'z') or ('A' <= c <= 'Z') or c in "ñÑüÜ"


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
                    raise Exception(f"Error léxico en línea {linea}, columna {col_inicio}: cadena sin cerrar")
                lexema += codigo[i]
                i += 1
                columna += 1

            if i >= len(codigo):
                raise Exception(f"Error léxico en línea {linea}, columna {col_inicio}: cadena sin cerrar")

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
                while i < len(codigo) and (es_letra(codigo[i]) or es_digito(codigo[i]) or codigo[i] == '_'):
                    lexema += codigo[i]
                    i += 1
                    columna += 1
                raise Exception(f"Error léxico en línea {linea}, columna {col_inicio}: identificador inválido '{lexema}'. No puede comenzar con un número.")

            if i < len(codigo) and codigo[i] == '.':
                lexema += '.'
                i += 1
                columna += 1

                if i >= len(codigo) or not es_digito(codigo[i]):
                    raise Exception(f"Error léxico en línea {linea}, columna {col_inicio}: decimal inválido '{lexema}'")

                while i < len(codigo) and es_digito(codigo[i]):
                    lexema += codigo[i]
                    i += 1
                    columna += 1

                if i < len(codigo) and codigo[i] == '.':
                    raise Exception(f"Error léxico en línea {linea}, columna {col_inicio}: número mal formado '{lexema}.'")

                tokens.append((TOKEN_DECIMAL, lexema, linea, col_inicio))
            else:
                tokens.append((TOKEN_ENTERO, lexema, linea, col_inicio))

            continue

        if es_letra(c):
            col_inicio = columna
            lexema = ""

            while i < len(codigo) and (es_letra(codigo[i]) or es_digito(codigo[i]) or codigo[i] == '_'):
                lexema += codigo[i]
                i += 1
                columna += 1

            if lexema in PALABRAS_RESERVADAS:
                tokens.append((PALABRAS_RESERVADAS[lexema], lexema, linea, col_inicio))
            else:
                tokens.append((TOKEN_ID, lexema, linea, col_inicio))

            continue

        if i + 1 < len(codigo):
            doble = codigo[i:i + 2]
            if doble in ["==", "!=", ">=", "<="]:
                tokens.append((SIMBOLOS[doble], doble, linea, columna))
                i += 2
                columna += 2
                continue

        if c in SIMBOLOS:
            tokens.append((SIMBOLOS[c], c, linea, columna))
            i += 1
            columna += 1
            continue

        raise Exception(f"Error léxico en línea {linea}, columna {columna}: símbolo no reconocido '{c}'")

    return tokens


class NodoPrograma:
    def __init__(self, funciones):
        self.funciones = funciones


class NodoFuncion:
    def __init__(self, nombre, params, cuerpo, linea, columna):
        self.nombre = nombre
        self.params = params
        self.cuerpo = cuerpo
        self.linea = linea
        self.columna = columna


class NodoDeclaracion:
    def __init__(self, nombre, expresion, linea, columna):
        self.nombre = nombre
        self.expresion = expresion
        self.linea = linea
        self.columna = columna


class NodoImpresion:
    def __init__(self, expresion, linea, columna):
        self.expresion = expresion
        self.linea = linea
        self.columna = columna


class NodoRetorno:
    def __init__(self, expresion, linea, columna):
        self.expresion = expresion
        self.linea = linea
        self.columna = columna


class NodoSi:
    def __init__(self, condicion, cuerpo_si, cuerpo_sino, linea, columna):
        self.condicion = condicion
        self.cuerpo_si = cuerpo_si
        self.cuerpo_sino = cuerpo_sino
        self.linea = linea
        self.columna = columna


class NodoMientras:
    def __init__(self, condicion, cuerpo, linea, columna):
        self.condicion = condicion
        self.cuerpo = cuerpo
        self.linea = linea
        self.columna = columna


class NodoBinaria:
    def __init__(self, operador, izquierda, derecha, linea, columna):
        self.operador = operador
        self.izquierda = izquierda
        self.derecha = derecha
        self.linea = linea
        self.columna = columna


class NodoNumero:
    def __init__(self, valor, tipo, linea, columna):
        self.valor = valor
        self.tipo = tipo
        self.linea = linea
        self.columna = columna


class NodoCadena:
    def __init__(self, valor, linea, columna):
        self.valor = valor
        self.linea = linea
        self.columna = columna


class NodoBooleano:
    def __init__(self, valor, linea, columna):
        self.valor = valor
        self.linea = linea
        self.columna = columna


class NodoIdentificador:
    def __init__(self, nombre, linea, columna):
        self.nombre = nombre
        self.linea = linea
        self.columna = columna


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
            raise Exception(f"Error sintáctico: se esperaba {nombre_token(token_esperado)} y se encontró el fin del archivo")
        if token[0] != token_esperado:
            raise Exception(f"Error sintáctico en línea {token[2]}, columna {token[3]}: se esperaba {nombre_token(token_esperado)} y se encontró {describir_token(token)}")
        self.pos += 1

    def programa(self):
        if self.actual() is None:
            raise Exception("Error sintáctico: el programa está vacío")
        funciones = []
        while self.actual() is not None:
            funciones.append(self.funcion())
        return NodoPrograma(funciones)

    def funcion(self):
        self.consumir(LURAYANA)
        tok_nombre = self.actual()
        self.consumir(TOKEN_ID)
        self.consumir(PAR_IZQ)
        parametros = self.params()
        self.consumir(PAR_DER)
        cuerpo = self.cuerpo()
        self.consumir(TUKUYANA)
        return NodoFuncion(tok_nombre[1], parametros, cuerpo, tok_nombre[2], tok_nombre[3])

    def params(self):
        parametros = []
        if self.actual() and self.actual()[0] == TOKEN_ID:
            parametros.append(self.actual()[1])
            self.consumir(TOKEN_ID)
            while self.actual() and self.actual()[0] == COMA:
                self.consumir(COMA)
                parametros.append(self.actual()[1])
                self.consumir(TOKEN_ID)
        return parametros

    def cuerpo(self):
        sentencias = []
        while self.actual() and self.actual()[0] in [WAKICHANA, UNTAYANA, KUTICHANA, JISA, KUTIÑA]:
            sentencias.append(self.sentencia())
        return sentencias

    def sentencia(self):
        token = self.actual()[0]
        if token == WAKICHANA:
            return self.declaracion()
        elif token == UNTAYANA:
            return self.impresion()
        elif token == KUTICHANA:
            return self.retorno()
        elif token == JISA:
            return self.si()
        elif token == KUTIÑA:
            return self.ciclo()
        else:
            actual = self.actual()
            raise Exception(f"Error sintáctico en línea {actual[2]}, columna {actual[3]}: se encontró {describir_token(actual)} donde se esperaba el inicio de una sentencia válida (declaración, impresión, retorno, condicional o ciclo)")

    def declaracion(self):
        self.consumir(WAKICHANA)
        tok_id = self.actual()
        self.consumir(TOKEN_ID)
        self.consumir(IGUAL)
        nodo_exp = self.expresion()
        return NodoDeclaracion(tok_id[1], nodo_exp, tok_id[2], tok_id[3])

    def impresion(self):
        tok = self.actual()
        self.consumir(UNTAYANA)
        nodo_exp = self.expresion()
        return NodoImpresion(nodo_exp, tok[2], tok[3])

    def retorno(self):
        tok = self.actual()
        self.consumir(KUTICHANA)
        nodo_exp = self.expresion()
        return NodoRetorno(nodo_exp, tok[2], tok[3])

    def si(self):
        tok = self.actual()
        self.consumir(JISA)
        self.consumir(PAR_IZQ)
        nodo_cond = self.condicion()
        self.consumir(PAR_DER)
        cuerpo_si = self.cuerpo()
        cuerpo_sino = []
        if self.actual() and self.actual()[0] == JANIWA:
            self.consumir(JANIWA)
            cuerpo_sino = self.cuerpo()
        self.consumir(TUKUYA_JISA)
        return NodoSi(nodo_cond, cuerpo_si, cuerpo_sino, tok[2], tok[3])

    def ciclo(self):
        tok = self.actual()
        self.consumir(KUTIÑA)
        self.consumir(PAR_IZQ)
        nodo_cond = self.condicion()
        self.consumir(PAR_DER)
        cuerpo = self.cuerpo()
        self.consumir(TUKUYA_KUTIÑA)
        return NodoMientras(nodo_cond, cuerpo, tok[2], tok[3])

    def condicion(self):
        izquierda = self.expresion()
        token = self.actual()
        if token is None:
            raise Exception("Error sintáctico: se esperaba un operador relacional (>, <, ==, !=, >=, <=) y se encontró el fin del archivo")
        if token[0] not in [MAYOR, MENOR, IGUAL_IGUAL, DIFERENTE, MAYOR_IGUAL, MENOR_IGUAL]:
            raise Exception(f"Error sintáctico en línea {token[2]}, columna {token[3]}: se esperaba un operador relacional (>, <, ==, !=, >=, <=) y se encontró {describir_token(token)}")
        self.pos += 1
        derecha = self.expresion()
        return NodoBinaria(token[1], izquierda, derecha, token[2], token[3])

    def expresion(self):
        nodo = self.termino()
        while self.actual() and self.actual()[0] in [SUMA, RESTA]:
            token_op = self.actual()
            self.pos += 1
            derecho = self.termino()
            nodo = NodoBinaria(token_op[1], nodo, derecho, token_op[2], token_op[3])
        return nodo

    def termino(self):
        nodo = self.factor()
        while self.actual() and self.actual()[0] in [MULT, DIV]:
            token_op = self.actual()
            self.pos += 1
            derecho = self.factor()
            nodo = NodoBinaria(token_op[1], nodo, derecho, token_op[2], token_op[3])
        return nodo

    def factor(self):
        token = self.actual()
        if token is None:
            raise Exception("Error sintáctico: la expresión está incompleta, se encontró el fin del archivo")
        if token[0] == TOKEN_ENTERO:
            self.pos += 1
            return NodoNumero(token[1], 'entero', token[2], token[3])
        if token[0] == TOKEN_DECIMAL:
            self.pos += 1
            return NodoNumero(token[1], 'decimal', token[2], token[3])
        if token[0] == TOKEN_ID:
            self.pos += 1
            return NodoIdentificador(token[1], token[2], token[3])
        elif token[0] == COMILLA:
            self.consumir(COMILLA)
            tok_cadena = self.actual()
            self.consumir(TOKEN_CADENA)
            self.consumir(COMILLA)
            return NodoCadena(tok_cadena[1], tok_cadena[2], tok_cadena[3])
        elif token[0] == PAR_IZQ:
            self.consumir(PAR_IZQ)
            nodo = self.expresion()
            self.consumir(PAR_DER)
            return nodo
        elif token[0] in [CHIQA, JANI]:
            self.pos += 1
            return NodoBooleano(token[0] == CHIQA, token[2], token[3])
        else:
            raise Exception(f"Error sintáctico en línea {token[2]}, columna {token[3]}: se esperaba un valor (número, identificador, cadena, '(' o chiqa/jani) y se encontró {describir_token(token)}")


class ErrorSemantico(Exception):
    pass


class AnalizadorSemantico:

    OPERADORES_RELACIONALES = {'>', '<', '==', '!=', '>=', '<='}
    OPERADORES_ARITMETICOS = {'+', '-', '*', '/'}

    def __init__(self):
        self.funciones = {}
        self.errores = []
        self.advertencias = []
        self.usadas = set()

    def analizar(self, nodo_programa):
        for f in nodo_programa.funciones:
            if f.nombre in self.funciones:
                self.errores.append(f"Error semántico: la función '{f.nombre}' ya fue definida anteriormente.")
            else:
                self.funciones[f.nombre] = f.params

        for f in nodo_programa.funciones:
            self.analizar_funcion(f)

        if self.errores:
            raise ErrorSemantico("\n".join(self.errores))

        return True

    def analizar_funcion(self, nodo_funcion):
        tabla = {p: 'indefinido' for p in nodo_funcion.params}
        self.usadas = set()
        for s in nodo_funcion.cuerpo:
            self.analizar_sentencia(s, tabla, nodo_funcion.nombre)
        for nombre in tabla:
            if nombre not in self.usadas:
                self.advertencias.append(f"Advertencia: la variable '{nombre}' se declara en la función '{nodo_funcion.nombre}' pero nunca se usa.")

    def analizar_sentencia(self, nodo, tabla, nombre_funcion):
        if isinstance(nodo, NodoDeclaracion):
            tipo = self.tipo_expresion(nodo.expresion, tabla, nombre_funcion)
            tabla[nodo.nombre] = tipo
        elif isinstance(nodo, NodoImpresion):
            self.tipo_expresion(nodo.expresion, tabla, nombre_funcion)
        elif isinstance(nodo, NodoRetorno):
            self.tipo_expresion(nodo.expresion, tabla, nombre_funcion)
        elif isinstance(nodo, NodoSi):
            self.tipo_expresion(nodo.condicion, tabla, nombre_funcion)
            for s in nodo.cuerpo_si:
                self.analizar_sentencia(s, tabla, nombre_funcion)
            for s in nodo.cuerpo_sino:
                self.analizar_sentencia(s, tabla, nombre_funcion)
        elif isinstance(nodo, NodoMientras):
            self.tipo_expresion(nodo.condicion, tabla, nombre_funcion)
            for s in nodo.cuerpo:
                self.analizar_sentencia(s, tabla, nombre_funcion)

    def tipo_expresion(self, nodo, tabla, nombre_funcion):
        if isinstance(nodo, NodoNumero):
            return nodo.tipo
        if isinstance(nodo, NodoCadena):
            return 'cadena'
        if isinstance(nodo, NodoBooleano):
            return 'booleano'
        if isinstance(nodo, NodoIdentificador):
            if nodo.nombre not in tabla:
                self.errores.append(f"Error semántico en línea {nodo.linea}, columna {nodo.columna} (función '{nombre_funcion}'): la variable '{nodo.nombre}' se usa sin haber sido declarada con 'wakichaña'.")
                return 'indefinido'
            self.usadas.add(nodo.nombre)
            return tabla[nodo.nombre]
        if isinstance(nodo, NodoBinaria):
            t_izq = self.tipo_expresion(nodo.izquierda, tabla, nombre_funcion)
            t_der = self.tipo_expresion(nodo.derecha, tabla, nombre_funcion)
            return self.tipo_operacion(nodo.operador, t_izq, t_der, nodo.linea, nodo.columna, nombre_funcion)
        raise Exception("Nodo de expresión no reconocido")

    def tipo_operacion(self, operador, t_izq, t_der, linea, columna, nombre_funcion):
        if t_izq == 'indefinido' or t_der == 'indefinido':
            return 'indefinido'
        if operador in self.OPERADORES_RELACIONALES:
            tipos_numericos = {'entero', 'decimal'}
            if t_izq in tipos_numericos and t_der in tipos_numericos:
                return 'booleano'
            if t_izq == t_der:
                return 'booleano'
            self.errores.append(f"Error semántico en línea {linea}, columna {columna} (función '{nombre_funcion}'): no se puede comparar un valor de tipo '{t_izq}' con uno de tipo '{t_der}' usando '{operador}'.")
            return 'indefinido'
        if operador in self.OPERADORES_ARITMETICOS:
            if t_izq == 'booleano' or t_der == 'booleano':
                self.errores.append(f"Error semántico en línea {linea}, columna {columna} (función '{nombre_funcion}'): los valores booleanos ('chiqa'/'jani') no pueden usarse en operaciones aritméticas ('{operador}').")
                return 'indefinido'
            if t_izq == 'cadena' or t_der == 'cadena':
                if operador == '+' and t_izq == 'cadena' and t_der == 'cadena':
                    return 'cadena'
                self.errores.append(f"Error semántico en línea {linea}, columna {columna} (función '{nombre_funcion}'): la operación '{operador}' no es válida entre tipo '{t_izq}' y tipo '{t_der}'. Las cadenas solo admiten concatenación con '+'.")
                return 'indefinido'
            if t_izq == 'decimal' or t_der == 'decimal':
                return 'decimal'
            return 'entero'
        raise Exception(f"Operador no reconocido: {operador}")


def a_infijo(nodo):
    if isinstance(nodo, NodoNumero):
        return nodo.valor
    if isinstance(nodo, NodoCadena):
        return f'"{nodo.valor}"'
    if isinstance(nodo, NodoBooleano):
        return 'chiqa' if nodo.valor else 'jani'
    if isinstance(nodo, NodoIdentificador):
        return nodo.nombre
    if isinstance(nodo, NodoBinaria):
        return f"({a_infijo(nodo.izquierda)} {nodo.operador} {a_infijo(nodo.derecha)})"
    raise Exception("Nodo de expresión no soportado en a_infijo")


def a_postfijo(nodo):
    if isinstance(nodo, NodoNumero):
        return [nodo.valor]
    if isinstance(nodo, NodoCadena):
        return [f'"{nodo.valor}"']
    if isinstance(nodo, NodoBooleano):
        return ['chiqa' if nodo.valor else 'jani']
    if isinstance(nodo, NodoIdentificador):
        return [nodo.nombre]
    if isinstance(nodo, NodoBinaria):
        return a_postfijo(nodo.izquierda) + a_postfijo(nodo.derecha) + [nodo.operador]
    raise Exception("Nodo de expresión no soportado en a_postfijo")


def recolectar_expresiones(funciones):
    resultados = []

    def visitar(sentencias):
        for s in sentencias:
            if isinstance(s, NodoDeclaracion):
                resultados.append((f"wakichaña {s.nombre} = ...", s.expresion))
            elif isinstance(s, NodoImpresion):
                resultados.append(("uñtayaña ...", s.expresion))
            elif isinstance(s, NodoRetorno):
                resultados.append(("kutichaña ...", s.expresion))
            elif isinstance(s, NodoSi):
                resultados.append(("condición de jisa(...)", s.condicion))
                visitar(s.cuerpo_si)
                visitar(s.cuerpo_sino)
            elif isinstance(s, NodoMientras):
                resultados.append(("condición de kutiña(...)", s.condicion))
                visitar(s.cuerpo)

    for f in funciones:
        visitar(f.cuerpo)

    return resultados


class GeneradorCuartetos:

    def __init__(self):
        self.cuartetos = []
        self.cont_temp = 0
        self.cont_etq = 0

    def nuevo_temp(self):
        self.cont_temp += 1
        return f"T{self.cont_temp}"

    def nueva_etiqueta(self):
        self.cont_etq += 1
        return f"E{self.cont_etq}"

    def emitir(self, op, a1, a2, res):
        self.cuartetos.append((op, a1, a2, res))

    def generar_expresion(self, nodo):
        if isinstance(nodo, NodoNumero):
            return nodo.valor
        if isinstance(nodo, NodoCadena):
            return f'"{nodo.valor}"'
        if isinstance(nodo, NodoBooleano):
            return 'chiqa' if nodo.valor else 'jani'
        if isinstance(nodo, NodoIdentificador):
            return nodo.nombre
        if isinstance(nodo, NodoBinaria):
            izq = self.generar_expresion(nodo.izquierda)
            der = self.generar_expresion(nodo.derecha)
            temp = self.nuevo_temp()
            self.emitir(nodo.operador, izq, der, temp)
            return temp
        raise Exception("Nodo de expresión no soportado en cuartetos")

    def generar_sentencia(self, nodo):
        if isinstance(nodo, NodoDeclaracion):
            valor = self.generar_expresion(nodo.expresion)
            self.emitir('=', valor, '_', nodo.nombre)
        elif isinstance(nodo, NodoImpresion):
            valor = self.generar_expresion(nodo.expresion)
            self.emitir('uñtayaña', valor, '_', '_')
        elif isinstance(nodo, NodoRetorno):
            valor = self.generar_expresion(nodo.expresion)
            self.emitir('kutichaña', valor, '_', '_')
        elif isinstance(nodo, NodoSi):
            cond = self.generar_expresion(nodo.condicion)
            etq_falso = self.nueva_etiqueta()
            self.emitir('JFALSO', cond, '_', etq_falso)
            for s in nodo.cuerpo_si:
                self.generar_sentencia(s)
            if nodo.cuerpo_sino:
                etq_fin = self.nueva_etiqueta()
                self.emitir('JMP', '_', '_', etq_fin)
                self.emitir('ETQ', etq_falso, '_', '_')
                for s in nodo.cuerpo_sino:
                    self.generar_sentencia(s)
                self.emitir('ETQ', etq_fin, '_', '_')
            else:
                self.emitir('ETQ', etq_falso, '_', '_')
        elif isinstance(nodo, NodoMientras):
            etq_inicio = self.nueva_etiqueta()
            etq_fin = self.nueva_etiqueta()
            self.emitir('ETQ', etq_inicio, '_', '_')
            cond = self.generar_expresion(nodo.condicion)
            self.emitir('JFALSO', cond, '_', etq_fin)
            for s in nodo.cuerpo:
                self.generar_sentencia(s)
            self.emitir('JMP', '_', '_', etq_inicio)
            self.emitir('ETQ', etq_fin, '_', '_')

    def generar_funcion(self, nodo_funcion):
        self.emitir('FUNC', nodo_funcion.nombre, '_', '_')
        for s in nodo_funcion.cuerpo:
            self.generar_sentencia(s)
        self.emitir('FIN_FUNC', nodo_funcion.nombre, '_', '_')

    def generar_programa(self, nodo_programa):
        for f in nodo_programa.funciones:
            self.generar_funcion(f)
        return self.cuartetos


if __name__ == "__main__":

    codigo = '''
lurayaña prueba()
    uñtayaña x
tukuyaña

'''

    try:
        tokens = analizador_lexico(codigo)
        print("TOKENS ENCONTRADOS:\n")
        for token in tokens:
            print(token)

        parser = Parser(tokens)
        ast = parser.programa()

        if parser.pos != len(tokens):
            token = tokens[parser.pos]
            raise Exception(f"Error sintáctico en línea {token[2]}, columna {token[3]}: se encontró {describir_token(token)} de forma inesperada; se esperaba el inicio de una nueva función ('lurayaña') o el fin del archivo")

        print("\nANÁLISIS SINTÁCTICO CORRECTO")

        analizador_sem = AnalizadorSemantico()
        analizador_sem.analizar(ast)

        print("\nANÁLISIS SEMÁNTICO CORRECTO")

        if analizador_sem.advertencias:
            print("\nADVERTENCIAS:")
            for adv in analizador_sem.advertencias:
                print(f"  - {adv}")

        print("\nCONVERSIÓN INFIJO -> POSTFIJO\n")
        for descripcion, nodo_exp in recolectar_expresiones(ast.funciones):
            infijo = a_infijo(nodo_exp)
            postfijo = " ".join(a_postfijo(nodo_exp))
            print(f"{descripcion:30s} infijo: {infijo:18s} postfijo: {postfijo}")

        generador = GeneradorCuartetos()
        cuartetos = generador.generar_programa(ast)

        print("\nCUARTETOS (CÓDIGO INTERMEDIO)\n")
        print(f"{'N':<4}{'OP':<10}{'ARG1':<10}{'ARG2':<10}{'RESULTADO':<10}")
        for idx, (op, a1, a2, res) in enumerate(cuartetos, start=1):
            print(f"{idx:<4}{op:<10}{a1:<10}{a2:<10}{res:<10}")

    except ErrorSemantico as e:
        print("\nERRORES SEMÁNTICOS DETECTADOS:")
        print(e)

    except Exception as e:
        print("\nERROR DETECTADO:")
        print(e)