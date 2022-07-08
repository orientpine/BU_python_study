# PDF를 순차적으로 열고
# Key 입력해서 자동으로 저장하게 만들고
# 후딱 보기

# 필요한 library
import os
from re import A
import subprocess
from natsort import natsorted
import pandas as pd
import keyboard
import subprocess
import psutil
import shutil
import argparse
from tqdm import tqdm

# 필요한 함수 선언


def refresh_dir(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    os.makedirs(file_path)


def ensure_dir(file_path):
    if not os.path.exists(file_path):
        os.makedirs(file_path)


def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()


# 프로그램 용도 1. PDF 보면서 list 정리하기 2. list에 따라 csv 옮겨주기
parser = argparse.ArgumentParser()
parser.add_argument(
    "--mode",
    "-mo",
    required=False,
    default="CHK",
    type=str,
    help="mode: CHK | PP | EXP",
)
args = parser.parse_args()
# 파일 주소
# RAW 폴더를 보고 돌아다니면서
# FIG에 있는 PDF 열고
# Included_checked 아래에 저장하기
dataDir = r"."
rawDir = r".\RAW"
figDir = r".\FIG"
includeDir = r".\CHK\RAW"
excludeDir = r".\EXC"
postponedDir = r".\PP"
dataExt = r"IMU.xlsx"
# 파일 목록 열기
# 파일 목록없으면 만들기 # 추후에 결과 출력용 만들 때 그떄 풀어놓기
# 목록 다 만들고 목록 출력용으로 만들어 놓기
#  전체 목록 읽으면서 포함 파일만 따로 보관하기


# 파일 목록 전체 들고오고 필요한 확장자만 고르고 들고온 파일 목록에서 .txt만 남기고 나머지 것들 제외시키기
dataList = natsorted(
    [os.path.join(i[0], i[2][0]) for i in list(os.walk(rawDir)) if ("IMU" in i[0])]
)
excluded_fig = []  # 제외된 경우 1이라고 표기
# 일단 총 개수 알려주기
# 데이터가 어디까지 처리되었는지 확인할 수 있도록 함.
# list_Excluded_byFig.xlsx를 참고해서 어차피 순차적으로 볼 꺼니까 어디까지 봤는지 확인하게 함
# 추후에 안된 것만 따로 돌수있도록 하는 기능 추가하던가..하자

# list_Excluded_byFig.xlsx 가 있으면
# dataList 손보기
# 없으면 만들기
listName = r"CheckList.xlsx"
if os.path.isfile(os.path.join(dataDir, listName)):
    list_Excluded_byFig = pd.read_excel(
        os.path.join(dataDir, listName), engine="openpyxl"
    )
else:
    list_Excluded_byFig = pd.DataFrame(columns=["filename", "type", "note", "checker"])
    list_Excluded_byFig["filename"] = dataList
    list_Excluded_byFig["type"] = "TBD"
# 그냥 시작
print("\n= Type your Name = ")
chk_name = input()
print(f"{chk_name} is entering...")

print("\n== Status ==")
print(list_Excluded_byFig["type"].value_counts())
if "TBD" in list_Excluded_byFig["type"].value_counts():
    num_TBD = list_Excluded_byFig["type"].value_counts()["TBD"]
if "PP" in list_Excluded_byFig["type"].value_counts():
    num_PP = list_Excluded_byFig["type"].value_counts()["PP"]
if args.mode == "EXP":
    print("\n=== EXPORT MODE ===")
    print("now exporting files...")
    # mode가 켜져있으면 list를 기반으로 출력 작업
    # 저장 폴더 만들기
    ensure_dir(includeDir)
    ensure_dir(excludeDir)  # 쓸일이 없네 필요하면
    ensure_dir(postponedDir)  # 쓸일이 없넹 필요하면 넣자

    # list는 이미 불렀음
    # 전체 리스트 순회
    for file in tqdm(list_Excluded_byFig["filename"]):
        basename = os.path.basename(file)
        # type에서 IN이라고 되어 있는 file이 있으면
        if (
            list_Excluded_byFig.loc[list_Excluded_byFig.filename == file, "type"]
            == "IN"
        ).bool():
            # 순회하면서 "IN"인 것만 raw에 저장하기
            if not os.path.exists(
                os.path.join(includeDir, basename)
            ):  # 파일이 이미 있으면 그냥 지나감
                shutil.copyfile(file, os.path.join(includeDir, basename))

        # type에서 IN이라고 되어 있는 file이 있으면
        elif (
            list_Excluded_byFig.loc[list_Excluded_byFig.filename == file, "type"]
            == "EXC"
        ).bool():
            # 순회하면서 "IN"인 것만 raw에 저장하기
            if not os.path.exists(
                os.path.join(excludeDir, basename)
            ):  # 파일이 이미 있으면 그냥 지나감
                shutil.copyfile(file, os.path.join(excludeDir, basename))
        # type에서 IN이라고 되어 있는 file이 있으면
        elif (
            list_Excluded_byFig.loc[list_Excluded_byFig.filename == file, "type"]
            == "PP"
        ).bool():
            # 순회하면서 "IN"인 것만 raw에 저장하기
            if not os.path.exists(
                os.path.join(postponedDir, basename)
            ):  # 파일이 이미 있으면 그냥 지나감
                shutil.copyfile(file, os.path.join(postponedDir, basename))
    print("Done!")

elif args.mode == "CHK":

    # mode가 꺼져있으면 listing 작업
    print("\n=== CHECK MODE ===")
    print("||   KEY - FUNCTION   ||")
    print("|| 'w' - go next file || 'p' - terminate program ||")
    print("|| 'q' - for include  || 'e' - for exclude       ||")
    print("|| 's' - for postpone ||                         ||")
    num_trial = 0
    firstScene = True
    for datum in dataList:
        if (
            list_Excluded_byFig.loc[
                list_Excluded_byFig.filename == datum, "type"
            ].values
            == "TBD"
        ):
            while True:
                if keyboard.read_key(suppress=True) == "w":
                    print(f"\nNo:{num_trial} | remains: {num_TBD-num_trial}")
                    num_trial = num_trial + 1
                    break
                if keyboard.read_key(suppress=True) == "p":  # 제거할 파일
                    print("\nwait for saving the list...")
                    list_Excluded_byFig.to_excel(
                        os.path.join(dataDir, listName), index=False
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
                    list_Excluded_byFig.loc[
                        list_Excluded_byFig.filename == datum, "type"
                    ] = "IN"
                    list_Excluded_byFig.loc[
                        list_Excluded_byFig.filename == datum, "checker"
                    ] = chk_name

                    # if not os.path.exists(os.path.join(includeDir,datum)): # 파일이 이미 있으면 그냥 지나감
                    #     shutil.copyfile(os.path.join(rawDir, datum), os.path.join(includeDir,datum))
                    print(f"Included!: {datum}")
                    break
                if keyboard.read_key(suppress=True) == "e":  # 제거할 파일
                    list_Excluded_byFig.loc[
                        list_Excluded_byFig.filename == datum, "type"
                    ] = "EXC"
                    list_Excluded_byFig.loc[
                        list_Excluded_byFig.filename == datum, "checker"
                    ] = chk_name
                    # if not os.path.exists(os.path.join(includeDir,datum)): # 파일이 이미 있으면 그냥 지나감
                    #     shutil.copyfile(os.path.join(rawDir, datum), os.path.join(excludeDir,datum))
                    print(f"Excluded!: {datum}")
                    break
                if keyboard.read_key(suppress=True) == "s":  # 포함시킬 파일
                    list_Excluded_byFig.loc[
                        list_Excluded_byFig.filename == datum, "type"
                    ] = "PP"
                    print("Enter your note:")
                    reason = input()
                    list_Excluded_byFig.loc[
                        list_Excluded_byFig.filename == datum, "note"
                    ] = reason
                    list_Excluded_byFig.loc[
                        list_Excluded_byFig.filename == datum, "checker"
                    ] = chk_name
                    # if not os.path.exists(os.path.join(includeDir,datum)): # 파일이 이미 있으면 그냥 지나감
                    #     shutil.copyfile(os.path.join(rawDir, datum), os.path.join(postpondDir,datum))
                    print(f"Postpond!: {datum}")
                    break

            # https://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true
            # 덕분에 해결함!
            kill(plot.pid)
            firstScene = False
        # else:
        #     if not firstScene:
        #         print(f'\nPassed: {datum}')
    print("\nThere is no data!")
    print("wait for saving the list...")
    list_Excluded_byFig.to_excel(os.path.join(dataDir, listName), index=False)
    print("See you!")
    quit()

elif args.mode == "PP":
    # mode가 꺼져있으면 listing 작업
    print("\n=== CHECK MODE ===")
    print("||   KEY - FUNCTION   ||")
    print("|| 'w' - go next file || 'p' - terminate program ||")
    print("|| 'q' - for include  || 'e' - for exclude       ||")
    print("|| 'c' - for postpone ||                         ||")
    num_trial = 0
    firstScene = True
    for datum in dataList:
        if (
            list_Excluded_byFig.loc[
                list_Excluded_byFig.filename == datum, "type"
            ].values
            == "PP"
        ):
            while True:
                if keyboard.read_key(suppress=True) == "w":
                    print(f"\nNo:{num_trial} | remains: {num_PP-num_trial}")
                    num_trial = num_trial + 1
                    break
                if keyboard.read_key(suppress=True) == "p":  # 제거할 파일
                    print("\nwait for saving the list...")
                    list_Excluded_byFig.to_excel(
                        os.path.join(dataDir, listName), index=False
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
                    list_Excluded_byFig.loc[
                        list_Excluded_byFig.filename == datum, "type"
                    ] = "IN"
                    list_Excluded_byFig.loc[
                        list_Excluded_byFig.filename == datum, "checker"
                    ] = chk_name

                    # if not os.path.exists(os.path.join(includeDir,datum)): # 파일이 이미 있으면 그냥 지나감
                    #     shutil.copyfile(os.path.join(rawDir, datum), os.path.join(includeDir,datum))
                    print(f"Included!: {datum}")
                    break
                if keyboard.read_key(suppress=True) == "e":  # 제거할 파일
                    list_Excluded_byFig.loc[
                        list_Excluded_byFig.filename == datum, "type"
                    ] = "EXC"
                    list_Excluded_byFig.loc[
                        list_Excluded_byFig.filename == datum, "checker"
                    ] = chk_name
                    # if not os.path.exists(os.path.join(includeDir,datum)): # 파일이 이미 있으면 그냥 지나감
                    #     shutil.copyfile(os.path.join(rawDir, datum), os.path.join(excludeDir,datum))
                    print(f"Excluded!: {datum}")
                    break
                if keyboard.read_key(suppress=True) == "s":  # 포함시킬 파일
                    list_Excluded_byFig.loc[
                        list_Excluded_byFig.filename == datum, "type"
                    ] = "PP"
                    print("Enter your note:")
                    reason = input()
                    list_Excluded_byFig.loc[
                        list_Excluded_byFig.filename == datum, "note"
                    ] = reason
                    list_Excluded_byFig.loc[
                        list_Excluded_byFig.filename == datum, "checker"
                    ] = chk_name
                    # if not os.path.exists(os.path.join(includeDir,datum)): # 파일이 이미 있으면 그냥 지나감
                    #     shutil.copyfile(os.path.join(rawDir, datum), os.path.join(postpondDir,datum))
                    print(f"Postpond!: {datum}")
                    break

            # https://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true
            # 덕분에 해결함!
            kill(plot.pid)
            firstScene = False
    print("\nThere is no data!")
    print("wait for saving the list...")
    list_Excluded_byFig.to_excel(os.path.join(dataDir, listName), index=False)
    print("See you!")
    quit()
