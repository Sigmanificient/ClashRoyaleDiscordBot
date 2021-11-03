# https://discord.com/api/oauth2/authorize?client_id=905373060272631828&permissions=2147748928&scope=bot

import json
import os
from discord.ext import commands
from app.utils import ClashRoyaleAPI


class Bot(commands.Bot):
    def __init__(self):
        """Initialize the bot"""
        os.makedirs('private', exist_ok=True)
        os.makedirs('app/data', exist_ok=True)
        if 'config.json' not in os.listdir('private'):
            with open('private/config.json', 'w') as config_file:
                json.dump(
                    {
                        'token': None,
                        'prefix': ';',
                        'embed_color': '0x2f3037'
                    },
                    config_file,
                    indent=4
                )
                config_file.close()

        config = json.load(open('private/config.json'))

        self._token = config.get('token')
        self.prefix = config.get('prefix', ';')
        self.clashRoyaleAPI = ClashRoyaleAPI(config.get('CR_token'))
        self.embed_color = int(config.get('embed_color', 0x2f3037), 16)
        super().__init__(self.prefix)
        self.remove_command("help")
        for filename in os.listdir("app/cogs"):
            if filename.endswith('.py'):
                self.load_extension(f'app.cogs.{filename[:-3]}')

    def run(self):
        """Run the bot"""
        with open('private/config.json') as config_file:
            config = json.load(config_file)
            config_file.close()
        if config.get('token') is None:
            print('[ERROR] No token found in the private/config.json file')
            return
        super().run(config.get('token'))

    async def on_message(self, message):
        """If the bot receive a message"""
        print(f'> {message.author.name} : {message.clean_content}')
        await self.process_commands(message)

    async def on_ready(self):
        """When the bot is ready"""
        print(f'Connected as {self.user}!')
