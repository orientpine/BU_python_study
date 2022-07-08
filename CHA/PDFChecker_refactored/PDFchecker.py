# This code was written by OrientPine.

# 필요한 라이브러리
from re import A
from tqdm import tqdm
from natsort import natsorted
import os
import pandas as pd
import shutil
import argparse
import keyboard
import subprocess

# custom module
from module_CBD.directory import DirController
from module_CBD.parse import makeArgs
from module_CBD.excel_base import ExcelBase
from module_CBD.cli import Cli


def main():
    # 필요한 경로 정의
    dataDir = r"."
    dataExt = r"IMU"
    # 프로그램 mode 입력받기
    args = makeArgs()
    # 경로 관련 클래스 초기화
    directory = DirController(dataDir, dataExt)
    # 엑셀베이스 관련 클래스 초기화
    excelBase = ExcelBase("CheckList.xlsx", dataDir)
    # 원하는 파일로 데이터베이스만들기 혹은 있으면 해당 파일 불러오기
    checkList = excelBase.load(directory.get_rawDir(), dataExt)
    # CLI 관련 클래스 초기화
    clInterface = Cli(checkList)
    # CLI 상태창
    clInterface.status()

    if args.mode == "CHK" or args.mode == "PP":
        # CLI QC 책임자 확인
        name = clInterface.identify()
        # CLI 메뉴얼 보여주기
        clInterface.showManual()
        excelBase.doTask(args.mode, directory.get_figDir(), name)
    if args.mode == "EXP":
        # 출력모드! 기존에 있던 폴더 몽땅 날리기
        directory.refreshDir_all()
        excelBase.doExport(
            directory.get_includeDir(),
            directory.get_excludeDir(),
            directory.get_postponedDir(),
        )


if __name__ == "__main__":
    main()
