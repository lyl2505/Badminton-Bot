import os
import discord
import re
from discord.errors import InvalidArgument
from discord.ext.commands.errors import MissingRequiredArgument
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
MAX_NAME_LENGTH = 32

# allows guild.members to display all members
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents = intents)
bot = commands.Bot(command_prefix='!', intents = intents)

@bot.event
async def on_ready():
    print(f'{client.user} has connected to Discord')

@bot.command(name='shame', help='Prints out the members of the shame list')
async def on_shame(ctx, *args):
    command_channel = discord.utils.get(ctx.guild.text_channels, name='bot-tinkering')
    if ctx.message.channel != command_channel:
        return

    if len(args) == 0:
        role = get(ctx.guild.roles, name='Shame Listed')
        members = await ctx.guild.fetch_members().flatten()  
        if len(members) == 0:
            await ctx.send("Wow, there are no members to shame!") 
        for member in members:
            if role in member.roles:
                await ctx.send(member.name)
    elif args[0] == 'init':
        await init_shame_list(ctx)
    else:
        await ctx.send('Not a valid command')

@bot.command(name='announce', help='Announces a time to play badminton for the current day')
async def on_announce(ctx, time):
    command_channel = discord.utils.get(ctx.guild.text_channels, name='bot-tinkering')
    if ctx.message.channel != command_channel:
        return

    channel = discord.utils.get(ctx.guild.text_channels, name='bot-tinkering') # different name
    regex = re.compile(r'((0?[1-9]|1[0-2]):([0-5]\d)((?:A|P)\.?M\.?))')
    is_match = regex.match(time.strip())
    print(time)
    print(is_match)
    try:
        if is_match is None:
            raise InvalidArgument('InvalidArgument: Argument must be in the format of HH:MM(PM|AM)')
        else:
            await command_channel.send('everyone Hello edgelords! Badminton will be played at ' + regex.group(0) + ' today.')
    except InvalidArgument as ex:
        await command_channel.send(ex.args)
        return
    
 
@on_announce.error
async def on_announce_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("MissingRequiredArguement: You're missing a time, dummy") # TODO add insulting name
 

'''
    Description:    Creates a shame_list based on whoever is tagged 'Shame Listed' on
                    the server. 
                    TODO
'''
async def init_shame_list(ctx):
    shame_list_channel = discord.utils.get(ctx.guild.text_channels, name='shame-list')
    await shame_list_channel.purge() # clears entire shame-list channel
    members = await ctx.guild.fetch_members().flatten() 
    role = get(ctx.guild.roles, name='Shame Listed')
    shame_list = '```The Shame List\n'
    for member in members:
        if role in member.roles:
            shame_list += (member.name + '\n')
    shame_list = shame_list + '```'
    await shame_list_channel.send(shame_list)

bot.run(TOKEN)