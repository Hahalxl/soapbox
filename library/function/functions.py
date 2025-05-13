

def newfile() -> bool:
    import json
    with open("../config.json") as configed:
        config = json.load(configed)["filing"]
        configed.close()
    with open(f"{config["dir"] + config["name"]}", 'x') as file:
        file.close()

    print("file created at " + config["dir"] + "\nNamed: " + config["name"])