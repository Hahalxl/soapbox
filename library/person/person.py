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
        longest = max(size)
        filler = self.fill * (longest + len("Organization:") + 6) #I JUST GOT LAZY HERE, PLEASE DON'T JUDGE. I KNOW THE RESULT IS 13!!!!
        return f"{filler}\nName:{self.name}\nOsis:{self.osis}\nEmail:{self.email}\nOrganization:{self.organization}\n{filler}\n\n"

    def save(self) -> bool:
        config = _config()
        infos = f"{self.name},{self.osis},{self.email},{self.organization}\n"
        print(f"{config["dir"] + config["name"]}")
        with open(f"{config["dir"] + config["name"]}", 'a') as file:
            file.write(infos)
            file.close()
        return True


    def check(self)->bool:
        # Incase they Repeat
        import pandas as pd
        config = _config()
        df = pd.read_csv(f"{config["dir"] + config["name"]}")
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


if (__name__ == "__main__"):
    import os
    os.chdir("C:\\Users\\Ronan\\Coding\\Python\\Flask\\531")
    alex = Person("Alex","6952423423","Alexliu@gmail.com","Alex Liu High School")
    print(alex)
    print(alex.check())
