import requests
import subprocess

response=requests.get("https://github.com/hichan0310/cardgame")
if response.status_code==200:
    try:
        result=subprocess.check_output(["git", "pull"])
        print(str(result))
        subprocess.check_output(["python", "game_exe.py"])
    except:
        print("와이파이에 연결하세요")
else:
    print("error")
