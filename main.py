import discord
import os
import time
import json
from dotenv import load_dotenv
import webscraper as ws
import movies_api as mv

client = discord.Client()

load_dotenv()
TOKEN = os.getenv('TOKEN')

global killers
global killer_images
global killer_urls


@client.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        if member.discriminator == '3478':
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


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Sends list of commands
    if message.content == '$help':
        command_list = ['$zdarova - greetings brother',
                        '$tell-me-joke - tells you joke in DM',
                        '$orar group - prints group(I2E2, I1A4 etc.) timetable',
                        '$kekw - pretty obvious, no?',
                        '$movies genre - prints list of most popular movies by genre',
                        '$killers - print list of killers with images',
                        '$killer [name] - prints overview about specific killer']
        command_string = '\n'.join(command_list)
        await message.channel.send(command_string)

    # Sends message in channel
    if message.content == '$zdarova':
        await message.channel.send('Zdarova broder! :^)')

    # Sends timetable in channel
    if message.content.startswith('$orar'):
        response = f'Usage: $orar group\n' \
                   f'**Available groups:**\n'
        for group in ws.get_groups():
            response += '\t' + group + '\n'
        msgSplit = message.content.split()
        if len(msgSplit) != 2:
            await message.channel.send(response)
        else:
            await message.channel.send(ws.get_timetable(msgSplit[1]))

    # Sends message in private to user who send the command
    if message.content == '$tell-me-joke':
        await message.author.send('You are gay.')

    if message.content == '$kekw':
        await message.channel.send('https://static.truckersmp.com/images/vtc/logo/10588.1581843551.jpg')

    if message.content.startswith('$movies'):
        genre_list = mv.get_genre_list()
        msgSplit = message.content.split()
        response = f'**Usage: $movies genre**\n' \
                   f'*Available genres:*\n'
        for line in genre_list:
            response += f'\t{line["name"]}\n'

        if len(msgSplit) < 2:
            await message.channel.send('Usage: $movies genre')
        else:
            genre = ' '.join(msgSplit[1:])
            movies = mv.get_movies_by_genre(genre)

            if movies == '{"error": "invalid genre"}':
                await message.channel.send(response)
                return

            json_data = json.loads(movies)['movies']
            response = 'Most popular movies by genre ' + genre + ':\n'
            for line in json_data:
                response += f'**Title**: {line["title"]}\n' \
                            f'\t**Popularity**: {line["popularity"]}\n' \
                            f'\t\t**Release date**: {line["release_date"]}\n\n'
            await message.channel.send(response)

    if message.content == '$killers':
        global killers
        global killer_images
        global killer_urls
        killers, killer_images, killer_urls = ws.get_killers()
        messages = ws.get_info_about_killers(killers, killer_images)
        for result in messages:
            await message.channel.send(result)

    if message.content.startswith('$killer '):
        split_string = message.content.split()
        killer_name = ' '.join(split_string[1:]).lower()
        if 'the ' in killer_name:
            killer_name = killer_name[4:]
        killer_index = -1
        if 'killers' not in globals():
            killers, killer_images, killer_urls = ws.get_killers()
        for killer in killers:
            if killer_name.lower() == killer[0].lower() or killer_name.lower() == killer[1].lower():
                killer_index = killers.index((killer[0], killer[1]))
        if killer_index == -1:
            await message.channel.send('Killer does''t exist! :(')
            return
        killer_url = killer_urls[killer_index]
        info = ws.get_killer_info(killer_url)
        result = '\n'.join(info)
        await message.channel.send(result)


@client.event
async def on_connect():
    await client.wait_until_ready()
    print('Gigel is up and running!')
    # general_channel = client.get_channel(309356532288585738)
    # await general_channel.send(
    #    "Gigel s-a conectat la server!\nScrie $help pentru a vedea comenzile disponibile!")


client.run(TOKEN)
