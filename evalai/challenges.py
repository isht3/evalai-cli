import click
from click import echo

from evalai.utils.challenges import (
                                    get_challenge_list,
                                    get_ongoing_challenge_list,
                                    get_past_challenge_list,
                                    get_future_challenge_list,
                                    get_challenge_count,
                                    get_phase_list,
                                    get_phase_details,)


class Challenge(object):
    def __init__(self, challenge=None):
        self.CHALLENGE = challenge


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--participant', is_flag=True,
              help="Show the challenges that you've participated")
@click.option('--host', is_flag=True,
              help="Show the challenges that you've hosted")
def challenges(ctx, participant, host):
    """
    Used to list challenges.
    Invoked by running `evalai challenges`
    """
    if participant or host:
        get_challenge_count(host, participant)
    elif ctx.invoked_subcommand is None:
        get_challenge_list()


@click.group()
@click.pass_context
@click.argument('CHALLENGE', type=int)
def challenge(ctx, challenge):
    ctx.obj = Challenge(challenge)


@challenges.command()
def ongoing():
    """
    Used to list all the challenges which are active.
    Invoked by running `evalai challenges ongoing`
    """
    get_ongoing_challenge_list()


@challenges.command()
def past():
    """
    Used to list all the past challenges.
    Invoked by running `evalai challenges past`
    """
    get_past_challenge_list()


@challenges.command()
def future():
    """
    Used to list all the challenges which are coming up.
    Invoked by running `evalai challenges future`
    """
    get_future_challenge_list()


@challenge.command()
@click.pass_obj
def phases(ctx):
    """
    Displays phase and phase related details.
    Invoked by running `evalai challenge CHALLENGE phases`
    """
    get_phase_list(ctx.CHALLENGE)


@challenge.command()
@click.pass_obj
@click.argument('PHASE', type=int)
def phase(ctx, phase):
    """
    Displays phases as a list.
    Invoked by running `evalai challenge CHALLENGE phase PHASE`
    """
    get_phase_details(ctx.CHALLENGE, phase)
