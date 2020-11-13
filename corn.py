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
        f.write("DISCORD_TOKEN=\nGUILD_ID=")

load_dotenv(configpath)

token = os.getenv("DISCORD_TOKEN")
if not token:
    print(f"The \"token\" field is empty - Please open \"{configpath}\" and put the discord bot token and Server ID in their respective fields.")
    exit()

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print("Bot is up.")

@bot.command()
async def aaa(ctx):
    pass


if __name__ == "__main__":
    bot.run(token)
