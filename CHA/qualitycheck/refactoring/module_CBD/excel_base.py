import os
import pandas as pd
import shutil
import keyboard
import subprocess
from module_CBD.process import kill
from tqdm import tqdm


class ExcelBase:
    def __init__(self, filename, location):
        self.filename = filename
        self.location = location
        self.checkList = None

    def load(self, dataList):
        if os.path.isfile(os.path.join(self.location, self.filename)):
            self.checkList = pd.read_excel(
                os.path.join(self.location, self.filename), engine="openpyxl"
            )
        else:
            self.checkList = pd.DataFrame(
                columns=["filename", "type", "note", "checker"]
            )
            self.checkList["filename"] = dataList
            self.checkList["type"] = "TBD"
        return self.checkList

    def doTask(self, taskType, figDir, chk_name):
        if taskType == "CHK":
            flag = "TBD"
        else:
            flag = "PP"

        count = 0
        for datum in self.checkList["filename"]:
            if (
                self.checkList.loc[self.checkList.filename == datum, "type"].values
                == flag
            ):
                num_flag = self.checkList["type"].value_counts()[flag]
                while True:
                    if keyboard.read_key(suppress=True) == "w":
                        print(f"\nNo:{count} | remains: {num_flag-count}")
                        count = count + 1
                        break
                    if keyboard.read_key(suppress=True) == "p":  # 프로그램 종료
                        print("\nwait for saving the list...")
                        self.checkList.to_excel(
                            os.path.join(self.location, self.filename), index=False
                        )
                        print("See you!")
                        quit()
                print(f"Target: {datum}")
                basename = basename = os.path.basename(datum)
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
                    if keyboard.read_key(suppress=True) == "q":  # 포함시킬 파일
                        self.checkList.loc[
                            self.checkList.filename == datum, "type"
                        ] = "IN"
                        self.checkList.loc[
                            self.checkList.filename == datum, "checker"
                        ] = chk_name

                        # if not os.path.exists(os.path.join(includeDir,datum)): # 파일이 이미 있으면 그냥 지나감
                        #     shutil.copyfile(os.path.join(rawDir, datum), os.path.join(includeDir,datum))
                        print(f"Included!: {datum}")
                        break
                    if keyboard.read_key(suppress=True) == "e":  # 제거할 파일
                        self.checkList.loc[
                            self.checkList.filename == datum, "type"
                        ] = "EXC"
                        self.checkList.loc[
                            self.checkList.filename == datum, "checker"
                        ] = chk_name
                        # if not os.path.exists(os.path.join(includeDir,datum)): # 파일이 이미 있으면 그냥 지나감
                        #     shutil.copyfile(os.path.join(rawDir, datum), os.path.join(excludeDir,datum))
                        print(f"Excluded!: {datum}")
                        break
                    if keyboard.read_key(suppress=True) == "s":  # 포함시킬 파일
                        self.checkList.loc[
                            self.checkList.filename == datum, "type"
                        ] = "PP"
                        print("Enter your note:")
                        reason = input()
                        self.checkList.loc[
                            self.checkList.filename == datum, "note"
                        ] = reason
                        self.checkList.loc[
                            self.checkList.filename == datum, "checker"
                        ] = chk_name
                        # if not os.path.exists(os.path.join(includeDir,datum)): # 파일이 이미 있으면 그냥 지나감
                        #     shutil.copyfile(os.path.join(rawDir, datum), os.path.join(postpondDir,datum))
                        print(f"Postponed!: {datum}")
                        break
                kill(plot.pid)

        print("\nThere is nothing to do!")
        print("wait for saving the list...")
        self.checkList.to_excel(os.path.join(self.location, self.filename), index=False)
        print("See you!")
        quit()

    def doExport(self,includeDir,excludeDir,postponedDir):
        print("\n=== EXPORT MODE ===")
        print("now exporting files...")

        for file in tqdm(self.checkList["filename"]):
            basename = os.path.basename(file)
            # type에서 IN이라고 되어 있는 file이 있으면
            if (
                self.checkList.loc[self.checkList.filename == file, "type"]
                == "IN"
            ).bool():
                # 순회하면서 "IN"인 것만 raw에 저장하기
                if not os.path.exists(
                    os.path.join(includeDir, basename)
                ):  # 파일이 이미 있으면 그냥 지나감
                    shutil.copyfile(file, os.path.join(includeDir, basename))

            # type에서 IN이라고 되어 있는 file이 있으면
            elif (
                self.checkList.loc[self.checkList.filename == file, "type"]
                == "EXC"
            ).bool():
                # 순회하면서 "IN"인 것만 raw에 저장하기
                if not os.path.exists(
                    os.path.join(excludeDir, basename)
                ):  # 파일이 이미 있으면 그냥 지나감
                    shutil.copyfile(file, os.path.join(excludeDir, basename))
            # type에서 IN이라고 되어 있는 file이 있으면
            elif (
                self.checkList.loc[self.checkList.filename == file, "type"]
                == "PP"
            ).bool():
                # 순회하면서 "IN"인 것만 raw에 저장하기
                if not os.path.exists(
                    os.path.join(postponedDir, basename)
                ):  # 파일이 이미 있으면 그냥 지나감
                    shutil.copyfile(file, os.path.join(postponedDir, basename))
        print("Done!")
