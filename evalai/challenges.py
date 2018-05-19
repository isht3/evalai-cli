import click

from click import echo

from evalai.utils.challenges import (
                                    get_challenge_list,
                                    get_past_challenge_list,
                                    get_future_challenge_list,
                                    get_challenge_count)


@click.group(invoke_without_command=True)
@click.pass_context
def challenges(ctx):
    """
    Challenges and related Options.
    """
    if ctx.invoked_subcommand is None:
        welcome_text = """Welcome to the EvalAI CLI. Use evalai challenges --help for viewing all the options"""
        echo(welcome_text)


@click.group(invoke_without_command=True, name='list')
@click.pass_context
@click.option('-participate', default='false',
              help="Show the challenges that you've participated")
@click.option('-host', default='false',
              help="Show the challenges that you've hosted")
def list_challenges(ctx, participate, host):
    """
    Lists all challenges.
    """
    if participate == 'true':
        get_challenge_count("participate")
    elif host == 'true':
        get_challenge_count("host")
    elif ctx.invoked_subcommand is None:
        get_challenge_list()


@click.command(name='past')
def list_past_challenges():
    """
    Lists past challenges.
    """
    get_past_challenge_list()


@click.command(name='future')
def list_future_challenges():
    """
    Lists future challenges.
    """
    get_future_challenge_list()


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('-c',
              help="Challenge ID for viewing its phases.")
@click.option('-p',
              help="Shows the phase details")
def phases(ctx, c, p):
    """
    Displays phase and phase related details.
    """
    print(ctx.invoked_subcommand, c, p)


@click.command(name='list')
@click.option('-c',
              help="Challenge ID for viewing its phases.")
def list_phases(c):
    """
    Displays phases as a list.
    """
    echo(c)


# Command -> evalai challenges list
challenges.add_command(list_challenges)

# Command -> evalai challenges list ongoing/past/future
list_challenges.add_command(list_past_challenges)
list_challenges.add_command(list_future_challenges)


# Command -> evalai challenges phases
challenges.add_command(phases)

# Command -> evalai challenges phases list
phases.add_command(list_phases)