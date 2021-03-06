import discord
from discord.ext import commands
import hotslogs
import re
import random
import youtube
import asyncio
import os
import sys


debug_mode = False
parameters = sys.argv

Client = discord.Client()
bot_prefix = "$"
client = commands.Bot(command_prefix=bot_prefix)


help_text = "**Wuss poppin!**\n" \
           "Here are some of my commands:\n\n" \
           "**$build** [*hero name*] : Fetches the best build for the given hero.\n\n" \
           "**$flip** : Flips a coin.\n\n" \
           "**$addquote** [*quote*] : Stores a quote.\n\n" \
           "**$quote** : Fetches a randomly stored quote.\n\n\n" \
           "**$join** : Invites the bot into the voice channel.\n\n" \
           "**$queue** [*song name*] : Stores a song in the queue.\n\n" \
           "**$playall** : Add the playlist of songs to the queue.\n\n" \
           "**$playlist** : Get the queue of songs.\n\n" \
           "**$wussplayin** : Tells you what song is currently playing.\n\n\n" \
           "Permitted Commands:\n\n" \
           "**$emptyquotes** : Empties the quote storage.\n\n" \
           "**$next_song** : End the current song.\n\n" \
           "**$clear** : Empties the server messages.\n\n" \
           "**$emptyqueue** : Removes all remaining songs from the queue."

client.queue = []
client.cycling = False
client.voice = discord.VoiceClient
client.player = None


def run_bot(key):
    if key == "YOUR KEY HERE":
        print("Enter your key in secret.py")
        
    else:
        client.run(key)
    
    
def debug_out(message):
    if debug_mode:
        print(message)


def is_command(message):
    if message.content.startswith("$") or message.author == client.user:
        return True


def play_again():
    func = implement_player()
    fut = asyncio.run_coroutine_threadsafe(func, client.loop)
    
    try:
        fut.result()
    except IndexError as e:
        print(f"Ending playlist. ({e})")


def shuffle():
    random.shuffle(client.queue)


async def modify_user_settings(name):
    with open(f'Avatars/{name}.png', 'rb') as f:
        await client.edit_profile(avatar=f.read())

    for server in client.servers:
        if debug_mode:
            await client.change_nickname(server.me, f'Debug-Mode {name}')
        else:
            await client.change_nickname(server.me, name)


@client.event
async def on_ready():
    nicknames = ["Yuno", "Rei", "Karen", "2B"]
    name = ''

    for arg in parameters:
        try:
            await modify_user_settings(arg)
            name = arg

        except:
            continue

    if name == '':
        name = random.choice(nicknames)
        await modify_user_settings(name)

    print("Bot online.")
    print(f'Name: {name}')
    print(f'ID: {client.user.id}')
    print(f'Version: {discord.__version__}')
    
    await client.change_presence(game=discord.Game(name="Black Desert Online"))


@client.command(pass_context=True, help="$clear : Empties the server messages.")
@commands.has_permissions(manage_messages=True, change_nickname=True)
async def clear(ctx):
    print("Purge command.")
    await client.purge_from(channel=ctx.message.channel, limit=500, check=None)


@client.command(pass_context=True)
@commands.has_permissions(change_nickname=True)
async def halp(ctx):
    print("Help command.")
    await client.send_message(ctx.message.channel, help_text, )


@client.command(pass_context=True, help="$build [*hero name*] : Fetches the best build for the given hero.")
@commands.has_permissions(change_nickname=True)
async def build(ctx):
    talents = hotslogs.get_talents(ctx.message.content[7:])
    try:
        await client.send_message(ctx.message.channel,
                                  f'*{ctx.message.content[7:]}* \n\n'
                                  "Level 1: " + re.sub(r"(\w)([A-Z])", r"\1 \2", talents[0]) + "\n\n"
                                  "Level 4: " + re.sub(r"(\w)([A-Z])", r"\1 \2", talents[1]) + "\n\n"
                                  "Level 7: " + re.sub(r"(\w)([A-Z])", r"\1 \2", talents[2]) + "\n\n"
                                  "Level 10: " + re.sub(r"(\w)([A-Z])", r"\1 \2", talents[3]) + "\n\n"
                                  "Level 13: " + re.sub(r"(\w)([A-Z])", r"\1 \2", talents[4]) + "\n\n"
                                  "Level 16: " + re.sub(r"(\w)([A-Z])", r"\1 \2", talents[5]) + "\n\n"
                                  "Level 20: " + ":ok_hand::joy:")
    except IndexError:
        await client.send_message(ctx.message.channel,
                                  f"There's no build data for {ctx.message.content[7:]}. Try to brew something!")


@client.command(pass_context=True, help="$flip : Flips a coin.")
@commands.has_permissions(change_nickname=True)
async def flip(ctx):
    await client.send_message(ctx.message.channel, random.choice(["Heads", "Tails"]))


@client.command(pass_context=True, help="$addquote [*quote*] : Stores a quote.")
@commands.has_permissions(change_nickname=True)
async def addquote(ctx):
    file = open("quotes.txt", "a")
    file.write(ctx.message.content[10:] + "\n")
    file.close()
    await client.send_message(ctx.message.channel, "Quote saved for eternity.")


@client.command(pass_context=True, help="$quote : Fetches a randomly stored quote.")
@commands.has_permissions(change_nickname=True)
async def quote(ctx):
    file = open("quotes.txt", "r")
    await client.send_message(ctx.message.channel, random.choice(file.readlines()))
    file.close()


@client.command(pass_context=True, help="$join : Invites the bot into the voice channel.")
@commands.has_permissions(change_nickname=True)
async def join(ctx):
    vchannel = ctx.message.author.voice_channel
    client.voice = await client.join_voice_channel(vchannel)


@client.command(pass_context=True, help="$queue [*song name*] : Stores a song in the queue.")
@commands.has_permissions(change_nickname=True)
@commands.cooldown(2, 60, commands.BucketType.user)
async def queue(ctx):
    client.queue.append(ctx.message.content[7:])
    await client.send_message(ctx.message.channel, "Video added to queue!")
    await implement_player()


@queue.error
async def queue_error(error, ctx):
    if isinstance(error, discord.ext.commands.CommandOnCooldown):
        await client.send_message(ctx.message.channel,
                                  f'Please wait **{str(error.retry_after)}** seconds before queuing more songs.')


@client.command(pass_context=True, help="$next_song : End the current song.")
@commands.has_permissions(change_nickname=True)
async def next_song():
    client.player.stop()


@client.command(pass_context=True, help="$wussplayin : Tells you what song is currently playing.")
@commands.has_permissions(change_nickname=True)
async def wussplayin(ctx):
    try:
        await client.send_message(ctx.message.channel, f'Currently playing: {client.player.title}')

    except AttributeError:
        await client.send_message(ctx.message.channel, f'Currently playing: Absolutely nothing.')


@client.command(pass_context=True, help="$emptyqueue : Removes all remaining songs from the queue.")
@commands.has_permissions(manage_messages=True)
async def emptyqueue(ctx):
    client.queue = []
    await client.send_message(ctx.message.channel, "Queue cleared!")


@client.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def purge(ctx):
    await client.purge_from(channel=ctx.message.channel, limit=500, check=is_command)


@client.command(pass_context=True, help="$emptyquotes : Empties the quote storage.")
@commands.has_permissions(manage_messages=True)
async def emptyquotes(ctx):
    file = open("quotes.txt", "w")
    file.write("")
    file.close()
    await client.send_message(ctx.message.channel, "Quotes cleared!")


@client.command(pass_context=True, help="$playall : Add the playlist of songs to the queue.")
@commands.has_permissions(change_nickname=True)
async def playall():
    file = open("playlist.txt", "r")
    songlist = file.readlines()
    for song in songlist:
        client.queue.append(song[:-1])
    shuffle()
    await implement_player()


@client.command(pass_context=True, help="$playlist : Get the queue of songs.")
@commands.has_permissions(change_nickname=True)
async def playlist(ctx):
    content = ""
    for song in client.queue:
        content = content + song + "\n"
    await client.send_message(ctx.message.channel, content=content)


@client.command(pass_context=True, help="$haolong : Displays the current video's statistics.")
async def haolong(ctx):
    pass


async def initialize_song(song):
    debug_out("Initializing song...")
    try:
        before_args = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
        client.player = await client.voice.create_ytdl_player(
            url=youtube.get_vid(song),
            ytdl_options="--proxy 128.0.0.1:8087",
            before_options=before_args,
            after=play_again, )
        client.player.start()
        debug_out("Song should be playing.")
    except RuntimeWarning as e:
        if e is RuntimeWarning:
            debug_out("Runtime warning occurred.")
            debug_out(e)
            await next_song()


async def implement_player():
    debug_out("Implementing player...")
    if client.player is not None:
        if not client.player.is_playing():
            song = client.queue.pop(0)
            await initialize_song(song)
    
    else:
        debug_out("New player being initialized...")
        song = client.queue.pop(0)
        await initialize_song(song)


if 'debug' in parameters:
    debug_mode = True
    debug_out("Debug-Mode activated.")

if debug_mode:
    run_bot(os.environ.get('DEBUG_TOKEN'))
else:
    run_bot(os.environ.get('GRIL_TOKEN'))
