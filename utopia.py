# bot.py
import os
import random
from dotenv import load_dotenv

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

@bot.command(name='roll', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))


bot.run(TOKEN)
