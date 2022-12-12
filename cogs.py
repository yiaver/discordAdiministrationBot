import discord
from discord.ext import commands
from discord import SlashCommand,application_command
from discord.ext.commands import has_permissions

guildlist = [1004735784403878019,771577360159735818]

class AdministrationC(commands.Cog):
    def __init__(self,client) -> None:
        self.client = client
        
        print(f"{__class__.__name__} inicialized!")
    
    

    @application_command(cls=SlashCommand,name = "newrole", description="Make a new role",guild_ids=guildlist)
    @has_permissions(administrator=True)
    async def newRole(self,ctx,name):
        perms = discord.Permissions(speak=True,send_messages=False)
        await ctx.guild.create_role(name=name,permissions=perms)
        await ctx.response.send_message(f"Role {name} created!")
        return
        
    @application_command(cls=SlashCommand,name = "delrole", description="Delete a role",guild_ids=guildlist)
    @has_permissions(administrator=True)
    async def delRole(self,ctx,name):
        role  =  discord.utils.get(ctx.guild.roles,name=name)
        await role.delete()
        await ctx.response.send_message(f"Role {name} deleted!")
        return

    @application_command(name="kick", pass_context=True ,description="Kick a member",guild_ids=guildlist)
    @has_permissions(administrator=True)
    async def kick(self,ctx,member:discord.Member):
        await member.kick()
        await ctx.response.send_message(f"{member} kicked!")
        return
    
    @application_command(name="ban",description="Ban a member",guild_ids=guildlist)
    @has_permissions(administrator=True)
    async def ban(self,ctx,member:discord.Member,rason="Bot Ban"):
        await member.ban()
        await ctx.response.send_message(f"{member} has ben banned!\n{rason}")
        return
    
    @application_command(name="unban",description="Unban a member",guild_ids=guildlist)
    @has_permissions(administrator=True)
    async def unban(self,ctx,member:discord.Member,rason="No rason"):
        await member.unban()
        await ctx.response.send_message(f"{member} is unbaned!\n{rason}")
        return


    @application_command(name="mute",description="Mute a member",guild_ids=guildlist)
    @has_permissions(administrator=True)
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member:discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Silenced")
        await member.add_roles(role)
        await member.move_to(None)
        await ctx.response.send_message(f"Usuario : {member} mutado")
        return

    @application_command(name="unmute",description="Unmute a member",guild_ids=guildlist)
    @has_permissions(administrator=True)
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member:discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Silenced")
        await member.remove_roles(role)
        await member.move_to(None)
        await ctx.response.send_message(f"Usuario : {member} desmutado")
        return
    
    @application_command(name="listcategory",description="create a new category",guild_ids=guildlist)
    @has_permissions(administrator=True)
    async def listCategory(self,ctx):
        categories = [x.name for x in ctx.guild.categories]
        await ctx.response.send_message(categories)
        return
    
    @application_command(name="addchannel",description="create a new voice channel",guild_ids=guildlist)
    @has_permissions(administrator=True)
    async def addVoiceChannel(self,ctx,name,category,type):
        categories = [x.name for x in ctx.guild.categories]
        if category in categories:
            categoryObj = discord.utils.get(ctx.guild.categories,name=category)
            if type in ("voice","VOICE","Voice"):
                await ctx.guild.create_voice_channel(name=name,category=categoryObj)
                await ctx.response.send_message(f"Voice channel {name} sucessfull created in {category} category.")
                return
            elif type in ("text","TEXT","Text"):
                await ctx.guild.create_text_channel(name=name,category=categoryObj)
                await ctx.response.send_message(f"Text channel {name} sucessfull created in {category} category.")
                return 
        else:
            await ctx.response.send_message(f"The category {category} don't exist!")
            return
    
    

    @application_command(name="addcategory",description="create a new category",guild_ids=guildlist)
    @has_permissions(administrator=True)
    async def addCategory(self,ctx,name,position,reason="No reason"):
        await ctx.guild.create_category(name=name,position=position ,reason=reason)
        await ctx.response.send_message(f"Category {name} was created!")
        return

    @application_command(name="setupserver",description="Setup server",guild_ids=guildlist)
    @has_permissions(administrator=True)
    async def setupServer(self,ctx):
        perms = discord.Permissions(speak=False,send_messages=False)
        await ctx.guild.create_role(name="Silenced",permissions=perms)
        afk = await ctx.guild.create_category(name="AFK",position=999,reason=None)
        await ctx.guild.create_voice_channel(name="AFK",category=afk)
        await ctx.response.send_message("Server Setup sucessfull")
        return

def setup(client):
    client.add_cog(AdministrationC(client))