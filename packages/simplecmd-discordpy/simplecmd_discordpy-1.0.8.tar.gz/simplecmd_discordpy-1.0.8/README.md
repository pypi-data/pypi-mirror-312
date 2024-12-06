## **Welcome!!**

**(PT:BR) - Uma biblioteca para criar comando para o Discord.py muito mais simples!!**
**(ENG) - A library to create a much simpler command for Discord.py!!**

## Usage example
```python
import simplecmd_discordpy as scmd
import discord

scmd.config.set(logs=True, prefix=f"$") # Seta as configurações necessárias

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@scmd.command("ping") # Função para criar comandos
async def ping_cmd(ctx, *args):
    if args:
        await ctx.channel.send(f"Pong🏓" + ''.join(args[0]), reference=ctx)
    else:
        await ctx.channel.send(f"Pong🏓", reference=ctx)

@client.event
async def on_ready():
    print(f"[{client.user.name}] - Online!!")

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.author.id == client.user.id:
        return
    await scmd.load(message) # Carrega Todos Os Comandos
```
