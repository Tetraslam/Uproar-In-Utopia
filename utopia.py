# bot.py
import os
import random
from dotenv import load_dotenv
import itertools

# 1
import discord
from discord.ext import commands

# Firebase
import firebase_admin

cred_obj = firebase_admin.credentials.Certificate('uproar-in-utopia-firebase-adminsdk-tod52-0b621bff02.json')
default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL': 'https://uproar-in-utopia-default-rtdb.asia-southeast1.firebasedatabase.app'
	})

import json
from firebase_admin import db

ref = db.reference("/")

# for key, value in ref.get().items():
#     if(value["Government Type"] == "Dictatorship"):
#         ref.child(key).update({"Index": 10})

# FIREBASE STAT RETRIEVAL FUNCTIONS

def getpolicylist(userID):
  for key, value in ref.get().items():
        if(value["Discord User ID"] == userID):
          rawjson = ref.child(key).get()
          policylog = rawjson["Policies"]
          i = 0
          listofpolicies = ""
          while i<len(policylog):
              addtolist = (policylog[i])
              listofpolicies += " " + addtolist
              i+=1
          return listofpolicies

def getstat(userID, statname):
    for key, value in ref.get().items():
        if(value["Discord User ID"] == userID):
            rawjson = ref.child(key).get()
            stat = rawjson[statname]
            return stat
        else:
            print("user not found")

def getaccount(userID):
    for key, value in ref.get().items():
        if(value["Discord User ID"] == userID):
            rawjson = ref.child(key).get()
            listofstats = ""
            j=0
            out = dict(itertools.islice(rawjson.items(), 43))
            listprint = ""
            for items in out:
                listprint+="\n" + items + ": " + str(out.get(items))

            return(str(listprint))



intents = discord.Intents.default()
intents.typing = True
intents.dm_messages = True
intents.presences = True
intents.members = True
intents.message_content = True
intents.guilds = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# 2
bot = commands.Bot(command_prefix='!', intents = intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name = 'policy')
async def policies(ctx):
    sendpolicies = getpolicylist(str(ctx.author.id))
    await ctx.send(sendpolicies)

@bot.command(name = 'approval')
async def approval(ctx):
    sendapproval = getstat(str(ctx.author.id), "Approval")
    await ctx.send(str(sendapproval))

@bot.command(name = 'account')
async def account(ctx):
    sendaccount = getaccount(str(ctx.author.id))
    await ctx.send("```" + str(sendaccount) + "```")

@bot.command(name='99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)


bot.run(TOKEN)
