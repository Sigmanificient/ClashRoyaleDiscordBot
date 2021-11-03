import requests
from typing import Optional
import json


class UserNotFound(Exception):
    def __init__(self, arg):
        self.args = arg


class ClashRoyaleAPI:
    def __init__(self, token):
        self.__headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + token
        }

    def __request(
            self,
            url: str,
            params: dict = None
    ) -> Optional[dict]:
        """
        :param url:
            Url for the request.

        :param params:
            Parameters for the request.

        :return:
            Returns the request as an json object, or an error if it fails.
        """

        r = requests.get(
            'https://api.clashroyale.com/v1' + url,
            headers=self.__headers,
            params=params
        )
        content = json.loads(r.content.decode('utf-8'))

        if not r.ok:
            if r.status_code == 404:
                raise UserNotFound('404: Not found')
            raise Exception(
                f'{r.status_code}: {content.get("reason")}: '
                f'{content.get("message")}')

        return content

    # Players: Access player specific information
    def get_player(self, player_tag: str) -> Optional[dict]:
        """
        Get information about a single player by player tag. Player tags can be
        found either in game or by from clan member lists.

        :param player_tag:
            Tag of the player (without the #).

        :return:
            Information about a single player.
        """
        return self.__request(f'/players/%23{player_tag}')

    def get_player_upcoming_chests(self, player_tag: str) -> Optional[dict]:
        """
        Get list of reward chests that the player will receive next in the game.

        :param player_tag:
            Tag of the player (without the #).

        :return:
            List of reward chests that the player will receive next in the game.
        """
        return self.__request(f'/players/%23{player_tag}/upcomingchests')

    def get_player_battle_log(self, player_tag: str) -> Optional[dict]:
        """
        Get list of recent battles for a player.

        :param player_tag:
            Tag of the player (without the #).

        :return:
            List of recent battles for a player.
        """
        return self.__request(f'/players/%23{player_tag}/battlelog')

    # Clans : Access clan specific information
    def get_clan_war_log(
            self,
            clan_tag: str,
            limit: int = None,
            after: str = None,
            before: str = None
    ) -> Optional[dict]:
        """
        Retrieve clan's clan war log.

        :param clan_tag:
            Tag of the clan.

        :param limit:
            Limit the number of items returned in the response.

        :param after:
            Return only items that occur after this marker. Before marker can be
            found from the response, inside the 'paging' property. Note that
            only after or before can be specified for a request, not both.

        :param before:
            Return only items that occur before this marker. Before marker can
            be found from the response, inside the 'paging' property. Note that
            only after or before can be specified for a request, not both.

        :return:
            Clan's clan war log
        """
        return self.__request(
            f'/players/%23{clan_tag}/warlog',
            params={'limit': limit, 'after': after, 'before': before}
        )


if __name__ == '__main__':
    main = ClashRoyaleAPI(json.load(open('../../config.json')).get('token', None))
    print(
        main.get_player('82LVCQGR'),
        main.get_player_upcoming_chests('82LVCQGR'),
        main.get_player_battle_log('82LVCQGR'),
        main.get_clan_war_log(''),
        sep='\n'
    )
