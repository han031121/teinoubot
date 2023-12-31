from teinou import ImageParser
from teinou.client import deletable_command
presidentImageParser = {
    '박정희':ImageParser('president/parkdad', 1, True),
    '전두환':ImageParser('president/jeon', 1, True),
    '노무현':ImageParser('president/roh', 1, True),
    '이명박':ImageParser('president/lee', 1, True),
    '박근혜':ImageParser('president/parkdaughter', 1, True),
    '문재인':ImageParser('president/moon', 1, True),
    '윤석열':ImageParser('president/yoon', 1, True)
}

@deletable_command(name = "대통령") #prerandNum index : 0
async def president(ctx, *args):
    if len(args)==0:
        return await ctx.channel.send('보고싶은 대통령을 함께 입력하세요')
    try:
        parser = presidentImageParser[args[0]]
        return await ctx.channel.send(file = parser.getRandomItem())
    except KeyError:
        return await ctx.channel.send(f'지원되지 않는 대통령입니다.\n\n 지원 대통령 목록\n> {str(list(presidentImageParser.keys()))[1:-1]}')