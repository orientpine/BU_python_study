#
import os
import shutil
from os.path import join
from natsort import natsorted


class DirController:
    def __init__(self, dataDir, dataExt):
        # 입력 설정
        self.dataDir = dataDir
        self.dataExt = dataExt
        # 자동 설정
        self.rawDir = join(dataDir, "RAW")
        self.figDir = join(dataDir, "FIG")
        self.includeDir = join(dataDir, "CHK", "RAW")
        self.excludeDir = join(dataDir, "EXC")
        self.postponedDir = join(dataDir, "PP")

    def refreshDir_all(self):
        refresh_dir(self.includeDir)
        refresh_dir(self.excludeDir)
        refresh_dir(self.postponedDir)

    def findData(self):
        return natsorted(
            [
                join(path[0], path[2][0])
                for path in list(os.walk(self.rawDir))
                if (self.dataExt in path[0])
            ]
        )
def refresh_dir(file_path):
    if os.path.exists(file_path):
        shutil.rmtree(file_path)
    os.makedirs(file_path)