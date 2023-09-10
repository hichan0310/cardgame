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
        print("error")
else:
    print("error")
