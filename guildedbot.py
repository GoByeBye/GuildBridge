import json
import logging
import os

import coloredlogs  # These two are just for logging purposes mostly just because I like em
import guilded
from discord_webhook import DiscordWebhook
import requests
from dotenv import load_dotenv
import re


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

    
    # Find all mentions in ctx.content
    # Mention example <@d8Gb36p4> or <@adgt2342JKKF>
    if '<@' in cleanedhere:
        mentions = re.findall(r'<@([a-zA-Z0-9]+)>', cleanedhere)
        with open("data/users.json", "r") as f:
            users = json.load(f)
            users = users["users"]

        logging.info(mentions)
        for mention in mentions:
            # Remove stuff around mention so we only get the user id
            mention = mention.replace('<@', '')
            mention = mention.replace('>', '')
            logging.info(mention)
            # Check if mention is in the list of users
            for user in users:
                if user["guildedID"] == mention:
                    logging.info("Mention matches linked account")
                    oldMention = f"<@{mention}>"
                    newMention = f"<@{user['discordID']}>"
                    cleanedhere = cleanedhere.replace(oldMention, newMention)
                    logging.info(cleanedhere)


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

    

    if ctx.content.startswith("bridge"):
        # Split message into arguments (args are separated by spaces)
        args = ctx.content.split(" ")
        # Remove the prefix
        args.pop(0)
        
        # if else spagetti for commands becuase guilded.py doesn't support cogs yet
        logging.info(args)
        if args[0] == "link":
            if len(args) == 2:
                logging.info("made it to link process")

                # Check if the code exists in data/auth.json
                with open("data/auth.json") as jsonFile:
                    data = json.load(jsonFile)
                    data = data["discord"]
                    for id in data:
                        if id["code"] == args[1]:
                            logging.info("Matched code!")
                            # If it does link the accounts
                            logging.info("Linking accounts")
                            guildedID = ctx.author.id
                            # Grab the discord ID from the auth.json file in the same bit as the 
                            discordID = id["discordID"]
                            logging.info("Guilded ID: " + guildedID)
                            logging.info("Discord ID: " + str(discordID))
                            # Create a new entry in data/users.json with the discordID and guildedID
                            # so that we can keep track of who is linked to who
                            # Example: { "users": [ { "discordID": "123456789", "guildedID": "d8Gb36p4" } ] }

                            with open("data/users.json", "r") as jsonFile:
                                data = json.load(jsonFile)
                                temp = data["users"]
                                y = {"discordID" : int(discordID), "guildedID" : str(guildedID)}
                                temp.append(y)
                                write_json(data, "data/users.json")
                
                await ctx.channel.send("Sucessfully linked accounts")

            else:
                await ctx.channel.send("Start linking process from discord for now")
                            

            
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
