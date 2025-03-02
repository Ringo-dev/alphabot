import discord
import os
from voicevox import voice_generate
from dotenv import load_dotenv
import discord.opus

load_dotenv()

token = os.getenv("Discord_Token")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("Online")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    elif message.content == "!join":
        if message.author.voice is None:
            await message.channel.send("You are not connected to a voice channel.")
            return

        await message.author.voice.channel.connect()
        await message.channel.send("Successfully joined the voice channel.")

    elif message.content == "!leave":
        if message.author.voice is None:
            await message.channel.send("You are not connected to a voice channel.")
            return

        await message.guild.voice_client.disconnect()
        await message.channel.send("Successfully left the voice channel.")

    else:
        if message.author.voice is None:
            return

        messages = message.content
        file_path = voice_generate(messages)

        print(file_path)

        sounds = await discord.FFmpegOpusAudio.from_probe(file_path)
        message.guild.voice_client.play(sounds)

        return

if token is None:
    print("Discord_Tokenにトークンが設定されていません。")
else:
    client.run(token)

