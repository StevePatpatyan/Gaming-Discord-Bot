from asyncio import wait_for
from distutils.command.check import check
import discord
from discord.ext import commands
from discord.ext.commands import MemberConverter
import os
import random
from discord import FFmpegPCMAudio
from dotenv import load_dotenv
import time
import enchant
bee = open("BeeMovieScript.txt","r").read().split("\n")
token = "OTIyMjcxNzI2NjAyMTc4NTkw.G_FvkE.t3LvLJTKi0yLHKyHvi-t1Xe3FS-sY34dczk85A"
bot = commands.Bot(command_prefix="~")
@bot.event
async def on_message(message):
    #whenever david types, posts entire bee movie script
    #if message.author.id == 724084272872423544:
        #for line in bee:
            #await message.channel.send(line)
    if message.author == bot.user:
        return
    #says h back 
    if message.content=="h":
        await message.channel.send("h")
    await bot.process_commands(message)
    #plays a user's assigned audio when joining vc
@bot.event
async def on_voice_state_update(member,before,after):
    ids = [274710108284649476,750138259719323768,493517199277948959,724084272872423544,745784946811207811,740776084483866644]
    audios = {
        274710108284649476: "WelcomeChannelMember.wav",
        750138259719323768: "AlexWelcome.wav",
        493517199277948959: "MikeWelcome.wav",
        724084272872423544: "DavidWelcome1.wav",
        745784946811207811: "VantehWelcome.wav",
        740776084483866644: "ArmanWelcome.wav"
        }
    server = member.guild
    user = member.id
    if before.channel is None and after.channel is not None and member.id in ids:
        open(str(server)+"audioplaying.txt","a").write(str(user)+",")
        isPlaying = open(str(server)+"audioplaying.txt","r").read().split(",")
        while isPlaying[0] != str(user):
            isPlaying = open(str(server)+"audioplaying.txt","r").read().split(",")
            time.sleep(1)
        source = FFmpegPCMAudio(audios[user])
        vc = await member.voice.channel.connect()
        vc.play(source)
        time.sleep(3) 
        await vc.disconnect(force=True)
        #if user == 724084272872423544:
            #await member.move_to(None)
        isPlaying.remove(str(user))
        open(str(server)+"audioplaying.txt","w").writelines(isPlaying)
        return
    #last to first word game
@bot.event
async def on_message(message):
    player = message.author.id
    channel = message.channel
    word = message.content
    history = await channel.history(limit=10).flatten()
    prev = history[1].content
    wordCheck = enchant.Dict("en_US")
    alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    if player==922271726602178590:
        return
    if str(bot.get_channel(channel.id)) != "last-to-first":
        return
    if player==history[1].author.id:
        await message.delete()
        return
    if wordCheck.check(word) == False:
        await message.channel.send("That word doesn't exist! Creating new letter to go off of...")
        await message.channel.send(alphabet[random.randint(0,25)])
        return
    if list(word)[0]!=list(prev)[len(list(prev))-1]:
        await message.channel.send("That word doesn't start with the right letter! Creating new letter to go off of...")
        await message.channel.send(alphabet[random.randint(0,25)])
        return
    if word==history[9].content:
        await message.channel.send("You can't repeat the same word as last time! Creating new letter to go off of...")
        await message.channel.send(alphabet[random.randint(0,25)])
        return
        #higher or lower game
@bot.command()
async def hol(message):
    def check(m):
        return m.author==message.author and m.channel == message.channel and m.content.isdigit()
    await message.channel.send("What is the max number?")
    maxNumMsg = await bot.wait_for("message",check=check)
    maxNum = maxNumMsg.content
    num = random.randint(1,int(maxNum))
    counter = 0
    def check2(m):
            return m.author == message.author and m.channel == message.channel and m.content.lower() in ["higher", "lower"]
    while True:
        await message.channel.send(str(num)+": Higher or Lower?")
        msg = await bot.wait_for("message",check=check2)
        nextNum = random.randint(1,int(maxNum))
        if msg.content.lower()=="higher" and nextNum>= num or msg.content.lower()=="lower" and nextNum<=num:
            counter += 1
            num = nextNum
        else:
            await message.channel.send(str(nextNum)+": Game over. Your score is "+ str(counter)+". GG.")
            break
            #join +leave voice channel
@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        vc = await channel.connect()
        source = FFmpegPCMAudio("WelcomeChannelMember.wav")
        vc.play(source)
@bot.command()
async def dip(ctx):
   if ctx.author.voice and ctx.voice_client:
       await ctx.voice_client.disconnect()
       #hangman
@bot.command()
async def hangman(ctx):
    channel = ctx.channel
    await ctx.author.send("Type your word.")
    def check(m):
            return m.author == ctx.author and m.channel.type == discord.ChannelType.private
    msgMsg = await bot.wait_for("message",check=check)
    msg = msgMsg.content
    await ctx.author.send("Who would you like to allow to guess your word. Type usernames without @ and separate them with a space.")
    challengerMsg = await bot.wait_for("message", check=check)
    challengers = challengerMsg.content.split(" ")
    lttrs = list(msg)
    filled = []
    lives = 5
    for chars in msg:
        if (chars==" "):
            filled.append(" ")
        else:
            filled.append("-")
    def check2(m):
        return m.channel == ctx.channel and len(m.content) == 1 and str(m.author) in challengers
    for challenger in challengers:
        user = await MemberConverter().convert(ctx,challenger)
        await ctx.channel.send("<@"+str(user.id)+">")
    await ctx.channel.send("<@"+str(ctx.author.id)+"> challenged you to Hangman.")
    while True:
        guessedRight = False
        notFilled = False
        response = " ".join(filled)
        await ctx.channel.send(response)
        guessMsg = await bot.wait_for("message",check=check2)
        guess = guessMsg.content
        for y in range(len(lttrs)):
            if guess.lower() == lttrs[y].lower():
                filled[y] = lttrs[y]
                guessedRight = True
        if guessedRight == False:
            lives-= 1
            await ctx.channel.send("There are no "+guess.lower()+"'s in the word. You have "+str(lives)+" lives left")
        for z in range(len(filled)):
            if filled[z] == "-":
                notFilled = True
        if notFilled == False:
            response = " ".join(filled)
            await ctx.channel.send(response+"\nYou guessed <@"+str(ctx.author.id)+">'s word!")
            break
        if lives==0:
            await ctx.channel.send("You ran out of lives. The word was "+msg+". GG.")
            break
        #says who the commander is
@bot.command()
async def me(ctx):
        await ctx.channel.send(ctx.author)
#sign up for economy of server
@bot.command()
async def suEcon(ctx):
    signedUp = False
    server = ctx.guild
    user = ctx.author.id
    users = open(str(server)+".txt").read().split("\n")
    init = open(str(server)+"initialbal.txt","r").read()
    for people in users:
        if people==str(user):
            signedUp = True
    if signedUp == False:
        open(str(server)+".txt","a").write(str(user)+"\n")
        if len(open(str(server)+"initialbal.txt","r").read().split("\n")) == 1:
            open(str(server)+"balance.txt","a").write(init+"\n")
        else:
            open(str(server)+"balance.txt","a").write("0\n")
        await ctx.channel.send(ctx.author.mention+" signed up successfully!")
    else:
        await ctx.channel.send(ctx.author.mention+" is already signed up.")
#check your balance of economy
@bot.command()
async def balance(ctx):
    signedUp = False
    server = ctx.guild
    user = ctx.author.id
    users = open(str(server)+".txt","r").read().split("\n")
    balances = open(str(server)+"balance.txt","r").read().split("\n")
    for people in users:
        if people==str(user):
            signedUp = True
    if signedUp == True:
        for x in range(len(users)):
            if users[x] == str(user):
                await ctx.channel.send(ctx.author.mention+" Your balance is "+balances[x]+".")
    else:
        await ctx.channel.send(ctx.author.mention+" You are not signed up. Use ~suEcon to sign up to the server's economy.")
#change initial value of balance given to user
@bot.command()
@commands.has_permissions(administrator=True)
async def initEcon(ctx):
    server = ctx.guild
    msg = ctx.message.content.replace("~initEcon ","",1)
    init = open(str(server)+"initialbal.txt","w").write(msg)
    await ctx.channel.send(ctx.author.mention+" changed initial balance to "+msg+".")
#make bets with econ system
@bot.command()
@commands.has_permissions(administrator = True)
async def addBets(ctx):
    server = ctx.guild
    bets = open(str(server)+"bets.txt","a")
    options = open(str(server)+"betoptions.txt","a")
    wagers = open(str(server)+"betwagers.txt","a")
    def check(m):
        return m.author.guild_permissions.administrator and m.channel == ctx.channel and m.author != bot.user
    await ctx.channel.send("Enter the bet.")
    betMsg = await bot.wait_for("message",check=check)
    await ctx.channel.send("Enter the options for the bet. Separate each option with a comma, no space.")
    optionsMsg = await bot.wait_for("message",check=check)
    await ctx.channel.send("Enter how much the bet is worth.")
    wagerMsg = await bot.wait_for("message",check=check)
    bets.write(betMsg.content+"\n")
    options.write(optionsMsg.content+"\n")
    wagers.write(wagerMsg.content+"\n")
    await ctx.channel.send("Successfullly created bet.")
@bot.command()
async def viewBets(ctx):
    server = ctx.guild

    bets = open(str(server)+"bets.txt","r").read().split("\n")
    options = open(str(server)+"betoptions.txt","r").read().split("\n")
    wagers = open(str(server)+"betwagers.txt","r").read().split("\n")
    for x in range(len(bets)-1):
        await ctx.channel.send("**Bet "+str(x+1)+":**\n"+bets[x]+"\n"+options[x]+"\n"+wagers[x])
#wager available bets
@bot.command()
async def bet(ctx):
    signedUp = False
    server = ctx.guild
    user = ctx.author.id
    users = open(str(server)+".txt","r").read().split("\n")
    balances = open(str(server)+"balance.txt","r").read().split("\n")
    bets = open(str(server)+"bets.txt","r").read().split("\n")
    options = open(str(server)+"betoptions.txt","r").read().split("\n")
    wagers = open(str(server)+"betwagers.txt","r").read().split("\n")
    pendingBets = open(str(server)+"pendingbets.txt","r").read().split("\n")
    pendingOptions = open(str(server)+"pendingoptions.txt","r").read().split("\n")
    betsList = []
    optionsList = []
    if len(bets) == 1:
        await ctx.channel.send("There are no active bets.")
        return
    for p in users:
        optionsList.append("")
        betsList.append("")
    for b in range(len(betsList)):
        if b < len(pendingBets):
            betsList[b] = pendingBets[b]
    for o in range(len(optionsList)):
        if o < len(pendingOptions):
            optionsList[o] = pendingOptions[o]
    for x in range(len(users)):
        if users[x]==str(user):
            signedUp = True
            userNum = x
    if signedUp == True:
        def check(m):
            return m.author==ctx.author and int(m.content) <= len(bets)-1
        await ctx.channel.send("Enter the bet number.")
        betMsg = await bot.wait_for("message",check=check)
        betNum = int(betMsg.content)
        if betMsg.content in betsList[userNum].split(","):
            await ctx.channel.send("You already placed a bet on **"+bets[betNum-1]+"**")
            return
        def check2(m):
            return m.author==ctx.author and m.content in options[betNum-1].split(",")
        selectedBet = bets[betNum-1]
        if int(balances[userNum])>=int(wagers[betNum-1]):
            await ctx.channel.send("**Bet: "+selectedBet+"**\nYou must wager "+wagers[betNum-1]+". What option are you betting on?\n"+options[betNum-1])
            optionMsg  = await bot.wait_for("message",check=check2)
            betsList[userNum] += str(betNum)+","
            pendingBets = open(str(server)+"pendingbets.txt","w")
            pendingBets.writelines(betsList)
            optionsList[userNum] += optionMsg.content+","
            pendingOptions = open(str(server)+"pendingoptions.txt","w")
            pendingOptions.writelines(optionsList)
            balances[userNum] = str(int(balances[userNum]) - int(wagers[betNum-1]))
            open(str(server)+"balance.txt","w").write("\n".join(balances))
            await ctx.channel.send("Successfully bet on "+optionMsg.content+". Your current balance is now "+balances[userNum]+".")
        else:
            await ctx.channel.send("You don't have enough money to bet on **"+selectedBet+"**")
    else:
        await ctx.channel.send("You are not signed for the economy. Use ~suEcon to sign up.")
@bot.command()
@commands.has_permissions(administrator = True)
async def result(ctx):
    server = ctx.guild
    winners = []
    users = open(str(server)+".txt","r").read().split("\n")
    balances = open(str(server)+"balance.txt","r").read().split("\n")
    bets = open(str(server)+"bets.txt","r").read().split("\n")
    options = open(str(server)+"betoptions.txt","r").read().split("\n")
    wagers = open(str(server)+"betwagers.txt","r").read().split("\n")
    pendingBets = open(str(server)+"pendingbets.txt","r").read().split("\n")
    pendingOptions = open(str(server)+"pendingoptions.txt","r").read().split("\n")
    def check(m):
        return m.author==ctx.author and int(m.content) <= len(bets)-1
    await ctx.channel.send("What bet will end?")
    betMsg = await bot.wait_for("message",check=check)
    betNum = int(betMsg.content) - 1
    def check2(m):
        return m.author==ctx.author and m.content in options[betNum].split(",")
    await ctx.channel.send("What option won for **"+bets[betNum]+"**")
    optionMsg = await bot.wait_for("message",check=check2)
    option = optionMsg.content
    foundBetter = False
    for x in range(len(pendingBets)):
        for y in range(len(pendingBets[x].split(","))):
            if pendingBets[x].split(",")[y] == str(betNum+1):
                if pendingOptions[x].split(",")[y] == option:
                    balances[x] = str(int(balances[x]) + int(wagers[betNum])*2)
                    open(str(server)+"balance.txt","w").write("\n".join(balances))
                    removeX = x
                    removeY = y
                    foundBetter = True
                    winners.append("<@"+users[x]+">")
    if foundBetter == True:
        userBets = pendingBets[removeX].split(",")
        userBets.remove(userBets[removeY])
        pendingBets[removeX] = ",".join(userBets)
        userOptions = pendingOptions[removeX].split(",")
        userOptions.remove(userOptions[removeY])
        pendingOptions[removeX] = ",".join(userOptions)
        open(str(server)+"pendingbets.txt","w").write("\n".join(pendingBets))
        open(str(server)+"pendingoptions.txt","w").write("\n".join(pendingOptions))
        pendingBets = open(str(server)+"pendingbets.txt","r").read().split("\n")
        pendingOptions = open(str(server)+"pendingoptions.txt","r").read().split("\n")
    if len(winners) > 1:
        await ctx.channel.send("The result of **"+bets[betNum]+"** is **"+option+"**. "+" ".join(winners)+" won "+wagers[betNum]+" each!")
    elif len(winners) == 1:
         await ctx.channel.send("The result of **"+bets[betNum]+"** is **"+option+"**. "+" ".join(winners)+" won "+wagers[betNum]+"!")
    else:
         await ctx.channel.send("The result of **"+bets[betNum]+"** is **"+option+"**. Nobody won...")
    bets.remove(bets[betNum])
    options.remove(options[betNum])
    wagers.remove(wagers[betNum])
    open(str(server)+"bets.txt","w").write("\n".join(bets))
    open(str(server)+"betoptions.txt","w").write("\n".join(options))
    open(str(server)+"betwagers.txt","w").write("\n".join(wagers))
    if len(pendingBets) > 1:
        for pends in range(len(pendingBets)):
            for bs in range(len(pendingBets[pends].split(","))):
                if pendingBets[pends].split(",")[bs] != "":
                    if int(pendingBets[pends].split(",")[bs]) > betNum+1:
                        numbers = pendingBets[pends].split(",")
                        print(numbers[bs])
                        numbers[bs] = str(int(numbers[bs]) - 1)
            pendingBets[pends] = ",".join(numbers)
        open(str(server)+"pendingbets.txt","w").write("\n".join(pendingBets))
        #user views their pending bets
@bot.command()
async def myBets(ctx):
    server = ctx.guild
    userId = str(ctx.author.id)
    signedUp = True
    bets = open(str(server)+"bets.txt","r").read().split("\n")
    wagers = open(str(server)+"betwagers.txt","r").read().split("\n")
    users = open(str(server)+".txt","r").read().split("\n")
    pendingBets = open(str(server)+"pendingbets.txt","r").read().split("\n")
    pendingOptions = open(str(server)+"pendingoptions.txt","r").read().split("\n")
    for x in range(len(users)):
        if userId==users[x]:
            userNum = x
            signedUp = True
    if signedUp == True:
        userBets = pendingBets[userNum].split(",")
        if len(userBets) == 1:
            await ctx.channel.send("You do not have any pending bets.")
        else:
            msg = []
            for pends in range(len(userBets)):
                betNum = int(pendingBets[pends]) - 1
                msg.append("For **"+bets[betNum]+"**, You bet on **"+pendingOptions[pends]+"** for **"+wagers[betNum]+".")
            await ctx.channel.send("\n".join(msg))
    else:
        await ctx.channel.send("You are not signed up for the economy system. Type ~suEcon to register.")
        #tic tac toe
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
    if symbolMsg.content.lower()=="x":
        x = ctx.author
        o = opponent
    elif symbolMsg.content.lower()=="o":
        x = opponent
        o = ctx.author
    await ctx.channel.send("<@"+str(opponent.id)+"> <@"+str(ctx.author.id)+"> challenged you to Tic-Tac-Toe! It's <@"+str(x.id)+">'s turn.")
    await ctx.channel.send("---|---|---\n---|---|---")
    while True:
        def check3(m):
            return m.author==x and m.channel==ctx.channel and m.content.isdigit() and int(m.content) in spaces
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
           return m.author==o and m.channel==ctx.channel and m.content.isdigit() and int(m.content) in spaces
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
        #blackjack with economy money
@bot.command()
async def bj(ctx):
    values = {
        "<:AceOfSpades:996659877827072010>":11, "<:AceOfClubs:996659874559709224>":11, "<:AceOfHearts:996659876786868274>":11, "<:AceOfDiamonds:996659875717328936>":11,
        "<:2OfSpades:996659834776723476>":2, "<:2OfClubs:996659831303835679>":2, "<:2OfHearts:996659833442938971>":2, "<:2OfDiamonds:996659832360804472>":2,
        "<:3OfSpades:996659839801491497>":3, "<:3OfClubs:996659835460403261>":3, "<:3OfHearts:996659838337683507>":3,"<:3OfDiamonds:996659836735475765>":3,
        "<:4OfSpades:996659844167778335>":4, "<:4OfClubs:996659841043013695>":4, "<:4OfHearts:996659843068862514>":4, "<:4OfDiamonds:996659842120962138>":4,
        "<:5OfSpades:996659849536487485>":5, "<:5OfClubs:996659845346365582>":5, "<:5OfHearts:996659848034910248>":5, "<:5OfDiamonds:996659846709510256>":5,
        "<:6OfSpades:999920805515374622>":6, "<:6OfClubs:996659852195676160>":6, "<:6OfHearts:996659853122613279>":6, "<:6OfDiamonds:996659850731847721>":6,
        "<:7OfSpades:996659858147385364>":7, "<:7OfClubs:996659854498332773>":7, "<:7OfHearts:996659856968777878>":7, "<:7OfDiamonds:996659855563702332>":7,
        "<:8OfSpades:996659862714986536>":8, "<:8OfClubs:996659859124662272>":8, "<:8OfHearts:996659861557358623>":8, "<:8OfDiamonds:996659860370366474>":8,
        "<:9OfSpades:996659868113055804>":9, "<:9OfClubs:996659863981658143>":9, "<:9OfHearts:996659867093848124>":9, "<:9OfDiamonds:996659865860722738>":9,
        "<:10OfSpades:996659873326575716>":10, "<:10OfClubs:996659869149040690>":10, "<:10OfHearts:996659872093446185>":10, "<:10OfDiamonds:996659870407348234>":10,
        "<:JackOfSpades:996659883178995732>":10, "<:JackOfClubs:996659878833700915>":10, "<:JackOfHearts:996659882071691274>":10, "<:JackOfDiamonds:996659880133939220>":10,
        "<:QueenOfSpades:996993577118879774>":10, "<:QueenOfClubs:996659890170900541>":10, "<:QueenOfHearts:996993575491481654>":10, "<:QueenOfDiamonds:996659891882168371>":10,
        "<:KingOfSpades:996659888505753662>":10, "<:KingOfClubs:996659884290494544>":10, "<:KingOfHearts:996659886781906996>":10, "<:KingOfDiamonds:996659885511016469>":10
        }
    diffVals = { "<:AceOfSpades:996659877827072010>":1, "<:AceOfClubs:996659874559709224>":1, "<:AceOfHearts:996659876786868274>":1, "<:AceOfDiamonds:996659875717328936>":1,
        "<:2OfSpades:996659834776723476>":2, "<:2OfClubs:996659831303835679>":2, "<:2OfHearts:996659833442938971>":2, "<:2OfDiamonds:996659832360804472>":2,
        "<:3OfSpades:996659839801491497>":3, "<:3OfClubs:996659835460403261>":3, "<:3OfHearts:996659838337683507>":3,"<:3OfDiamonds:996659836735475765>":3,
        "<:4OfSpades:996659844167778335>":4, "<:4OfClubs:996659841043013695>":4, "<:4OfHearts:996659843068862514>":4, "<:4OfDiamonds:996659842120962138>":4,
        "<:5OfSpades:996659849536487485>":5, "<:5OfClubs:996659845346365582>":5, "<:5OfHearts:996659848034910248>":5, "<:5OfDiamonds:996659846709510256>":5,
        "<:6OfSpades:999920805515374622>":6, "<:6OfClubs:996659852195676160>":6, "<:6OfHearts:996659853122613279>":6, "<:6OfDiamonds:996659850731847721>":6,
        "<:7OfSpades:996659858147385364>":7, "<:7OfClubs:996659854498332773>":7, "<:7OfHearts:996659856968777878>":7, "<:7OfDiamonds:996659855563702332>":7,
        "<:8OfSpades:996659862714986536>":8, "<:8OfClubs:996659859124662272>":8, "<:8OfHearts:996659861557358623>":8, "<:8OfDiamonds:996659860370366474>":8,
        "<:9OfSpades:996659868113055804>":9, "<:9OfClubs:996659863981658143>":9, "<:9OfHearts:996659867093848124>":9, "<:9OfDiamonds:996659865860722738>":9,
        "<:10OfSpades:996659873326575716>":10, "<:10OfClubs:996659869149040690>":10, "<:10OfHearts:996659872093446185>":10, "<:10OfDiamonds:996659870407348234>":10,
        "<:JackOfSpades:996659883178995732>":11, "<:JackOfClubs:996659878833700915>":11, "<:JackOfHearts:996659882071691274>":11, "<:JackOfDiamonds:996659880133939220>":11,
        "<:QueenOfSpades:996993577118879774>":12, "<:QueenOfClubs:996659890170900541>":12, "<:QueenOfHearts:996993575491481654>":12, "<:QueenOfDiamonds:996659891882168371>":12,
        "<:KingOfSpades:996659888505753662>":13, "<:KingOfClubs:996659884290494544>":13, "<:KingOfHearts:996659886781906996>":13, "<:KingOfDiamonds:996659885511016469>":13}
    server = ctx.guild
    allSignedUp = []
    unqualified = []
    players = []
    userSpots = []
    users = open(str(server)+".txt","r").read().split("\n")
    balances = open(str(server)+"balance.txt","r").read().split("\n")
    await ctx.author.send("Who will be in the game? Enter everybody's username with the # and 4 digit number, with a space separating the names. If you are going to play. Enter your username, too.")
    def check(m):
        return m.author==ctx.author and m.channel.type==discord.ChannelType.private
    usersMsg = await bot.wait_for("message",check=check)
    usersMsg = usersMsg.content.split(" ")
    for user in usersMsg:
        converted = await MemberConverter().convert(ctx,user)
        players.append(converted)
    for user in usersMsg:
        allSignedUp.append(False)
    for x in range(len(usersMsg)):
        for y in range(len(users)):
            if users[y] == str(players[x].id):
                allSignedUp[x] = True
                userSpots.append(y)
    for y in range(len(allSignedUp)):
        if allSignedUp[y] == False:
            unqualified.append(str(players[y]))
    if len(unqualified) > 0:
        await ctx.author.send("Cannot start game because the following people are not signed up for the economy system: "+",".join(unqualified))
        return
    while len(players) > 0:
        realPlayers = players[:]
        payedUp = []
        payedUpSpots = []
        cards = ["<:AceOfSpades:996659877827072010>", "<:AceOfClubs:996659874559709224>", "<:AceOfHearts:996659876786868274>", "<:AceOfDiamonds:996659875717328936>",
        "<:2OfSpades:996659834776723476>", "<:2OfClubs:996659831303835679>", "<:2OfHearts:996659833442938971>", "<:2OfDiamonds:996659832360804472>",
        "<:3OfSpades:996659839801491497>", "<:3OfClubs:996659835460403261>", "<:3OfHearts:996659838337683507>", "<:3OfDiamonds:996659836735475765>",
        "<:4OfSpades:996659844167778335>", "<:4OfClubs:996659841043013695>", "<:4OfHearts:996659843068862514>", "<:4OfDiamonds:996659842120962138>",
        "<:5OfSpades:996659849536487485>", "<:5OfClubs:996659845346365582>", "<:5OfHearts:996659848034910248>", "<:5OfDiamonds:996659846709510256>",
        "<:6OfSpades:999920805515374622>", "<:6OfClubs:996659852195676160>", "<:6OfHearts:996659853122613279>", "<:6OfDiamonds:996659850731847721>",
        "<:7OfSpades:996659858147385364>", "<:7OfClubs:996659854498332773>", "<:7OfHearts:996659856968777878>", "<:7OfDiamonds:996659855563702332>",
        "<:8OfSpades:996659862714986536>", "<:8OfClubs:996659859124662272>", "<:8OfHearts:996659861557358623>", "<:8OfDiamonds:996659860370366474>",
        "<:9OfSpades:996659868113055804>", "<:9OfClubs:996659863981658143>", "<:9OfHearts:996659867093848124>", "<:9OfDiamonds:996659865860722738>",
        "<:10OfSpades:996659873326575716>", "<:10OfClubs:996659869149040690>", "<:10OfHearts:996659872093446185>", "<:10OfDiamonds:996659870407348234>",
        "<:JackOfSpades:996659883178995732>", "<:JackOfClubs:996659878833700915>", "<:JackOfHearts:996659882071691274>", "<:JackOfDiamonds:996659880133939220>",
        "<:QueenOfSpades:996993577118879774>", "<:QueenOfClubs:996659890170900541>", "<:QueenOfHearts:996993575491481654>", "<:QueenOfDiamonds:996659891882168371>",
        "<:KingOfSpades:996659888505753662>", "<:KingOfClubs:996659884290494544>", "<:KingOfHearts:996659886781906996>", "<:KingOfDiamonds:996659885511016469>"]
        hand = []
        handVal = []
        faceVal = []
        dealer = []
        dealerVal = []
        trueVals = []
        gameBets = []
        quitters = []
        trueDealerVal = 0
        for user in range(len(players)):
            def check(m):
                return m.author==players[user] and m.channel==ctx.channel and m.content.lower() in ["r","q"]
            await ctx.channel.send("<@"+str(players[user].id)+"> Press r to play and q to quit the game.")
            userMsg = await bot.wait_for("message",check=check)
            if userMsg.content=="q":
                await ctx.channel.send("<@"+str(players[user].id)+"> left the game.")
                quitters.append(players[user])
            else:
                balances = open(str(server)+"balance.txt","r").read().split("\n")
                def check2(m):
                    return m.author==players[user] and m.channel==ctx.channel and m.content.isdigit() and int(m.content) <= int(balances[userSpots[user]])
                await ctx.channel.send("<@"+str(players[user].id)+"> Place your bet It must be within your balance (~balance). Type 0 to pass for this round.")
                betMsg = await bot.wait_for("message",check=check2)
                if betMsg.content=="0":
                    await ctx.channel.send("<@"+str(players[user].id)+"> busted (Pause).")
                    realPlayers.remove(players[user])
                else:
                    gameBets.append(betMsg.content)
                    finalBal = int(balances[userSpots[user]])-int(betMsg.content)
                    balances[userSpots[user]] = str(finalBal)
                    open(str(server)+"balance.txt","w").write("\n".join(balances))
                    await ctx.channel.send("<@"+str(players[user].id)+"> bet "+gameBets[len(gameBets)-1]+".")
                    card = cards[random.randint(0,len(cards)-1)]
                    hand.append(card)
                    handVal.append(str(values[card]))
                    faceVal.append(str(diffVals[card]))
                    cards.remove(card)
                    card = cards[random.randint(0,len(cards)-1)]
                    hand[len(hand)-1] = hand[len(hand)-1]+" "+card
                    handVal[len(handVal)-1] = handVal[len(handVal)-1]+" "+str(values[card])
                    faceVal[len(faceVal)-1] = faceVal[len(faceVal)-1]+" "+str(diffVals[card])
                    cards.remove(card)
                    trueVals.append("0")
        for quitter in quitters:
            players.remove(quitter)
        if len(players) == 0:
            await ctx.channel.send("There are no more players in the game. GG")
            return
        handDone = []
        for user in realPlayers:
            handDone.append("f")
        winners = []
        card = cards[random.randint(0,len(cards)-1)]
        dealer.append(card)
        dealerVal.append(str(values[card]))
        cards.remove(card)
        realPlayers = players[:]
        for user in range(len(realPlayers)):
            while True:
                userHands = hand[user].split(",")
                for h in range(len(userHands)):    
                    while True:
                        userHandDone = handDone[user].split(",")
                        if userHandDone[h]=="t":
                            break
                        val = 0
                        numAces = 0
                        for vals in dealerVal:
                            val += int(vals)
                            if vals=="11":
                                numAces+=1
                        if val > 21:
                            for aces in numAces:
                                val-=10
                                if val <= 21:
                                    break
                        await ctx.channel.send("Dealer's Hand:\n"+" ".join(dealer))
                        await ctx.channel.send(str(val))
                        canDouble = True
                        while True:
                            if userHandDone[h]=="t":
                                break
                            userHand = handVal[user].split(",")[h].split(" ")
                            numAces = 0
                            val = 0
                            for vals in userHand:
                                val += int(vals)
                                if vals=="11":
                                    numAces += 1
                            if val > 21:
                                for aces in range(numAces):
                                    val -= 10
                                    if val <= 21:
                                        break
                            if val==21:
                                userVals = trueVals[user].split(",")
                                userVals[h] = str(val)
                                trueVals[user] = ",".join(userVals)
                                userFace = faceVal[user].split(",")[h].split(" ")
                                if len(userFace) == 2 and int(userFace[0]) > 10 and int(userFace[1]) == 1 or len(userFace) == 2 and int(userFace[0]) == 1 and int(userFace[1]) > 10:
                                    await ctx.channel.send("Hand "+str(h+1)+"of "+str(len(userHands))+":\n"+userHands[h])
                                    await ctx.channel.send("<@"+str(realPlayers[user].id)+"> Blackjack!!! You won "+str(int(gameBets[user]*2))+".")
                                else:
                                    await ctx.channel.send("Hand "+str(h+1)+"of "+str(len(userHands))+":\n"+userHands[h])
                                    await ctx.channel.send("<@"+str(realPlayers[user].id)+"> got 21!.")
                                break
                            else:
                                await ctx.channel.send("<@"+str(realPlayers[user].id)+">\n"+"Hand "+str(h+1)+" of "+str(len(userHands))+":\n"+userHands[h])
                                await ctx.channel.send(str(val))
                            def check3(m):
                                return m.author==realPlayers[user] and m.channel==ctx.channel and m.content.lower() in ["hit","stand","split","double"]
                            await ctx.channel.send("Your move: Hit, Stand, Split, Double")
                            userMove = await bot.wait_for("message",check=check3)
                            if userMove.content.lower()=="hit":
                                card = cards[random.randint(0,len(cards)-1)]
                                userHands = hand[user].split(",")
                                userHands[h] = userHands[h]+" "+card
                                hand[user] = ",".join(userHands)
                                userHandVals = handVal[user].split(",")
                                userHandVals[h] = userHandVals[h]+" "+str(values[card])
                                handVal[user] = ",".join(userHandVals)
                                userFaceVals = faceVal[user].split(",")
                                userFaceVals[h] = userFaceVals[h]+" "+str(diffVals[card])
                                faceVal[user] = ",".join(userFaceVals)
                                cards.remove(card)
                                userHand = handVal[user].split(",")[h].split(" ")
                                numAces = 0
                                val = 0
                                for vals in userHand:
                                    val += int(vals)
                                    if vals=="11":
                                        numAces += 1
                                if val > 21:
                                    for aces in range(numAces):
                                        val -= 10
                                        if val <= 21:
                                            break
                                if val > 21:
                                    userVals = trueVals[user].split(",")
                                    userVals[h] = str(val)
                                    trueVals[user] = ",".join(userVals)
                                    await ctx.channel.send("<@"+str(realPlayers[user].id)+">\n"+"Hand "+str(h+1)+"of "+str(len(userHands))+":\n"+userHands[h])
                                    await ctx.channel.send(str(val))
                                    await ctx.channel.send("<@"+str(realPlayers[user].id)+"> got a bust.")
                                    userHandDone[h] = "t"
                                    handDone[user] = ",".join(userHandDone)
                                    break
                                elif val == 21:
                                    userVals = trueVals[user].split(",")
                                    userVals[h] = str(val)
                                    trueVals[user] = ",".join(userVals)
                                    await ctx.channel.send("Hand "+str(h+1)+"of "+len(userHands)+":\n"+userHands[h])
                                    await ctx.channel.send("<@"+str(realPlayers[user].id)+"> Blackjack!!! You won "+str(int(gameBets[user]*2))+".")
                                    userHandDone[h] = "t"
                                    handDone[user] = ",".join(userHandDone)
                                    break
                                canDouble = False
                            elif userMove.content.lower()=="stand":
                                userHand = handVal[user].split(",")[h].split(" ")
                                numAces = 0
                                val = 0
                                for vals in userHand:
                                    val += int(vals)
                                    if vals=="11":
                                        numAces += 1
                                if val > 21:
                                    for aces in range(numAces):
                                        val -= 10
                                        if val < 21:
                                            break
                                userVals = trueVals[user].split(",")
                                userVals[h] = str(val)
                                trueVals[user] = ",".join(userVals)
                                userHandDone[h] = "t"
                                handDone[user] = ",".join(userHandDone)
                                break
                            elif userMove.content.lower()=="split":
                                balances = open(str(server)+"balance.txt","r").read().split("\n")
                                userIndivFaceVals = faceVal[user].split(",")[h].split(" ")
                                if len(userIndivFaceVals)!=2 or userIndivFaceVals[0]!=userIndivFaceVals[1]:
                                    await ctx.channel.send("<@"+str(realPlayers[user].id)+"> You do not have just 2 cards of the same value to split.")
                                elif int(balances[userSpots[user]]) < int(gameBets[user].split(",")[h]):
                                    await ctx.channel.send("You don't have enough money to split my guy...")
                                    break
                                else:
                                    card = cards[random.randint(0,len(cards)-1)]
                                    cards.remove(card)
                                    card2 = cards[random.randint(0,len(cards)-1)]
                                    cards.remove(card2)
                                    userHands = hand[user].split(",")
                                    userHands[h] = userHands[h].split(" ")[0]+" "+card+","+userHands[h].split(" ")[1]+" "+card2
                                    userHandVals = handVal[user].split(",")
                                    userHandVals[h] = userHandVals[h].split(" ")[0]+" "+str(values[card])+","+userHandVals[h].split(" ")[1]+" "+str(values[card2])
                                    userFaceVals = faceVal[user].split(",")
                                    userFaceVals[h] = userFaceVals[h].split(" ")[0]+" "+str(diffVals[card])+","+userFaceVals[h].split(" ")[1]+" "+str(diffVals[card2])
                                    hand[user] = ",".join(userHands)
                                    handVal[user] = ",".join(userHandVals)
                                    faceVal[user] = ",".join(userFaceVals)
                                    userGameBets = gameBets[user].split(",")
                                    userGameBets[h] = userGameBets[h]+","+userGameBets[h]
                                    gameBets[user] = ",".join(userGameBets)
                                    userHands = hand[user].split(",")
                                    userHandVals = handVal[user].split(",")
                                    userFaceVals = faceVal[user].split(",")
                                    userGameBets = gameBets[user].split(",")
                                    finalBal = int(balances[userSpots[user]])-int(gameBets[user].split(",")[h])
                                    balances[userSpots[user]] = str(finalBal)
                                    open(str(server)+"balance.txt","w").write("\n".join(balances))
                                    userHandDone[h] = userHandDone[h]+",f"
                                    handDone[user] = ",".join(userHandDone)
                                    userHandDone = handDone[user].split(",")
                                    await ctx.channel.send("<@"+str(players[user].id)+"> split his hand into two, each with a "+gameBets[user].split(",")[h]+" wager.")
                            elif userMove.content.lower()=="double" and canDouble:
                                balances = open(str(server)+"balance.txt","r").read().split("\n")
                                if int(balances[userSpots[user]]) < gameBets[user].split(",")[h]:
                                    await ctx.channel.send("You don't have enough money to double my guy...")
                                    break
                                else:
                                    finalBal = int(balances[userSpots[user]])-int(gameBets[user].split(",")[h])
                                    userGameBets = gameBets[user].split(",")
                                    userGameBets[h] = str(int(userGameBets[h]*2))
                                    gameBets[user] = ",".join(userGameBets)
                                    balances[userSpots[user]] = str(finalBal)
                                    open(str(server)+"balance.txt","w").write("\n".join(balances))
                                    await ctx.channel.send("<@"+str(players[user].id)+"> doubled his bet to "+gameBets[user].split(",")[h]+".")
                                    card = cards[random.randint(0,len(cards)-1)]
                                    userHands = hand[user].split(",")
                                    userHands[h] = userHands[h]+" "+card
                                    hand[user] = ",".join(userHands)
                                    userHandVals = handVal[user].split(",")
                                    userHandVals[h] = userHandVals[h]+" "+str(values[card])
                                    handVal[user] = ",".join(userHandVals)
                                    userFaceVals = faceVal[user].split(",")
                                    userFaceVals[h] = userFaceVals[h]+" "+str(diffVals[card])
                                    faceVal[user] = ",".join(userFaceVals) 
                                    cards.remove(card)
                                    userHand = handVal[user].split(",")[h].split(" ")
                                    numAces = 0
                                    val = 0
                                    for vals in userHand:
                                        val += int(vals)
                                        if vals=="11":
                                            numAces += 1
                                    if val > 21:
                                        for aces in range(numAces):
                                            val -= 10
                                            if val <= 21:
                                                break
                                    if val > 21:
                                        userVals = trueVals[user].split(",")
                                        userVals[h] = str(val)
                                        trueVals[user] = ",".join(userVals)
                                        await ctx.channel.send("<@"+str(realPlayers[user].id)+">\n"+"Hand "+str(h+1)+"of "+str(len(userHands))+":\n"+userHands[h])
                                        await ctx.channel.send(str(val))
                                        await ctx.channel.send("<@"+str(realPlayers[user].id)+"> got a bust.")
                                    elif val == 21:
                                        userVals = trueVals[user].split(",")
                                        userVals[h] = str(val)
                                        trueVals[user] = ",".join(userVals)
                                        await ctx.channel.send("Hand "+str(h+1)+"of "+len(userHands)+":\n"+userHands[h])
                                        await ctx.channel.send("<@"+str(realPlayers[user].id)+"> Blackjack!!! You won "+str(int(gameBets[user]*2))+".")
                                    else:
                                        userVals = trueVals[user].split(",")
                                        userVals[h] = str(val)
                                        trueVals[user] = ",".join(userVals)
                                        await ctx.channel.send("<@"+str(realPlayers[user].id)+">\n"+"Hand "+str(h+1)+"of "+str(len(userHands))+":\n"+userHands[h])
                                        await ctx.channel.send(str(val))
                                    userHandDone[h] = "t"
                                    handDone[user] = ",".join(userHandDone)
                                    break
                            elif userMove.content.lower()=="double" and not canDouble:
                                await ctx.channel.send("<@"+str(realPlayers[user].id)+"> You already hit so you cannot double.")
                            userHands = hand[user].split(",")
                if h == len(userHands)-1:
                    break
        await ctx.channel.send("Dealer's Turn...")
        time.sleep(3)
        while True:
            card = cards[random.randint(0,len(cards)-1)]
            dealer.append(card)
            dealerVal.append(str(values[card]))
            cards.remove(card)
            val = 0
            numAces = 0
            for vals in dealerVal:
                val += int(vals)
                if vals=="11":
                    numAces+=1
            if val > 21:
                for aces in range(numAces):
                    val-=10
                    if val <= 21:
                        break
            await ctx.channel.send(" ".join(dealer))
            await ctx.channel.send(str(val))
            profits = []
            if val > 21:
                await ctx.channel.send("Dealer busted (Ayo).")
                for user in range(len(realPlayers)):
                    winnings = 0
                    for bets in gameBets[user].split(","):
                        winnings -= int(bets)
                    userHands = hand[user].split(",")
                    userVals = trueVals[user].split(",")
                    for h in range(len(userHands)):
                        if int(userVals[h]) < 22:
                            balances = open(str(server)+"balance.txt","r").read().split("\n")
                            finalBal = int(balances[userSpots[user]])+(int(gameBets[user].split(",")[h])*2)
                            balances[userSpots[user]] = str(finalBal)
                            open(str(server)+"balance.txt","w").write("\n".join(balances))
                            winnings+= int(gameBets[user].split(",")[h])*2
                    profits.append(winnings)
                break
            elif val >= 16:
                for user in range(len(realPlayers)):
                    winnings = 0
                    for bets in gameBets[user].split(","):
                        winnings -= int(bets)
                    userHands = hand[user].split(",")
                    userVals = trueVals[user].split(",")
                    for h in range(len(userHands)):
                        userFace = faceVal[user].split(",")[h].split(" ")
                        if int(userVals[h]) > val and int(userVals[h]) < 22:
                            balances = open(str(server)+"balance.txt","r").read().split("\n")
                            finalBal = int(balances[userSpots[user]])+(int(gameBets[user].split(",")[h])*2)
                            balances[userSpots[user]] = str(finalBal)
                            open(str(server)+"balance.txt","w").write("\n".join(balances))
                            winnings+= int(gameBets[user].split(",")[h])*2
                        elif int(userVals[h]) == val:
                            if len(userFace) == 2 and int(userFace[0]) > 10 and int(userFace[1]) == 1 or len(userFace) == 2 and int(userFace[0]) == 1 and int(userFace[1]) > 10:
                                balances = open(str(server)+"balance.txt","r").read().split("\n")
                                finalBal = int(balances[userSpots[user]])+(int(gameBets[user].split(",")[h])*2)
                                balances[userSpots[user]] = str(finalBal)
                                open(str(server)+"balance.txt","w").write("\n".join(balances))
                                winnings+= int(gameBets[user].split(",")[h])*2
                            else:
                                if len(dealer) != 2 and diffVals[dealer[0]] <= 10 and diffVals[dealer[1]] != 1 or len(dealer) != 2 and diffVals[dealer[0]] != 1 and diffVals[dealer[1]] <= 10:
                                    await ctx.channel.send("Dealer hit Blackjack!")                            
                                    balances = open(str(server)+"balance.txt","r").read().split("\n")
                                    finalBal = int(balances[userSpots[user]])+int(gameBets[user].split(",")[h])
                                    balances[userSpots[user]] = str(finalBal)
                                    open(str(server)+"balance.txt","w").write("\n".join(balances))
                                    winnings += int(gameBets[user].split(",")[h])
                    profits.append(winnings)
                break
        await ctx.channel.send("GG! Here are everyone's total winnings:")
        for user in range(len(realPlayers)):
            await ctx.channel.send("<@"+str(realPlayers[user].id)+"> - *"+str(profits[user])+"*")
            time.sleep(2)
#old maid with/without economy money
@bot.command()
async def oldmaid(ctx):
    players = []
    stableCards = [        "<:QueenOfSpades:996993577118879774>",
            "<:AceOfSpades:996659877827072010>", "<:AceOfClubs:996659874559709224>", "<:AceOfHearts:996659876786868274>", "<:AceOfDiamonds:996659875717328936>",
        "<:2OfSpades:996659834776723476>", "<:2OfClubs:996659831303835679>", "<:2OfHearts:996659833442938971>", "<:2OfDiamonds:996659832360804472>",
        "<:3OfSpades:996659839801491497>", "<:3OfClubs:996659835460403261>", "<:3OfHearts:996659838337683507>", "<:3OfDiamonds:996659836735475765>",
        "<:4OfSpades:996659844167778335>", "<:4OfClubs:996659841043013695>", "<:4OfHearts:996659843068862514>", "<:4OfDiamonds:996659842120962138>",
        "<:5OfSpades:996659849536487485>", "<:5OfClubs:996659845346365582>", "<:5OfHearts:996659848034910248>", "<:5OfDiamonds:996659846709510256>",
        "<:6OfSpades:999920805515374622>", "<:6OfClubs:996659852195676160>", "<:6OfHearts:996659853122613279>", "<:6OfDiamonds:996659850731847721>",
        "<:7OfSpades:996659858147385364>", "<:7OfClubs:996659854498332773>", "<:7OfHearts:996659856968777878>", "<:7OfDiamonds:996659855563702332>",
        "<:8OfSpades:996659862714986536>", "<:8OfClubs:996659859124662272>", "<:8OfHearts:996659861557358623>", "<:8OfDiamonds:996659860370366474>",
        "<:9OfSpades:996659868113055804>", "<:9OfClubs:996659863981658143>", "<:9OfHearts:996659867093848124>", "<:9OfDiamonds:996659865860722738>",
        "<:10OfSpades:996659873326575716>", "<:10OfClubs:996659869149040690>", "<:10OfHearts:996659872093446185>", "<:10OfDiamonds:996659870407348234>",
        "<:JackOfSpades:996659883178995732>", "<:JackOfClubs:996659878833700915>", "<:JackOfHearts:996659882071691274>", "<:JackOfDiamonds:996659880133939220>",
        "<:KingOfSpades:996659888505753662>", "<:KingOfClubs:996659884290494544>", "<:KingOfHearts:996659886781906996>", "<:KingOfDiamonds:996659885511016469>"]
    values = {
                "<:QueenOfSpades:996993577118879774>":"0",
        "<:AceOfSpades:996659877827072010>":"1", "<:AceOfClubs:996659874559709224>":"1", "<:AceOfHearts:996659876786868274>":"1", "<:AceOfDiamonds:996659875717328936>":"1",
        "<:2OfSpades:996659834776723476>":"2", "<:2OfClubs:996659831303835679>":"2", "<:2OfHearts:996659833442938971>":"2", "<:2OfDiamonds:996659832360804472>":"2",
        "<:3OfSpades:996659839801491497>":"3", "<:3OfClubs:996659835460403261>":"3", "<:3OfHearts:996659838337683507>":"3","<:3OfDiamonds:996659836735475765>":"3",
        "<:4OfSpades:996659844167778335>":"4", "<:4OfClubs:996659841043013695>":"4", "<:4OfHearts:996659843068862514>":"4", "<:4OfDiamonds:996659842120962138>":"4",
        "<:5OfSpades:996659849536487485>":"5", "<:5OfClubs:996659845346365582>":"5", "<:5OfHearts:996659848034910248>":"5", "<:5OfDiamonds:996659846709510256>":"5",
        "<:6OfSpades:999920805515374622>":"6", "<:6OfClubs:996659852195676160>":"6", "<:6OfHearts:996659853122613279>":"6", "<:6OfDiamonds:996659850731847721>":"6",
        "<:7OfSpades:996659858147385364>":"7", "<:7OfClubs:996659854498332773>":"7", "<:7OfHearts:996659856968777878>":"7", "<:7OfDiamonds:996659855563702332>":"7",
        "<:8OfSpades:996659862714986536>":"8", "<:8OfClubs:996659859124662272>":"8", "<:8OfHearts:996659861557358623>":"8", "<:8OfDiamonds:996659860370366474>":"8",
        "<:9OfSpades:996659868113055804>":"9", "<:9OfClubs:996659863981658143>":"9", "<:9OfHearts:996659867093848124>":"9", "<:9OfDiamonds:996659865860722738>":"9",
        "<:10OfSpades:996659873326575716>":"10", "<:10OfClubs:996659869149040690>":"10", "<:10OfHearts:996659872093446185>":"10", "<:10OfDiamonds:996659870407348234>":"10",
        "<:JackOfSpades:996659883178995732>":"11", "<:JackOfClubs:996659878833700915>":"11", "<:JackOfHearts:996659882071691274>":"11", "<:JackOfDiamonds:996659880133939220>":"11",
        "<:KingOfSpades:996659888505753662>":"12", "<:KingOfClubs:996659884290494544>":"12", "<:KingOfHearts:996659886781906996>":"12", "<:KingOfDiamonds:996659885511016469>":"12"
        }
    server = ctx.guild
    unqualified = []
    while True:
        await ctx.author.send("Who will be in the game? Enter everybody's username with the # and 4 digit number, with a space separating the names. If you are going to play. Enter your username, too.")
        def check(m):
            return m.author==ctx.author and m.channel.type==discord.ChannelType.private 
        usersMsg = await bot.wait_for("message",check=check)
        usersMsg = usersMsg.content.split(" ")
        for user in usersMsg:
            try:
                member = await MemberConverter().convert(ctx,user)
            except:
                unqualified.append(user)
            else:
                players.append(member)
        if len(unqualified) > 0:
            await ctx.author.send("The following users are not in the server or do not exist:")
            for user in unqualified:
                await ctx.author.send(user)
        if len(players) == 0:
            await ctx.author.send("Cancelled game.")
            return
        await ctx.author.send("Would you like to continue with the eligible players? (y/n)")
        def check2(m):
            return m.author==ctx.author and m.channel.type==discord.ChannelType.private and m.content.lower() in ["y","n"]
        continueMsg = await bot.wait_for("message",check=check2)
        if continueMsg.content.lower()=="n":
           await ctx.author.send("Cancelled game.")
           return
        for user in unqualified:
            realPlayers.remove(user)
        while True:
           realPlayers = players[:]
           unqualified = []
           users = open(str(server)+".txt","r").read().split("\n")
           balances = open(str(server)+"balance.txt","r").read().split("\n")
           lenFile = len(users)
           for player in players:
               signedUp = False
               for user in users:
                   if str(player.id)==user:
                       signedUp = True
               if signedUp==False:
                    unqualified.append(str(player))
                    realPlayers.remove(player)
           if len(unqualified) > 0:
                await ctx.author.send("The following users are not registered in the server's economy system:")
                for user in unqualified:
                    await ctx.author.send(user)
                await ctx.author.send("Would you like to retry the sign up check, continue with current eligible players, or cancel the game? (retry/cont/cancel)")
                def check3(m):
                    return m.author==ctx.author and m.channel.type==discord.ChannelType.private and m.content.lower() in ["retry","cont","cancel"]
                continueMsg = await bot.wait_for("message",check=check3)
           else:
                break
           if continueMsg.content.lower()=="cancel":
                await ctx.author.send("Cancelled game.")
                return
           elif continueMsg.content.lower()=="cont":
                break
        if len(realPlayers) >= 2:
            break
        else:
            await ctx.author.send("There are not enough players to start the game.")
    players = realPlayers[:]
    userSpots = []
    for player in players:
        for user in range(len(users)):
            if str(player.id) == users[user]:
                userSpots.append(user)
    while True:
        realPlayers = players[:]
        await ctx.author.send("Type the amount everyone will wager. If there is no wager, type 0.")
        def check4(m):
                return m.author==ctx.author and m.channel.type==discord.ChannelType.private and m.content.isdigit()
        betMsg = await bot.wait_for("message",check=check4)
        realPlayers = players[:]
        unqualified = []
        users = open(str(server)+".txt","r").read().split("\n")
        balances = open(str(server)+"balance.txt","r").read().split("\n")
        for user in range(len(players)):
            if int(betMsg.content) > int(balances[userSpots[user]]):
                unqualified.append(str(player))
                realPlayers.remove(player)
        if len(unqualified) > 0:
            await ctx.author.send("The following users do not have enough money to play with the wager:")
            for user in unqualified:
                await ctx.author.send(user)
            await ctx.author.send("Would you like to retry the wager check, continue with current eligible players, or cancel the game? (retry/cont/cancel)")
            def check5(m):
                return m.author==ctx.author and m.channel.type==discord.ChannelType.private and m.content.lower() in ["retry","cont","cancel"]
            continueMsg = await bot.wait_for("message",check=check5)
        else:
            break
        if continueMsg.content.lower()=="cancel":
            await ctx.author.send("Cancelled game.")
            return
        elif continuteMsg.content.lower()=="cont":
            break
    players = realPlayers[:]
    while True:
        realPlayers = players[:]
        cards = [        "<:QueenOfSpades:996993577118879774>",
            "<:AceOfSpades:996659877827072010>", "<:AceOfClubs:996659874559709224>", "<:AceOfHearts:996659876786868274>", "<:AceOfDiamonds:996659875717328936>",
        "<:2OfSpades:996659834776723476>", "<:2OfClubs:996659831303835679>", "<:2OfHearts:996659833442938971>", "<:2OfDiamonds:996659832360804472>",
        "<:3OfSpades:996659839801491497>", "<:3OfClubs:996659835460403261>", "<:3OfHearts:996659838337683507>", "<:3OfDiamonds:996659836735475765>",
        "<:4OfSpades:996659844167778335>", "<:4OfClubs:996659841043013695>", "<:4OfHearts:996659843068862514>", "<:4OfDiamonds:996659842120962138>",
        "<:5OfSpades:996659849536487485>", "<:5OfClubs:996659845346365582>", "<:5OfHearts:996659848034910248>", "<:5OfDiamonds:996659846709510256>",
        "<:6OfSpades:999920805515374622>", "<:6OfClubs:996659852195676160>", "<:6OfHearts:996659853122613279>", "<:6OfDiamonds:996659850731847721>",
        "<:7OfSpades:996659858147385364>", "<:7OfClubs:996659854498332773>", "<:7OfHearts:996659856968777878>", "<:7OfDiamonds:996659855563702332>",
        "<:8OfSpades:996659862714986536>", "<:8OfClubs:996659859124662272>", "<:8OfHearts:996659861557358623>", "<:8OfDiamonds:996659860370366474>",
        "<:9OfSpades:996659868113055804>", "<:9OfClubs:996659863981658143>", "<:9OfHearts:996659867093848124>", "<:9OfDiamonds:996659865860722738>",
        "<:10OfSpades:996659873326575716>", "<:10OfClubs:996659869149040690>", "<:10OfHearts:996659872093446185>", "<:10OfDiamonds:996659870407348234>",
        "<:JackOfSpades:996659883178995732>", "<:JackOfClubs:996659878833700915>", "<:JackOfHearts:996659882071691274>", "<:JackOfDiamonds:996659880133939220>",
        "<:KingOfSpades:996659888505753662>", "<:KingOfClubs:996659884290494544>", "<:KingOfHearts:996659886781906996>", "<:KingOfDiamonds:996659885511016469>"]
        hand = []
        handVal = []
        quitters = []
        for user in range(len(players)):
            def check6(m):
                return m.author==players[user] and m.channel==ctx.channel and m.content.lower() in ["r","q"]
            await ctx.channel.send("<@"+str(players[user].id)+"> Press r to play and q to quit the game. If you are ready, you will automatically wager and enter the game.")
            userMsg = await bot.wait_for("message",check=check6)
            if userMsg.content=="q":
                await ctx.channel.send("<@"+str(realPlayers[user].id)+"> left the game.")
                quitters.append(players[user])
            else:
                finalBal = int(balances[userSpots[user]])-int(betMsg.content)
                balances[userSpots[user]] = str(finalBal)
                open(str(server)+"balance.txt","w").write("\n".join(balances))
                await ctx.channel.send("<@"+str(players[user].id)+"> bet "+betMsg.content+".")
                card = cards[random.randint(0,len(cards))]
                hand.append(card)
                handVal.append(values[card])
                cards.remove(card)
        for quitter in quitters:
            players.remove(quitter)
        if len(players) < 2:
            await ctx.channel.send("There are not enough players to continue. GG")
            return
        while len(cards) > 0:
            for x in range(len(players)):
                card = cards[random.randint(0,len(cards)-1)]
                hand[x] = hand[x] + " " + card
                handVal[x] = handVal[x] + " " + values[card]
                cards.remove(card)
                if len(cards) == 0:
                    break
        realPlayers = players[:]
        winners = []
        while True:
            for user in range(len(realPlayers)):
                userHand = hand[user].split(" ")
                for card in hand[user].split(" "):
                    for card2 in hand[user].split(" "):
                        if values[card]==values[card2] and card!=card2:
                            if card in userHand and card2 in userHand:
                                userHand.remove(card)
                                userHand.remove(card2)
                hand[user] = " ".join(userHand[:])
                for card in range(len(hand[user].split(" "))):
                    if card==0:
                        handVal[user] = hand[user].split(" ")[card]
                    else:
                        handVal[user] = handVal[user]+" "+hand[user].split(" ")[card]
                if len(hand[user].split(" "))==0:
                    winners.append(realPlayers[user])
                    await ctx.channel.send("<@"+str(realPlayers[user].id)+"> is out of cards! GG big man.")
            for winner in winners:
                realPlayers.remove(winner)
            if len(realPlayers) == 1:
                await ctx.channel.send("<@"+str(realPlayers[0].id)+"> got stuck with the old maid! Everyone except the loser won "+str((int(betMsg.content)*len(players))/(len(players)-1))+".")
                userSpots = []
                for user in range(len(players)):
                    users = open(str(server)+".txt","r")
                    balances = open(str(server)+"balance.txt","r")
                    for u in range(len(users)):
                        if users[u] == players[user]:
                            userSpots.append(u)
                    if players[user]==realPlayers[0]:
                        finalBal = None
                    else:
                        finalBal = str(int(balances[userSpots[user]])+((int(betMsg.content)*len(players))/(len(players)-1)))
                        balances[userSpots[user]] = finalBal
                open(str(server)+"balance.txt","w").write("\n".join(balances))
            for user in range(len(realPlayers)):
                picker = realPlayers[user]
                pickerNum = user
                if user==len(realPlayers)-1:
                    giver = realPlayers[0]
                    giverNum = 0
                else:
                    giver = realPlayers[user+1]
                    giverNum = user+1
                await ctx.channel.send ("<@"+str(picker.id)+"> will be picking a card from <@"+str(giver.id)+">.")
                await ctx.channel.send("Waiting for <@"+str(giver.id)+"> to choose the arrangement of their cards...")
                while True:
                    await giver.send(hand[giverNum])
                    await giver.send("Choose your arrangement of cards by typing them in the order you wish. If you don't want to rearrange any cards, just type 'skip'.")
                    def check7(m):
                        return m.author==giver and m.channel.type==discord.ChannelType.private
                    orgMsg = await bot.wait_for("message",check=check7)
                    orgHand = orgMsg.content.split(" ")
                    handCheck = orgHand[:]
                    for card in hand:
                        for card2 in orgHand:
                            if card==card2:
                                handCheck.remove(card)
                    if len(handCheck) > 0:
                        await giver.send("The following are not in your hand...")
                        for card in handCheck:
                            await giver.send(card)
                    else:
                        hand[user] = " ".join(orgHand)
                        break
                while True:
                    numCards = 0
                    for card in hand[giverNum].split(" "):
                        numCards+= 1
                    await ctx.channel.send("<@"+str(picker.id)+"> Choose a card from <@"+giver.id+">'s card by typing in a number that corresponds to the card placement.")
                    await ctx.channel.send("<:CardBack:1003044289493860434>"*numCards)
                    def check8(m):
                        return m.author==picker and m.channel==ctx.channel and m.content.isdigit()
                    pickMsg = await bot.wait_for("message",check=check8)
                    if int(pickMsg.content) > numCards:
                      await ctx.channel.send("<@"+str(picker.id)+"> That's not a valid number. Your choice is a number from 1-"+str(numCards)+"")
                    else:
                        newHand = hand[giverNum].split(" ")
                        newHand.remove(newHand[int(pickMsg.content)-1])
                        hand[giverNum] = " ".join(newHand)
                        hand[pickerNum] = hand[pickerNum]+" "+newHand[int(pickMsg.content)-1]
                        await picker.send(hand[pickerNum])
                        await giver.send(hand[giverNum])







bot.run(token)