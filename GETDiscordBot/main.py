import os
import discord
from discord.ext import commands
from requests.api import get
from thegraph.getusageday import getusageday
from thegraph.getchart import getchart
from thegraph.getneedprediction import getneedprediction
from saveimage.saveimage import saveimage


discordtoken = os.getenv('DISCORD_TOKEN')

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
async def sendgetusageday(ctx, day):
    getusage = getusageday(day)

    if getusage['status'] == 'OK':
        response = ("GET Protocol usage report for date: {date}:\n"
                    "Amount of tickets (NFT's) created: {soldCount}\n"
                    "GET fuel spent: {spentFuel}\n"
                    "GET fuel reserved: {reservedFuel}\n"
                    "The average amount of GET reservered per (minted) ticket: {averageReservedPerTicket}"
                    ).format(
                        date=getusage['data']['date'],
                        soldCount=getusage['data']['soldCount'],
                        spentFuel=round(float(getusage['data']['spentFuel']), 2),
                        reservedFuel=round(float(getusage['data']['reservedFuel']), 2),
                        averageReservedPerTicket= round(float(getusage['data']['averageReservedPerTicket']), 2)
        )
    else:
        response = (
            "Error getting the GET Protocol usage for this day. Reason: {}"
        ).format(getusage['reason'])
    await ctx.send(response)


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
            title='GET usage last month',
            description="Here's the requested graph:",
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
            title='GET usage last quarter',
            description="Here's the requested graph:",
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
        response = ("Based on the data of the last 100 days, "
                    "the protocols needs:\n\n"
                    "{} GET Tokens per day\n"
                    "{} GET Tokens per month\n"
                    "{} GET Tokens per year\n\n"
                    "to run without problems.\n\n"
                    "The amount of GET tokens neccesary is subject to "
                    "change when the token price changes and is related to the "
                    "amount of tickets sold. "
                    "The GET token amount neccesary goes up if the price goes "
                    "down and visa versa. When more tickets are sold, more GET "
                    "tokens are neccesary.").format(
            getneeded['data']['getneedperday'],
            getneeded['data']['getneedpermonth'],
            getneeded['data']['getneedperyear']
        )
    else:
        response = (
            "Error getting the GET Protocol graph. Reason: {}"
        ).format(getneeded['reason'])

    await ctx.send(response)


bot.run(discordtoken)
