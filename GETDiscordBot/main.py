import asyncio
import os
import discord
import schedule
from discord.ext import commands
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
        print(f"{bot.user} is connected to the following guild:")
        print(f"{guild.name} - {guild.id}")


@bot.command(
    name='getusageday',
    help='Gives a usage report for the GET Protocol for a certain day'
)
async def sendgetusageday(ctx, day = 'today'):
    getusage = getusageday(day)

    if getusage['status'] == 'OK':
        sold_count=getusage['data']['soldCount']
        spent_fuel=round(float(getusage['data']['spentFuel']), 2)
        reserved_fuel=round(float(getusage['data']['reservedFuel']), 2)
        average_reserved_per_ticket= round(
            float(getusage['data']['averageReservedPerTicket']), 2)
        total_sales_volume= float(getusage['data']['totalSalesVolume'])
        response = (f"NFT tickets created: **{sold_count}**\n"
                    f"Fuel reserved: **{reserved_fuel} GET**\n"
                    f"Fuel spent: **{spent_fuel} GET**\n"
                    f"Total sales volume: **${total_sales_volume:,.2f}**\n"
                    f"Average fuel reservered per (minted) ticket: "
                    f"**{average_reserved_per_ticket} GET**"
                    )
    else:
        response = \
            f"Error getting the GET Protocol usage for this day. Reason: {getusage['reason']}"
    embed = discord.Embed(
        title=f"GET Protocol Usage Report for {getusage['data']['date']}",
        description=response,
        color=0x01C696)
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
        except Exception as ex:
            print(f"Can't save picture. Reason: {ex.args[0]}")
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
        response = f"Error getting the GET Protocol graph. Reason: {getgraphurl['reason']}"
        await ctx.send(response)

@bot.command(
    name='getquartergraph',
    help='Gives a graph showing the GET Protocol usage in the last quarter'
)
async def sendquartergraph(ctx):
    getgraphurl = getchart(92)

    if getgraphurl['status'] == 'OK':
        try:
            filename = 'temppic.png'
            saveimage(getgraphurl['url'], filename)
        except Exception as ex:
            print(f"Can't save picture. Reason: {ex.args[0]}")
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
        response = f"Error getting the GET Protocol graph. Reason: {getgraphurl['reason']}"
        await ctx.send(response)


@bot.command(
    name='gettokensprediction',
    help='Shows how much GET you need per month/year based on the last 100 days'
)
async def sendtokenspredeiction(ctx):
    getneeded = getneedprediction()
    if getneeded['status'] == 'OK':
        response = ("Based on the data of the last 100 days, the protocol needs an average of:\n\n"
                    f"**{getneeded['data']['getneedperday']} GET** fuel per-day\n"
                    f"**{ getneeded['data']['getneedpermonth']} GET** fuel per-month\n"
                    f"**{getneeded['data']['getneedperyear']} GET** fuel per-year\n\n"
                    "*Note: the amount of fuel needed is subject to change dependent on price "
                    "changes of GET, the point at which integrators top up, and amount of tickets "
                    "sold. Check "
                    "[the docs](https://docs.get-protocol.io/docs/token-economics-interactions) "
                    "for more information on how this is caculated.*"
                    )
    else:
        response =  f"Error getting the GET Protocol graph. Reason: {getneeded['reason']}"

    embed = discord.Embed(
        title="GET Protocol Usage Prediction",
        description=response,
        color=0x01C696
        )
    await ctx.send(embed=embed)

async def daily_report():
    getusage = getusageday('yesterday')
    total_sales_volume =  float(getusage['data']['totalSalesVolume'])
    reserved_fuel = float(getusage['data']['reservedFuel'])
    description = (
        f"**{getusage['data']['soldCount']} NFT tickets** sold and "
        f"**{getusage['data']['eventCount']} events** created on the protocol in the last 24 hours,"
        f" with a total sales volume of **${total_sales_volume:,.2f}**.\n\n"
        f"A total of **{reserved_fuel:.2f} GET** was used as fuel.\n\n"
        "*See [usage charts](https://dashboard.get-community.com/charts). Learn more about "
        "[GET](https://www.get-protocol.io/token) and its usage as "
        "[fuel](https://docs.get-protocol.io/docs/token-economics-fuel).*"
    )
    embed = discord.Embed(
        title="GET Protocol Daily Report",
        description=description,
        color=0x01C696
        )
    await bot.wait_until_ready()
    channel = bot.get_channel(id=report_channel_id)
    await channel.send(embed=embed)


schedule.every().day.at("09:00").do(lambda: asyncio.create_task(daily_report()))

async def status_update():
    getusage = getusageday('today')
    reserved_fuel = float(getusage['data']['reservedFuel'])
    status = f"{reserved_fuel:.2f} GET used today"
    await bot.wait_until_ready()
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name=status))

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
