import asyncio
import discord
import os
import time
import json
from dotenv import load_dotenv
import webscraper as ws
import movies_api as mv
from datetime import datetime, time, timedelta

intents = discord.Intents.all()
client = discord.Client(intents=intents)

load_dotenv()
TOKEN = os.getenv('TOKEN')

global killers
global killer_images
global killer_urls
global vc

TIME_TO_SEND_MESSAGE = time(7, 0, 0)

@client.event
async def on_voice_state_update(member, before, after):
    global vc
    if before.channel is None and after.channel is not None:
        if member.discriminator in ['9938', '3361', '2779', '8882', '6644', '6532', '3478']:
            voice_channel = after.channel
            time.sleep(1)
            try:
                vc = await voice_channel.connect()
            except discord.errors.ClientException:
                pass
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
        killer_image = killer_images[killer_index]
        killer_url = killer_urls[killer_index]
        info = ws.get_killer_info(killer_url)
        await message.channel.send(killer_image)
        information = '\n'.join(info)
        await message.channel.send(information)

@client.event
async def on_connect():
    await client.wait_until_ready()
    print('Gigel is up and running!')

async def send_gif_daily():
    await client.wait_until_ready()
    user = await get_user_by_id('DBD', 3478)
    await user.send("https://tenor.com/view/morning-positive-vibes-gif-20875150")

async def check_time():
    now = datetime.utcnow()
    if now.time() > TIME_TO_SEND_MESSAGE:
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds = (tomorrow - now).total_seconds()
        await asyncio.sleep(seconds)
    while True:
        now = datetime.utcnow()
        target_time = datetime.combine(now.date(), TIME_TO_SEND_MESSAGE)
        seconds_until_target = (target_time - now).total_seconds()
        await asyncio.sleep(seconds_until_target)
        await send_gif_daily()
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds = (tomorrow - now).total_seconds()
        await asyncio.sleep(seconds)

async def get_user_by_id(server_name, id):
    servers = client.guilds
    for server in servers:
        if server.name == server_name:
            users = server.members
            for user in users:
                if user.discriminator == str(id):
                    return user

client.loop.create_task(check_time())
client.run(TOKEN)
