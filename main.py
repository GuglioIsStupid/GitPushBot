import discord
import dotenv
import os
import importlib

dotenv.load_dotenv()

client = discord.Client(
    intents=discord.Intents.all()
)

DISCORD_TOKEN = dotenv.get_key(dotenv.find_dotenv(), 'DISCORD_TOKEN')
OWNER_ID = dotenv.get_key(dotenv.find_dotenv(), 'OWNER_ID')
PREFIX = dotenv.get_key(dotenv.find_dotenv(), 'PREFIX')

commands: dict[str, callable] = {}

def load_commands():
    for file in os.listdir("commands"):
        if not file.endswith(".py") or file.startswith("_"):
            continue

        module_name = f"commands.{file[:-3]}"
        module = importlib.import_module(module_name)

        if hasattr(module, "name") and hasattr(module, "run"):
            commands[module.name] = module.run
            print(f"Loaded command: {module.name}")

load_commands()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if not message.content.startswith(PREFIX):
        return
    
    if not str(message.author.id) == OWNER_ID:
        return

    content = message.content[len(PREFIX):]
    parts = content.split()
    command_name = parts[0].lower()
    args = parts[1:]

    command = commands.get(command_name)
    if command:
        await command(client, message, args)

client.run(DISCORD_TOKEN)
