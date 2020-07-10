import paramiko
import os
import json
from __logging__ import logging


class Runner:
    def __init__(self, hostname, path=None):
        self.hostname = hostname
        self.output = {}
        self.path = path
        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.WarningPolicy())

    def get_structure(self):
        remote_agent = os.path.join(os.path.dirname(__file__), 'agent.py')
        self.ssh.connect(self.hostname)
        sftp = self.ssh.open_sftp()
        sftp.put(remote_agent, 'agent.py')
        sftp.close()
        stdin, stdout, stderr = self.ssh.exec_command(
            'python agent.py %s' % self.path)
        stdout = stdout.read()
        logging.debug(stdout)
        stdout = stdout.replace(''', ''')
        self.output = json.loads(stdout)
        self.ssh.close()

    def remote_commands(self):
        remote_commands = os.path.join(
            os.path.dirname(__file__),
            'plugins/remote-commands.sh')
        self.ssh.connect(self.hostname)
        sftp = self.ssh.open_sftp()
        sftp.put(remote_commands, 'remote-commands.sh')
        sftp.close()
        stdin, stdout, stderr = self.ssh.exec_command('./agent.py %s')
        stdout = stdout.read()
        logging.debug(stdout)
        stdout = stdout.replace(''', ''')
        self.output = json.loads(stdout)
        self.ssh.close()
