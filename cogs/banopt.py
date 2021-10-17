import discord 
from discord.ext import commands
import json

class banopt(commands.cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def usm(self, ctx):
        await ctx.send ("cogs usm is loaded")

    @commands.command()
    async def unban_all(self,ctx):
        banned_users = await ctx.guild.bans()
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.id) == (user.id):
                await ctx.guild.unban(user)
                await ctx.send (f"unbanning {user.id}")
            else:
                await ctx.send (f"failed to unban {user.id}")
    
    #bans member when they joined
    @commands.Cog.listener
    async def on_member_join(self, member):
        with open('banwhenjoinlist.json', 'r') as f:
            bannedlist = json.load(f)
            if member.id in bannedlist[f'{member.guild.id}']:
                await member.ban(reason = "automatic ban")

            else:
                pass
    @commands.command
    async def addban(self, id):
        with open('banwhenjoinlist.json','r') as bam:
            listban= json.load(bam)
        await self.updatelist(id)
        with open('banwhenjoinlist.json','r') as bam:
            listban= json.dump(bam)
        async def updatelist(self,message):
            if str(f"{message.guild.id}") not in listban:
                listban[f'{message.guild.id}'] = ['readyban']
                listban[f'{message.guild.id}']['readyban'] = {id}
            elif id not in listban[f'{message.guild.id}']['readyban']:
                listban[f'{message.guild.id}']['readyban'] = {id}
        
    

def setup(client):
    client.add_cog(banopt(client))