import os
import discord
import re
import datetime as dt
from discord.errors import InvalidArgument
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
MAX_NAME_LENGTH = 32

# allows guild.members to display all members
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)

filename = "check-in_dates.txt"


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

    time = time.upper()
    channel = discord.utils.get(ctx.guild.text_channels, name='bot-tinkering')  # different name
    regex = re.compile(r'((0?[1-9]|1[0-2]):([0-5]\d)([AP]\.?M\.?))')
    is_match = regex.match(time.strip())
    try:
        if is_match is None:
            raise InvalidArgument('InvalidArgument: Argument must be in the format of HH:MM(PM|AM)')
        else:
            await command_channel.send(
                'everyone Hello edgelords! Badminton will be played at ' + is_match.group(0) + ' today.')
    except InvalidArgument as ex:
        await command_channel.send(ex.args)
        return


@on_announce.error
async def on_announce_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("MissingRequiredArguement: You're missing a time, dummy")  # TODO add insulting name


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


@bot.command(name='checkin', help='Logs a user\'s participation\nUsage: !checkin (name) {date}\n\tDates should be in'
                                  'format YYYYXMMXDD where X is a delimeter: /|-:,; or whitespace')
async def checkin(ctx, name: str, date: str = None):
    """
    Updates check-in_dates.txt with a given user and a new checkin date. date defaults to today according to system
    time. Adds a new line entry
    :param ctx: Calling Context
    :param name: Name, #, and discriminator of the user to checkin e.g. "Joe#1234"
    :param date: Date of checkin e.g. 2021-11-01
    :return: None
    """

    channel = ctx.message.channel

    command_channel = discord.utils.get(ctx.guild.text_channels, name='bot-commands')
    if channel is not command_channel:
        return

    members = await ctx.guild.fetch_members().flatten()
    date_format = "%Y-%m-%d"

    try:
        date_time = None
        if date is not None:
            delimiters = ["/", "|", "-", ":", ";", " "]
            for d in delimiters:
                date = date.replace(d, ",")
            date = date.strip()
            date_components = [int(c) for c in date.split(",")]
            if len(date_components) is not 3:  # or False in [c.isnumeric() for c in date_components]
                raise InvalidArgument(
                    "Dates should be in format YYYYXMMXDD where X is a delimeter: /|-:,; or whitespace")
            date_time = dt.datetime(date_components[0], date_components[1], date_components[2])
            if date_time > dt.datetime.now():
                raise InvalidArgument("That date is in the future, I'm not stupid")
            date_time = date_time.strftime(date_format)
        else:
            date_time = dt.datetime.now().strftime(date_format)

        if name not in [member.name + "#" + member.discriminator for member in members]:
            raise InvalidArgument("That user does not exist!")

        with open(filename, 'r+') as file:
            user_found = False

            data = ""

            for line in file:
                line_name = line.split()[0]
                line_date = line.split()[1]
                if line_name == name:
                    user_found = True
                    data += line_name + " " + date_time + "\n"
                else:
                    data += line_name + " " + line_date + "\n"
            if not user_found:
                data += name + " " + date_time + "\n"
            file.seek(0)
            file.write(data)
            file.truncate()
        await channel.send("Successfully checked in " + name + " for " + date_time)

    except InvalidArgument as ex:
        await channel.send(ex.args)


async def update_shame_list(ctx):
    """
    Updates members of the server with the 'Shame Listed' role based on information found in
    the 'check-in_dates.txt' file. TODO
    :param ctx: Calling context
    :return: None
    """
    with open(filename, 'r'):
        pass


bot.run(TOKEN)
