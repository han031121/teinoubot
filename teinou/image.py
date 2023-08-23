import os

IMAGE_PATH = '/assets/teinoubot_image/' #image path

class ImageParser:
    # 특정 path에 대한 이미지 출력을 맡는 인스턴스를 생성하는 class 이다.
    def __init__(self, path:str, noDupLimit=10):
        self.path = path
        self.dirList = os.listdir(os.getcwd() + IMAGE_PATH + path)
        self.noDupLimit = noDupLimit
        print(self.dirList)

    def getRandomItem(self):
        '''
        return random item with file binary format from this instance.
        '''
        
        pass
    