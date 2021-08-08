import logging
import coloredlogs # These two are just for logging purposes mostly just because I like em

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from discord_webhook import DiscordWebhook, DiscordEmbed
# import urllib.request
import re
import random
import string
import json

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
    if ctx.author.id == bot.user.id:
        return
        
    displayname = ctx.author.name
    cleaned = ctx.content

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
    with open("data/users.json", "r") as f:
            users = json.load(f)
            users = users["users"]

    for mention in ctx.mentions:
        discordID = mention.id
        logging.info(cleaned)
        for user in users:
            if user["discordID"] == discordID:
                newMention = f"<@{user['guildedID']}>"
                oldMention = f"<@!{str(user['discordID'])}>"
                
                # For some god awful reason if you try to directly edit ctx.context it just doesn't wanna do it
                # So we have to make the message into it's own new variable then edit it
                # This is a terrible way to do this but I don't care
                cleaned = cleaned.replace(oldMention, newMention)
                logging.info(cleaned)
                
        
        # Replace remaining mentions 
        newMention = f"***{mention.name}***"
        oldMention = f"<@!{str(mention.id)}>"
        cleaned = cleaned.replace(oldMention, newMention)

    webhook = DiscordWebhook(url=os.getenv('GUILDED_WEBHOOK'), content=f"**<{displayname}>** {cleaned}") 
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



    def write_json(data, filename="data/auth.json"):
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)


    # Process the command
    if ctx.content.startswith("bridge"):
        # Split the message into args (seperated by space)
        args = ctx.content.split(" ")
        # Remove the prefix from the args list
        args.pop(0)

        if args[0] == "link":
            with open("data/auth.json", "r") as f:
                auth = json.load(f)
                temp = auth["discord"]

            
            # Check if discordID is already in data/auth.json
            for id in temp:
                if id["discordID"] == int(ctx.author.id):
                    await ctx.channel.send("You are already linked to a user.")
                    return

            # Generate a 16 letter code
            code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
            # Send the code to the user in dms
            await ctx.author.send(f"Your code is: **{code}**")
            # Save the code to data/auth.json along with the user ID
            # Example
            # { "DiscordID": 1234567890, code: "abcdef" }
            # where dID is the discord ID of the user and code is the code generated
           

            discordID = ctx.author.id
            y = {"discordID" : int(discordID), "code" : str(code)}
            logging.debug(y)
            temp.append(y)

            write_json(auth)


bot.run(os.getenv('DISCORD_TOKEN'))



