from logging import lastResort

import pandas as pd
import os

from library.function.functions import _config
class Person:
    def __init__(self, last:str, first:str, email:str, phone:str, school:str, osis:str, dob:str, role:str):
        self.last = last
        self.first = first
        self.email = email
        self.phone = phone
        self.school = school
        self.osis = osis
        self.dob = dob
        self.role = role

    def exists(self) -> bool:
        config = _config()
        df = pd.read_csv(config["dir"]+config["name"])
        df["osis"] = df["osis"].astype(str)
        return not df.loc[((df["osis"] == self.osis)), :].empty

    def save(self) ->bool:
        config = _config()
        if not os.path.exists(config["dir"]+config["name"]):
            with open(config["dir"]+config["name"], "w") as file:
                file.write("last,first,email,phone,school,osis,dob,role\n")
                file.close()

        if self.exists():
            return False

        with open(config["dir"]+config["name"], "a") as file:
            file.write(f"{self.last},{self.first},{self.email},{self.phone},{self.school},{self.osis},{self.dob},{self.role}\n")
            file.close()

if (__name__ == "__main__"):
    import os
    os.chdir(r"C:\Users\Ronan\OneDrive\Desktop\Coding project\soapbox")
    e = Person("Liu", "Alex", "alexliu@gmail", "929-269-3123", "Han Solo High School", "213213221312", "2/12/2011", "Watcher")
    e.save()
