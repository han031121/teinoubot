'''
특정 디렉토리 내 이미지 파일들을 한번에 파싱해서 출력할 수 있게 해주는 유틸리티 클래스

object = ImageParser(path, noDupLimit, spoiler)
    path : assets/ 폴더 내에 특정할 폴더 이름을 지정합니다.
        ex. path = "nazuna" 일 경우, assets/nazuna/ 폴더 내 모든 파일을 대상으로 함.
    noDupLimit : 랜덤하게 이미지를 꺼낼 때, 중복이 안되게 하는 최소 텀을 지정합니다.
        ex. noDupLimit = 5 일 때, 특정 사진이 나오나서 최소, 그 다음 4장은 다른 이미지가 나옴.
    spoiler : 이미지를 출력할 때 스포일러로 나오게 하는 여부를 정함.\
        ex. spoiler = true 이면 이미지 출력시 스포일러 상태로 출력됨.

object.toggleSpoiler():
    앞으로 내보낼 사진에 스포일러 여부를 토글합니다.
object.refreshDupList():
    현재 중복 방지 리스트를 새롭게 정합니다.
object.getRandomItem() :
    discord.py File 형식으로 이번에 나올 이미지를 반환
'''

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
    