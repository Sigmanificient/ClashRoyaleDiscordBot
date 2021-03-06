import io
import urllib.request

from PIL import Image, ImageFont, ImageDraw, PngImagePlugin
from pincer import command
from pincer.objects import Message, Embed, MessageContext

from app.utils import UserNotFound


class Player:
    def __init__(self, client):
        """Initialize the different commands."""
        self.client = client

    @command(
        name='profile',
        description='used to see your or someone else\'s profile'
    )
    async def profile_command(self, ctx: MessageContext, player_id: str):
        await ctx.interaction.ack()
        try:
            result = self.client.clash_royale_api.get_player(player_id)
            chests = self.client.clash_royale_api.get_player_upcoming_chests(
                player_id
            )

        except UserNotFound:
            return 'This user does not exist'

        # deck into an image start form here
        PngImagePlugin.MAX_TEXT_CHUNK = 100 * (1024 ** 2)

        # https://stackoverflow.com/a/53663233/15485584
        def trans_paste(fg_img, bg_img, alpha=1.0, box=(0, 0)):
            fg_img_trans = Image.new("RGBA", fg_img.size)
            fg_img_trans = Image.blend(fg_img_trans, fg_img, alpha)
            bg_img.paste(fg_img_trans, box, fg_img_trans)
            return bg_img

        # background of the deck
        deck = trans_paste(
            Image.new('RGBA', (630, 115), (151, 191, 225)),
            Image.new('RGBA', (630, 500), (23, 96, 173)),
            box=(0, 0)
        )

        # adding different cards
        for card_index, card in enumerate(result.get('currentDeck', {})):
            y, x = divmod(card_index, 4)

            image_url = card.get('iconUrls', {}).get('medium', None)
            if image_url is None:
                return

            # pasting the cards on the deck
            card = urllib.request.urlopen(image_url).read()
            card = io.BytesIO(card)
            card = Image.open(card)
            card = card.resize((138, 165))
            deck = trans_paste(
                card, deck, box=((x * 150) + 22, (y * 180) + 135)
            )

        # font by "https://fontsmagazine.com/"
        cr_font = ImageFont.truetype('app/utils/cr_font.ttf', 40)

        d1 = ImageDraw.Draw(deck)
        d1.text((120, 28), 'Current deck', fill=(255, 255, 255), font=cr_font)

        return Message(
            embeds=[
                Embed(
                    title=f'Profile of {result.get("name")}',
                    description=(
                        f'**level:** {result.get("expLevel")} (xp points: {result.get("expPoints")})\n'
                        f'**trophies:** {result.get("trophies")} (best: {result.get("bestTrophies")})\n'
                        f'**arena:** {result.get("arena").get("name")}\n'
                        f'**star points:** {result.get("starPoints")}\n'
                        f'**total donations:** {result.get("totalDonations")}\n'
                        f'**total donations collected:** {result.get("clanCardsCollected")}\n'
                    ),
                    color=self.client.embed_color
                ).add_field(
                    name='Games stats',
                    value=(
                        f'**W/R:** {(result.get("wins") / (result.get("battleCount") + 1)):.2f}\n'
                        f'**wins:** {result.get("wins")}\n'
                        f'**losses:** {result.get("losses")}\n'
                        f'**total battle count:** {result.get("battleCount")}\n'
                        f'**tree crown wins:** {result.get("threeCrownWins")}\n'
                    )
                ).add_field(
                    name='Clan stats',
                    value=(
                        (
                            f'**name:** {result.get("clan").get("name")}\n'
                            f'**tag:** {result.get("clan").get("tag")}\n'
                            f'**role:** {result.get("role")}\n'
                            f'**donations:** {result.get("donations")}\n'
                            f'**donations received:** {result.get("donationsReceived")}\n'
                        )
                        if result.get('clan') is not None
                        else 'not in a clan'
                    ),
                    inline=True,
                ).add_field(
                    name='Upcoming chests',
                    value='\n'.join(
                        (
                                ("+" + str(chest.get("index"))
                                 if chest.get("index") != 0
                                 else "next")
                                + f' : {chest.get("name")}'
                        )
                        for chest in chests.get('items')
                    ),
                    inline=False,
                ).set_image(url="attachment://image0.png")
            ],
            attachments=[deck]
        )


setup = Player
