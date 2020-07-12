from datetime import datetime, timedelta
from db import Client, Log, Structure
from libs.diffDic import Compare
from launcher import launcher
from config import INTERVAL_LOG
from runner import Runner
from __logging__ import logging


logging = logging.getLogger(__name__)


class Server:
    '''
    Processing Class Structure
    '''

    def __init__(self, id=None, mail=None, base=None,
                 hostname=None, path=None, remote=False):
        self.id = id
        self.mail = mail
        self.base = base
        self.hostname = hostname
        self.path = path
        self.remote = remote

    def status(self):
        status = Client.objects(id=self.id)[:0]
        return status[0].status

    def check(self):
        if self.remote:
            try:
                connect = Runner(self.hostname, self.path)
                connect.get_structure()
                data = connect.output
                logging.debug(data)
                logging.debug(connect.output)
                return data
            except ValueError as e:
                logging.error(f'{e}')
                error = 0
                return error
        else:
            import agent
            return agent.integrity_monitor(self.path)

    def log(self, type_log, item='0'):
        log = Log(client=self.id, type=type_log, item=item)
        logging.debug(f'type: {type_log} files: {item}')
        # change this time if you want to receive repeated log more often
        interval_min = datetime.now() - timedelta(minutes=INTERVAL_LOG)

        previous_log = Log.objects(
            client=self.id, type=type_log, item=str(
                ','.join(item)), date__gte=interval_min)

        if not previous_log:
            new_log = Log.objects.create(client=self.id,
                                         type=type_log,
                                         item=str(','.join(item)))

            attrs = [self.mail, self.hostname, str(
                type_log), str(','.join(item))]
            logging.debug(attrs)
            launcher(attrs, remote=self.remote)

    def compare(self):
        '''
        -adding file type 1
        -change file type 2
        -delete file type 3
        '''
        print(self.check())
        if self.check():
            new = self.check()
            if self.status() is True:
                original = self.base
                logging.debug(f'original structure: {original}')
                logging.debug(f'new structure: {new}')
                diffDic = Compare(new, original)
                if diffDic.added():
                    type_log = 1
                    item = diffDic.added()
                    self.log(type_log, item)
                if diffDic.changed():
                    type_log = 2
                    item = diffDic.changed()
                    self.log(type_log, item)
                if diffDic.removed():
                    type_log = 3
                    item = diffDic.removed()
                    self.log(type_log, item)
            else:
                # create new structure base
                client = Client.objects(id=self.id)[0]
                client.update(status=True)
                structure = Structure(client=client, structure=new)
                structure.save()
                print(structure)
        else:
            self.log(4)
            logging.error(f'connection refused - {__name__}.py')
