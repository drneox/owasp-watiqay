from __about__ import __version__
from server import Server
from db import Client, Structure
from time import sleep
from __logging__ import logging

from config import INTERVAL_SCANNING

logging = logging.getLogger(__name__)

if __name__ == '__main__':
    logging.info(f'OWASP-Watiqay v{ __version__}')

    while True:
        for client in Client.objects:
            try:
                structure = Structure.objects(
                    client=client).order_by('-_id')[0]['structure']
                get_web = Server(
                    id=client.id,
                    mail=client.email,
                    base=structure,
                    hostname=client.hostname,
                    path=client.path,
                    remote=False)
            except IndexError:
                logging.error('structure not found')
                structure = Structure(client=client)
                structure.save()
                get_web = Server(
                    id=client.id,
                    mail=client.email,
                    base=None,
                    hostname=client.hostname,
                    path=client.path,
                    remote=client.remote)
            logging.debug(get_web.compare())

            sleep(INTERVAL_SCANNING)
