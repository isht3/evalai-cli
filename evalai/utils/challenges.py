import os
import json
import requests

from click import echo

from pylsy import pylsytable

from evalai.utils.auth import get_headers
from evalai.utils.common import valid_token
from evalai.utils.urls import urls


API_HOST_URL = os.environ.get("EVALAI_API_URL", 'http://localhost:8000')


def get_challenge_table(challenges):
    column_names = ['ID', 'Challenge Name', 'Short Description']
    attributes = ['id', 'title', 'short_description']
    table = pylsytable(column_names)

    for attribute, column_name in zip(attributes, column_names):
        items = []
        for challenge in challenges:
            if attribute == 'short_description':
                items.append(challenge[attribute][:50])
            else:
                items.append(challenge[attribute])

        table.add_data(column_name, items)
    return table


def get_challenges(url):
    headers = get_headers()
    response = requests.get(url, headers=headers)
    response_json = json.loads(response.text)

    if valid_token(response_json):
        challenges = response_json["results"]
        challenges_table = get_challenge_table(challenges)
        echo(challenges_table)
    else:
        echo("The authentication token you are using isn't valid. Please try again")


def get_teams(url):
    headers = get_headers()
    response = requests.get(url, headers=headers)
    response_json = json.loads(response.text)
    if valid_token(response_json):
        return response_json['results']
    else:
        return 0
        echo("The token is not valid. Try again.")


def get_challenge_list():
    """
    Fetches the list of challenges from the backend.
    """
    url = "{}{}".format(API_HOST_URL, urls["get_challenge_list"])
    get_challenges(url)


def get_past_challenge_list():
    """
    Fetches the list of challenges from the backend.
    """
    url = "{}{}".format(API_HOST_URL, urls["get_past_challenge_list"])
    get_challenges(url)


def get_future_challenge_list():
    """
    Fetches the list of challenges from the backend.
    """
    url = "{}{}".format(API_HOST_URL, urls["get_future_challenge_list"])
    get_challenges(url)


def get_challenge_count(mode):
    """
    Gets the challenge the user has participated/hosted.
    """

    challenges = []

    if mode == 'host':
        url = urls['get_host_teams']
        url = "{}{}".format(API_HOST_URL, url)
        teams = get_teams(url)
        if not teams:
            echo("The token is not valid. Try again.")

        url = "{}{}".format(API_HOST_URL, urls['get_host_challenges'])
        for team in teams:
            headers = get_headers()
            response = requests.get(url.format(team['id']), headers=headers)
            response_json = json.loads(response.text)
            challenges = challenges + response_json['results']
    elif mode == 'participate':
        url = urls['get_participant_teams']
        url = "{}{}".format(API_HOST_URL, url)
        teams = get_teams(url)
        if not teams:
            echo("The token is not valid. Try again.")

        url = "{}{}".format(API_HOST_URL, urls['get_participant_challenges'])
        for team in teams:
            headers = get_headers()
            response = requests.get(url.format(team['id']), headers=headers)
            response_json = json.loads(response.text)
            challenges = challenges + response_json['results']
    else:
        echo("Option doesn't exist. Use --help for information")

    challenges_table = get_challenge_table(challenges)
    echo(challenges_table)
