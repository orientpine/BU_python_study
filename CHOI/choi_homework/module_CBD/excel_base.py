import os
from numpy import True_
import pandas as pd
import shutil
import keyboard
import subprocess
from natsort import natsorted
from module_CBD.process import kill
from tqdm import tqdm


class ExcelBase:
    def __init__(self, filename, location):
        self.filename = filename
        self.location = location
        self.name = None
        self.checkList = None
        self.count = 0
        self.flag = None

    def load(self, rawDir, dataExt):
        self.dataList = natsorted(
            [
                os.path.join(path[0], path[2][0])
                for path in list(os.walk(rawDir))
                if (dataExt in path[0])
            ]
        )
        if os.path.isfile(os.path.join(self.location, self.filename)):
            self.checkList = pd.read_excel(
                os.path.join(self.location, self.filename), engine="openpyxl"
            )
        else:
            self.checkList = pd.DataFrame(
                columns=["filename", "type", "note", "checker"]
            )
            self.checkList["filename"] = self.dataList
            self.checkList["type"] = "TBD"

    def identify(self):
        while self.name == None:
            self.name = input("Type your Name : ")
        print(f"{self.name} is entering...")
        return self.name

    def showManual(self):
        print("||   KEY - FUNCTION   ||")
        print("|| 'w' - go next file || 'p' - terminate program ||")
        print("|| 'q' - for include  || 'e' - for exclude       ||")
        print("|| 's' - for postpone ||                         ||")

    def showStatus(self):
        print("=== STATUS ===")
        print(self.checkList["type"].value_counts())

    def doTask(self, taskType, figDir):
        if taskType == "CHK":
            self.flag = "TBD"
        else:
            self.flag = "PP"
        # 처리해야하는게 있으면 메뉴얼 보여주기
        self.showManual()
        for datum in self.checkList["filename"]:
            if (
                self.checkList.loc[self.checkList.filename == datum, "type"].values
                == self.flag
            ):

                while True:
                    if self.receive_pass():
                        break
                print(f"Target: {datum}")
                basename = os.path.basename(datum)
                plot = subprocess.Popen(
                    [
                        os.path.join(
                            figDir,
                            basename.split("_")[0],
                            basename.replace(".xlsx", ".pdf"),
                        )
                    ],
                    shell=True,
                )

                while True:
                    if self.receive_decision(datum, "q", "IN"):
                        break
                    if self.receive_decision(datum, "e", "EXC"):
                        break
                    if self.receive_decision(datum, "s", "PP"):
                        break
                kill(plot.pid)

        print("\nThere is nothing to do!")
        print("wait for saving the list...")
        self.checkList.to_excel(os.path.join(self.location, self.filename), index=False)
        print("See you!")
        quit()

    def receive_pass(self):
        num_flag = self.checkList["type"].value_counts()[self.flag]
        if keyboard.read_key(suppress=True) == "w":
            print(f"\nNo:{self.count} | remains: {num_flag-self.count}")
            self.count = self.count + 1
            return True
        elif keyboard.read_key(suppress=True) == "p":  # 프로그램 종료
            print("\nwait for saving the list...")
            self.checkList.to_excel(
                os.path.join(self.location, self.filename), index=False
            )
            print("See you!")
            quit()
        else:
            return False

    def receive_decision(self, datum, inputKey, mark):
        if keyboard.read_key(suppress=True) == inputKey:  # 제거할 파일
            self.checkList.loc[self.checkList.filename == datum, "type"] = mark
            self.checkList.loc[self.checkList.filename == datum, "checker"] = self.name

            if mark == "PP":
                reason = input("Enter your note : ")
                self.checkList.loc[self.checkList.filename == datum, "note"] = reason
            print(f"{mark}: {datum}")
            return True
        else:
            return False

    def doExport(self, includeDir, excludeDir, postponedDir):
        print("\n=== EXPORT MODE ===")
        print("now exporting files...")

        for file in tqdm(self.checkList["filename"]):
            basename = os.path.basename(file)
            # type에서 IN이라고 되어 있는 file이 있으면
            if (
                self.checkList.loc[self.checkList.filename == file, "type"] == "IN"
            ).bool():
                # 순회하면서 "IN"인 것만 raw에 저장하기
                if not os.path.exists(
                    os.path.join(includeDir, basename)
                ):  # 파일이 이미 있으면 그냥 지나감
                    shutil.copyfile(file, os.path.join(includeDir, basename))

            # type에서 IN이라고 되어 있는 file이 있으면
            elif (
                self.checkList.loc[self.checkList.filename == file, "type"] == "EXC"
            ).bool():
                # 순회하면서 "IN"인 것만 raw에 저장하기
                if not os.path.exists(
                    os.path.join(excludeDir, basename)
                ):  # 파일이 이미 있으면 그냥 지나감
                    shutil.copyfile(file, os.path.join(excludeDir, basename))
            # type에서 IN이라고 되어 있는 file이 있으면
            elif (
                self.checkList.loc[self.checkList.filename == file, "type"] == "PP"
            ).bool():
                # 순회하면서 "IN"인 것만 raw에 저장하기
                if not os.path.exists(
                    os.path.join(postponedDir, basename)
                ):  # 파일이 이미 있으면 그냥 지나감
                    shutil.copyfile(file, os.path.join(postponedDir, basename))
        print("Done!")
