import re

enhira = []
TEXT_PATH = "assets/teinoubot_texts/"
with open(TEXT_PATH + "en_hiragana.txt","r",encoding='UTF8') as f_engtohira:
    tmpList = f_engtohira.readlines()
    tmpList = [line.rstrip('\n') for line in tmpList]
    for i in range(len(tmpList)):
        enhira.append(tmpList[i].split('\t'))

def iskanji(string):
    kanji = r'[㐀-䶵一-鿋豈-頻]'
    if re.fullmatch(kanji,string):
        return True
    return False

def ishiragana(string):
    hiragana = r'[ぁ-ゟ]'
    strlist = re.findall(hiragana,string)
    if len(string)!=len(strlist):
            return False
    for i in range(len(strlist)):
        if string[i]!=strlist[i]:
            return False
    return True

def engtohira(string):
    res = ""
    op = 1 # option. 1 = hiragana, 2 = katakana

    while(len(string)>0):
        print(string)
        print(string[0])
        if (string[0]=='*'):
            if (len(string)==1):
                break
            if (op == 1):
                op = 2
            else:
                op = 1
            string = string[1:]

        curlen = len(string)
        if(len(string)>1):
            if(string[0]==string[1] and string[0] in "kstp"):
                if op==1:
                    res += "っ"
                elif op==2:
                    res += "ッ"
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
            return "."
        
    return res