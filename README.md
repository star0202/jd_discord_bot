## 중요!!
- 이 봇은 제 학교 디스코드 서버에서 사용되는 봇입니다
- 이 레포의 과거 기록에서 auth.py에 있는 토큰은 현재 사용되지 않는 토큰입니다

# 코드 구조
`/assets` : 이미지 등등

`/functions` : 코그(파일만 추가하면 main.py에서 자동으로 로드해줌)

`/utils` : 자주 쓰는 기능들/모듈

`Procfile` : Heroku 프로필(수정 금지)

`config.py` : 컨피그 파일
- `COLOR` : 기본 임베드 색 <- `int(hex)`
- `BAD` : 좋지 않은 상황일 때 임베드 색 <- `int(hex)`
- `GOOD` : 좋은 상황일 때 임베드 색 <- `int(hex)`
- `TEST_GUILD_ID` : 테스트 서버 아이디 <- `int`
- `DEV_ID` : 개발자의 아이디 <- `int`
- `STATUS` : 상태 메세지 <- `str`

`main.py` : 실행파일(봇 설정, 코그 로드)

`requirements.txt` : 의존성 라이브러리 목록

`runtime.txt` : `Heroku` 파이썬 버전(수정 금지)

# 개발에 참여
## 개발 준비
1. 저장소를 포크한다(오른쪽 상단 `Fork`버튼 클릭)

2. 포크한 저장소를 클론한다
```shell
$ git clone https://github.com/<닉네임>/jd_discord_bot.git
```
3. 디펜던시를 설치한다
```shell
$ pip install -r requirements.txt
```
4. 브랜치를 만든다

`stable`브랜치를 복제하여 새로운 브랜치를 만든다, 
브랜치 이름은 브랜치 이름은 버그 수정의 경우 `bug/<버그 요약>`, 
기능 추가 및 보수의 경우 `feature/<기능 이름>`, 
기타 코드 개선 작업 등은 `maintain/{요약}`으로 한다

5. .env 파일을 설정한다

프로젝트 폴더 최상단에 다음과 같은 양식으로 `.env`파일을 생성한다
```python
TOKEN = "토큰"
DB_CHANNEL_ID = "데이터베이스 채널 아이디"
```
## 개발
- 작업하는 브랜치가 맞는지 확인한다
- 다른 파일들을 참고하여 코드를 작성한다(코드 스타일은 전부 비슷하게)
- 커밋 전에 `flake8`을 이용하여 포맷팅을 확인한다
```shell
$ python -m flake8
```
- 커밋 메세지는 `Fix <버그 요약> bug`, `Add <기능 이름> feature` 등등으로 작성한다
## 봇에 반영
- `stable`브랜치를 베이스로 해 PR을 생성하면 확인 후 `stable`브랜치에 머지된다
- `stable`브랜치가 수정되면 `Heroku`에서 자동으로 봇을 재부팅해 코드가 봇에 반영된다

# 예시 코그

```py
# myextension.py
from discord.ext import commands
import logging

logger = logging.getLogger(__name__)


class MyExtension(commands.Cog):
    # 코드


def setup(bot):
    logger.info("Loaded")
    bot.add_cog(MyExtension())


def teardown():
    logger.info("Unloaded")
```

# 참고용 문서
[Pycord 공식 매뉴얼](https://docs.pycord.dev/en/master/api.html)