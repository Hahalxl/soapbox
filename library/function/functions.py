import random
from email.utils import collapse_rfc2231_value
from os import getcwd

import pandas as pd


def _config() -> dict:
    import json
    with open("config.json") as configed:
        config = json.load(configed)["filing"]
        configed.close()
    return config

def _config_admin() -> dict:
    import json
    with open("config.json") as configed:
        config = json.load(configed)["admin"]
        configed.close()
    return config

def newfile() -> bool:
    config = _config()
    try:
        with open(f"{config['dir'] + config['name']}", 'x') as file:
            file.write("name,osis,email,organization\n")
            file.close()
    except FileExistsError:
        if(__name__ == "__main__"):
            with open(f"{config['dir'] + config['name']}", 'w') as file:
                file.write("name,osis,email,organization\n")
                file.close()
            print("__main__ Bypassed!")
        else:
            return False


    print("file created at " + config["dir"] + "\nNamed: " + config["name"])
    return True

def colorhex(colors:list[int]) ->str:
    _re = "#"

    for i in colors:
        _re += hex(i)[2:] if len(hex(i)[2:]) > 1 else "0" + hex(i)[2:]

    return _re

def randcol()->str:
    return colorhex([random.randint(40, 150) for _ in range(3)])

def information() -> dict:
    import pandas
    config = _config()
    df = pd.read_csv(f"{config['dir'] + config['name']}")
    total = len(df)
    dewey = len(df.loc[(df.organization == "John Dewey High School"), :])
    other = len(df.loc[(df.organization != "John Dewey High School"), :])
    return {"total": total, "dewey":dewey,"other":other}

if(__name__ == "__main__"):
    import os
    os.chdir("../../")
    print(information())

