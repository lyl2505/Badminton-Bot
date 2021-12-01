import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# allows guild.members to display all members
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents = intents)

bot = commands.Bot(command_prefix='!', intents = intents)

@bot.event
async def on_ready():
    print(f'{client.user} has connected to Discord')

@bot.command(name='shame', help='Prints out the members of the shame list')
async def on_command(ctx):
    role = get(ctx.guild.roles, name='Shame')
    members = await ctx.guild.fetch_members().flatten()   
    await ctx.send(members)
    """ for member in ctx.message.guild.members:
        await ctx.send(member.name)
        if role in member.roles:
            await ctx.send(member.name) """

bot.run(TOKEN)