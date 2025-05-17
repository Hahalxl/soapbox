from library.function.functions import _config
class Person:
    def __init__(self, name:str, osis:str, email:str, organization:str="John Dewey High School", fill:str="="):
        self.name = name
        self.osis = osis
        self.email = email
        self.organization = organization
        self.fill = fill

    def __str__(self) -> str:
        size = list(map(len, [self.name, self.osis, self.email,self.organization]))
        name_size = [4, 4, 5, 12]
        longest = max(size)
        spacing = (longest + len("Organization:")) #I JUST GOT LAZY HERE, PLEASE DON'T JUDGE. I KNOW THE RESULT IS 12!!!!
        filler = self.fill * (spacing + name_size[2])
        return f"{filler}\n||Name:{self.name + " "*(spacing - (len(self.name) + name_size[0]))}||\n||Osis:{self.osis + " "*(spacing - (len(self.osis) + name_size[1]))}||\n||Email:{self.email + " "*(spacing - (len(self.email) + name_size[2]))}||\n||Organization:{self.organization + " "*(spacing - (len(self.organization) + name_size[3]))}||\n{filler}\n\n"


    def save(self) -> bool:
        config = _config()
        infos = f"{self.name},{self.osis},{self.email},{self.organization}\n"
        try:
            with open(f"{config["dir"] + config["name"]}", 'a') as file:
                file.write(infos)
                file.close()
        except Exception as E:
            print(f"Falied to save to {config["dir"] + config["name"]}\nReason{E}")
            return False
        print(f"Successfully saved to {config["dir"] + config["name"]}")
        return True


    def check(self)->bool:
        # Incase they Repeat
        import pandas as pd
        config = _config()
        config["filename"] = f"{config["dir"] + config["name"]}"
        df = pd.read_csv(config["filename"])
        df["osis"] = df["osis"].astype(str)
        person = df.loc[(df["name"] == self.name) & (df["osis"] == (self.osis)), :]
        return not person.empty
    
    def asjson(self)->dict:
        return {
            "name":self.name,
            "osis":self.osis,
            "email":self.email,
            "organization":self.organization
        }

    def __eq__(self, other:Person):
        return all([self.name == other.name, self.osis == other.osis, self.email == other.email, self.organization == other.organization])

class Admin:
    def __init__(self, name:str, password:str):
        self.name = name
        self.password = password


if (__name__ == "__main__"):
    import os
    #THIS HAS TO CHANGE
    os.chdir("C:\\Users\\Ronan\\Coding\\Python\\Flask\\531")
    alex = Person("Alex the sigma 2nd","69524234233132321","Alexliu@gmail.com","Alex Liu High School what the sigma bnrasdasd")
    print(alex)
    print(alex.check())
