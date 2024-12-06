#!/home/rens/.virtualenvs/monitor/bin/python
import os
import sys
import threading
from typing import Type

import click
from dotenv import load_dotenv
from loguru import logger

from monitor.api import API
from monitor.cliprinter import CliPrinter
from monitor.handler import Handler
from monitor.poller import Poller
from monitor.screenupdater import ScreenUpdater
from monitor.tray import SystrayCreator

load_dotenv()

API_KEY = os.getenv("API_KEY")
USER_AGENT = os.getenv("USER_AGENT")


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("--debug/--no-debug", default=False)
@click.option(
    "--api-key",
    default=API_KEY,
    help="Override API_KEY environment variable.",
)
@click.option(
    "--api-url",
    default="https://api.ned.nl/v1",
    show_default=True,
)
@click.option(
    "--user-agent",
    default=USER_AGENT,
    help="Override USER_AGENT environment varaible.",
)
@click.option(
    "--polltime",
    default=60,
    show_default=True,
)
@click.version_option(package_name="co2monitor")
@click.pass_context
def app(ctx, debug, api_key, api_url, user_agent, polltime):
    "Shows the current CO2 emissions per kWh of electricity in the Netherlands."
    logger.remove()
    logger.add(sys.stdout, level="DEBUG" if debug else "INFO")
    ctx.ensure_object(dict)
    ctx.obj["api_url"] = api_url
    ctx.obj["api_key"] = api_key
    ctx.obj["user_agent"] = user_agent
    ctx.obj["polltime"] = polltime


def default_handler(handler: Type[Handler]):
    def decorator(command_function):
        @click.pass_context
        def wrapper(ctx, *args, **kwargs):
            run(ctx.obj, handler())

        return wrapper

    return decorator


@app.command(name="cli", help="Print emissions to the commandline.")
@default_handler(CliPrinter)
def cli():
    pass


@app.command(name="screen", help="Show emissions on an EPD screen connected via GPIO.")
@default_handler(ScreenUpdater)
def screen():
    pass


@app.command(name="tray", help="Add a system tray icon with emissions.")
@click.pass_context
def tray(ctx):
    with SystrayCreator() as handler:
        t = threading.Thread(target=lambda: run(ctx.obj, handler))
        t.start()
        handler.app.exec()


def run(opts: dict, handler: Handler):
    api = API(opts["api_url"], opts["api_key"], opts["user_agent"])
    poller = Poller(api, handler, int(opts["polltime"]))
    poller.start()
