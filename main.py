import discord
from discord.ext import commands
import json
import os
import requests

config_path = './config.json'
lang_path = './lang/'

if os.path.exists(config_path):
    with open(config_path, 'r') as f:
        config_data = json.load(f)
else:
    raise FileNotFoundError("Config file not found")

TOKEN = config_data.get('token', '')

bot = commands.Bot(config_data.get('prefix', '.') , intents=discord.Intents().all())

def load_language(language):
    lang_file_path = os.path.join(lang_path, f'{language}.json')
    if os.path.exists(lang_file_path):
        with open(lang_file_path, 'r') as f:
            return json.load(f)
    else:
        raise FileNotFoundError(f"Language file for '{language}' not found")

language = config_data.get('language', 'en')
messages = load_language(language)

def get_message(key, **kwargs):
    message = messages.get(key, "")
    return message.format(**kwargs)

def save_config():
    with open(config_path, 'w') as f:
        json.dump(config_data, f, indent=4)

@bot.event
async def on_ready():
    print(get_message('bot_connected', bot_name=bot.user.name))

@bot.command(name='start')
async def start(ctx):
    user_id = str(ctx.author.id)

    if user_id not in config_data['whitelist']['start']:
        await ctx.send(get_message('no_permission_start'))
        return

    server_id = config_data['server_id']
    api_key = config_data['api_key']
    panel_link = config_data['panel_link']

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    start_url = f'{panel_link}/api/client/servers/{server_id}/power'
    payload = {
        'signal': 'start'
    }

    response = requests.post(start_url, headers=headers, json=payload)

    if response.status_code == 204:
        await ctx.send(get_message('server_started', server_id=server_id))
    else:
        await ctx.send(get_message('error_starting'))

@bot.command(name='stop')
async def stop(ctx):
    user_id = str(ctx.author.id)

    if user_id not in config_data['whitelist']['stop']:
        await ctx.send(get_message('no_permission_stop'))
        return

    server_id = config_data['server_id']
    api_key = config_data['api_key']
    panel_link = config_data['panel_link']

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    stop_url = f'{panel_link}/api/client/servers/{server_id}/power'
    payload = {
        'signal': 'stop'
    }

    response = requests.post(stop_url, headers=headers, json=payload)

    if response.status_code == 204:
        await ctx.send(get_message('server_stopped', server_id=server_id))
    else:
        await ctx.send(get_message('error_stopping'))

@bot.command(name='execute')
async def execute(ctx, *, command: str):
    user_id = str(ctx.author.id)

    if user_id not in config_data['whitelist']['execute']:
        await ctx.send(get_message('no_permission_execute'))
        return

    server_id = config_data['server_id']
    api_key = config_data['api_key']
    panel_link = config_data['panel_link']

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    execute_url = f'{panel_link}/api/client/servers/{server_id}/command'
    payload = {
        'command': command
    }

    response = requests.post(execute_url, headers=headers, json=payload)

    if response.status_code == 204:
        await ctx.send(get_message('command_executed', server_id=server_id))
    else:
        await ctx.send(get_message('error_executing'))

bot.run(TOKEN)
