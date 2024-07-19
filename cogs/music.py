import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
import asyncio
from async_timeout import timeout
import requests
import json
import os

# queue for music
queues = {}

def check_queue(ctx, id):
    if queues[id] != []:
        voice = ctx.guild.voice_client
        source = queues[id].pop(0)  
        player = voice.play(source, after=lambda e: check_queue(ctx, id))
        

class music(commands.Cog):

    def __init__(self, client):
        self.client = client


    # bot joins voice chat and plays Recording.m4a
    @commands.command(pass_context = True)
    async def join(self, ctx):
        if (ctx.author.voice):
            channel = ctx.message.author.voice.channel
            voice = await channel.connect()
            source = FFmpegPCMAudio('./audio/Recording.m4a')
            player = voice.play(source)
        else:
            await ctx.send("You are not in a voice channel. Join a voice channel to run this command.")


    # makes bot leave voice chat
    @commands.command(pass_contex = True)
    async def leave(self, ctx):
        if (ctx.voice_client):
            await ctx.guild.voice_client.disconnect()
            await ctx.send("Left the Voice Chat")
        else: 
            await ctx.send("Not in voice channel")


    # pause music currently playing
    @commands.command(pass_contex = True)
    async def pause(self, ctx):
        if (ctx.author.voice == None):
            return await ctx.send("You need to be in a voice channel to use this command")
        
        if (ctx.voice_client == None):
            return await ctx.send("The bot isn't in the voice channel.")
        
        voice = discord.utils.get(self.client.voice_clients, guild = ctx.guild)
        if (voice.is_playing()):
            voice.pause()
        else:
            await ctx.send("No audio currently playing in the voice channel")


    # resume paused music
    @commands.command(pass_contex = True)
    async def resume(self, ctx):
        if (ctx.author.voice == None):
            return await ctx.send("You need to be in a voice channel to use this command")
        
        if (ctx.voice_client == None):
            return await ctx.send("The bot isn't in the voice channel.")
        
        voice = discord.utils.get(self.client.voice_clients, guild = ctx.guild)
        if (voice.is_paused()):
            voice.resume()
        else:
            await ctx.send("No audio currently paused")


    # stop music currently playing
    @commands.command(pass_contex = True)
    async def stop(self, ctx):
        if (ctx.author.voice == None):
            return await ctx.send("You need to be in a voice channel to use this command")
        
        if (ctx.voice_client == None):
            return await ctx.send("The bot isn't in the voice channel.")

        voice = discord.utils.get(self.client.voice_clients, guild = ctx.guild)
        voice.stop()


    # play music, queue if currently playing music
    @commands.command(pass_contex = True)
    async def play(self, ctx, arg):
        if (ctx.author.voice == None):
            return await ctx.send("You need to be in a voice channel to use this command")
        
        if (ctx.voice_client == None):
            return await ctx.send("The bot isn't in the voice channel.")

        voice = ctx.guild.voice_client
        song = arg + '.m4a'
        source = FFmpegPCMAudio('./audio/' + song)
        guild_id = ctx.message.guild.id

        if guild_id not in queues:
            queues[guild_id] = []

        queues[guild_id].append(source)

        if not voice.is_playing():
            check_queue(ctx, guild_id)


    # queue music 
    @commands.command(pass_contex = True)
    async def queue(self, ctx, arg):
        if (ctx.author.voice == None):
            return await ctx.send("You need to be in a voice channel to use this command")
        
        if (ctx.voice_client == None):
            return await ctx.send("The bot isn't in the voice channel.")

        voice = ctx.guild.voice_client
        song = arg + '.m4a'
        source = FFmpegPCMAudio('./audio/' + song)

        guild_id = ctx.message.guild.id

        if guild_id not in queues:
            queues[guild_id] = []
        
        queues[guild_id].append(source)
        
        await ctx.send("Added to queue")

async def setup(client):
    await client.add_cog(music(client))