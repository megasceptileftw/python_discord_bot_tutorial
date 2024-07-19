import discord
from discord.ext import commands
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
from discord.utils import get
import requests
import json
import os

# Checking for no no words in member's messages
no_no_words = ["kys", "k y s"]

class admin(commands.Cog):

    def __init__(self, client):
        self.client = client


    # Checking for no no words in member's messages
    @commands.Cog.listener()
    async def on_message(self, message):
        for n in no_no_words:
            if n in message.content:
                await message.delete()
                await message.channel.send("Don't send that again bro")
        
        # await self.client.process_commands(message)
        

    # Kicking and Banning Commands
    @commands.command()
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'User {member} has been kicked')

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to kick people")

    @commands.command()
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'User {member} has been banned')

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to ban people")


    # embed tutorial
    @commands.command()
    async def embed(self, ctx):
        embed = discord.Embed(title="Dog", url="https://google.com", description="We love dogs!", color=0x4287f5)
        embed.set_author(name=ctx.author.display_name, url="https://x.com/_AlexVGC_", icon_url=ctx.author.avatar.url)
        embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/1320573394719395840/nkYexy3O_400x400.jpg")
        embed.add_field(name="Labrador", value="Cute dogs", inline="True")
        embed.add_field(name="Pugs", value="Cute dogs", inline="True")
        embed.set_footer(text="Thanks for reading")
        await ctx.send(embed=embed)


    # missing permission error
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to run this command!")


    # dm message
    @commands.command()
    async def message(self, ctx, user:discord.Member, *, message=None):
        message = "Welcome to the server!"
        embed = discord.Embed(title=message)
        await user.send(embed=embed)


    # adding role command w/ permissions error checking
    @commands.command(pass_context = True)
    @commands.has_permissions(manage_roles = True)
    async def addRole(self, ctx, user : discord.Member, *, role : discord.Role):

        if role in user.roles:
            await ctx.send(f"{user.mention} already has the role, {role}")
        else:
            await user.add_roles(role)
            await ctx.send(f"Added {role} to {user.mention}")
    
    @addRole.error
    async def role_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to use this command!")

    
    # removing role command w/ permissions error checking
    @commands.command(pass_context = True)
    @commands.has_permissions(manage_roles = True)
    async def removeRole(self, ctx, user : discord.Member, *, role : discord.Role):

        if role in user.roles:
            await user.remove_roles(role)
            await ctx.send(f"Removed {role} from {user.mention}")
        else:
            await ctx.send(f"{user.mention} does not have the role, {role}")
    
    @removeRole.error
    async def role_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to use this command!")
    
async def setup(client):
    await client.add_cog(admin(client))