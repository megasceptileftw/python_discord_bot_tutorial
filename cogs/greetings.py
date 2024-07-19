import discord
from discord.ext import commands
import requests
import json

# import various tokens
from apikeys import *

class greetings(commands.Cog):
    
    def __init__(self, client):
        self.client = client
    
    # hello command
    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hello, I am the Weiss Matchmaking Bot")


    # join server event w/ dad joke
    @commands.Cog.listener()
    async def on_member_join(self, member):
        url = "https://dad-jokes7.p.rapidapi.com/dad-jokes/joke-of-the-day"

        headers = {
            "x-rapidapi-key": "4f695c484fmsh96d766a59cc1228p16547fjsn939eb4d12513",
            "x-rapidapi-host": "dad-jokes7.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers)

        channel = self.client.get_channel(1148771636301008948)
        await channel.send("Welcome to the server, here is a joke:")
        joke_data = response.json()
        joke = joke_data.get('joke')
        await channel.send(joke)


    # goodbye event when member leaves
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.client.get_channel(1148771636301008948)
        await channel.send("Goodbye!")
    
    # tutorial reaction event, reaction added 
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        channel = reaction.message.channel

        # ignores reactions from bots
        if user.bot:
            return

        await channel.send(user.name + " added: " + reaction.emoji)

    # tutorial reaction event, reaction removal
    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        channel = reaction.message.channel
        await channel.send(user.name + " removed: " + reaction.emoji)

    # bot reactions
    @commands.Cog.listener()
    async def on_message(self, message):

        # if bot sends message happy, doesn't react to itself
        if message.author == self.client.user:
            return
        
        if ("happy") in message.content: 
            emoji = '😊'
            await message.add_reaction(emoji)

async def setup(client):
    await client.add_cog(greetings(client))