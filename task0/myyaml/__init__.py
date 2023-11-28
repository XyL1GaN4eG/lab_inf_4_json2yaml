from enum import Enum, auto

# Enum для представления типов данных YAML
class Type(Enum):
    NULL = auto()
    BOOL = auto()
    INT = auto()
    FLOAT = auto()
    STR = auto()
    ARR = auto()
    OBJ = auto()

    # Метод класса, который принимает значение и возвращает соответствующий тип данных YAML
    def to_type(value):
        if isinstance(value, bool):       return Type.BOOL
        elif isinstance(value, int):      return Type.INT
        elif isinstance(value, float):    return Type.FLOAT
        elif isinstance(value, str):      return Type.STR
        elif isinstance(value, type([])): return Type.ARR
        elif isinstance(value, type({})): return Type.OBJ
        return Type.NULL


# Класс для представления объектов YAML
class Yaml:
    # Статический метод, принимающий объект и возвращающий строку YAML
    def dump(obj):
        return "---\n" + Yaml.create(obj).to_string()

    # Конструктор класса, инициализирующий объект
    def __init__(self, data_type, data):
        self._data, self._data_type = data, data_type

    # Статический метод, создающий объект Yaml из переданного объекта
    def create(obj):
        data_type = Type.to_type(obj)
        data = obj
        if data_type == Type.ARR:
            data = [Yaml.create(val) for val in obj]
        elif data_type == Type.OBJ:
            data = dict((key, Yaml.create(val))
                        for (key, val) in obj.items())
        return Yaml(data_type, data)

    # Метод для преобразования объекта в строку YAML
    def to_string(self, tabs=0, prefix=''):
        def pre(tabs):
            return "  " * tabs

        # Пустые массивы и объекты
        if ((self._data_type == Type.ARR or self._data_type == Type.OBJ) and len(self._data) == 0):
            return "[]" if self._data_type == Type.ARR else "{}"
        # Обработка массива
        elif self._data_type == Type.ARR:
            return '' if tabs == 0 else '\n' + '\n'.join(
                ["{}- {}".format(pre(tabs - 1),
                                 val.to_string(tabs))
                 for val in self._data]) + '\n'
        # Обработка объекта
        elif self._data_type == Type.OBJ:
            return '\n{}'.format(pre(tabs)).join(
                ["{}:\n{}{}".format(key, pre(tabs + 1), val.to_string(tabs + 1, prefix=' ')) if (val._data_type == Type.OBJ) else "{}:{}".format(key, val.to_string(tabs + 1, prefix=' '))
                    for (key, val) in self._data.items()])
        # Обработка значения null
        elif self._data_type == Type.NULL:
            return prefix + "null"
        # Обработка строк
        elif self._data_type == Type.STR:
            # Если строка содержит переводы строк
            if len(self._data.split('\n')) > 1:
                return " |\n" + '\n'.join(pre(tabs + 1) + val
                                          for val in self._data.split('\n'))
            else:
                return prefix + self._data
        # Обработка прочих типов данных (bool, int, float)
        else:
            return prefix + str(self._data)
