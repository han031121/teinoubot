# teinoubot
teinoubot / 저능아봇 / 低能ボット
han031121@gmail.com

## invitiation

Clike [here](https://discord.com/api/oauth2/authorize?client_id=1127962452005507215&permissions=40671259392832&scope=bot) to invite this bot.

## commands

### !나즈나

엄선된 나나쿠사 나즈나의 사진을 출력합니다.

### !일본한자

일본 상용한자를 무작위로 출력합니다.
1부터 5까지 난이도를 설정할 수 있습니다.

### !꺼져, !꼬맹

단순 출력 멘트.

## Todo-list
- 

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

To run project as a bot,

```bash
poetry run python main.py
```
