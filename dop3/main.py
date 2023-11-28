import sys
sys.path.append("..")

import os
from myyaml import Yaml
import myjson as json

def parse(string):
    return Yaml.dump(json.loads(string))

if __name__ == "__main__":
    input_file = os.path.join(os.path.dirname(__file__), "../data/in2.json")
    output_file = os.path.join(os.path.dirname(__file__), "../data/out-dop3.yaml")

    string = open(input_file, "r").read()

    open(output_file, "w").write(parse(string))

    print("dop3.main complete!")
