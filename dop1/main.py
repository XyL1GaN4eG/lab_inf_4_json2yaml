import os
import yaml
import json


# Функция parse принимает строку JSON, парсит ее с использованием библиотеки json,
# затем преобразует результат в строку YAML с использованием библиотеки yaml,
# с определенными параметрами форматирования.
def parse(string):
    return yaml.dump(json.loads(string), default_flow_style=False, allow_unicode=True, sort_keys=False)


if __name__ == "__main__":
    # Получаем пути к входному и выходному файлам
    input_file = os.path.join(os.path.dirname(__file__), "../data/in.json")
    output_file = os.path.join(os.path.dirname(__file__), "../data/out-dop1.yaml")

    # Читаем содержимое входного файла
    string = open(input_file, "r").read()

    # Применяем функцию parse к содержимому и записываем результат в выходной файл
    open(output_file, "w").write(parse(string))

    # Выводим сообщение о завершении работы скрипта
    print("dop1.main complete!")
