import discord

commands = {}

def command(cmd):
    def decorator(func):
        commands[cmd] = func
        return func
    return decorator

class ConfigCmd:
    def __init__(self):
        self.settings = {"logs": False, "prefix": "$"}
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
    content = message.content
    prefix = str(config.get("prefix"))
    normalized_content = content.lower()
    for cmd, func in commands.items():
        normalized_cmd = (prefix + cmd).lower()
        if normalized_content.startswith(normalized_cmd):
            if config.get("logs"):
                print(f"• {prefix}{cmd} Called!! [ {message.author.name} ]")
            args = content[len(prefix + cmd):].strip().split()
            try:
                if args:
                    await func(message, *args)
                else:
                    await func(message)
            except TypeError as e:
                if config.get("logs"):
                    print(f"Erro ao chamar o comando '{cmd}': {e}")
            return