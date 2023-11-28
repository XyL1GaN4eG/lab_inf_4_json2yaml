# Импорт модуля sys
import sys

# Добавление пути ".." в sys.path, чтобы иметь доступ к модулю myyaml
sys.path.append("..")

# Импорт модулей os, Yaml (как yaml), и myjson (как json) из задачи 0
import os
from task0.myyaml import Yaml as yaml
import task0.myjson as json

# Функция parse принимает строку JSON, преобразует ее в объект Python, а затем в строку YAML
def parse(string):
    return yaml.dump(json.loads(string))

# Если скрипт запущен как основной (а не импортирован как модуль)
if __name__ == "__main__":
    # Формирование путей к входному и выходному файлам
    input_file = os.path.join(os.path.dirname(__file__), "../data/in2.json")
    output_file = os.path.join(os.path.dirname(__file__), "../data/out.yaml")

    # Чтение содержимого входного файла
    string = open(input_file, "r").read()

    # Запись результата парсинга в выходной файл
    open(output_file, "w").write(parse(string))

    # Вывод сообщения о завершении работы скрипта
    print("task0.main complete!")
