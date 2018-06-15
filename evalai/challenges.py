import click
from click import echo

from evalai.utils.challenges import (
                                    get_challenge_list,
                                    get_ongoing_challenge_list,
                                    get_past_challenge_list,
                                    get_future_challenge_list,
                                    get_challenge_count,)
from evalai.utils.submissions import get_submission_stats


class Challenge(object):
    def __init__(self, challenge=None, phase=None):
        self.CHALLENGE = challenge
        self.PHASE = phase


@click.group(invoke_without_command=True)
@click.pass_context
def challenges(ctx):
    """
    Challenges and related options.
    """
    if ctx.invoked_subcommand is None:
        welcome_text = ("Welcome to the EvalAI CLI. Use evalai"
                        "challenges --help for viewing all the options.")
        echo(welcome_text)


@click.group()
@click.pass_context
@click.argument('CHALLENGE', type=int)
def challenge(ctx, challenge):
    """
    Displays challenge specific details.
    """
    ctx.obj = Challenge(challenge)


@click.group(invoke_without_command=True, name='list')
@click.pass_context
@click.option('--participant', is_flag=True,
              help="Show the challenges that you've participated")
@click.option('--host', is_flag=True,
              help="Show the challenges that you've hosted")
def list_challenges(ctx, participant, host):
    """
    Used to list challenges.
    Invoked by running `evalai challenges list`
    """
    if participant:
        get_challenge_count(host, participant)
    elif host:
        get_challenge_count(host, participant)
    elif ctx.invoked_subcommand is None:
        get_challenge_list()


@click.command(name='ongoing')
def list_ongoing_challenges():
    """
    Used to list all the challenges which are active.
    Invoked by running `evalai challenges list ongoing`
    """
    get_ongoing_challenge_list()


@click.command(name='past')
def list_past_challenges():
    """
    Used to list all the past challenges.
    Invoked by running `evalai challenges list past`
    """
    get_past_challenge_list()


@click.command(name='future')
def list_future_challenges():
    """
    Used to list all the challenges which are coming up.
    Invoked by running `evalai challenges list future`
    """
    get_future_challenge_list()


@click.group(invoke_without_command=True)
@click.pass_obj
@click.argument('PHASE', type=int)
def phase(ctx, phase):
    """
    Displays details a particular phase.
    Invoked by running `evalai challenge CHALLENGE phase PHASE`
    """
    ctx.PHASE = phase


@phase.command(name='submission-stats')
@click.pass_obj
def submission_stats(ctx):
    """
    Your submissions stats to a particular Challenge.
    Invoked by running `evalai challenge CHALLENGE phase PHASE submission-stats`.
    """
    get_submission_stats(ctx.CHALLENGE, ctx.PHASE)


challenge.add_command(phase)


# Command -> evalai challenges list
challenges.add_command(list_challenges)

# Command -> evalai challenges list ongoing/past/future
list_challenges.add_command(list_ongoing_challenges)
list_challenges.add_command(list_past_challenges)
list_challenges.add_command(list_future_challenges)
