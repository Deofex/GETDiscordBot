import asyncio
import os
import discord
import schedule
import time
from discord.ext import commands
from requests.api import get
from thegraph.getusageday import getusageday
from thegraph.getchart import getchart
from thegraph.getneedprediction import getneedprediction
from saveimage.saveimage import saveimage


discordtoken = os.getenv('DISCORD_TOKEN')
report_channel_id = int(os.getenv('DAILY_REPORT_CHANNEL_ID'))

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    for guild in bot.guilds:
        print("{} is connected to the following guild:".format(bot.user))
        print("{} - {}".format(guild.name, guild.id))


@bot.command(
    name='getusageday',
    help='Gives a usage report for the GET Protocol for a certain day'
)
async def sendgetusageday(ctx, day = 'today'):
    getusage = getusageday(day)

    if getusage['status'] == 'OK':
        response = ("NFT tickets created: **{soldCount}**\n"
                    "Fuel reserved: **{reservedFuel} GET**\n"
                    "Fuel spent: **{spentFuel} GET**\n"
                    "Total sales volume: **${totalSalesVolume:,.2f}**\n"
                    "Average fuel reservered per (minted) ticket: **{averageReservedPerTicket} GET**"
                    ).format(
                        date=getusage['data']['date'],
                        soldCount=getusage['data']['soldCount'],
                        spentFuel=round(float(getusage['data']['spentFuel']), 2),
                        reservedFuel=round(float(getusage['data']['reservedFuel']), 2),
                        averageReservedPerTicket= round(float(getusage['data']['averageReservedPerTicket']), 2),
                        totalSalesVolume= float(getusage['data']['totalSalesVolume']),
        )
    else:
        response = (
            "Error getting the GET Protocol usage for this day. Reason: {}"
        ).format(getusage['reason'])
    embed = discord.Embed(title="GET Protocol Usage Report for {}".format(getusage['data']['date']), description=response, color=0x01C696)
    await ctx.send(embed=embed)


@bot.command(
    name='getmonthgraph',
    help='Gives a graph showing the GET Protocol usage in the last month'
)
async def sendmonthgraph(ctx):
    getgraphurl = getchart(31)

    if getgraphurl['status'] == 'OK':
        try:
            filename = 'temppic.png'
            saveimage(getgraphurl['url'], filename)
        except Exception as e:
            print("Can't save picture. Reason: {}".format(e.args[0]))
            getgraphurl['status'] = 'unabletosavepicture'
            getgraphurl['reason'] = 'Unable to save picture'

    if getgraphurl['status'] == 'OK':
        chartembed = discord.Embed(
            title='GET Usage Last Month',
            description="Here's the requested graph:",
            color=0x01C696
        )
        file = discord.File(filename, filename='chart.png')
        chartembed.set_image(url="attachment://chart.png")
        await ctx.send(file=file, embed=chartembed)
    else:
        response = (
            "Error getting the GET Protocol graph. Reason: {}"
        ).format(getgraphurl['reason'])
        await ctx.send(response)

@bot.command(
    name='getquartergraph',
    help='Gives a graph showing the GET Protocol usage in the last quarter'
)
async def sendmonthgraph(ctx):
    getgraphurl = getchart(92)

    if getgraphurl['status'] == 'OK':
        try:
            filename = 'temppic.png'
            saveimage(getgraphurl['url'], filename)
        except Exception as e:
            print("Can't save picture. Reason: {}".format(e.args[0]))
            getgraphurl['status'] = 'unabletosavepicture'
            getgraphurl['reason'] = 'Unable to save picture'

    if getgraphurl['status'] == 'OK':
        chartembed = discord.Embed(
            title='GET Usage Last Quarter',
            description="Here's the requested graph:",
            color=0x01C696
        )
        file = discord.File(filename, filename='chart.png')
        chartembed.set_image(url="attachment://chart.png")
        await ctx.send(file=file, embed=chartembed)
    else:
        response = (
            "Error getting the GET Protocol graph. Reason: {}"
        ).format(getgraphurl['reason'])
        await ctx.send(response)


@bot.command(
    name='gettokensprediction',
    help='Shows how much GET you need per month/year based on the last 100 days'
)
async def sendtokenspredeiction(ctx):
    getneeded = getneedprediction()
    if getneeded['status'] == 'OK':
        response = ("Based on the data of the last 100 days, the protocol needs an average of:\n\n"
                    "**{} GET** fuel per-day\n"
                    "**{} GET** fuel per-month\n"
                    "**{} GET** fuel per-year\n\n"
                    "*Note: the amount of fuel needed is subject to change dependent on price changes of GET, the point at which integrators top up, and amount of tickets sold. Check [the docs](https://docs.get-protocol.io/docs/token-economics-interactions) for more information on how this is caculated.*"
                    ).format(
            getneeded['data']['getneedperday'],
            getneeded['data']['getneedpermonth'],
            getneeded['data']['getneedperyear']
        )
    else:
        response = (
            "Error getting the GET Protocol graph. Reason: {}"
        ).format(getneeded['reason'])

    embed = discord.Embed(title="GET Protocol Usage Prediction", description=response, color=0x01C696)
    await ctx.send(embed=embed)

async def daily_report():
    getusage = getusageday('yesterday')
    description = (
        '**{} NFT tickets** sold and **{} events** created on the protocol in the last 24 hours, with a total sales volume of **${:,.2f}**.\n\n'
        'A total of **{:.2f} GET** was used as fuel.\n\n'
        '*See [usage charts](https://dashboard.get-community.com/charts). Learn more about [GET](https://www.get-protocol.io/token) and its usage as [fuel](https://docs.get-protocol.io/docs/token-economics-fuel).*'
    ).format(
        getusage['data']['soldCount'],
        getusage['data']['eventCount'],
        float(getusage['data']['totalSalesVolume']),
        float(getusage['data']['reservedFuel']),
    )
    embed = discord.Embed(title="GET Protocol Daily Report", description=description, color=0x01C696)
    await bot.wait_until_ready()
    channel = bot.get_channel(id=report_channel_id)
    await channel.send(embed=embed)


schedule.every().day.at("09:00").do(lambda: asyncio.create_task(daily_report()))

async def status_update():
    getusage = getusageday('today')
    status = ('{:.2f} GET used today').format(float(getusage['data']['reservedFuel']))
    await bot.wait_until_ready()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))

schedule.every(5).minutes.do(lambda: asyncio.create_task(status_update()))

async def scheduler():
    seconds = schedule.idle_seconds()
    while seconds is not None:
        if seconds > 0:
            await asyncio.sleep(seconds)
        schedule.run_pending()
        seconds = schedule.idle_seconds()

asyncio.ensure_future(status_update())
asyncio.ensure_future(scheduler())

# The bot must be ran last as this starts (& runs) the event loop.
bot.run(discordtoken)
