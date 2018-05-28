import os
import requests
import sys

from click import echo, style

from pylsy import pylsytable

from evalai.utils.auth import get_headers
from evalai.utils.urls import Urls
from evalai.utils.common import valid_token


API_HOST_URL = os.environ.get("EVALAI_API_URL", 'http://localhost:8000')


def print_challenge_table(challenge):
    br = style("------------------------------------------------------------------", bold=True)

    challenge_title = "\n{}".format(style(challenge["title"], bold=True, fg="green"))
    challenge_id = "ID: {}\n\n".format(style(str(challenge["id"]), bold=True, fg="blue"))

    title = "{} {}".format(challenge_title, challenge_id)

    description = "{}\n".format(challenge["short_description"])
    date = "End Date : " + style(challenge["end_date"].split("T")[0], fg="red")
    date = "\n{}\n\n".format(style(date, bold=True))
    challenge = "{}{}{}{}".format(title, description, date, br)
    return challenge


def get_challenges(url):

    headers = get_headers()
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        echo(err)
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        echo(err)
        sys.exit(1)

    response_json = response.json()
    if valid_token(response_json):

        challenges = response_json["results"]
        if len(challenges) is not 0:
            for challenge in challenges:
                challenge = print_challenge_table(challenge)
                echo(challenge)
        else:
            echo("Sorry, no challenges found.")


def get_challenge_list():
    """
    Fetches the list of challenges from the backend.
    """
    url = "{}{}".format(API_HOST_URL, Urls.challenge_list.value)
    get_challenges(url)


def get_past_challenge_list():
    """
    Fetches the list of past challenges from the backend.
    """
    url = "{}{}".format(API_HOST_URL, Urls.past_challenge_list.value)
    get_challenges(url)


def get_ongoing_challenge_list():
    """
    Fetches the list of ongoing challenges from the backend.
    """
    url = "{}{}".format(API_HOST_URL, Urls.challenge_list.value)
    get_challenges(url)


def get_future_challenge_list():
    """
    Fetches the list of future challenges from the backend.
    """
    url = "{}{}".format(API_HOST_URL, Urls.future_challenge_list.value)
    get_challenges(url)


def get_phase_list(challenge_id):
    """
    Gets the phase lists of a particular challenge.
    """
    url = Urls.phase_list.value
    url = "{}{}".format(API_HOST_URL, url)    
    url = url.format(challenge_id)
    headers = get_headers()

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        echo(err)
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        echo(err)
        sys.exit(1)

    response_json = response.json()
    if valid_token(response_json):
        phases = response_json["results"]
        for phase in phases:
            br = style("------------------------------------------------------------------", bold=True)

            phase_title = "\n{}".format(style(phase["name"], bold=True, fg="green"))            
            challenge_id = "Challenge ID: {}".format(style(str(phase["challenge"]), bold=True, fg="blue"))
            phase_id = "Phase ID: {}\n\n".format(style(str(phase["id"]), bold=True, fg="blue"))

            title = "{} {} {}".format(phase_title, challenge_id, phase_id)

            description = "{}\n\n".format(phase["description"])
            phase = "{}{}{}".format(title, description, br)
            echo(phase)


def get_phase_details(challenge_id, phase_id):
    """
    Gets the phase details of a particular challenge phase.
    """
    url = Urls.phase_details.value
    url = "{}{}".format(API_HOST_URL, url)    
    url = url.format(challenge_id, phase_id)
    headers = get_headers()

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        echo(err)
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        echo(err)
        sys.exit(1)


    response_json = response.json()

    if valid_token(response_json):
        phase = response_json

        phase_title = "\n{}".format(style(phase["name"], bold=True, fg="green"))            
        challenge_id = "Challenge ID: {}".format(style(
                                          str(phase["challenge"]), bold=True, fg="blue"))
        phase_id = "Phase ID: {}\n\n".format(style(str(phase["id"]), bold=True, fg="blue"))

        title = "{} {} {}".format(phase_title, challenge_id, phase_id)

        description = "{}\n".format(phase["description"])

        start_date = "Start Date : " + style(phase["start_date"].split("T")[0], fg="green")
        start_date = "\n{}\n".format(style(start_date, bold=True))

        end_date = "End Date : " + style(phase["end_date"].split("T")[0], fg="red")
        end_date = "\n{}\n".format(style(end_date, bold=True))

        max_submissions_per_day = style("\nMaximum Submissions per day : {}\n".format(
                                    str(phase["max_submissions_per_day"])), bold=True)

        max_submissions = style("\nMaximum Submissions : {}\n".format(
                                    str(phase["max_submissions"])), bold=True)

        codename = style("\nCode Name : {}\n".format(
                                              phase["codename"]), bold=True)

        leaderboard_public = style("\nLeaderboard Public : {}\n".format(
                                              phase["leaderboard_public"]), bold=True)

        is_active = style("\nActive : {}\n".format(
                                              phase["is_active"]), bold=True)

        is_public = style("\nPublic : {}\n".format(
                                              phase["is_public"]), bold=True)

        phase = "{}{}{}{}{}{}{}{}{}{}".format(title, description, start_date, end_date,
                                          max_submissions_per_day, max_submissions, leaderboard_public,
                                          codename, is_active, is_public)
        echo(phase)
