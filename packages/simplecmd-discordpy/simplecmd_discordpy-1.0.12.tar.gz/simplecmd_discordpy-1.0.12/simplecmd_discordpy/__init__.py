import discord
import os
import importlib

commands = {}

def command(cmd):
    def decorator(func):
        commands[cmd] = func
        return func
    return decorator

class ConfigCmd:
    def __init__(self):
        self.settings = {"logs": True, "prefix": "$", "folder": "commands/"}
    def set(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.settings:
                self.settings[key] = value
            else:
                raise KeyError(f"Configuração '{key}' não encontrada.")
    def get(self, key):
        return self.settings.get(key, None)
config = ConfigCmd()

async def load_files(message):
    folder = config.get("folder")
    if not os.path.exists(folder):
        print(f"A pasta '{folder}' não foi encontrada.")
        return
    for filename in os.listdir(folder):
        if filename.endswith(".py"):
            command_name = filename[:-3]
            module_path = folder.replace("/", ".") + command_name
            try:
                module = importlib.import_module(module_path)
                if hasattr(module, "run"):
                    commands[command_name] = module.run
                else:
                    print(f"O arquivo '{filename}' não contém uma função 'run'.")
            except Exception as e:
                print(f"Erro ao carregar o comando '{command_name}': {e}")

async def load(message):
    content = message.content
    prefix = str(config.get("prefix"))
    normalized_content = content.lower()
    for cmd, func in commands.items():
        normalized_cmd = (prefix + cmd).lower()
        if normalized_content.startswith(normalized_cmd):
            args = content[len(prefix + cmd):].strip().split()
            try:
                if args:
                    if config.get("logs"):
                        print(f"• {prefix}{cmd} Called!! [ {message.author.name} ]")
                    await func(message, *args)
                else:
                    if config.get("logs"):
                        print(f"• {prefix}{cmd} Called!! [ {message.author.name} ]")
                    await func(message)
            except Exception as e:
                print(f"Erro ao executar o comando '{cmd}': {e}")
            return