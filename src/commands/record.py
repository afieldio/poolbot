import requests

from .base import BaseCommand


class RecordCommand(BaseCommand):
    """Records the result of a match."""

    command_term = 'record'
    url_path = 'api/match/'
    victory_nouns = (
        'beat',
        'defeated',
        'clobbered',
        'crushed',
        'defeated',
        'disgraced',
        'embarrased',
        'grannied',
        'hammered',
        'obliterated',
        'pounded',
        'trounced',
        'thrashed',
        'walloped',
    )

    def process_request(self, message):
        """The author is always the winner."""
        try:
            defeated_player = self._find_user_mentions(message)[0]
        except IndexError:
            return 'Sorry, I was unable to find an opponent in that message...' 

        lower_text = message['text'].lower()
        if not any(noun in lower_text for noun in self.victory_nouns):
            return 'Sorry, I am unable to determine the result'

        response = requests.post(
            self._generate_url(),
            data={
                'winner': message['user'],
                'loser': defeated_player,
                'channel': message['channel'],
                'granny': 'grannied' in lower_text,
            }
        )

        if response.status_code == 201:
            return 'Another big win for {winner}! Victory recorded in the DB.'.format(
                winner=self.poolbot.users[message['user']]['name']
            )
        else:
            return 'Sorry, I was unable to record that result.'
        # TODO generate some funny phrase to celebrate the victory
        # eg highlight an unbetean run, or X consequtive lose etc
