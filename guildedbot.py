import logging
import coloredlogs # These two are just for logging purposes mostly just because I like em

import guilded
import os
from dotenv import load_dotenv
from discord_webhook import DiscordWebhook

coloredlogs.install(level="INFO", fmt="%(levelname)s | %(asctime)s | %(name)s | %(message)s")

load_dotenv()

bot = guilded.Bot(command_prefix='bridge!', owner_id='d8Gb36p4')

@bot.event()
async def on_ready():
    logging.info('Guilded bot logged in as ' + bot.user.name)

@bot.event()
async def on_message(ctx):
    # Check if the channel ID matches the one we're listening for 
    if ctx.channel.id != os.getenv('GUILDED_CHANNEL'): return
    if ctx.author.name == "Gil": return # This is just to prevent the bot from responding to itself
    if ctx.content == None:
        logging.info("Ignoring empty message | This happens with code blocks")  
        return # Happens when embeds are sent such as code blocks

    cleanedeveryone = ctx.content.replace('@everyone', '@​everyone')
    cleanedhere = cleanedeveryone.replace('@here', '@​here')
    webhook = DiscordWebhook(url=os.getenv('DISCORD_WEBHOOK'), content=cleanedhere, username=ctx.author.name, avatar_url=ctx.author.avatar_url)
    response = webhook.execute()

bot.run(os.getenv('GUILDED_EMAIL'), os.getenv('GUILDED_PASSWORD'))