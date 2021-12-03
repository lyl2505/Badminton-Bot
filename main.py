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

# allows guild.members to display all members and manage permissions
intents = discord.Intents.default()
intents.members = True
discord.Permissions.manage_roles = True
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
    try:
        if len(args) == 0:
            role = get(ctx.guild.roles, name='Shame Listed')
            members = await ctx.guild.fetch_members().flatten()  
            if len(members) == 0:
                await ctx.send("Wow, there are no members to shame!") 
            for member in members:
                if role in member.roles:
                    await ctx.send(member.name)
        elif args[0] == 'init':
            if len(args) > 2:
                raise InvalidArgument('InvalidArgument: Too many arguments')
            await init_shame_list(ctx)
        elif args[0] == 'remove':
            if len(args) < 2:
                raise InvalidArgument('InvalidArgument: Must list 1 or more server members with [Shame Listed] tag')
            members = args[1:]
            await remove_from_shame_list(ctx, members)
        else:
            await ctx.send('Not a valid command')
    except InvalidArgument as ex:
                await ctx.send(ex.args)

'''
    !announce time
    Pings the entire guild on i-request-badminton channel and tells the time when it happens
    @exception InvalidArgument if {time} doesn't fit the HH:MM(PM|AM) regex
'''
@bot.command(name='announce', help='Announces a time to play badminton for the current day')
async def on_announce(ctx, time):
    command_channel = discord.utils.get(ctx.guild.text_channels, name='bot-tinkering')
    if ctx.message.channel != command_channel:
        return

    time = time.upper()
    channel = discord.utils.get(ctx.guild.text_channels, name='bot-tinkering') # different name
    regex = re.compile(r'((0?[1-9]|1[0-2]):([0-5]\d)((?:A|P)\.?M\.?))')
    is_match = regex.match(time.strip())
    try:
        if is_match is None:
            raise InvalidArgument('InvalidArgument: Argument must be in the format of HH:MM(PM|AM)')
        else:
            await command_channel.send('everyone Hello edgelords! Badminton will be played at ' + is_match.group(0) + ' today.') # @everyone
    except InvalidArgument as ex:
        await command_channel.send(ex.args)
        return
    
 
@on_announce.error
async def on_announce_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("MissingRequiredArguement: You're missing a time, dummy") # TODO add insulting name
 

'''
    Creates a shame_list based on whoever is tagged 'Shame Listed' on
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

async def remove_from_shame_list(ctx, members): 
    removal_log = ""
    shame_role = get(ctx.guild.roles, name='Shame Listed')
    for member in members:
        username = member.split('#')
        if member == username:
            removal_log += member + ' is not in the correct format\n'
        else:
            is_member = get(await ctx.guild.fetch_members().flatten(), name=username[0], discriminator=username[1])
            if is_member is None:
                removal_log += member + ' does not exist\n'
            elif shame_role not in is_member.roles:
                removal_log += member + ' is not Shame Listed\n'
            else:
                await is_member.remove_roles(shame_role)
                removal_log += member + ' is removed from the Shame List'
                
    await ctx.send(removal_log)

bot.run(TOKEN)