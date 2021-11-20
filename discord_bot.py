import discord
from discord.ext import commands
from discord.ext.commands import bot
from discord.utils import get
import random
import json
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

client = commands.Bot(command_prefix=commands.when_mentioned_or ('p?'))

@client.event
async def on_ready():
    for filename in os.listdir("./cogs"):
        if filename.endswith ('.py'):
            client.load_extension(f"cogs.{filename[:-3]}")
            print (f"cogs loaded {filename[:-3]}")
    print('bot is ready')
    await client.change_presence(status=discord.Status.idle, activity=discord.Game ('bot online'))

#cogs
@client.command()
async def load(ctx, extension):
    if ctx.author.id == 000 : #add your discord uid
        client.load_extension (f"cogs.{extension}")
        client.wait_until_ready()
        await ctx.send (f"loaded cogs {extension}")

@client.command()   
async def unload(ctx, extension):
    if ctx.author.id == 000 : #add your discord uid
        client.unload_extension(f"cogs.{extension}")
        client.wait_until_ready()
        await ctx.send (f"unloaded cogs {extension}")

@client.command()
async def reload(ctx, extension):
    if ctx.author.id == 000 : #add your discord uid
        client.reload_extension(f"cogs.{extension}")
        client.wait_until_ready()
        await ctx.send (f"reloaded cogs {extension}")
#/cogs



@client.command()
async def ping(ctx):
    await ctx.send (f'pong! {round(client.latency * 1000)}ms')

@client.command()
async def roll(ctx):
    await ctx.send (f"Roll number {random.randint(0,1000)}")

@client.command()
async def guildid(ctx):
    await ctx.send (f'{ctx.message.guild.id}')

# @client.command()
# async def infog(ctx):
#     avrurl = client.user.avatar_url
#     platinaid= 433019005146628107
#     await ctx.send (discord.Member.)



    



# @client.command()
# async def info(ctx):
#     embeds = discord.Embed(title = "Bot info", description= f"The Bot was created for testing purpose by PlatinaSB (<@433019005146628107>)" 
#     , color = discord.Color.red())
#     embeds.set_thumbnail(url = discord.Member.avatar_url)

#     await ctx.send (embed=embeds)

    


#need to add clean, pruge, help, info, member count, server info, invite info,

client.run(os.getenv('token'))
