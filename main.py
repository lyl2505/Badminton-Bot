import os
import discord
import re
from datetime import datetime as dt
from discord.errors import InvalidArgument
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
MAX_NAME_LENGTH = 32

# allows guild.members to display all members and manage permissions
intents = discord.Intents.default()
intents.members = True
<<<<<<< HEAD
discord.Permissions.manage_roles = True
client = discord.Client(intents = intents)
bot = commands.Bot(command_prefix='!', intents = intents)
=======
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)

filename = "check-in_dates.txt"

>>>>>>> 18ab307e5b43ae2aba4e6abb53322ec582778845

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

<<<<<<< HEAD
'''
    !announce time
    Pings the entire guild on i-request-badminton channel and tells the time when it happens
    @exception InvalidArgument if {time} doesn't fit the HH:MM(PM|AM) regex
'''
=======
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
    elif args[0] == 'update':
        await update_shame_list(ctx)
    else:
        await ctx.send('Not a valid command')


>>>>>>> 18ab307e5b43ae2aba4e6abb53322ec582778845
@bot.command(name='announce', help='Announces a time to play badminton for the current day')
async def on_announce(ctx, time):
    command_channel = discord.utils.get(ctx.guild.text_channels, name='bot-tinkering')
    if ctx.message.channel != command_channel:
        return

    time = time.upper()
    channel = discord.utils.get(ctx.guild.text_channels, name='bot-tinkering')  # different name
    regex = re.compile(r'((0?[1-9]|1[0-2]):([0-5]\d)([AP]\.?M\.?))')
    is_match = regex.match(time.strip())
    try:
        if is_match is None:
            raise InvalidArgument('InvalidArgument: Argument must be in the format of HH:MM(PM|AM)')
        else:
<<<<<<< HEAD
            await command_channel.send('everyone Hello edgelords! Badminton will be played at ' + is_match.group(0) + ' today.') # @everyone
=======
            await command_channel.send(
                'everyone Hello edgelords! Badminton will be played at ' + is_match.group(0) + ' today.')
>>>>>>> 18ab307e5b43ae2aba4e6abb53322ec582778845
    except InvalidArgument as ex:
        await command_channel.send(ex.args)
        return


@on_announce.error
async def on_announce_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
<<<<<<< HEAD
        await ctx.send("MissingRequiredArguement: You're missing a time, dummy") # TODO add insulting name
 

'''
    Creates a shame_list based on whoever is tagged 'Shame Listed' on
    the server. 
    TODO
'''
=======
        await ctx.send("MissingRequiredArguement: You're missing a time, dummy")  # TODO add insulting name


>>>>>>> 18ab307e5b43ae2aba4e6abb53322ec582778845
async def init_shame_list(ctx):
    """
        Description:    Creates a shame_list based on whoever is tagged 'Shame Listed' on
                        the server.
                        TODO
    """
    shame_list_channel = discord.utils.get(ctx.guild.text_channels, name='shame-list')
    await shame_list_channel.purge()  # clears entire shame-list channel
    members = await ctx.guild.fetch_members().flatten()
    role = get(ctx.guild.roles, name='Shame Listed')
    shame_list = '```The Shame List\n'
    for member in members:
        if role in member.roles:
            shame_list += (member.name + '\n')
    shame_list = shame_list + '```'
    await shame_list_channel.send(shame_list)

<<<<<<< HEAD
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
=======

@bot.command(name='checkin', help='Logs a user\'s participation\nUsage: !checkin (name) {date}\n\tDates should be in'
                                  'format YYYYXMMXDD where X is a delimeter: /|-:,; or whitespace')
async def checkin(ctx, name: str = None, date: str = None):
    """
    Updates check-in_dates.txt with a given user and a new checkin date.
    Date defaults to today according to system time.
    Name defaults to message author.
    Adds a new line entry if the specified user is not currently in the database.
    :param ctx: Calling Context
    :param name: Name, #, and discriminator of the user to checkin e.g. "Joe#1234"
    :param date: Date of checkin e.g. 2021-11-01
    :return: None
    """

    channel = ctx.message.channel

    command_channel = discord.utils.get(ctx.guild.text_channels, name='bot-tinkering')
    if channel is not command_channel:
        return

    members = await ctx.guild.fetch_members().flatten()
    date_format = "%Y-%m-%d"
    member_id = None

    if name is None:
        name = ctx.message.author.name + "#" + ctx.message.author.discriminator

    try:
        date_time = None
        if date is not None:
            delimiters = ["/", "|", "-", ":", ";", " "]
            for d in delimiters:
                date = date.replace(d, ",")
            date = date.strip()
            date_components = [int(c) for c in date.split(",")]
            if len(date_components) != 3:  # or False in [c.isnumeric() for c in date_components]
                raise InvalidArgument(
                    "Dates should be in format YYYYXMMXDD where X is a delimeter: /|-:,; or whitespace")
            date_time = dt(date_components[0], date_components[1], date_components[2])
            if date_time > dt.now():
                raise InvalidArgument("That date is in the future, I'm not stupid")
            date_time = date_time.strftime(date_format)
        else:
            date_time = dt.now().strftime(date_format)

        match_member = [m for m in members if m.name + "#" + m.discriminator == name]
        if len(match_member) > 0:
            member_id = match_member[0].id
        else:
            raise InvalidArgument("That user does not exist!")

        with open(filename, 'r+') as file:
            user_found = False

            data = ""

            for line in file:
                line_name = line.split()[0]
                line_date = line.split()[1]
                line_id = line.split()[2]
                if line_name == name and int(line_id) == member_id:
                    user_found = True
                    data += line_name + " " + date_time + " " + line_id + "\n"
                else:
                    data += line_name + " " + line_date + " " + line_id + "\n"
            if not user_found:
                data += name + " " + date_time + " " + str(member_id) + "\n"
            file.seek(0)
            file.write(data)
            file.truncate()
        await channel.send("Successfully checked in " + name + " for " + date_time)

    except InvalidArgument as ex:
        await channel.send(ex.args)

@bot.command(pass_context=True)
@commands.has_role("Badminton God")
async def update_shame_list(ctx):
    """
    Updates members of the server with the 'Shame Listed' role based on information found in
    the 'check-in_dates.txt' file. TODO
    :param ctx: Calling context
    :return: None
    """

    badminton_bot_id = 915347773522583603
    shame_listed_role_id = 915410173596663868

    command_channel = discord.utils.get(ctx.guild.text_channels, name='bot-commands')
    shame_listed_role = ctx.guild.get_role(shame_listed_role_id)
    if shame_listed_role is None:
        # this is a problem, lol
        return
    badminton_bot = ctx.guild.get_member(badminton_bot_id)
    can_manage_roles = badminton_bot.permissions_in(command_channel).manage_roles

    if not can_manage_roles:
        return

    with open(filename, 'r') as file:

        for line in file:
            member = await ctx.guild.fetch_member(int(line.split()[2]))
            date_components = [int(c) for c in line.split()[1].split('-')]
            date_time = dt(date_components[0], date_components[1], date_components[2])
            delta = dt.now() - date_time
            if delta.days >= 21:
                if shame_listed_role not in member.roles:
                    await member.add_roles(shame_listed_role, reason=member.name + " hates badminton and never attends! "
                                                                             "Everybody boo them!")
                    await ctx.channel.send(member.name + " hates badminton and never attends! "
                                                         "Everybody boo them!")
            else:
                if shame_listed_role in member.roles:
                    await member.remove_roles(shame_listed_role, reason=member.name + " has finally attended badminton! "
                                                                                "Everybody slow-clap.")
                    await ctx.channel.send(member.name + " has finally attended badminton! "
                                                         "Everybody slow-clap.")


bot.run(TOKEN)
>>>>>>> 18ab307e5b43ae2aba4e6abb53322ec582778845
