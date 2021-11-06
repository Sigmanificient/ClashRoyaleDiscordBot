# https://discord.com/api/oauth2/authorize?client_id=905373060272631828&permissions=2147748928&scope=bot

import json
import os

from pincer import Client

from app.utils import ClashRoyaleAPI


class Bot(Client):
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
        self.clashRoyaleAPI = ClashRoyaleAPI(config.get('CR_token'))

        self.embed_color = int(config.get('embed_color', 0x2f3037), 16)

        with open('private/config.json') as config_file:
            config = json.load(config_file)
            config_file.close()
        if config.get('token') is None:
            print('[ERROR] No token found in the private/config.json file')
            return

        super().__init__(token=config.get('token'))

        # for filename in os.listdir("app/cogs"):
        #     if filename.endswith('.py'):
        #         self.load_extension(f'app.cogs.{filename[:-3]}')

    @Client.event
    async def on_ready(self):
        """When the bot is ready"""
        print(f'Connected as {self.bot}!')
