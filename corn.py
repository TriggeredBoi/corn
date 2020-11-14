import os
import re
import json
import random


#below are the ones that aren't python builtins
import discord
from discord.errors import Forbidden
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

bot = discord.ext.commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print("Bot is up.")

class CornController():
    def __init__(self):
        self.cornleaderboard = {}
        self.leaderboardfile = "leaderboard.json"
        self.loadcorn()

    def addcorn(self, msg, corns):
        who = str(msg.author.id)

        total = self.cornleaderboard.get(who) or 0
        total += len(corns)

        self.cornleaderboard[who] = total
        self.savecorn()
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
    if msg.author == bot: return
    corns = re.findall("corn|🌽|🍿", msg.content.lower())
    if not corns:
        return
    total = Corn.addcorn(msg, corns)
    print(f"{msg.author} corned {len(corns)} times, now at a total of {total}.")
    try: await msg.add_reaction("🌽")
    except discord.errors.Forbidden: pass
    if random.random() == 100:
        try: await msg.channel.send("corn")
        except discord.errors.Forbidden: pass
    print(msg.channel)
    await bot.process_commands(msg)

@bot.command()
async def corn(ctx):
    txt = ""

    sortedboard = sorted(Corn.cornleaderboard.items(), key=lambda item: item[1], reverse=True) #(list of tuples)
    items = iter(sortedboard) #ghetto generator? or is a generator an advanced iterator? either way, this works.

    for i in range( min(len(sortedboard), 10) ):
        id, amt = next(items)
        txt += f"#{i+1} | <@{id}> - {amt}\n"
        
    embed=discord.Embed(title="🌽 Leaderboards", description=txt)
    await ctx.send(embed=embed)


if __name__ == "__main__":
    bot.run(token)
