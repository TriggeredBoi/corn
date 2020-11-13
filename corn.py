import os
from random import choice
from time import sleep
import re


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

cornleaderboard = {}

def addcorn(who, corns):
    global cornleaderboard
    if not cornleaderboard.get(who):
        cornleaderboard[who] = corns
        return corns

    cornleaderboard[who] += corns
    return cornleaderboard[who]

@bot.event
async def on_message(msg):
    corns = re.findall("corn", msg.content.lower())
    if not corns:
        return
    total = addcorn(msg.author.id, len(corns))
    print(f"{msg.author} corned {len(corns)} times, now at a total of {total}")

@bot.command()
async def aaa(ctx):
    pass


if __name__ == "__main__":
    bot.run(token)
