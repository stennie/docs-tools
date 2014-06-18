import json
import logging
import os

logger = logging.getLogger(os.path.basename(__file__))

import argh

from giza.config.runtime import RuntimeStateConfig

import giza.operations.generate
from giza.operations.configuration import render_config
from giza.operations.clean import clean
from giza.operations.git import apply_patch, pull_rebase, cherry_pick
from giza.operations.sphinx import sphinx

def main():
    parser = argh.ArghParser()
    parser.add_argument('--level', '-l',
                        choices=['debug', 'warning', 'info', 'critical', 'error'],
                        default='info')
    parser.add_argument('--serial', '-s', default=None, dest='runner', const='serial', action='store_const')
    parser.add_argument('--force', '-f', default=False, action='store_true')

    commands = [
        render_config,
        clean,
        sphinx
    ]

    argh.add_commands(parser, commands)
    argh.add_commands(parser, [apply_patch, pull_rebase, cherry_pick], namespace='git')

    generate_commands = [
        giza.operations.generate.api,
        giza.operations.generate.assets,
        giza.operations.generate.images,
        giza.operations.generate.intersphinx,
        giza.operations.generate.options,
        giza.operations.generate.primer,
        giza.operations.generate.steps,
        giza.operations.generate.tables,
        giza.operations.generate.toc,
    ]

    argh.add_commands(parser, generate_commands, namespace='generate')

    args = RuntimeStateConfig()
    argh.dispatch(parser, namespace=args)

if __name__ == '__main__':
    main()