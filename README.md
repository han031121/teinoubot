# Teinoubot

<p align="center">
<img width=200 src="./assets/splash.png">
<br>
teinoubot / 저능봇 / 低能ボット
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

### /말걸기

저능아봇에게 말을 겁니다.

### /이미지 

특정 캐릭터의 그림을 출력합니다.

### /일본한자

검색을 통해 일본 한자 정보를 출력합니다.
음독, 훈독을 히라가나 또는 영어 발음을 통해 검색할 수 있습니다.
한자를 직접 입력하여 검색할 수도 있습니다.

### /일본한자_랜덤

무작위의 일본 한자 정보를 출력합니다. 
난이도를 설정할 수 있습니다.

### /중국한자

검색을 통해 중국 한자 정보를 출력합니다.
한어병음을 입력하거나 직접 한자를 입력하여 검색할 수 있습니다.

### /일본어

일본어 발음을 영어로 입력받아 히라가나로 출력합니다.   
특정 부분을 *로 감싸 카타카나로 출력할 수 있습니다.   
일본어 입력기의 규칙을 대부분 반영하였습니다.   

### /숫자야구

숫자 야구 게임을 진행합니다.
입력값을 제공하지 않으면 게임을 시작하거나 종료합니다.

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
