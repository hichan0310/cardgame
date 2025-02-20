# cardgame
한양대학교 게임 만드는 대회<br>
팀명 : 내 파이썬이 이렇게 귀여울 리가 없어<br>
미완성인데 딱히 더 만들거나 하지는 않을듯<br>

art : magicdragon48, yunho06lee(미소녀 Stable Diffusion 모델 제공)
character design : hichan0310
enemy design : hichan0310
special card design : hichan0310
coding : hichan0310

<img src="cardgame.jpeg">

git을 설치한 후
아래 코드를 실행하면 자동으로 설치, 실행됩니다. 

```python
import requests
import subprocess
import os

response=requests.get("https://github.com/hichan0310/cardgame")
if response.status_code==200:
    if 'cardgame' not in os.listdir("./"):
        subprocess.check_output(["git", "clone", "https://github.com/hichan0310/cardgame"])
    try:
        result=subprocess.check_output(["git", "pull"], cwd='./cardgame')
        print(str(result))
        subprocess.check_output(["python", "game_exe.py"], cwd='./cardgame')
    except:
        print("git error")
else:
    print("network error")
```
