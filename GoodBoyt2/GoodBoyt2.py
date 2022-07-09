import discord
from discord.ext.commands import MemberConverter
from discord.ext import commands
bot = commands.Bot(command_prefix="~")
@bot.command()
async def ttt(ctx):
    spaces = [1,2,3,4,5,6,7,8,9]
    state = ["-","-","-","-","-","-","-","-","-"]
    symbols = ["x","o"]
    x = None
    o = None
    xWins = False
    oWins = False
    await ctx.author.send("Type the name of the user you want to play against with the # and 4 digit number.")
    def check(m):
        return m.author==ctx.author and m.channel.type==discord.ChannelType.private
    oppMsg = await bot.wait_for("message",check=check)
    opponent = await MemberConverter().convert(ctx,oppMsg.content)
    await ctx.author.send("Are you x or o?")
    def check2(m):
        return m.author==ctx.author and m.channel.type==discord.ChannelType.private and m.content.lower() in symbols
    symbolMsg = await bot.wait_for("message",check=check2)
    if symbolMsg.content=="x":
        x = ctx.author
        o = opponent
    else:
        x = opponent
        o = ctx.author
        await ctx.channel.send("<@"+str(opponent.id)+"> <@"+str(ctx.author.id)+"> challenged you to Tic-Tac-Toe!")
        await ctx.channel.send("---|---|---\n---|---|---")
    while True:
        def check3(m):
            return m.author==x and m.channel==ctx.channel and int(m.content) in spaces
        xMsg = await bot.wait_for("message",check=check3)
        state[int(xMsg.content)-1] = "x"
        spaces.remove(int(xMsg.content))
        await ctx.channel.send(state[0]+"  "+state[1]+"  "+state[2]+"\n"+state[3]+"  "+state[4]+"  "+state[5]+"\n"+state[6]+"  "+state[7]+"  "+state[8])
        if len(spaces)==0:
            await ctx.channel.send("The game ended in a draw.")
            return
        elif state[0]==state[1]==state[2]=="x" or state[3]==state[4]==state[5]=="x" or state[6]==state[7]==state[8]=="x":
            await ctx.channel.send("<@"+str(x.id)+">"+" matched horizontally! GG.")
            return
        elif state[0]==state[3]==state[6]=="x" or state[1]==state[4]==state[7]=="x" or state[3]==state[5]==state[8]=="x":
            await ctx.channel.send("<@"+str(x.id)+">"+" matched vertically! GG.")
            return
        elif state[0]==state[4]==state[8]=="x" or state[2]==state[4]==state[6]=="x":
            await ctx.channel.send("<@"+str(x.id)+">"+" matched diagonally! GG.")
            return
        elif state[0]==state[1]==state[2]=="o" or state[3]==state[4]==state[5]=="o" or state[6]==state[7]==state[8]=="o":
            await ctx.channel.send("<@"+str(o.id)+">"+" matched horizontally! GG.")
            return
        elif state[0]==state[3]==state[6]=="o" or state[1]==state[4]==state[7]=="o" or state[3]==state[5]==state[8]=="o":
            await ctx.channel.send("<@"+str(o.id)+">"+" matched vertically! GG.")
            return
        elif state[0]==state[4]==state[8]=="o" or state[2]==state[4]==state[6]=="o":
            await ctx.channel.send("<@"+str(o.id)+">"+" matched diagonally! GG.")
            return
        def check4(m):
           return m.author==o and m.channel==ctx.channel and int(m.content) in spaces
        oMsg = await bot.wait_for("message",check=check4)
        state[int(oMsg.content)-1] = "o"
        spaces.remove(int(oMsg.content))
        await ctx.channel.send(state[0]+"  "+state[1]+"  "+state[2]+"\n"+state[3]+"  "+state[4]+"  "+state[5]+"\n"+state[6]+"  "+state[7]+"  "+state[8])
        if len(spaces)==0:
            await ctx.channel.send("The game ended in a draw.")
            return
        elif state[0]==state[1]==state[2]=="x" or state[3]==state[4]==state[5]=="x" or state[6]==state[7]==state[8]=="x":
            await ctx.channel.send("<@"+str(x.id)+">"+" matched horizontally! GG.")
            return
        elif state[0]==state[3]==state[6]=="x" or state[1]==state[4]==state[7]=="x" or state[3]==state[5]==state[8]=="x":
            await ctx.channel.send("<@"+str(x.id)+">"+" matched vertically! GG.")
            return
        elif state[0]==state[4]==state[8]=="x" or state[2]==state[4]==state[6]=="x":
            await ctx.channel.send("<@"+str(x.id)+">"+" matched diagonally! GG.")
            return
        elif state[0]==state[1]==state[2]=="o" or state[3]==state[4]==state[5]=="o" or state[6]==state[7]==state[8]=="o":
            await ctx.channel.send("<@"+str(o.id)+">"+" matched horizontally! GG.")
            return
        elif state[0]==state[3]==state[6]=="o" or state[1]==state[4]==state[7]=="o" or state[3]==state[5]==state[8]=="o":
            await ctx.channel.send("<@"+str(o.id)+">"+" matched vertically! GG.")
            return
        elif state[0]==state[4]==state[8]=="o" or state[2]==state[4]==state[6]=="o":
            await ctx.channel.send("<@"+str(o.id)+">"+" matched diagonally! GG.")
            return
bot.run("OTIyMjcxNzI2NjAyMTc4NTkw.GmAxDD.aA0v-DasVSYrGmXh3Zr2z3nK7QMa_7ny0du4RY")




