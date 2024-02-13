# Teinoubot

<p align="center">
<img width=200 src="./assets/splash.png">
<br>
teinoubot / 저능아봇 / 低能ボット
</p>



## Collaborators

| <img width=100 src="https://avatars.githubusercontent.com/u/61414506?v=4">                                           | <img width=100 src="https://avatars.githubusercontent.com/u/65532873?v=4">                                  |
|:-----------------------------------------:|:-------------------------------------:|
| [han031121](https://github.com/han031121) | [chayhan](https://github.com/chayhan) |
| Project Owner, develops features.         | develops core and middlewares of bot. |


## Invitiation

Clike [here](https://discord.com/api/oauth2/authorize?client_id=1127962452005507215&permissions=40671259392832&scope=bot) to invite this bot.

## Execution

To execute bots with tokens, you could use two ways to launch bots: develop version and product version.

- To initiate the bot with Developing version, issue below command.

```bash
poetry run dev
```

- Or you can also deploy the bot via `poetry` with below command.

```bash
poetry run start
```

## commands

### !나즈나

엄선된 나나쿠사 나즈나의 사진을 출력합니다.   

### ~~!료~~

~~야마다 료의 사진을 출력합니다. 딱히 엄선된 사진은 아닙니다.~~   
미구현 상태입니다.   

### !일본한자

!일본한자 : 일본 상용한자를 무작위로 출력합니다.   
!일본한자 {난이도값} : 특정 난이도의 상용한자를 출력합니다. (1~5 입력 가능)   
!일본한자 {검색어} : 음독, 훈독으로 상용한자를 검색할 수 있으며, 히라가나와 영어로 검색할 수 있습니다.   

### !일본어

일본어 발음을 영어로 입력받아 히라가나로 출력합니다.   
특정 부분을 *로 감싸 카타카나로 출력할 수 있습니다.   
일본어 입력기의 규칙을 대부분 반영하였습니다.   

### ~~!일본단어~~

~~일본 단어를 무작위로 출력합니다.~~   
미구현 상태입니다.   

### !야구

숫자 야구 게임을 진행합니다.   
!야구 시작 : 게임이 시작되고, 정답을 생성합니다.   
!야구 {세 자리 숫자} : 스트라이크, 볼의 개수를 출력합니다. 정답일 경우 게임을 종료합니다.   
!야구 종료 : 게임을 종료하고, 정답을 공개합니다.   

### !꺼져, !꼬맹

단순 출력 커맨드.   

<!-- ## Todo-list -->


---

## Getting start with poetry

The project is managed by `poetry`, which let python runs on virtual environments seperately from global environment.

To set a virtual environment for `poetry` **in your project**, issue below the commands.

### poetry venv settings

If you want to build a virtual poetry environment within your project's work environment, run the command below.

```bash
# warning : this instructions are optional in case you want to run your virtual env in your project folder.
# warning : this might change your personal poetry config.
poetry config virtualenvs.in-project true
poetry config virtualenvs.path "./.venv"
poetry install && poetry update

# and set python's interpreter to your virtual environment in your folder named `.venv` in your project.
```
### dependency installation

run below command to install the dependencies of this project into your poetry virtual environment.

```bash
poetry install
```