import discord
from discord.ext import commands
import pytesseract
from PIL import Image
import glob
import os
import io
import requests
from decouple import config
from googletrans import Translator


#GLOBAL VARIABLES
client = commands.Bot(command_prefix = "--")
client.remove_command("help")
image_types = ["png", "jpeg", "jpg", "gif"]
main_color = 0x5ce1e6
footer = "will add documentation here if needed."

#LANGUAGE LIST
language_list = {
    'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'eu': 'basque',
    'be': 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ceb': 'cebuano',
    'ny': 'chichewa',
    'zh-cn': 'chinese (simplified)',
    'zh-tw': 'chinese (traditional)',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'eo': 'esperanto',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'haw': 'hawaiian',
    'iw': 'hebrew',
    'he': 'hebrew',
    'hi': 'hindi',
    'hmn': 'hmong',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'ko': 'korean',
    'ku': 'kurdish (kurmanji)',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar (burmese)',
    'ne': 'nepali',
    'no': 'norwegian',
    'or': 'odia',
    'ps': 'pashto',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tg': 'tajik',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'ug': 'uyghur',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu',
}

#ENV VARIABLES
token = config("token")

#events
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="--help | v1.0  "))




@client.command()
async def ping(ctx):
        await ctx.send(f'My ping is {round(client.latency * 1000)}ms')


@client.command()
async def transcribe(ctx, passed_lang = "eng"):
    if not ctx.message.attachments:
        await ctx.send("Send an image to be transcribed.")
        
    else:  
        if passed_lang == None:
            for attachment in ctx.message.attachments:
                if any(attachment.filename.lower().endswith(image) for image in image_types):
                    number = int(ctx.message.author.id)
                    await ctx.message.attachments[0].save(f"fileby{number}.jpg")
                    transcribed_text = pytesseract.image_to_string(Image.open(f"fileby{number}.jpg")) 
                    await ctx.send(f"Transcribed text: \n {transcribed_text} \n Not what you wanted? --help transcribe for possible error reasons")
                    os.remove(f"fileby{number}.jpg")
        elif passed_lang != None:
            for attachment in ctx.message.attachments:
                if any(attachment.filename.lower().endswith(image) for image in image_types):
                    number = int(ctx.message.author.id)
                    await ctx.message.attachments[0].save(f"fileby{number}.jpg")
                    transcribed_text = pytesseract.image_to_string(Image.open(f"fileby{number}.jpg"), lang = passed_lang) 
                    await ctx.send(f"Transcribed text: \n {transcribed_text} \nNot what you wanted? --help transcribe for possible error reasons")
                    os.remove(f"fileby{number}.jpg")

#RESOLUTION 
@client.command()
async def resolution(ctx):
    if not ctx.message.attachments:
        await ctx.send("Send an image to recieve the resolution")
    else:
        for attachment in ctx.message.attachments:
            if any(attachment.filename.lower().endswith(image) for image in image_types):
                number = int(ctx.message.author.id)
                await ctx.message.attachments[0].save(f"resolution{number}.jpg")
                im = Image.open(f"resolution{number}.jpg")
                await ctx.send(f"The image dimensions are {im.size}")
                im.close()
                os.remove(f"resolution{number}.jpg")
#TRANSLATE
@client.command()
async def translate(ctx, src, target, *, text):
    tl = Translator()
    if target not in language_list or src not in language_list:
        await ctx.send("Unknown target and/or source language. Visit https://py-googletrans.readthedocs.io/en/latest/ for supported languages.")
    else:
        result = tl.translate(text, src=src, dest=target).text
        await ctx.send(f"Translated text: {result}")

@translate.error
async def translate_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing argument, {ctx.message.author.mention}. See --help translate for more ")
        return

#HELP
@client.command()
async def help(ctx, cmd = None):
    cmd_list = ["transcribe", "ping", "resolution", "translate", None]
    if cmd not in cmd_list:
        await ctx.send("That command doesn't exist, type --help for command list")
    else:
        if cmd == None:
            embed=discord.Embed(title="bluefire help", description="How to use help? type --help <commandname>", color=main_color)
            embed.add_field(name="Command list", value="More commands are coming soon", inline=True)
            embed.add_field(name="transcribe", value="extracts text from an image", inline=False)
            embed.add_field(name="ping", value="returns ping", inline=False)
            embed.add_field(name="resolution", value = "gives resolution of a sent image")
            embed.add_field(name="translate", value = "translates text", inline=False)
            embed.set_footer(text = footer)
            await ctx.send(embed=embed)
        elif cmd == "transcribe":
            embed=discord.Embed(title="transcribe help", description="this command extracts text from any given image | default is latin alphabet", color=0x5ce1e6)
            embed.add_field(name="Usage", value="--transcribe* lang**", inline=True)
            embed.add_field(name="Supported image types", value="png, jpg, jpeg ,gif", inline=True)
            embed.add_field(name="Supported languages", value="For supported languages, see official pytesseract documentation", inline=False)
            embed.add_field(name="Potential problems", value="Low resolution, unclear text, close colors between text and backrgound and noise can cause problems. Works best with black text on white background.")
            embed.set_footer(text="*required **optional | this command uses the pytesseract library")
            await ctx.send(embed=embed)
        elif cmd == "resolution":
            embed=discord.Embed(title="resolution help", color=0x5ce1e6)
            embed.add_field(name="Usage", value="--resolution*", inline=False)
            embed.add_field(name="Supported image types", value="png, jpg, jpeg")
            embed.set_footer(text = "*required **optional")
            await ctx.send(embed=embed)
        elif cmd == "translate":
            embed=discord.Embed(title="translate help", color=0x5ce1e6)
            embed.add_field(name="Usage", value="--translate* source* target* text*", inline=True)
            embed.add_field(name="Supported languages", value="Visit https://py-googletrans.readthedocs.io/en/latest/ for supported languages.")
            embed.add_field(name="Example usage", value="--translate en es this is a text", inline=False)
            embed.set_footer(text="*required **optional | this command uses the googletrans library")
            await ctx.send(embed=embed)
        elif cmd == "ping":
            embed=discord.Embed(title="ping help", color=0x5ce1e6)
            embed.add_field(name="usage", value="--ping returns the ping in ms")
            await ctx.send(embed=embed)




client.run(token)
