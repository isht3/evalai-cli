import click
from click import echo

from evalai.utils.submissions import (
                                      submit_file,
                                      get_submission_details
                                     )


@click.group(invoke_without_command=True)
@click.pass_context
@click.argument('SUBMISSION', type=int)
def submission(ctx, submission):
    """
    Get status of a particular submission.
    Invoked by `evalai submission SUBMISSION`.
    """
    get_submission_details(submission)


@submission.command()
@click.argument('file', type=click.File('rb'))
def submit(file):
    submit_file(file)
