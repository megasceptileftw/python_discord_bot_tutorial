# import required dependencies
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
import requests
import json
import os

# import various tokens
from apikeys import *

intents = discord.Intents.all()
intents.members = True

# queue for music
queues = {}

async def check_queue(ctx, id):
    if queues[id] != []:
        voice = ctx.guild.voice_client
        source = queues[id].pop(0)
        player = voice.play(source)

client = commands.Bot(command_prefix = '!', intents = intents)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Streaming(name='Huniepop', url='https://www.twitch.tv/alexxvgc'))
    print("The bot is now ready for use!")
    print("-----------------------------")


# hello command
@client.command()
async def hello(ctx):
    await ctx.send("Hello, I am the Weiss Matchmaking Bot")


# join server event w/ dad joke
@client.event
async def on_member_join(member):
    url = "https://dad-jokes7.p.rapidapi.com/dad-jokes/joke-of-the-day"

    headers = {
        "x-rapidapi-key": JOKETOKEN,
        "x-rapidapi-host": "dad-jokes7.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    
    channel = client.get_channel(1148771636301008948)
    await channel.send("Welcome to the server, here is a dad joke")
    await channel.send(response.json())


# goodbye event when member leaves
@client.event
async def on_member_remove(member):
    channel = client.get_channel(1148771636301008948)
    await channel.send("Goodbye!")


# bot joins voice chat and plays Recording.m4a
@client.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('./audio/Recording.m4a')
        player = voice.play(source)
    else:
        await ctx.send("You are not in a voice channel. Join a voice channel to run this command.")


# makes bot leave voice chat
@client.command(pass_contex = True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Left the Voice Chat")
    else: 
        await ctx.send("Not in voice channel")


# pause music currently playing
@client.command(pass_contex = True)
async def pause(ctx):
    if (ctx.author.voice == None):
        return await ctx.send("You need to be in a voice channel to use this command")
    
    if (ctx.voice_client == None):
        return await ctx.send("The bot isn't in the voice channel.")
    
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    if (voice.is_playing()):
        voice.pause()
    else:
        await ctx.send("No audio currently playing in the voice channel")


# resume paused music
@client.command(pass_contex = True)
async def resume(ctx):
    if (ctx.author.voice == None):
        return await ctx.send("You need to be in a voice channel to use this command")
    
    if (ctx.voice_client == None):
        return await ctx.send("The bot isn't in the voice channel.")
    
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    if (voice.is_paused()):
        voice.resume()
    else:
        await ctx.send("No audio currently paused")


# stop music currently playing
@client.command(pass_contex = True)
async def stop(ctx):
    if (ctx.author.voice == None):
        return await ctx.send("You need to be in a voice channel to use this command")
    
    if (ctx.voice_client == None):
        return await ctx.send("The bot isn't in the voice channel.")

    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    voice.stop()

# play music, queue if currently playing music
@client.command(pass_contex = True)
async def play(ctx, arg):
    if (ctx.author.voice == None):
        return await ctx.send("You need to be in a voice channel to use this command")
    
    if (ctx.voice_client == None):
        return await ctx.send("The bot isn't in the voice channel.")

    voice = ctx.guild.voice_client
    song = arg + '.m4a'
    source = FFmpegPCMAudio('./audio/' + song)

    guild_id = ctx.message.guild.id

    if (guild_id in queues):
        queues[guild_id].append(source)
        while (queues[guild_id] != [] & source.is_playint):
            await check_queue(ctx, guild_id)
    else:
        queues[guild_id] = [source]
        await check_queue(ctx, guild_id)


# queue music 
# @client.command(pass_contex = True)
# async def queue(ctx, arg):
#     if (ctx.author.voice == None):
#         return await ctx.send("You need to be in a voice channel to use this command")
    
#     if (ctx.voice_client == None):
#         return await ctx.send("The bot isn't in the voice channel.")

#     voice = ctx.guild.voice_client
#     song = arg + '.m4a'
#     source = FFmpegPCMAudio('./audio/' + song)

#     guild_id = ctx.message.guild.id

#     if (guild_id in queues):
#         queues[guild_id].append(source)
#     else:
#         queues[guild_id] = [source]
    
#     await ctx.send("Added to queue")


# Checking for no no words in member's messages
no_no_words = ["kys", "k y s"]

@client.event
async def on_message(message):
    for n in no_no_words:
        if n in message.content:
            await message.delete()
            await message.channel.send("Don't send that again bro")
    
    await client.process_commands(message)


# Kicking and Banning Commands
@client.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'User {member} has been kicked')

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to kick people")

@client.command()
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'User {member} has been banned')

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to ban people")

# embed tutorial
@client.command()
async def embed(ctx):
    embed = discord.Embed(title="Dog", url="https://google.com", description="We love dogs!", color=0x4287f5)
    embed.set_author(name=ctx.author.display_name, url="https://x.com/_AlexVGC_", icon_url=ctx.author.avatar.url)
    embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/1320573394719395840/nkYexy3O_400x400.jpg")
    embed.add_field(name="Labrador", value="Cute dogs", inline="True")
    embed.add_field(name="Pugs", value="Cute dogs", inline="True")
    embed.set_footer(text="Thanks for reading")
    await ctx.send(embed=embed)


# missing permission error
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to run this command!")

# dm message
@client.command()
async def message(ctx, user:discord.Member, *, message=None):
    message = "Welcome to the server!"
    embed = discord.Embed(title=message)
    await user.send(embed=embed)

client.run(BOTTOKEN)