import os
import json
import requests
import sys

from click import echo, style

from evalai.utils.auth import get_headers
from evalai.utils.urls import Urls
from evalai.utils.common import valid_token


API_HOST_URL = os.environ.get("EVALAI_API_URL", 'http://localhost:8000')


def submit_file(file):
    url = "http://localhost:8000/api/jobs/challenge/4/challenge_phase/7/submission/"
    headers = get_headers()
    file = {'input_file': file}
    data = {
            'status': 'submitting',
           }

    response = requests.post(
                            url,
                            headers=headers,
                            files=file,
                            data=data,
                            )
    print(response.text)


def print_submission_details(submission):
    """
    Pretty prints details of submission
    """
    team_title = "\n{}".format(style(submission['participant_team_name'], bold=True, fg="green"))
    sid = "Submission ID: {}\n".format(style(str(submission['id']), bold=True, fg="blue"))

    title = "{} {}".format(team_title, sid)

    status = style("\nSubmission Status : {}\n".format(
                                submission['status']), bold=True)
    execution_time = style("\nSubmission Status : {}\n".format(
                                submission['execution_time']), bold=True)
    submitted_at = style("\nSubmission Status : {}\n".format(
                                submission['submitted_at'].split('T')[0]), bold=True)

    phase = "{}{}{}{}".format(title, status, execution_time, submitted_at)
    echo(phase)


def get_submission_details(submission_id, challenge_id=4, phase_id=7):
    """
    Fetches the details of a particular submission
    """
    url = Urls.submission.value
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
        print_submission_details(response_json)
