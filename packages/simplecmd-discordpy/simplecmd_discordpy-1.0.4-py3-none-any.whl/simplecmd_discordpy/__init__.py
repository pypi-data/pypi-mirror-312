import discord

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

async def command(message, cmd):
    if message.content.lower().startswith((str(config.get("prefix")) + cmd).lower()):
        if config.get("logs"):
            print(f"• {config.get('prefix')}{cmd} Called!! [ {message.author.name} ]")
        return True
    return False
