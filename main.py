import discord
from discord.ext import commands
import pytesseract
from PIL import Image
import os
import io
import requests
from decouple import config



#GLOBAL VARIABLES
client = commands.Bot(command_prefix = "--")
client.remove_command("help")
image_types = ["png", "jpeg", "jpg", "gif"]
main_color = 0x5ce1e6
footer = "will add documentation here if needed."
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
    if ctx.message.attachments is None:
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
@client.command()
async def help(ctx, cmd = None):
    cmd_list = ["transcribe", "ping", None]
    if cmd not in cmd_list:
        await ctx.send("That command doesn't exist, type --help for command list")
    else:
        if cmd == None:
            embed=discord.Embed(title="bluefire help", description="How to use help? type --help <commandname>", color=main_color)
            embed.add_field(name="Command list", value="More commands are coming soon", inline=True)
            embed.add_field(name="transcribe", value="extracts text from an image", inline=False)
            embed.add_field(name="ping", value="returns ping", inline=False)
            embed.set_footer(text = footer)
            await ctx.send(embed=embed)
        elif cmd == "transcribe":
            embed=discord.Embed(title="transcribe help", description="this command extracts text from any given image | default is latin alphabet", color=0x5ce1e6)
            embed.add_field(name="Usage", value="--transcribe lang**", inline=True)
            embed.add_field(name="Supported image types", value="png, jpg, jpeg ,gif", inline=True)
            embed.add_field(name="Supported languages", value="For supported languages, see official pytesseract documentation", inline=False)
            embed.set_footer(text="*required **optional | this command uses the pytesseract library")
            await ctx.send(embed=embed)






client.run(token)
