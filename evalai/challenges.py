import click

from evalai.utils.challenges import (
                                    display_all_challenge_list,
                                    display_future_challenge_list,
                                    display_ongoing_challenge_list,
                                    display_past_challenge_list,
                                    display_participated_or_hosted_challenges,
                                    display_challenge_phase_list,
                                    display_challenge_phase_detail,)
from evalai.utils.teams import participate_in_a_challenge
from evalai.utils.submissions import make_submission


class Challenge(object):
    """
    Stores user input ID's.
    """
    def __init__(self, challenge=None, phase=None, subcommand=None):
        self.challenge_id = challenge
        self.phase_id = phase
        self.subcommand = subcommand


class PhaseGroup(click.Group):
    """
    Fetch the submcommand data in the phase group.
    """
    def invoke(self, ctx):
        subcommand = tuple(ctx.protected_args)
        ctx.obj.subcommand = subcommand
        super(PhaseGroup, self).invoke(ctx)


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--participant', is_flag=True,
              help="List the challenges that you've participated")
@click.option('--host', is_flag=True,
              help="List the challenges that you've hosted")
def challenges(ctx, participant, host):
    """
    Lists challenges
    """
    """
    Invoked by running `evalai challenges`
    """
    if participant or host:
        display_participated_or_hosted_challenges(host, participant)
    elif ctx.invoked_subcommand is None:
        display_all_challenge_list()


@click.group()
@click.pass_context
@click.argument('CHALLENGE', type=int)
def challenge(ctx, challenge):
    """
    View challenge specific details.
    """
    ctx.obj = Challenge(challenge=challenge)


@challenges.command()
def ongoing():
    """
    List all active challenges
    """
    """
    Invoked by running `evalai challenges ongoing`
    """
    display_ongoing_challenge_list()


@challenges.command()
def past():
    """
    List all past challenges
    """
    """
    Invoked by running `evalai challenges past`
    """
    display_past_challenge_list()


@challenges.command()
def future():
    """
    List all upcoming challenges
    """
    """
    Invoked by running `evalai challenges future`
    """
    display_future_challenge_list()


@challenge.command()
@click.pass_obj
def phases(ctx):
    """
    List all phases of a challenge
    """
    """
    Invoked by running `evalai challenges CHALLENGE phases`
    """
    display_challenge_phase_list(ctx.challenge_id)


@click.group(invoke_without_command=True, cls=PhaseGroup)
@click.pass_obj
@click.argument('PHASE', type=int)
def phase(ctx, phase):
    """
    List phase details of a phase
    """
    """
    Invoked by running `evalai challenges CHALLENGE phase PHASE`
    """
    ctx.phase_id = phase
    if len(ctx.subcommand) == 0:
        display_challenge_phase_detail(ctx.challenge_id, phase)


@challenge.command()
@click.pass_obj
@click.argument('TEAM', type=int)
def participate(ctx, team):
    """
    Participate in a challenge.
    """
    """
    Invoked by running `evalai challenge CHALLENGE participate TEAM`
    """
    participate_in_a_challenge(ctx.challenge_id, team)


@phase.command()
@click.pass_obj
@click.argument('FILE', type=click.File('rb'))
def submit(ctx, file):
    """
    Make submission to a challenge.
    """
    """
    Invoked by running `evalai challenge CHALLENGE phase PHASE submit FILE`
    """
    make_submission(ctx.challenge_id, ctx.phase_id, file)


challenge.add_command(phase)
