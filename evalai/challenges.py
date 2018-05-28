import click
from click import echo

from evalai.utils.challenges import (
                                    get_challenge_list,
                                    get_ongoing_challenge_list,
                                    get_past_challenge_list,
                                    get_future_challenge_list,
                                    get_phase_list,
                                    get_phase_details,)


@click.group(invoke_without_command=True)
@click.pass_context
def challenges(ctx):
    """
    Challenges and related options.
    """
    if ctx.invoked_subcommand is None:
        welcome_text = """Welcome to the EvalAI CLI. Use evalai challenges --help for viewing all the options."""
        echo(welcome_text)


@click.group(invoke_without_command=True, name='list')
@click.pass_context
def list_challenges(ctx):
    """
    Used to list all the challenges.
    Invoked by running `evalai challenges list`
    """
    if ctx.invoked_subcommand is None:
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
@click.pass_context
@click.option('-c',
              help="Challenge ID for viewing its phases.")
@click.option('-p',
              help="Phase ID for showing the phase details")
def phases(ctx, c, p):
    """
    Displays phase and phase related details.
    """
    if ctx.invoked_subcommand != "list":
        if c is None or p is None:
            echo("Please pass in both parameters.")
        else:
            try:
                challenge_id = int(c)
                challenge_phase_id = int(p)
                get_phase_details(challenge_id, challenge_phase_id)
            except ValueError:
                echo("The parameter passed is not an integer.")


@click.command(name='list')
@click.option('-c',
              help="Challenge ID for viewing its phases.")
def list_phases(c):
    """
    Displays phases as a list.
    """
    try:
        if c is None:
            echo("Please pass in parameters.")
        else:
            challenge_id = int(c)
            get_phase_list(challenge_id)
    except ValueError:
        echo("The parameter passed is not an integer.")


# Command -> evalai challenges list
challenges.add_command(list_challenges)

# Command -> evalai challenges list ongoing/past/future
list_challenges.add_command(list_ongoing_challenges)
list_challenges.add_command(list_past_challenges)
list_challenges.add_command(list_future_challenges)

# Command -> evalai challenges phases
challenges.add_command(phases)

# Command -> evalai challenges phases list
phases.add_command(list_phases)