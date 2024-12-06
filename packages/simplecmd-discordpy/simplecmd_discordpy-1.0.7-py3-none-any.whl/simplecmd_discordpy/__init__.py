import discord

commands = {}
def command(cmd):
    def decorator(func):
        commands[cmd] = func
        return func
    return decorator

class ConfigCmd:
    def __init__(self):
        self.settings = {"logs": False, "prefix": False}
    def set(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.settings:
                self.settings[key] = value
            else:
                raise KeyError(f"Configuração '{key}' não encontrada.")
    def get(self, key):
        return self.settings.get(key, None)
config = ConfigCmd()

async def load(message):
    content = message.content.lower()
    prefix = str(config.get("prefix"))
    for cmd, func in commands.items():
        if content.startswith(prefix + cmd):
            if config.get("logs"):
                print(f"• {prefix}{cmd} Called!! [ {message.author.name} ]")
            await func(message)
            return
            