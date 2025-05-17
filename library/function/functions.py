from os import getcwd

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
        with open(f"{config["dir"] + config["name"]}", 'x') as file:
            file.write("name,osis,email,organization\n")
            file.close()
    except FileExistsError:
        if(__name__ == "__main__"):
            with open(f"{config["dir"] + config["name"]}", 'w') as file:
                file.write("name,osis,email,organization\n")
                file.close()
            print("__main__ Bypassed!")
        else:
            return False


    print("file created at " + config["dir"] + "\nNamed: " + config["name"])
    return True


if(__name__ == "__main__"):
    import os
    os.chdir("C:\\Users\\Ronan\\Coding\\Python\\Flask\\531")
    newfile()