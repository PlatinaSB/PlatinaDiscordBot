import discord 
from discord.ext import commands
import json
from discord import guild

class levelsys(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self,member):
        with open('level.json', 'r') as f:
            level = json.load(f)
        await self.update_data(level, member)
        with open('level.json', 'w') as f:
            json.dump(level, f, indent=4)

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_message(self, message):
        if isinstance(message.channel, discord.DMChannel)==True:
            await message.channel.send("dm is bloked for leveling")
            return
        if message.author.bot == False:
            with open('level.json', 'r') as f:
                level = json.load(f)
            await self.update_data(level, message.author, message)
            await self.add_experience(level, message.author, 4, message)
            await self.level_up(level, message.author, message)
            with open('level.json', 'w') as f:
                json.dump(level, f,indent=4)
		else:
			pass
                
        

    async def update_data(self, level, user, message):
        if str(f"{message.guild.id}") not in level:
            level[f'{message.guild.id}'] = {}
            level[f'{message.guild.id}'][f'{user.id}'] = {}
            level[f'{message.guild.id}'][f'{user.id}']['experience'] = 0
            level[f'{message.guild.id}'][f'{user.id}']['level'] = 0
        elif str(f"{message.author.id}") not in level[f"{message.guild.id}"]:
            level[f'{message.guild.id}'][f'{user.id}'] = {}
            level[f'{message.guild.id}'][f'{user.id}']['experience'] = 0
            level[f'{message.guild.id}'][f'{user.id}']['level'] = 0

    async def add_experience(self, level, user, exp, message):
        level[f'{message.guild.id}'][f'{user.id}']['experience'] += exp

    async def level_up(self, level, user, message):
        experience = level[f'{message.guild.id}'][f'{user.id}']['experience']
        lvl_start = level[f'{message.guild.id}'][f'{user.id}']['level']
        lvl_end = int(experience ** (1/4))
        if lvl_start < lvl_end:
            await message.channel.send(f'{user.mention} has leveled up to level {lvl_end}')
            level[f'{message.guild.id}'][f'{user.id}']['level'] = lvl_end


def setup(client):
    client.add_cog(levelsys(client))

