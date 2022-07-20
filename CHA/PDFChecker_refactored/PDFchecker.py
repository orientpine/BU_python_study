# This code was written by OrientPine.

# 필요한 라이브러리
import json

# custom module
from module_CBD.directory import DirController
from module_CBD.parse import makeArgs
from module_CBD.excel_base import ExcelBase


def main():
    # 필요한 설정값을 설정 파일에서 불러오기
    with open("settings.json", "r") as f:
        settings = json.load(f)
    dataDir = settings["dataDir"]
    dataExt = settings["dataExt"]
    checkList_filename = settings["checkList_filename"]
    # 프로그램 mode 입력받기
    args = makeArgs()
    # 경로 관련 클래스 초기화
    directory = DirController(dataDir, dataExt)
    # 엑셀베이스 관련 클래스 초기화
    excelBase = ExcelBase(checkList_filename, dataDir)
    # 원하는 파일로 데이터베이스만들기 혹은 있으면 해당 파일 불러오기
    excelBase.load(directory.get_rawDir(), dataExt)
    # 현재 데이터 확인
    excelBase.showStatus()

    if args.mode == "CHK" or args.mode == "PP":
        # 확인모드! 아직 점검하지 않은 파일을 보거나, 결정을 미룬 파일을 다시 보거나!
        # QC 책임자 확인
        excelBase.identify()
        # 확인하기
        excelBase.doTask(args.mode, directory.get_figDir())
    if args.mode == "EXP":
        # 출력모드! 기존에 있던 폴더 몽땅 날리기
        directory.refreshDir_all()
        # 출력하기
        excelBase.doExport(
            directory.get_includeDir(),
            directory.get_excludeDir(),
            directory.get_postponedDir(),
        )


if __name__ == "__main__":
    main()
