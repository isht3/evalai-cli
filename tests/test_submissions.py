import json
import responses

from click.testing import CliRunner

from evalai.submissions import submission
from tests.data import submission_response

from evalai.utils.challenges import API_HOST_URL
from evalai.utils.urls import Urls


class TestSubmission:

    def setup(self):

        self.submission = json.loads(submission_response.submission)

        url = "{}{}"
        responses.add(responses.GET, url.format(API_HOST_URL, Urls.submission.value).format("4", "7"),
                      json=self.submission, status=200)


    @responses.activate
    def test_get_submission(self):


        team_title = "\n{}".format(self.submission['participant_team_name'])
        sid = "Submission ID: {}\n".format(str(self.submission['id']))

        title = "{} {}".format(team_title, sid)

        status = "\nSubmission Status : {}\n".format(
                                    self.submission['status'])
        execution_time = "\nSubmission Status : {}\n".format(
                                    self.submission['execution_time'])
        submitted_at = "\nSubmission Status : {}\n".format(
                                    self.submission['submitted_at'].split('T')[0])

        phase = "{}{}{}{}\n".format(title, status, execution_time, submitted_at)

        runner = CliRunner()
        result = runner.invoke(submission, ['9'])
        response = result.output
        assert response == phase