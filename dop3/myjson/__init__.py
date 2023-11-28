import re

# Определение символов JSON и других констант
JSON_COMMA = ','
JSON_COLON = ':'
JSON_LEFTBRACKET = '['
JSON_RIGHTBRACKET = ']'
JSON_LEFTBRACE = '{'
JSON_RIGHTBRACE = '}'
JSON_QUOTE = '"'
QUOTE = '"'

# Пробельные символы
WHITESPACE = [' ', '\t', '\b', '\n', '\r']

# Список всех символов JSON
SYNTAX = [JSON_COMMA, JSON_COLON, JSON_LEFTBRACKET, JSON_RIGHTBRACKET,
          JSON_LEFTBRACE, JSON_RIGHTBRACE]

# Длины ключевых слов JSON
FALSE_LEN = len('false')
TRUE_LEN = len('true')
NULL_LEN = len('null')

# Грамматика JSON
# Здесь используется формальная грамматика, представленная в виде комментариев,
# для определения структуры JSON. Это улучшает читаемость и понимание кода.

# Грамматика строки JSON:
# string -> QUOTE (any printable char except QUOTE or BACKSLASH or control char)* QUOTE

# Грамматика числа JSON:
# number -> int frac exp
# int -> digit / digit1-9 digit
# frac -> '' / '.' digit
# exp -> '' / 'e' sign digit
# sign -> '' / '+' / '-'
# digit1-9 -> '1'-'9'
# digit -> '0'-'9'

# Грамматика JSON:
# json -> element
# element -> object / array / string / number / 'true' / 'false' / 'null'

# Лексический анализ: извлечение строк из JSON
def lex_string(string):
    # Используем формальную грамматику для извлечения строки JSON
    match = re.match(r'"{1}([^"\\]|\\.)*"{1}', string)
    if match:
        return match.group(), string[match.end():]
    return None, string

# Лексический анализ: извлечение чисел из JSON
def lex_number(string):
    # Используем формальную грамматику для извлечения числа JSON
    match = re.match(r'-?(0|[1-9]\d*)(\.\d+)?([eE][-+]?\d+)?', string)
    if match:
        return match.group(), string[match.end():]
    return None, string

# Лексический анализ: извлечение ключевого слова 'null' из JSON
def lex_null(string):
    # Используем формальную грамматику для извлечения ключевого слова 'null'
    if string.startswith('null'):
        return 'null', string[NULL_LEN:]
    return None, string

# Лексический анализ: извлечение ключевых слов 'true' или 'false' из JSON
def lex_bool(string):
    # Используем формальную грамматику для извлечения ключевых слов 'true' или 'false'
    if string.startswith('true'):
        return True, string[TRUE_LEN:]
    elif string.startswith('false'):
        return False, string[FALSE_LEN:]
    return None, string

# Лексический анализ: разбор всего JSON
def lex(string):
    tokens = []

    # Парсинг строки на токены
    while len(string):
        json_string, string = lex_string(string)
        if json_string is not None:
            tokens.append(json_string)
            continue

        json_number, string = lex_number(string)
        if json_number is not None:
            tokens.append(json_number)
            continue

        json_bool, string = lex_bool(string)
        if json_bool is not None:
            tokens.append(json_bool)
            continue

        json_null, string = lex_null(string)
        if json_null is not None:
            tokens.append(None)
            continue

        # Удаление пробельных символов
        if string[0] in WHITESPACE:
            string = string[1:]
        # Добавление синтаксических символов в токены
        elif string[0] in SYNTAX:
            tokens.append(string[0])
            string = string[1:]
        else:
            raise Exception("Unknown character: {}".format(string[0]))

    return tokens

# Разбор массива JSON
def parse_array(tokens):
    json_array = []

    t = tokens[0]
    # Проверка наличия закрывающей квадратной скобки
    if t == JSON_RIGHTBRACKET:
        return json_array, tokens[1:]

    # Рекурсивный разбор элементов массива
    while True:
        json, tokens = parse(tokens)
        json_array.append(json)

        t = tokens[0]
        # Проверка наличия закрывающей квадратной скобки или запятой (разделителя элементов)
        if t == JSON_RIGHTBRACKET:
            return json_array, tokens[1:]
        elif t != JSON_COMMA:
            raise Exception('Expected comma after object in array')
        else:
            tokens = tokens[1:]

# Разбор объекта JSON
def parse_object(tokens):
    json_object = {}
    t = tokens[0]

    # Проверка наличия закрывающей фигурной скобки
    if t == JSON_RIGHTBRACE:
        return json_object, tokens[1:]

    # Рекурсивный разбор пар ключ-значение объекта
    while True:
        json_key = tokens[0]

        # Проверка, что ключ является строкой
        if type(json_key) is str:
            tokens = tokens[1:]
        else:
            raise Exception('Expected key of type string')

        # Проверка наличия двоеточия (разделителя пары ключ-значение)
        if tokens[0] != JSON_COLON:
            raise Exception('Expected colol ( : ) in object type dict')
        else:
            tokens = tokens[1:]

        # Рекурсивный разбор значения объекта
        json_value, tokens = parse(tokens)
        json_object[json_key] = json_value

        t = tokens[0]
        # Проверка наличия закрывающей фигурной скобки или запятой (разделителя пар)
        if t == JSON_RIGHTBRACE:
            return json_object, tokens[1:]
        elif t != JSON_COMMA:
            raise Exception('Expected comma after pair in object, got: {}'.format(t))
        tokens = tokens[1:]

# Разбор JSON
def parse(tokens):
    t = tokens[0]
    # Проверка наличия открывающей квадратной скобки (начало массива)
    if t == JSON_LEFTBRACKET:
        return parse_array(tokens[1:])
    # Проверка наличия открывающей фигурной скобки (начало объекта)
    elif t == JSON_LEFTBRACE:
        return parse_object(tokens[1:])
    # Если токен не открывающая скобка, возвращается токен и оставшиеся токены
    else:
        return t, tokens[1:]

# Обертка для функции parse с добавлением лексического анализа
def loads(string):
    return parse(lex(string))[0]
