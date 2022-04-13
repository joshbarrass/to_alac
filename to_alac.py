#!/usr/bin/env python3
"""to_alac
Usage:
  to_alac [-v] [-V] [--outdir=<directory>] [-y] <input_files>...
  to_alac -h | --help
  to_alac --version

Options:
  -h --help                 Show this screen
  -v --verbose              Verbose logging
  -V --debug                Print debugging information
  -o --outdir=<directory>   Directory to write files to [default: .]
  -y --overwrite            Overwrite file if it already exists
"""

import logging
import os

import docopt

from converter import convert
from consts import LOGGING_FORMAT

VERSION = "0.1.0"

if __name__ == '__main__':
    logging.basicConfig(format=LOGGING_FORMAT, level=logging.WARNING)
    logger = logging.getLogger("to_alac")

    arguments = docopt.docopt(__doc__, version=VERSION)
    if arguments["--debug"]:
        logger.setLevel(level=logging.DEBUG)
    elif arguments["--verbose"]:
        logger.setLevel(level=logging.INFO)

    logger.debug("arguments: {}".format(arguments))

    output_dir = os.path.abspath(arguments["--outdir"])
    logger.info("Outputting to directory: {}".format(output_dir))

    num_to_convert = len(arguments["<input_files>"])
    for i, fp in enumerate(arguments["<input_files>"]):
        logger.info(
            "Converting {} of {}: {}".format(
                i + 1, num_to_convert, fp
            )
        )
        convert(
            fp, out_dir=output_dir, overwrite=arguments["--overwrite"]
        )
