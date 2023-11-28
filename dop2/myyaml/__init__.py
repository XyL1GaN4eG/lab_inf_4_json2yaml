# Импорт модуля Enum и auto для создания перечисления Type
from enum import Enum, auto

# Определение перечисления Type с автоматическими значениями
class Type(Enum):
    NULL = auto()
    BOOL = auto()
    INT = auto()
    FLOAT = auto()
    STR = auto()
    ARR = auto()
    OBJ = auto()

    # Статический метод to_type, который возвращает тип данных для заданного значения
    @staticmethod
    def to_type(value):
        if isinstance(value, bool):       return Type.BOOL
        elif isinstance(value, int):      return Type.INT
        elif isinstance(value, float):    return Type.FLOAT
        elif isinstance(value, str):      return Type.STR
        elif isinstance(value, list):     return Type.ARR
        elif isinstance(value, dict):     return Type.OBJ
        return Type.NULL

# Класс Yaml для работы с YAML-представлением данных
class Yaml:
    # Статический метод dump: принимает объект, создает Yaml объект и возвращает его строковое представление
    @staticmethod
    def dump(obj):
        return "---\n" + Yaml.create(obj).to_string()

    # Конструктор класса Yaml, принимает тип данных и данные
    def __init__(self, data_type, data):
        self._data, self._data_type = data, data_type

    # Статический метод create: принимает объект и возвращает Yaml объект с соответствующим типом данных
    @staticmethod
    def create(obj):
        data_type = Type.to_type(obj)
        data = obj
        # Если тип данных - массив, рекурсивно создаем Yaml объекты для каждого элемента
        if data_type == Type.ARR:
            data = [Yaml.create(val) for val in obj]
        # Если тип данных - словарь, рекурсивно создаем Yaml объекты для каждого значения
        elif data_type == Type.OBJ:
            data = dict((key, Yaml.create(val)) for (key, val) in obj.items())
        return Yaml(data_type, data)

    # Метод to_string: преобразует Yaml объект в строку, используя отступы и префикс
    def to_string(self, tabs=0, prefix=''):
        # Вспомогательная функция pre: создает отступы на основе уровня вложенности
        def pre(tabs):
            return "  " * tabs

        # Обработка случая, когда данные - массив или объект и их длина равна 0
        if ((self._data_type == Type.ARR or self._data_type == Type.OBJ) and len(self._data) == 0):
            return "[]" if self._data_type == Type.ARR else "{}"
        # Обработка случая, когда данные - массив
        elif self._data_type == Type.ARR:
            return '' if tabs == 0 else '\n' + '\n'.join(
                ["{}- {}".format(pre(tabs - 1),
                                 val.to_string(tabs))
                 for val in self._data]) + '\n'
        # Обработка случая, когда данные - объект
        elif self._data_type == Type.OBJ:
            return '\n{}'.format(pre(tabs)).join(
                ["{}:\n{}{}".format(key, pre(tabs + 1), val.to_string(tabs + 1, prefix=' ')) if (val._data_type == Type.OBJ) else "{}:{}".format(key, val.to_string(tabs + 1, prefix=' '))
                    for (key, val) in self._data.items()])
        # Обработка случая, когда данные - null
        elif self._data_type == Type.NULL:
            return prefix + "null"
        # Обработка случая, когда данные - строка
        elif self._data_type == Type.STR:
            if len(self._data.split('\n')) > 1:
                return " |\n" + '\n'.join(pre(tabs + 1) + val
                                          for val in self._data.split('\n'))
            else:
                return prefix + self._data
        # Обработка остальных случаев (число, булево значение)
        else:
            return prefix + str(self._data)
