import math
import urllib.request
import io
import discord
import re
import random
from wand.image import Image


client = discord.Client()


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    if message.content.startswith(".spongle"):
        await spongle(await get_image_list(message), message)

    elif message.content.startswith(".obliterate"):
        await obliterate(await get_image_list(message), message)


async def get_image_list(message: discord.Message):
    attachment_url_list = list()
    attachments = message.attachments
    for a in attachments:
        attachment_url_list.append(a.url)
    urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', message.content)
    total_list = attachment_url_list + urls

    if len(total_list) == 0:
        logs = await message.channel.history(limit=20).flatten()
        log: discord.Message
        for log in logs:
            if len(log.attachments) >= 1:
                total_list.append(log.attachments[0].url)
                break
    return total_list


async def obliterate(image_list: list, message: discord.Message):
    for a in image_list:
        req = urllib.request.Request(a, headers={'User-Agent': "Magic Browser"})
        response = urllib.request.urlopen(req)
        try:
            with Image(file=response) as img:
                img.implode(random.uniform(.45, .7))
                img_bin = img.make_blob()
                f = io.BytesIO(img_bin)
                await message.channel.send(file=discord.File(f, 'return.png'))
        except:
            print("nope")
        finally:
            response.close()


async def spongle(image_list: list, message: discord.Message):
    for a in image_list:
        req = urllib.request.Request(a, headers={'User-Agent': "Magic Browser"})
        response = urllib.request.urlopen(req)
        try:
            with Image(file=response) as img:
                if img.width > 800:
                    img.sample(800, math.floor(img.height * (800/img.width)))

                before_width = img.width
                before_height = img.height
                img.liquid_rescale(math.floor(img.width * random.uniform(.3, .7)),
                                   math.floor(img.height * random.uniform(.3, .7)))
                img.liquid_rescale(before_width, before_height)

                img_bin = img.make_blob()
                f = io.BytesIO(img_bin)
                await message.channel.send(file=discord.File(f, 'return.png'))
        except:
            print("nope")
        finally:
            response.close()
client.run('token')
