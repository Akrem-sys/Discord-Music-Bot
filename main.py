###############################################################################################
#                               GNU GENERAL PUBLIC LICENSE                                    #
#                                 Version 3, 29 June 2007                                     #
###############################################################################################
#       Copyright (C) 2007 Free Software Foundation, Inc. https://fsf.org/ Everyone           #
#       is permitted to copy and distribute verbatim copies of this license document,         #
#       but changing it is not allowed.                                                       #
###############################################################################################
import discord
from discord.ext import commands
import youtube_dl
import os,urllib.request,re,time,threading
client = commands.Bot(command_prefix="!")


def used(x):
    try:
        os.rename("Songs/"+x,"Songs/1"+x)
        os.rename("Songs/1"+x,"Songs/"+x)
        return False
    except:
        return True

def fileremover():
    for file in os.listdir("./Songs/"):
        while used(file):
            time.sleep(1)
        os.remove("Songs/"+file)

@client.command()
async def play(ctx,*args):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return
    try:
        voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=str(ctx.author.voice.channel))
        await voiceChannel.connect()
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    except:
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if args[0].startswith("https://www.youtube.com/watch"):
        with open("playlist","a") as f:
            f.write(args[0]+"\n")
    else:
        data = urllib.request.urlopen("https://www.youtube.com/results?search_query="+"+".join(args)).read().decode()
        data = re.findall(r"watch\?v=(\S{11})", data)
        data = "https://www.youtube.com/watch?v=" +data[0]
        with open("playlist","a") as f:
            f.write(data+"\n")
    if not voice.is_playing() and not voice.is_paused():
        Thread1=threading.Thread(target=lambda: Stream(voice))
        Thread1.start()

def Stream(voice):
    time.sleep(10)
    while True:
        for file in os.listdir("./Songs/"):
            if file.endswith(".mp3"):
                while used(file):
                    time.sleep(1)
                if voice.is_connected():
                    voice.play(discord.FFmpegPCMAudio("Songs/"+file))
                while voice.is_playing() or voice.is_paused():
                    time.sleep(1)
                try:
                    os.remove("Songs/"+file)
                except:
                    pass
        if len(os.listdir("./Songs/"))==0:
            break


def download():
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': './Songs/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    data=[]
    while True:
        try:
            if data==[]:
                with open("playlist","r") as f:
                    data=f.readlines()
                os.remove("playlist")
        except:
            pass
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([data[0].replace("\n","")])
            data.pop(0)
        except:
            time.sleep(5)

@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    try:
        voice.is_connected()
        await voice.disconnect()
        fileremover()
    except:
        await ctx.send("The bot is not connected to a voice channel.")

@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    try:
        voice.is_playing()
        voice.pause()
    except:
        await ctx.send("Currently no audio is playing.")

@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    try:
        voice.is_paused()
        voice.resume()
    except:
        await ctx.send("The audio is not paused.")

@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    try:
        voice.stop()
    except:
        await ctx.send("Currently no audio is playing.")
@client.command()
async def playing(ctx):
    for file in os.listdir("./Songs/"):
        file=file.replace(".mp3","")
        file=file.replace(".webm","")
        await ctx.send(file)
        break
fileremover()
Thread=threading.Thread(target=download)
Thread.start()
client.run(YOURDISCORDTOKEN)
