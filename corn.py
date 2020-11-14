import os
import re
import json


#below are the ones that aren't python builtins
from discord.ext import commands
from dotenv import load_dotenv



configpath = "config.txt"
if not os.path.isfile(configpath): #why would someone delete it? no idea! but they could.
    with open(configpath, "w") as f:
        f.write("DISCORD_TOKEN=")

load_dotenv(configpath)

token = os.getenv("DISCORD_TOKEN")
if not token:
    print(f"The \"token\" field is empty - Please open \"{configpath}\" and put the discord bot token and Server ID in their respective fields.")
    exit()

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print("Bot is up.")

class CornController():
    def __init__(self):
        self.cornleaderboard = {}
        self.leaderboardfile = "leaderboard.json"
        self.loadcorn()

    def addcorn(self, msg, corns):
        who = msg.author.id

        total = self.cornleaderboard.setdefault(who, 0)
        total += len(corns)

        self.cornleaderboard[who] = total
        return total
    
    def loadcorn(self):
        if not os.path.isfile(self.leaderboardfile):
            with open(self.leaderboardfile, "w") as f:
                f.write("{}")

        with open(self.leaderboardfile, "r") as file: 
            self.cornleaderboard = json.loads(file.read())

    def savecorn(self):
        with open(self.leaderboardfile, "w") as file:
            txt = json.dumps(self.cornleaderboard, indent=4)
            file.write(txt)

Corn = CornController()

@bot.event
async def on_message(msg):
    print(msg.content.lower())
    corns = re.findall("corn|🌽", msg.content.lower())
    if not corns:
        return
    total = Corn.addcorn(msg, corns)
    print(f"{msg.author} corned {len(corns)} times, now at a total of {total}.")

@bot.command()
async def save(ctx):
    Corn.savecorn()


if __name__ == "__main__":
    bot.run(token)
