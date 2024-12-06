import os

import click

import q3rconlib


@click.command()
@click.option("--host", default="localhost", show_default=True)
@click.option("--port", type=click.IntRange(1024, 65535), default=28960)
@click.option("--password", default=os.environ.get("RCON_PASS"))
@click.option("--login-timeout", type=click.FloatRange(0.01), default=2.0)
def run(host: str, port: int, password: str, login_timeout: float):
    with q3rconlib.connect(
        host=host, port=port, password=password, login_timeout=login_timeout
    ) as rcon:
        click.echo("Press 'Q' or <Enter> to exit")

        while input_line := click.prompt("cmd", default="", show_default=False):
            if input_line.upper() == "Q":
                break

            if resp := rcon.send(input_line):
                click.echo(resp)
