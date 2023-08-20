# teinoubot
teinoubot / 저능아봇 / 低能ボット
han031121@gmail.com

## invitiation

Clike [here](https://discord.com/api/oauth2/authorize?client_id=1127962452005507215&permissions=40671259392832&scope=bot) to invite this bot.

## commands

### !나즈나 `캐릭터 이름`

제일 좋아하는 캐릭터의 사진을 출력합니다.

입력하지 않을 시 캐릭명이 `나즈나` 로 검색됩니다.

### !대통령 `이름`

그분들의 사진을 출력합니다.

대통령 기준은 [나](https://github.com/johannblue)는 모름.

### !유저검색 `닉네임`

메이플 gg로부터 데이터를 크롤링하여 해당 캐릭터의 정보를 불러옵니다.

- 사진
- 코디정보
- 레벨
- 인기도
- 무릉도장 최고 기록

### !꺼져, !꼬맹

단순 출력 멘트.

## Todo-list
- `/` 커맨드 지원
- 과도한 요청 지연 관리

---

## Getting start with poetry

The project is managed by `poetry`, which let python runs on virtual environments seperately from global environment.

To set a virtual environment for `poetry` **in your project**, issue below the commands.

```bash
# warning : this instructions are optional in case you want to run your virtual env in your project folder.
# warning : this might change your personal poetry config.
poetry config virtualenvs.in-project true
poetry config virtualenvs.path "./.venv"
poetry install && poetry update

# and set python's interpreter to your virtual environment in your folder named `.venv` in your project.
```

```bash
poetry install
```
