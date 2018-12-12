#!/usr/bin/env python3
"""
Usage:
    run.py (-h | --help | --version)
    run.py initialize <app>
    run.py server <app>

Options:
    -h, --help
        Show this help message and exit
    --version, -V
        Display the version of Vial
"""

from docopt import docopt


def initialize(app_name):
    project = __import__(f'{app_name}.app')
    application = getattr(project, 'app')
    application.initialize_db()


def server(app_name):
    project = __import__(f'{app_name}.app')
    application = getattr(project, 'app')
    application.run_server()


def cli():
    args = docopt(__doc__, version='0.1.0')

    try:
        if args['server']:
            server(args['<app>'])
        elif args['initialize']:
            initialize(args['<app>'])

    except ModuleNotFoundError as e:
        print("The application you've specified does not exist or hasn't been organized correctly")


if __name__ == '__main__':
    cli()
