import os
import requests
import json
from multiprocessing import Process

def script1():
    os.system("python discordbot.py")     
def script2():
    os.system("python guildedbot.py") 


def checkForUpdate():
    # Check version number against version on https://github.com/GoByeBye/GuildBridge/data/version.json
    if os.path.isfile("data/version.json"):
        with open("data/version.json") as f:
            __version__ = json.load(f)["version"]
        
        # Grab the version number from https://raw.githubusercontent.com/GoByeBye/GuildBridge/master/data/version.json
        version = requests.get("https://raw.githubusercontent.com/GoByeBye/GuildBridge/master/data/version.json")
        if version.status_code == 200:
            version = version.json()["version"]
            
            # Check if the version number is the same as the one on the server
            if version  == __version__:
                print("GuildBridge is up to date!")
            else:
                print("GuildBridge is outdated!")
                print("Please update GuildBridge when you have a moment to")

def cleanHooks():
    """Resets data/hooks.json to default to prevent the file from getting huge"""
    if os.path.isfile("data/hooks.json"):
        with open("data/hooks.json", "w") as f:
            # Default data
            # { "messages": [] }
            json.dump({"messages": []}, f)


if __name__ == '__main__':
    cleanHooks()
    checkForUpdate()
    p = Process(target=script1)
    q = Process(target=script2)
    p.start()
    q.start()
    p.join()
    q.join()