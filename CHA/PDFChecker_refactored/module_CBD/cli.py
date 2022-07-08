class Cli:
    def __init__(self, checkList):
        self.name = ""
        self.checkList = checkList

    def identify(self):
        while len(self.name) == 0:
            self.name = input("Type your Name : ")
        print(f"{self.name} is entering...")
        return self.name

    def status(self):
        print("=== STATUS ===")
        print(self.checkList["type"].value_counts())
        if "TBD" in self.checkList["type"].value_counts():
            num_TBD = self.checkList["type"].value_counts()["TBD"]
        if "PP" in self.checkList["type"].value_counts():
            num_PP = self.checkList["type"].value_counts()["PP"]

    def showManual(self):
        print("||   KEY - FUNCTION   ||")
        print("|| 'w' - go next file || 'p' - terminate program ||")
        print("|| 'q' - for include  || 'e' - for exclude       ||")
        print("|| 's' - for postpone ||                         ||")
