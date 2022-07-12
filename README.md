# 코드 구조
/assets : 이미지 등등

/functions : 코그(파일만 추가하면 main.py에서 자동으로 로드해줌)

/utils : 자주 쓰는 기능들/모듈

Procfile : Heroku 프로필(수정 금지)

auth.py : 토큰<b>(유출 금지!!)</b>
- TOKEN : 토큰 <- str

config.py : 컨피그 파일
- COLOR : 기본 임베드 색 <- int(hex)
- BAD : 좋지 않은 상황일 때 임베드 색 <- int(hex)
- GOOD : 좋은 상황일 때 임베드 색 <- int(hex)
- TEST_GUILD_ID : 테스트 서버 아이디 <- int
- DEV_ID : 개발자의 아이디 <- int
- DB_CHANNEL_ID : 데이터베이스 채널의 아이디 <- int
- STATUS : 상태 메세지 <- str

main.py : 실행파일(봇 설정, 코그 로드)

requirements.txt : 의존성 라이브러리 목록

runtime.txt : Heroku 파이썬 버전(수정 금지)

# 개발에 참여

- dev 브랜치를 클론한다
```pwsh
git clone -b dev git@github.com:star0202/jd_discord_bot.git
```
- 의존성 라이브러리를 설치한다
```pwsh
pip install -r requirements.txt
```
- auth.py와 config.py를 생성한다(위의 코드 구조 참고)
- 개발을 마친 후, dev 브랜치에 커밋하고 stable <- dev로 PR을 연다
- 확인 후 머지한다

# 예시 코그

```py
# myextension.py
from discord.ext import commands


class MyExtension(commands.Cog):
    # 코드


def setup(bot):
    print("myextension.py is loaded")
    bot.add_cog(MyExtension())


def teardown():
    print("myextension.py is unloaded")
```

# 참고용 문서
[Pycord 공식 매뉴얼](https://docs.pycord.dev/en/master/api.html)
