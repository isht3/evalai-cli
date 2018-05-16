import ast
import click
import responses

from click.testing import CliRunner
from pylsy import pylsytable

from evalai.challenges import challenges
from tests.data import challenge_response


class TestChallenges:

    def setup(self):

        json_data = ast.literal_eval(challenge_response.challenges)

        responses.add(responses.GET, 'http://localhost:8000/api/challenges/challenge/all',
                      json=json_data, status=200)

        responses.add(responses.GET, 'http://localhost:8000/api/challenges/challenge/past',
                      json=json_data, status=200)

        responses.add(responses.GET, 'http://localhost:8000/api/challenges/challenge/future',
                      json=json_data, status=200)

        column_names = ['ID', 'Challenge Name', 'Short Description']
        attributes = ['id', 'title', 'short_description']
        table = pylsytable(column_names)

        challenges_response = json_data["results"]
        for attribute, column_name in zip(attributes, column_names):
            items = []
            for challenge in challenges_response:
                if attribute == 'short_description':
                    items.append(challenge[attribute][:50])
                else:
                    items.append(challenge[attribute])

            table.add_data(column_name, items)

        self.CLI_table = str(table).rstrip()

    @responses.activate
    def test_challenge_lists(self):
        runner = CliRunner()
        result = runner.invoke(challenges, ['list'])
        response_table = result.output.rstrip()
        assert response_table == self.CLI_table

    @responses.activate
    def test_challenge_lists_past(self):
        runner = CliRunner()
        result = runner.invoke(challenges, ['list', 'past'])
        response_table = result.output.rstrip()
        assert response_table == self.CLI_table

    @responses.activate
    def test_challenge_lists_future(self):
        runner = CliRunner()
        result = runner.invoke(challenges, ['list', 'future'])
        response_table = result.output.rstrip()
        assert response_table == self.CLI_table
