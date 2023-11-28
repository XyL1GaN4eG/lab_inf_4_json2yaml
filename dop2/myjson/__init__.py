# Импорт модуля re (регулярные выражения)
import re

# Определение символов JSON и их значений
JSON_COMMA = ','
JSON_COLON = ':'
JSON_LEFTBRACKET = '['
JSON_RIGHTBRACKET = ']'
JSON_LEFTBRACE = '{'
JSON_RIGHTBRACE = '}'
JSON_QUOTE = '"'
QUOTE = '"'

# Определение символов пробелов и других управляющих символов
WHITESPACE = [' ', '\t', '\b', '\n', '\r']

# Список всех синтаксических символов JSON
SYNTAX = [JSON_COMMA, JSON_COLON, JSON_LEFTBRACKET, JSON_RIGHTBRACKET,
          JSON_LEFTBRACE, JSON_RIGHTBRACE]

# Компиляция регулярных выражений для лексического анализа
number_regex = re.compile(r"(-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?)\s*(.*)", re.DOTALL)
string_regex = re.compile(r"(\"(?:[^\\']|\\['\\/bfnrt]|\\u[0-9a-fA-F]{4})*?\")\s*(.*)", re.DOTALL)
null_regex = re.compile(r"(null)\s*(.*)", re.DOTALL)
bool_regex = re.compile(r"(true|false)\s*(.*)", re.DOTALL)


# Функция lex_string: лексический анализ строки, выделяет JSON-строку
def lex_string(string):
    match = string_regex.match(string)
    if not match:
        return None, string

    json_string, _ = match.groups()
    return eval(json_string), string[len(json_string):]


# Функция lex_number: лексический анализ строки, выделяет JSON-число
def lex_number(string):
    match = number_regex.match(string)
    if not match:
        return None, string

    json_number, rest = match.groups()
    return eval(json_number), rest


# Функция lex_null: лексический анализ строки, выделяет значение null
def lex_null(string):
    match = null_regex.match(string)
    if match is not None:
        _, rest = match.groups()
        return 'null', rest
    else:
        return None, string


# Функция lex_bool: лексический анализ строки, выделяет булево значение (true/false)
def lex_bool(string):
    match = bool_regex.match(string)
    if match is not None:
        json_bool, rest = match.groups()
        return json_bool == 'true', rest
    else:
        return None, string


# Функция lex: лексический анализ строки, разбивает ее на токены
def lex(string):
    tokens = []

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

        # Пропуск пробелов и добавление синтаксических символов
        if string[0] in WHITESPACE:
            string = string[1:]
        elif string[0] in SYNTAX:
            tokens.append(string[0])
            string = string[1:]
        else:
            raise Exception("Unknown character: {}".format(string[0]))

    return tokens


# Функция parse_array: разбор массива JSON
def parse_array(tokens):
    json_array = []

    t = tokens[0]
    if t == JSON_RIGHTBRACKET:
        return json_array, tokens[1:]

    while True:
        json, tokens = parse(tokens)
        json_array.append(json)

        t = tokens[0]
        if t == JSON_RIGHTBRACKET:
            return json_array, tokens[1:]
        elif t != JSON_COMMA:
            raise Exception('Expected comma after object in array')
        else:
            tokens = tokens[1:]


# Функция parse_object: разбор объекта JSON
def parse_object(tokens):
    json_object = {}
    t = tokens[0]

    if t == JSON_RIGHTBRACE:
        return json_object, tokens[1:]

    while True:
        json_key = tokens[0]

        if type(json_key) is str:
            tokens = tokens[1:]
        else:
            raise Exception('Expected key of type string')

        if tokens[0] != JSON_COLON:
            raise Exception('Expected colon ( : ) in object type dict')
        else:
            tokens = tokens[1:]

        json_value, tokens = parse(tokens)
        json_object[json_key] = json_value

        t = tokens[0]
        if t == JSON_RIGHTBRACE:
            return json_object, tokens[1:]
        elif t != JSON_COMMA:
            raise Exception('Expected comma after pair in object, got: {}'.format(t))
        tokens = tokens[1:]


# Функция parse: общая функция разбора JSON
def parse(tokens):
    t = tokens[0]
    if t == JSON_LEFTBRACKET:
        return parse_array(tokens[1:])
    elif t == JSON_LEFTBRACE:
        return parse_object(tokens[1:])
    else:
        return t, tokens[1:]


# Функция loads: принимает строку JSON, выполняет лексический анализ и разбор, возвращает результат
def loads(string):
    return parse(lex(string))[0]
