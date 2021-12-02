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
async def on_command(ctx, *args):
    if len(args) == 0:
        role = get(ctx.guild.roles, name='Shame Listed')
        members = await ctx.guild.fetch_members().flatten()  
        if len(members) == 0:
            await ctx.send("Wow, there are no members to shame!") 
        for member in members:
            if role in member.roles:
                await ctx.send(member.name)
    elif args[0] == 'init':
        shame_list_channel = discord.utils.get(ctx.guild.text_channels, name='shame-list')
        await shame_list_channel.purge() # clears entire shame-list channel
        members = await ctx.guild.fetch_members().flatten() 
        role = get(ctx.guild.roles, name='Shame Listed')
        shame_list = '```The Shame List\n'
        for member in members:
            if role in member.roles:
                shame_list += member.name + '\n'
        shame_list = shame_list + '```'
        await shame_list_channel.send(shame_list)
    else:
        await ctx.send('Not a valid command')

bot.run(TOKEN)