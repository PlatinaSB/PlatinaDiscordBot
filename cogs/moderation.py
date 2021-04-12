import discord
from discord.ext import commands
import json
import array
from datetime import datetime


class moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def testmod(self, ctx):
        await ctx.send ("cogs moderation is loaded")

    @commands.command()
    @commands.has_guild_permissions(ban_members = True)
    async def ban(self, ctx, user:discord.member, *, reason=None):
        if ctx.message.author.roles > user.roles :
            await user.ban (reason=reason)
            await ctx.send (f"{user.mention} telah di ban oleh {ctx.author.mention}.")
        else:
            await ctx.send (f"Hai {ctx.author.name} kamu tidak memiliki izin")
    
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send (f"Hai {ctx.author.name} kamu tidak memiliki izin")
    
    @commands.command()
    @commands.has_guild_permissions(ban_members=True)
    async def unban(self,ctx, *,member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send (f"{user.mention} telah di unban oleh {ctx.author.mention}.")
                return
    
    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send (f"Hai {ctx.author.name} kamu tidak memiliki izin")
    
    @commands.command()
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self, ctx, user:discord.Member, *, reason=None):
        if ctx.message.author.roles > user.roles:
            await user.kick(reason=reason)
            await ctx.send (f"{user.mention} telah di kick oleh {ctx.author.name}.")
        else:
            await ctx.send (f"{user.name} memiliki role setara atau di atas kamu.")    
    
    
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send (f"Hai {ctx.author.name} kamu tidak memiliki izin")
    
    @commands.command()
    @commands.has_guild_permissions(manage_roles=True)
    async def giverole(self, ctx ,user:discord.Member, role:discord.Role, *, reason=None):
        if ctx.message.author.roles > user.roles:
            if ctx.message.author.roles > role:
                if role not in user.roles:
                    await user.add_roles(role)
                    await ctx.send (f"{user.mention} telah di berikan role {role.name} oleh {ctx.author.mention}.")
                else:
                    await ctx.send(f"{user.name} sudah memiliki role {role.name}.")
            else:
                await ctx.send (f"role yang ingin di berikan berada di atas kamu.")
        else:
            await ctx.send (f"{user.name} memiliki role setara atau di atas kamu.")
    
    @giverole.error
    async def giverole_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send (f"Hai {ctx.author.name} kamu tidak memiliki izin")
    
    @commands.command()
    @commands.has_guild_permissions(manage_nicknames= True)
    async def csn(self, ctx, user:discord.Member,*, nick):
        if ctx.message.author.roles > user.roles:
            await user.edit(nick=nick)
            await ctx.send (f"{user.mention} Nickname telah di ganti oleh {ctx.author.mention}.")
        else:
            await ctx.send (f"{user.name} memiliki role setara atau di atas kamu.")
    
    @csn.error
    async def csn_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send (f"Hai {ctx.author.name} kamu tidak memiliki izin")

    @commands.command()
    @commands.has_guild_permissions(mute_members=True)
    async def mute(self, ctx, user:discord.Member, *, reason=None):
        role_muted = discord.utils.get(ctx.guild.roles, name="mute test")
        role_muted_permission = discord.Permissions(send_messages=False, speak=False, connect=False, read_messages=True)
        
        if ctx.message.author.roles > user.roles: 
            if role_muted in user.roles:
                await ctx.send (f"{user.mention} sudah di mute.")
            elif role_muted:
                await user.add_roles(role_muted, reason=reason)
                await ctx.send (f"{user.mention} telah di mute oleh {ctx.author.mention}")
            else:
                await ctx.guild.create_role(name="mute test", permissions=role_muted_permission)
                await commands.wait_until_ready()
                await user.add_roles(role_muted, reason=reason)
                await ctx.send (f"{user.mention} telah di mute oleh {ctx.author.mention}")
        else:
            await ctx.send (f"{user.name} memiliki role setara atau di atas kamu.")
    
    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send (f"Hai {ctx.author.name} kamu tidak memiliki izin")

    #warn
    @commands.command()
    @commands.has_guild_permissions(ban_members=True, kick_members=True)
    async def warn(self, ctx, user:discord.Member, *,reason=None):
        with open('warnlist.json', 'r') as f:
            warnlist = json.load(f)
        await self.warn_member (ctx, warnlist, user, reason)
        await self.add_warn (ctx,warnlist,user,reason)
        with open("warnlist.json",'w') as f:
            json.dump(warnlist,f, indent=4)

    async def warn_member(self,ctx,warnlist,user,reason):
        if str(f"{ctx.guild.id}") not in warnlist:
            warnlist[f'{ctx.guild.id}'] = {}
            warnlist[f'{ctx.guild.id}'][f'{user.id}'] = {}
            warnlist[f'{ctx.guild.id}'][f'{user.id}']["warning"]=[]
        if str(f"{user.id}") not in warnlist[f"{ctx.guild.id}"]:
            warnlist[f'{ctx.guild.id}'][f'{user.id}'] = {}
            warnlist[f'{ctx.guild.id}'][f'{user.id}']["warning"]=[]
        elif ("warning") not in warnlist[f'{ctx.guild.id}'][f'{user.id}']:
            warnlist[f'{ctx.guild.id}'][f'{user.id}']["warning"] = []

    async def add_warn(self, ctx, warnlist, user,reason):
        with open('warnlist.json', 'r') as f:
            wls = json.load(f)  
            dtn = datetime.now()
            dt_s = dtn.strftime("%d/%m/%Y %H:%M:%S")        
            warns = warnlist[f'{ctx.guild.id}'][f'{user.id}']["warning"]
            warnstructure = {
        "warned by": f"{ctx.author.id}",
        "reason" : f"{reason}",
        "date" : f"{dt_s}"
        }
        warns.append(warnstructure)
        await ctx.send(f"{user.mention} Telah di warn oleh {ctx.author.mention} pada waktu {dt_s} dengan alasan {reason}")


def setup(client):
    client.add_cog(moderation(client))