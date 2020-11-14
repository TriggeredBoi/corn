import os
import re
import json
import random
import datetime as dt

#below are the ones that aren't python builtins
import discord
from discord.ext import commands
from dotenv import load_dotenv


def createifnotexists(path, mode, textifnotthere=""):
    if not os.path.isfile(path):
        with open(path, "w") as f:
            f.write(textifnotthere)
            
    return open(path, mode)

configpath = "config.txt"
if not os.path.isfile(configpath): #why would someone delete it? no idea! but they could.
    with open(configpath, "w") as f:
        f.write("DISCORD_TOKEN=")

load_dotenv(configpath)

token = os.getenv("DISCORD_TOKEN")
if not token:
    print(f"The \"token\" field is empty - Please open \"{configpath}\" and put the discord bot token and Server ID in their respective fields.")
    exit()


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
        with createifnotexists(self.leaderboardfile, "r", "{}") as file: 
            self.cornleaderboard = json.loads(file.read())

    def savecorn(self):
        with open(self.leaderboardfile, "w") as file:
            txt = json.dumps(self.cornleaderboard, indent=4)
            file.write(txt)


Corn = CornController()
bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    print("Bot is up.")

    time = loadlasttime()
    if not time:
        return
    
    counter = 0
    corncounter = 0
    for guild in bot.guilds:
        for channel in guild.text_channels:
            botmember = discord.utils.find(lambda member: member.id == bot.user.id, guild.members)

            if not (botmember and botmember.permissions_in(channel).read_message_history):
                print(f"Couldn't read message history from {channel}")
                continue

            lastmsg = None
            messages = await channel.history(after=time, limit=1000).flatten()
            for message in messages:
                if corns := search4corn(message):
                    counter += 1
                    corncounter += corns[0]
                    lastmsg = message
            print(f"Found {len(messages)} messages in {channel}")

    savelasttime(lastmsg)

    Corn.savecorn()
    if corncounter:
        print(f"Looks like {counter} messages were missed since last the bot was active, and {corncounter} corns. These have been added to the leaderboard.")
    else: print("No corns were lost while the bot was away!")


def loadlasttime():
    with createifnotexists("lastmessagetime", "r") as file:
        date = None
        try:
            date = dt.datetime.fromisoformat(file.read())
        finally:
            return date

def savelasttime(msg):
    if not msg: return
    with open("lastmessagetime", "w") as file:
        file.write(msg.created_at.isoformat())

def search4corn(msg):
    corns = re.findall("corn|🌽|🍿", msg.content.lower())
    if not corns:
        return

    total = Corn.addcorn(msg, corns)
    return len(corns), total


@bot.event
async def on_message(msg):
    if msg.author == bot: return
    await bot.process_commands(msg)

    savelasttime(msg)
    
    tupl = search4corn(msg)
    if not tupl:
        return
    corns, total = tupl
    print(f"{msg.author} corned {corns} times, now at a total of {total}.")

    try: await msg.add_reaction("🌽")
    except discord.errors.Forbidden: pass

    if random.random() == 100:
        try: await msg.channel.send("corn")
        except discord.errors.Forbidden: pass

    #print(msg.channel)


@bot.command(aliases=["corn", "corntop", "lb", "🌽"])
async def leaderboards(ctx, howmany=10):
    txt = ""

    sortedboard = sorted(Corn.cornleaderboard.items(), key=lambda item: item[1], reverse=True) #(list of tuples)
    items = iter(sortedboard) #ghetto generator? or is a generator an advanced iterator? either way, this works.

    for i in range(howmany):
        id, amt = next(items)
        txt += f"#{i+1} | <@{id}> - {amt}\n"
        
    embed=discord.Embed(title="🌽 Leaderboards", description=txt)
    await ctx.send(embed=embed)

@bot.command()
async def reload(ctx):
    Corn.loadcorn()
    await ctx.message.add_reaction("✅")



if __name__ == "__main__":
    bot.run(token)
