import click

from datetime import datetime
from rireki.utils.time_helpers import now

timestamps = False


def enable_timestamps():
    global timestamps
    timestamps = True


def log(message):
    if timestamps:
        prefix = '[%s] ' % datetime.fromtimestamp(now()).isoformat()
    else:
        prefix = ''

    click.echo(prefix + message)
