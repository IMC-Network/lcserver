import argparse

import logging
import streaming

cli = argparse.ArgumentParser(
    prog = "lcserver",
    description = "Server environment for coordinating media management and streaming on behalf of LiveCloud apps."
)

cli.add_argument(
    "-i", "--input-handler",
    help = "choose input handler for command input",
    type = str,
    nargs = "?",
    choices = ["tty", "lc"], 
    default = "tty"
)

cli.add_argument(
    "-o", "--print-handler",
    help = "choose print handler for log output",
    type = str,
    nargs = "?",
    choices = ["tty", "lc"], 
    default = "tty"
)

arguments = cli.parse_args()

print(arguments)