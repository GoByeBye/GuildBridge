<!--- Badges --->
![optimized-badge] [![support-badge]][support]

# GuildBridge
GuildBridge is a fork of [guilded-bridge by burritosoftware](https://github.com/WiiLink24/guilded-bridge)

GuildBridge is simply bridging the gap between Discord and Guilded guilds.

# Installing
```bash
pip install -r requirements.txt

# or 

pip3 install -r requirements.txt
```
Which one you want to use depends on how your python installation is setup

# Usage
Make a `.env` file filling out the information from `.env.example` and fill out the information

    DISCORD_TOKEN=Discord bot token.
    DISCORD_WEBHOOK=Discord webhook for a channel.
    DISCORD_CHANNEL_ID=Channel ID to only scan for messages in a certain channel.
    DISCORD_STATUS=Set the playing status of the bot.

    GUILDED_EMAIL=Guilded account email.
    GUILDED_PASSWORD=Guilded account password.
    GUILDED_WEBHOOK=Guilded webhook for a channel
    GUILDED_CHANNEL=Guilded channel id to wait for messages 


A properly formatted .env file would look something along the lines of this
    
    DISCORD_TOKEN=ODczNjAwNDQ3OTcyMjYxODg4.YQ6x0Q.4t0fOkD6l1gHGHhAChHm9EV_dD0
    DISCORD_WEBHOOK=https://canary.discord.com/api/webhooks/873600598858166312/8dd4NjmOMfkgSlcmvvfNPv3lq6mir9AoVlksL899xbFgs_uys2oki_4hJFoAwlUm3wHh
    DISCORD_CHANNEL_ID=800834248222179368
    DISCORD_STATUS=Bridging The Gap

    GUILDED_EMAIL=pleaselovemedadineedlove@email.com
    GUILDED_PASSWORD=MyPasswordIsTheStrongest
    GUILDED_WEBHOOK=https://media.guilded.gg/webhooks/4843c505-6ca0-4b34-ba68-d6d2d403ddcb/8QlHz3sJ562C2kEY4amQw4Oywai0CS0scKqYkgEoY4UA0IcK8G4YskAgmc0O0EqgooMac0IQOUE2a2g8AyMmYa
    GUILDED_CHANNEL=cf3578de-2ccd-4302-af58-d5cbdd709b6e

<details>
<summary>
    <strong>How to find guilded channel ID</strong>
</summary>
    Right click on the channel and select copy link
![copylink](https://raw.githubusercontent.com/GoByeBye/GuildBridge/master/assets/copylink.gif)
    
    
<strong>Example</strong>

`https://www.guilded.gg/Disco-Support/groups/WD5nXJEd/channels/cf3578de-2ccd-4302-af58-d5cbdd709b6e/chat`

Becomes 
`cf3578de-2ccd-4302-af58-d5cbdd709b6e`
</details>

## Start the bot
Windows
```batch
> python launch.py
```

```bash
$ python3 launch.py
```

Need support? Hit me up on guilded

[![support-badge]][support]


<!--- Badges code --->

[optimized-badge]: https://i.imgur.com/lmiLNGi.png

[support]: https://www.guilded.gg/i/jpLJ5xJ2?cid=cf3578de-2ccd-4302-af58-d5cbdd709b6e&intent=chat
[support-badge]: https://i.imgur.com/17tyFkX.png