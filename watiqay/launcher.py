import os
import sys
from runner import Runner
from __logging__ import logging


def launcher(attrs, remote=False):
    logging.debug(attrs)
    logging.info('launcher is starting')
    parameters = ' '.join(attrs)
    principal_dir = os.path.dirname(__file__)
    sys.path.insert(0, principal_dir)
    plugins = os.listdir(os.path.dirname(__file__) + '/plugins')
    for file in plugins:
        if file.endswith('.py'):
            os.system(f'python {principal_dir}/plugins/{file} {parameters}')
        elif file.endswith('.sh'):
            if remote:
                runner = Runner(attrs[2])
                runner.remote_commands()
