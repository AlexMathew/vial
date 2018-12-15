#!/usr/bin/env python3
"""
Usage:
    vial (-h | --help | --version)
    vial initialize
    vial server [--host=<host>] [--port=<port>]

Options:
    -h, --help
        Show this help message and exit
    --version, -V
        Display the version of Vial
    --host=<host>, -H <host>
        Specifies the host name to run on [default: 127.0.0.1]
    --port=<port>, -P <port>
        Specifies the port to run on [default: 8000]
"""

from docopt import docopt
import ipdb


def initialize():
    project = __import__('app')
    application = getattr(project, 'app')
    application.initialize_db()


def server(host, port):
    project = __import__('app')
    application = getattr(project, 'app')
    application.run_server(host=host, port=port)


def cli():
    args = docopt(__doc__, version='0.1.0')

    try:
        if args['server']:
            server(host=args['--host'], port=int(args['--port']))
        elif args['initialize']:
            initialize()

    except ModuleNotFoundError as e:
        print("The application does not exist or hasn't been organized correctly")


if __name__ == '__main__':
    cli()
