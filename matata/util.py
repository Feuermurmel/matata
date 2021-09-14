import sys


def log(message):
    print(message, file=sys.stderr, flush=True)


class UserError(Exception):
    pass
