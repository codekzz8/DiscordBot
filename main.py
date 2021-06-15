import discord
import os
import time
from dotenv import load_dotenv
from webscraper import get_timetable

client = discord.Client()

load_dotenv()
TOKEN = os.getenv('TOKEN')


@client.event
async def on_voice_state_update(member, before, after):
    alreadyDisconnected = False

    if before.channel is None and after.channel is not None:
        if member.discriminator == '3478':
            alreadyDisconnected = True
            voice_channel = after.channel
            time.sleep(1)
            vc = await voice_channel.connect()
            vc.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe",
                                           source="https://www.myinstants.com/media/sounds/yeet_ivPgINo.mp3"))
            while vc.is_playing():
                time.sleep(.1)
            time.sleep(0.3)
            await member.move_to(None)
            await vc.disconnect()

    if not alreadyDisconnected and before.channel is not None and after.channel is None:
        voice_channel = before.channel
        await voice_channel.disconnect()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Sends list of commands
    if message.content == '$help':
        command_list = ['$zdarova - greetings brother',
                        '$tell-me-joke - tells you joke in DM',
                        '$orar group - prints group(I2E2, I1A4 etc.) timetable']
        command_string = '\n'.join(command_list)
        await message.channel.send(command_string)

    # Sends message in channel
    if message.content == '$zdarova':
        await message.channel.send('Zdarova broder! :^)')

    # Sends timetable in channel
    if message.content.startswith('$orar'):
        msgSplit = message.content.split()
        if len(msgSplit) != 2:
            await message.channel.send('Usage: $orar group')
        else:
            await message.channel.send(get_timetable(msgSplit[1]))

    # Sends message in private to user who send the command
    if message.content == '$tell-me-joke':
        await message.author.send('You are gay.')


@client.event
async def on_connect():
    await client.wait_until_ready()
    print('Gigel is up and running!')
    general_channel = client.get_channel(309356532288585738)
    #await general_channel.send(
    #    "Gigel s-a conectat la server!\nScrie $help pentru a vedea comenzile disponibile manca-ti-as!")


client.run(TOKEN)