from discord.ext import commands
from discord import Intents, TextChannel
import os, json

token = open('token.txt').read().strip()

intents = Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix = "!",
    intents = intents
)

@bot.command()
async def archive(
    ctx: commands.Context
):

    try:

        #
        channels: list[TextChannel] = list(filter(
            lambda c: hasattr(c, 'history'),
            ctx.guild.channels 
        ))

        await ctx.send(f"""
    Starting Archival Process!
    ----------------------------------------
    Tool Created By: <@773970954539892746>
    https://github.com/MineFartS/discord-server-archiver
    """)
        
        for x, channel in enumerate(channels):
                
            await ctx.send(f"Archiving Channel ({x+1}/{len(channels)}): {channel.name}")

            path = f'./{channel.guild.name}/{channel.name}'

            # Create output directory if it doesn't exist
            if not os.path.exists(path):
                os.makedirs(path)

            with open(f'{path}/messages.txt', 'w', encoding='utf-8') as file:

                # Fetch all messages
                async for message in channel.history(limit=None, oldest_first=True):

                    # Writing message content, author, and timestamp to the file
                    file.write(f"[{message.created_at}] {message.author}: {message.content}\n")
                    
                    # Writing embeds in JSON format
                    for embed in message.embeds:
                        file.write(json.dumps(embed.to_dict()) + '\n')

                    # Save attachments
                    for attachment in message.attachments:

                        # Create a unique file name based on the message ID and original file name
                        await attachment.save(f"{path}/{message.id}_{attachment.filename}")

            #
        await ctx.send("Archival Complete!")

    except Exception as e:
        ctx.send(e.args)


bot.run(token=token)