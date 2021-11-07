# https://discord.com/oauth2/authorize?client_id=905373060272631828&permissions=2147748928&scope=applications.commands%20bot

import json
import os
from glob import glob

from pincer import Client

from app.utils import ClashRoyaleAPI


class Bot(Client):

    def __init__(self):
        """Initialize the bot"""
        load_config()

        config = json.load(open('private/config.json'))
        self.clash_royale_api = ClashRoyaleAPI(config.get('CR_token'))

        self.embed_color = int(config.get('embed_color', 0x2f3037), 16)

        with open('private/config.json') as config_file:
            config = json.load(config_file)
            config_file.close()

        if config.get('token') is None:
            print('[ERROR] No token found in the private/config.json file')
            return

        self.load_cogs()
        super().__init__(token=config.get('token'))

    def load_cogs(self):
        """Load all cogs from the `cogs` directory."""
        for cog in glob("app/cogs/*.py"):
            self.load_cog(cog.replace("/", ".").replace("\\", ".")[:-3])
            print("Loaded cogs from", cog)

    @Client.event
    async def on_ready(self):
        """When the bot is ready"""
        print(f'Connected as {self.bot}!')


def load_config():
    os.makedirs('private', exist_ok=True)
    os.makedirs('app/data', exist_ok=True)
    if 'config.json' in os.listdir('private'):
        return

    with open('private/config.json', 'w') as config_file:
        json.dump(
            {
                'token': None,
                'embed_color': '0x2f3037'
            },
            config_file,
            indent=4
        )
        config_file.close()
