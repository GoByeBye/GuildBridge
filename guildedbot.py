import json
import logging
import os

import coloredlogs  # These two are just for logging purposes mostly just because I like em
import guilded
from discord_webhook import DiscordWebhook
import requests
from dotenv import load_dotenv

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

    # Check if author has avatar url
    if ctx.author.avatar_url == None:
        logging.info("Ignoring message | No avatar URL")
        return # Ignore messages without an avatar

    
    cleanedeveryone = ctx.content.replace('@everyone', '@​everyone')
    cleanedhere = cleanedeveryone.replace('@here', '@​here')
    webhook = DiscordWebhook(url=os.getenv('DISCORD_WEBHOOK'), content=cleanedhere, username=ctx.author.name, avatar_url=ctx.author.avatar_url)
    response = webhook.execute()


    # Parse the response and grab the ID of the message if it was successful
    if response.status_code == 200:
        guildedMsgID = ctx.id
        discordMsgID = response.json()['id']
        logging.info("Message sent | ID: " + response.json()['id'])
        logging.debug("Guilded ID: " + guildedMsgID)
        # If the message was sent successfully take the ID and append it to hooks.json with IDs corralating eachother.
        # example json data:
        # { guildedMsgID: discordMsgID }
        # becomes
        # {"b530b95d-f78a-4c89-b60f-d703883b3c47": "873866587965362236"}
        def write_json(data, filename="data/hooks.json"):
            with open(filename, "w") as f:
                json.dump(data, f, indent=4)

        with open("data/hooks.json") as jsonFile:
            data = json.load(jsonFile)
            temp = data["messages"]
            y = {"GuildedID" : str(guildedMsgID), "DiscordID" : int(discordMsgID)}
            logging.info(y)
            temp.append(y)
        
        write_json(data)

    else:
        logging.error("Message failed to send | Code: " + response.status_code)

@bot.event()
async def on_message_edit(ctx):
    logging.debug("Message edited: " + ctx.id)

    # Load messages from data/hooks.json
    with open("data/hooks.json") as f:
        data = json.load(f)
        data = data["messages"]
    
    for id in data:
        if id["GuildedID"] == ctx.id:
            logging.debug("Found guilded ID in hooks.json")
            discordID = id["DiscordID"]
            # Send patch request to webhook url to edit message
            # required JSON param
            # content: string
            hookURL = os.getenv("DISCORD_WEBHOOK")
            hookURL = hookURL + "/messages/" + f"{discordID}"
            logging.debug(hookURL)
            payload = {
                "content": ctx.content
            }
            headers = {
                "Content-Type": "application/json"
            }
            response = requests.patch(hookURL, data=json.dumps(payload), headers=headers)
            logging.info("Message edited | Code: " + str(response.status_code))
            logging.debug(response.text)



@bot.event()
async def on_message_delete(ctx):
    logging.debug("Message deleted: " + ctx.id)
    # Load messages from data/hooks.json
    with open("data/hooks.json") as f:
        data = json.load(f)
        data = data["messages"]
    
    for id in data:
        if id["GuildedID"] == ctx.id:
            logging.debug("Found guilded ID in hooks.json")
            discordID = id["DiscordID"]
            
            hookURL = os.getenv("DISCORD_WEBHOOK")
            hookURL = hookURL + "/messages/" + f"{discordID}"
            
            # Send delete request to delete the message
            response = requests.delete(hookURL)
            if response.status_code == 204:
                logging.info("Message deleted | Code: " + str(response.status_code))
            else:
                logging.error("Message failed to delete | Code: " + str(response.status_code))
        





bot.run(os.getenv('GUILDED_EMAIL'), os.getenv('GUILDED_PASSWORD'))
