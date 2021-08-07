import logging
import coloredlogs # These two are just for logging purposes mostly just because I like em

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from discord_webhook import DiscordWebhook, DiscordEmbed
# import urllib.request
import re

load_dotenv()

bot = commands.Bot(command_prefix='bridge!')

coloredlogs.install(level="INFO", fmt="%(levelname)s | %(asctime)s | %(name)s | %(message)s")

@bot.event
async def on_ready():
    logging.info('Discord bot logged in as ' + bot.user.name)
    await bot.change_presence(activity=discord.Game(name=os.getenv('DISCORD_STATUS')))

@bot.event
async def on_message(ctx):
    if str(ctx.webhook_id) == re.findall("discord.com\/api\/webhooks\/([^\/]+)\/", os.getenv('DISCORD_WEBHOOK'))[0]:
        return
    if str(ctx.channel.id) != os.getenv('DISCORD_CHANNEL_ID'):
        return

    displayname = ctx.author.name

    try:
        if ctx.author.nick:
            displayname = ctx.author.name # Modded this since there's no use in showing nicks
    except:
        pass

    # Add this back in the event webhooks support custom avatar URLs
    """    
        # Try to grab author avatar_url
        try:
            user = ctx.author
            avatar_url = user.avatar_url
            print(avatar_url)
        except Exception as e:
            print(e)
            avatar_url = None
            pass # Yes I know shitty error handling but leave me alone
    """
    
    # Find all mentions in a message. and replace them with the name instead of <@446546546>
    # This is to make pings readable across clients
    # Example
    # Hi <@4546546546> how are you?
    # becomes
    # Hi John Doe how are you?
    # where is the name of the user mentioned
    for mention in ctx.mentions:
        cleanName = "***" + mention.name + "*** "
        # Find all mentions in ctx.content using a regex 
        mentionList = re.findall(f'<@!?{mention.id}>', ctx.content)
        # mentionList will return somehting alone the lines of ["<@8546546546465>", "<@5464654654>"]
        # Iterate through the list and replace the mention with the clean name
        for mention in mentionList:
            ctx.content = ctx.content.replace(mention, cleanName)


    webhook = DiscordWebhook(url=os.getenv('GUILDED_WEBHOOK'), content=f"**<{displayname}>** {ctx.content}") 
    logging.debug(ctx.content)
    attachment_urls = []

    if ctx.attachments:
        for attachment in ctx.attachments:
        # When Guilded supports file uploads, we can use this. For now, we'll leave it there.
        #    req = urllib.request.Request(
        #        attachment.url,
        #        headers={'User-Agent':'DiscordBot (https://wiilink24.com, 1.0.0)'}
        #    )
        #    webhook.add_file(file=urllib.request.urlopen(req), filename=attachment.filename)
            attachment_urls.append(attachment.url)
        webhook = DiscordWebhook(url=os.getenv('GUILDED_WEBHOOK'), content=ctx.content + " " + " ".join(attachment_urls) + " ")

    response = webhook.execute()
    logging.info("Sent webhook")
    logging.debug(response)

bot.run(os.getenv('DISCORD_TOKEN'))