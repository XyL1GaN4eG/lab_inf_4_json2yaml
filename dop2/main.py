# Импорт модуля sys для работы с системными параметрами и путями
import sys

# Добавление ".." в sys.path, чтобы импортировать модуль из родительского каталога
sys.path.append("..")

# Импорт модулей os, Yaml и json из соответствующих пакетов
import os
from dop2.myyaml import Yaml as yaml
import dop2.myjson as json

# Определение функции parse, которая принимает строку JSON, парсит ее и затем преобразует в формат YAML
def parse(string):
    return yaml.dump(json.loads(string))

# Если код выполняется как самостоятельный скрипт (а не импортируется как модуль), то выполнить следующие действия
if __name__ == "__main__":
    # Определение путей к файлам ввода и вывода
    input_file = os.path.join(os.path.dirname(__file__), "../data/in.json")
    output_file = os.path.join(os.path.dirname(__file__), "../data/out-dop2.yaml")

    # Чтение содержимого файла ввода
    string = open(input_file, "r").read()

    # Применение функции parse к строке JSON и запись результата в файл вывода
    open(output_file, "w").write(parse(string))

    # Вывод сообщения об успешном завершении
    print("dop2.main complete!")
