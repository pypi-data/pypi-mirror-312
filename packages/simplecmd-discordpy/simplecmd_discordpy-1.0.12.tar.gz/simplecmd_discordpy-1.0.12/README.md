## **Welcome!!**

**(PT:BR) - Uma biblioteca para criar comandos para o Discord.py!!, lembrando que não quero substituir nada estou apenas tentando criar algo com a estrutura mais simples para os iniciantes**
**(ENG) - A library to create commands for Discord.py!!, remembering that I don't want to replace anything, I'm just trying to create something with the simplest structure for beginners**

## Usage example
```python
import simplecmd_discordpy as scmd
import discord

scmd.config.set(logs=True, prefix=f"$") # Seta as configurações necessárias

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@scmd.command("ping") # Função para criar comandos
async def ping_cmd(msg, *args):
    if args:
        await msg.channel.send(f"Pong🏓" + ''.join(args[0]), reference=msg)
    else:
        await msg.channel.send(f"Pong🏓", reference=msg)

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.author.id == client.user.id:
        return
    await scmd.load(message) # Carrega Todos Os Comandos
```

## Using example per file
```python
import simplecmd_discordpy as scmd
import discord

scmd.config.set(logs=True, prefix=f"$", folder="commands/") # Seta as configurações necessárias

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.author.id == client.user.id:
        return
    await scmd.load_files(message) # Carrega os arquivos da pasta de comandos
    await scmd.load(message) # Carrega todos os arquivos obtido completamente
    
```

* Já dentro da pasta `commands/ping.py`
```python
import discord

async def run(message, *args):
    await message.channel.send("Pong🏓")
```