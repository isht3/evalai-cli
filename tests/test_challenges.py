import ast
import click
import responses

from click.testing import CliRunner
from pylsy import pylsytable

from evalai.challenges import challenges
from tests.data import challenge_response

from evalai.utils.challenges import get_challenge_table


class TestChallenges:

    def setup(self):

        json_data = ast.literal_eval(challenge_response.challenges)

        responses.add(responses.GET, 'http://localhost:8000/api/challenges/challenge/all',
                      json=json_data, status=200)

        responses.add(responses.GET, 'http://localhost:8000/api/challenges/challenge/past',
                      json=json_data, status=200)

        responses.add(responses.GET, 'http://localhost:8000/api/challenges/challenge/future',
                      json=json_data, status=200)

        table = get_challenge_table(json_data["results"])

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


class TestParticipantChallenges:

    def setup(self):

        challenge_data = ast.literal_eval(challenge_response.challenges)
        host_team_data = ast.literal_eval(challenge_response.challenge_host_teams)
        participant_team_data = ast.literal_eval(challenge_response.challenge_participant_teams)

        responses.add(responses.GET, 'http://localhost:8000/api/participants/participant_team',
                      json=participant_team_data, status=200)

        responses.add(responses.GET, 'http://localhost:8000/api/hosts/challenge_host_team/',
                      json=host_team_data, status=200)

        responses.add(responses.GET, 'http://localhost:8000/api/challenges/participant_team/3/challenge',
                      json=challenge_data, status=200)

        responses.add(responses.GET, 'http://localhost:8000/api/challenges/challenge_host_team/2/challenge',
                      json=challenge_data, status=200)

        challenge_table = get_challenge_table(challenge_data["results"])
        self.CLI_table = str(challenge_table).rstrip()

    @responses.activate
    def test_challenge_lists_host(self):
        runner = CliRunner()
        result = runner.invoke(challenges, ['list', '-host', 'true'])
        response_table = result.output.rstrip()
        assert response_table == self.CLI_table

    @responses.activate
    def test_challenge_lists_participant(self):
        runner = CliRunner()
        result = runner.invoke(challenges, ['list', '-participate', 'true'])
        response_table = result.output.rstrip()
        assert response_table == self.CLI_table
