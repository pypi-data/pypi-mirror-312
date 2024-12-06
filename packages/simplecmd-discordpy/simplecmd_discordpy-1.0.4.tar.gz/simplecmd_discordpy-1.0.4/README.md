## **Welcome!!**

**(PT:BR) - Uma biblioteca para criar comando para o Discord.py muito mais simples!!**
**(ENG) - A library to create a much simpler command for Discord.py!!**

## Usage example
```python
import discord
import simplecmd_discordpy as scmd # Importando o simplecmd

scmd.config(logs=True, prefix="!") # Setando as configurações sobre os comandos
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    if massage.author.id == client.user.id:
        return
    # Como criar o comando >>
    if await scmd.command(message, "ping"):
        await message.channel.send("Pong🏓", reference=message)
        
```
