#
import os
import shutil
from os.path import join


class DirController:
    def __init__(self, dataDir, dataExt):
        # 입력 설정
        self.dataDir = dataDir
        self.dataExt = dataExt
        # 자동 설정
        self.rawDir = join(dataDir, "RAW")
        self.figDir = join(dataDir, "figure")
        self.includeDir = join(dataDir, "CHK", "RAW")
        self.excludeDir = join(dataDir, "EXC")
        self.postponedDir = join(dataDir, "PP")

    def refreshDir_all(self):
        refresh_dir(self.includeDir)
        refresh_dir(self.excludeDir)
        refresh_dir(self.postponedDir)

    def get_rawDir(self):
        return self.rawDir

    def get_figDir(self):
        return self.figDir

    def get_includeDir(self):
        return self.includeDir

    def get_excludeDir(self):
        return self.excludeDir

    def get_postponedDir(self):
        return self.postponedDir


def refresh_dir(file_path):
    if os.path.exists(file_path):
        shutil.rmtree(file_path)
    os.makedirs(file_path)
