'''
해당 파일을 실행하면 본 패키지의 클라이언트를 적용하고,
해당 클라이언트(봇)을 실행합니다.
'''

from teinou import client, token, apply

def main():
    apply(client)
    client.run(token)