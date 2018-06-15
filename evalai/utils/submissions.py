
import os
import requests
import sys

from beautifultable import BeautifulTable
from click import echo, style

from evalai.utils.auth import get_headers
from evalai.utils.urls import Urls
from evalai.utils.common import valid_token


API_HOST_URL = os.environ.get("EVALAI_API_URL", 'http://localhost:8000')


def display_submission_table(submissions):
    """
    Displays the submissions for a particular Challenge.
    """
    table = BeautifulTable()
    print(submissions)


def get_submission_stats(challenge_id, phase_id):
    """
    Fetches stats of a particular challenge..
    """
    url = Urls.submissions.value
    url = "{}{}".format(API_HOST_URL, url)
    url = url.format(challenge_id, phase_id)
    headers = get_headers()

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        echo(style("Error: " + response.json()['error'], fg="red", bold=True))
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        echo(err)
        sys.exit(1)

    response_json = response.json()

    if valid_token(response_json):
        submissions = response_json["results"]
        display_submission_table(submissions)
