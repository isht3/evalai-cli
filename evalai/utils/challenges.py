import requests
import sys

from bs4 import BeautifulSoup
from click import echo, style

from evalai.utils.auth import get_request_header
from evalai.utils.common import validate_token
from evalai.utils.urls import URLS
from evalai.utils.config import API_HOST_URL, EVALAI_ERROR_CODES


def pretty_print_challenge_data(challenge):
    """
    Function to print the challenge data
    """
    br = style("----------------------------------------"
               "--------------------------", bold=True)

    challenge_title = "\n{}".format(style(challenge["title"],
                                    bold=True, fg="green"))
    challenge_id = "ID: {}\n\n".format(style(str(challenge["id"]),
                                       bold=True, fg="blue"))

    title = "{} {}".format(challenge_title, challenge_id)

    cleaned_desc = BeautifulSoup(challenge["short_description"], "lxml").text
    description = "{}\n".format(cleaned_desc)
    end_date = "End Date : {}".format(style(challenge["end_date"].split("T")[0], fg="red"))
    end_date = "\n{}\n\n".format(style(end_date, bold=True))
    challenge = "{}{}{}{}".format(title, description, end_date, br)
    echo(challenge)


def display_challenges(url):
    """
    Function to fetch & display the challenge list based on API
    """

    header = get_request_header()
    try:
        response = requests.get(url, headers=header)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if (response.status_code == 401):
            validate_token(response.json())
        echo(err)
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        echo(err)
        sys.exit(1)

    response = response.json()

    challenges = response["results"]
    if len(challenges) is not 0:
        for challenge in challenges:
            pretty_print_challenge_data(challenge)
    else:
        echo("Sorry, no challenges found!")


def display_all_challenge_list():
    """
    Displays the list of all challenges from the backend
    """
    url = "{}{}".format(API_HOST_URL, URLS.challenge_list.value)
    display_challenges(url)


def display_past_challenge_list():
    """
    Displays the list of past challenges from the backend
    """
    url = "{}{}".format(API_HOST_URL, URLS.past_challenge_list.value)
    display_challenges(url)


def display_ongoing_challenge_list():
    """
    Displays the list of ongoing challenges from the backend
    """
    url = "{}{}".format(API_HOST_URL, URLS.challenge_list.value)
    display_challenges(url)


def display_future_challenge_list():
    """
    Displays the list of future challenges from the backend
    """
    url = "{}{}".format(API_HOST_URL, URLS.future_challenge_list.value)
    display_challenges(url)


def get_participant_or_host_teams(url):
    """
    Returns the participant or host teams corresponding to the user
    """
    header = get_request_header()

    try:
        response = requests.get(url, headers=header)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if (response.status_code == 401):
            validate_token(response.json())
        echo(err)
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        echo(err)
        sys.exit(1)

    response = response.json()

    return response['results']


def get_participant_or_host_team_challenges(url, teams):
    """
    Returns the challenges corresponding to the participant or host teams
    """
    challenges = []
    for team in teams:
        header = get_request_header()
        try:
            response = requests.get(url.format(team['id']), headers=header)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            if (response.status_code == 401):
                validate_token(response.json())
            echo(err)
            sys.exit(1)
        except requests.exceptions.RequestException as err:
            echo(err)
            sys.exit(1)
        response = response.json()
        challenges += response['results']
    return challenges


def display_participated_or_hosted_challenges(is_host=False, is_participant=False):
    """
    Function to display the participated or hosted challenges by a user
    """

    challenges = []

    if is_host:
        team_url = "{}{}".format(API_HOST_URL,
                                 URLS.host_teams.value)
        challenge_url = "{}{}".format(API_HOST_URL,
                                      URLS.host_challenges.value)

        teams = get_participant_or_host_teams(team_url)
        challenges = get_participant_or_host_team_challenges(challenge_url, teams)
        echo(style("\nHosted Challenges\n", bold=True))

        if len(challenges) != 0:
            for challenge in challenges:
                pretty_print_challenge_data(challenge)
        else:
            echo("Sorry, no challenges found!")

    if is_participant:
        team_url = "{}{}".format(API_HOST_URL,
                                 URLS.participant_teams.value)
        challenge_url = "{}{}".format(API_HOST_URL,
                                      URLS.participant_challenges.value)

        teams = get_participant_or_host_teams(team_url)
        challenges = get_participant_or_host_team_challenges(challenge_url, teams)
        echo(style("\nParticipated Challenges\n", bold=True))

        if len(challenges) != 0:
            for challenge in challenges:
                pretty_print_challenge_data(challenge)
        else:
            echo("Sorry, no challenges found!")


def pretty_print_challenge_details(challenge):
    """
    Function to pretty print the challenge details.
    """
    challenge_title = style(challenge["title"], bold=True, fg="green")
    challenge_id = "ID: {}".format(style(str(challenge["id"]), bold=True))

    challenge_title = "\n{} {}\n".format(challenge_title, challenge_id)
    print(challenge_title)

    start_date = style(challenge["start_date"], bold=True)
    start_date = "Start Date: {}\n".format(start_date)
    print(start_date)

    end_date = style(challenge["end_date"], bold=True)
    end_date = "End Date: {}\n".format(end_date)
    print(end_date)

    team = style(challenge["creator"]["team_name"], bold=True)
    team = "Organised By: {}\n".format(team)
    print(team)

    description = style(challenge["description"])
    description = "{}\n{}\n".format(style("Description", bold=True, fg="yellow"), description)
    print(description)

    submission_guidelines = style(challenge["submission_guidelines"])
    submission_guidelines = "{}\n{}\n".format(style("Submission Guidelines", bold=True, fg="yellow"), submission_guidelines)
    print(submission_guidelines)

    evaluation_details = style(challenge["evaluation_details"])
    evaluation_details = "{}\n{}\n".format(style("Evaluation Details", bold=True, fg="yellow"), evaluation_details)
    print(evaluation_details)

    terms_and_conditions = style(challenge["terms_and_conditions"])
    terms_and_conditions = "{}\n{}\n".format(style("Terms and Conditions", bold=True, fg="yellow"), terms_and_conditions)
    print(terms_and_conditions)


def display_challenge_details(challenge):
    """
    Function to display challenge details.
    """
    url = URLS.challenge_details.value
    url = "{}{}".format(API_HOST_URL, url)
    url = url.format(challenge)

    header = get_request_header()
    try:
        response = requests.get(url, headers=header)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if (response.status_code == 401):
            validate_token(response.json())
        echo(err)
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        echo(err)
        sys.exit(1)

    response = response.json()
    pretty_print_challenge_details(response)


def pretty_print_all_challenge_phases(phases):
    """
    Function to print all the challenge phases of a challenge
    """
    for phase in phases:
        br = style("--------------------------------"
                   "----------------------------------", bold=True)

        phase_title = "\n{}".format(style(phase["name"], bold=True,
                                          fg="green"))
        challenge_id = "Challenge ID: {}".format(style(str(phase["challenge"]),
                                                       bold=True, fg="blue"))
        phase_id = "Phase ID: {}\n\n".format(style(str(phase["id"]),
                                                   bold=True, fg="blue"))

        phase_title = "{} {} {}".format(phase_title, challenge_id, phase_id)

        cleaned_desc = BeautifulSoup(phase["description"], "lxml").text
        description = "{}\n\n".format(cleaned_desc)
        challenge_phase = "{}{}{}".format(phase_title, description, br)
        echo(challenge_phase)


def display_challenge_phase_list(challenge_id):
    """
    Function to display all challenge phases for a particular challenge.
    """
    url = URLS.challenge_phase_list.value
    url = "{}{}".format(API_HOST_URL, url)
    url = url.format(challenge_id)
    headers = get_request_header()

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if (response.status_code in EVALAI_ERROR_CODES):
            validate_token(response.json())
            echo(style("Error: {}".format(response.json()["error"], fg="red", bold=True)))
        else:
            echo(err)
    except requests.exceptions.RequestException as err:
        echo(err)
        sys.exit(1)

    response = response.json()
    challenge_phases = response["results"]
    pretty_print_all_challenge_phases(challenge_phases)


def pretty_print_challenge_phase_data(phase):
    """
    Function to print the details of a challenge phase.
    """
    phase_title = "\n{}".format(style(phase["name"], bold=True, fg="green"))
    challenge_id = "Challenge ID: {}".format(style(str(phase["challenge"]), bold=True, fg="blue"))
    phase_id = "Phase ID: {}\n\n".format(style(str(phase["id"]), bold=True, fg="blue"))

    title = "{} {} {}".format(phase_title, challenge_id, phase_id)

    cleaned_desc = BeautifulSoup(phase["description"], "lxml").text
    description = "{}\n".format(cleaned_desc)

    start_date = "Start Date : {}".format(style(phase["start_date"].split("T")[0], fg="green"))
    start_date = "\n{}\n".format(style(start_date, bold=True))

    end_date = "End Date : {}".format(style(phase["end_date"].split("T")[0], fg="red"))
    end_date = "\n{}\n".format(style(end_date, bold=True))
    max_submissions_per_day = style("\nMaximum Submissions per day : {}\n".format(
                                    str(phase["max_submissions_per_day"])), bold=True)

    max_submissions = style("\nMaximum Submissions : {}\n".format(str(phase["max_submissions"])),
                            bold=True)

    codename = style("\nCode Name : {}\n".format(phase["codename"]), bold=True)
    leaderboard_public = style("\nLeaderboard Public : {}\n".format(phase["leaderboard_public"]), bold=True)
    is_active = style("\nActive : {}\n".format(phase["is_active"]), bold=True)
    is_public = style("\nPublic : {}\n".format(phase["is_public"]), bold=True)

    challenge_phase = "{}{}{}{}{}{}{}{}{}{}".format(title, description, start_date,
                                                    end_date,
                                                    max_submissions_per_day,
                                                    max_submissions,
                                                    leaderboard_public,
                                                    codename, is_active, is_public)
    echo(challenge_phase)


def display_challenge_phase_detail(challenge_id, phase_id):
    """
    Function to print details of a challenge phase.
    """
    url = URLS.challenge_phase_detail.value
    url = "{}{}".format(API_HOST_URL, url)
    url = url.format(challenge_id, phase_id)
    headers = get_request_header()

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if (response.status_code in EVALAI_ERROR_CODES):
            validate_token(response.json())
            echo(style("Error: {}".format(response.json()["error"], fg="red", bold=True)))
        else:
            echo(err)
    except requests.exceptions.RequestException as err:
        echo(err)
        sys.exit(1)

    response = response.json()

    phase = response
    pretty_print_challenge_phase_data(phase)
