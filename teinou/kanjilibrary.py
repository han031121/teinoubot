import re
from PIL import ImageFont, ImageDraw, Image
from os import path, makedirs
from discord import ui

enhira = []
TEXT_PATH = "assets/teinoubot_texts/"
with open(TEXT_PATH + "en_hiragana.txt","r",encoding='UTF8') as f_engtohira:
    tmpList = f_engtohira.readlines()
    tmpList = [line.rstrip('\n') for line in tmpList]
    for i in range(len(tmpList)):
        enhira.append(tmpList[i].split('\t'))

def cncharImage(string):
    if not path.isdir("assets/teinoubot_image/.cnchar"):
        makedirs("assets/teinoubot_image/.cnchar")
    filename = f"assets/teinoubot_image/.cnchar/{string}.jpg"
    if not path.isfile(filename):
        width, height = (200,200)
        image = Image.new('RGB', (width,height), (255,255,255))
        font = ImageFont.truetype("assets/NotoSansSC-Regular.ttf", 160)
        draw = ImageDraw.Draw(image)
        draw.text((20, -25), string, fill="black", font=font)
        open(filename, "a")
        image.save(filename)
    return filename

def kanjiImage(string):
    if not path.isdir("assets/teinoubot_image/.kanji"):
        makedirs("assets/teinoubot_image/.kanji")
    filename = f"assets/teinoubot_image/.kanji/{string}.jpg"
    if not path.isfile(filename):
        width, height = (200,200)
        image = Image.new('RGB', (width,height), (255,255,255))
        font = ImageFont.truetype("assets/NotoSansJP-Regular.ttf", 160)
        draw = ImageDraw.Draw(image)
        draw.text((20, -25), string, fill="black", font=font)
        open(filename, "a")
        image.save(filename)
    return filename

def select_list(placeholder:str, options:list, disabled:bool = False):
    return ui.Select(
        placeholder = placeholder,
        min_values = 1,
        max_values = 1,
        options = options,
        disabled = disabled)

def isincludeKanji(string):
    return re.search("[㐀-䶵一-鿋豈-頻]",string)
def iskanji(string):
    return re.fullmatch("^[㐀-䶵一-鿋豈-頻]+$",string)
def ishiragana(string):
    return re.fullmatch("^[ぁ-ゟ]+$",string)
def ishangeul(string):
    return re.fullmatch("^[가-힣]+$",string)
def engtohira(string):
    string = string.lower()
    res = ""
    op = 1 # option. 1 = hiragana, 2 = katakana
    while(len(string)>0):
        if (string[0]=='*'): #카타카나 변환
            if (len(string)==1):
                break
            if (op == 1):
                op = 2
            else:
                op = 1
            string = string[1:]
        curlen = len(string)
        if(len(string)>1):
            if (string[0]==string[1] and (string[0] not in "nmaeiou")) or (string.find("tch")==0): #자음 중복으로 촉음 입력
                if op==1:
                    res += "っ"
                elif op==2:
                    res += "ッ"
                string = string[1:]
                continue
            if (string[0]=='m' and string[1] in "bmp"): #m으로 ん입력
                if op==1:
                    res += "ん"
                elif op==2:
                    res += "ン"
                string = string[1:]
                continue
        for i in range(len(enhira)):
            if(len(enhira[i][op])==0):
                continue
            if(string.find(enhira[i][0])==0):
                res += enhira[i][op]
                string = string[len(enhira[i][0]):]
                break
        if (len(string)==curlen):
            return -1
    return res
