import os
import random
from discord import File
IMAGE_PATH = '/assets/teinoubot_image/' #image path

class ImageParser:
    # 특정 path에 대한 이미지 출력을 맡는 인스턴스를 생성하는 class 이다.
    def __init__(self, path:str, noDupLimit=10, spoiler=False):
        if path[-1] != '/':
            path += '/'
        self.path = os.getcwd() + IMAGE_PATH + path
        self.dirList = os.listdir(self.path)
        self.noDupList = []
        if len(self.dirList) < noDupLimit:
            noDupLimit = len(self.dirList)
        self.noDupLimit = noDupLimit
        self.spoiler = spoiler
    def toggleSpoiler(self):
        self.spoiler = not self.spoiler

    def refreshDupList(self):
        self.noDupList = [t for t in random.sample(range(0, len(self.dirList)), self.noDupLimit)]

    def getRandomItem(self):
        '''
        return random item with file binary format from this instance.
        '''
        if len(self.noDupList) == 0:
            self.refreshDupList()
        
        item = self.path + self.dirList[self.noDupList.pop()]
        return File(open(item, mode="rb"), spoiler=self.spoiler)
    