from db import Client, Log
from termcolor import cprint
import sys
from tabulate import tabulate


class Menu:
    def __init__(self):
        cprint(' ____    __    ____  ___   .___________. __    ______           ___   ____    ____\n'
               ' \   \  /  \  /   / /   \  |           ||  |  /  __  \         /   \  \   \  /   /\n'
               '  \   \/    \/   / /  ^  \ `---|  |----`|  | |  |  |  |       /  ^  \  \   \/   /\n'
               '   \            / /  /_\  \    |  |     |  | |  |  |  |      /  /_\  \  \_    _/\n'
               '    \    /\    / /  _____  \   |  |     |  | |  `--'  '--.  /  _____  \   |  |\n'
               '     \__/  \__/ /__/     \__\  |__|     |__|  \_____\_____\/__/     \__\  |__|  v 0.5 \n',
               'yellow', attrs=['bold'])

        cprint('(watiqay.org)', 'yellow', attrs=['bold'])
        cprint('-----------------------------------', 'yellow', attrs=['bold'])

    @staticmethod
    def main():
        while True:
            option = input('wtq >')
            if option == 'exit':
                sys.exit()
            else:
                try:
                    getattr(Menu, option)()
                except AttributeError as e:
                    print('invalid option')
                    print(e)

    @staticmethod
    def clear():
        '''
        this method clean to screen
        '''
        sys.stderr.write('\x1b[2J\x1b[H')
        Menu().main()

    @staticmethod
    def credits():
        '''
        this method show to the credits
        '''
        print(
            'Lead developer: Carlos Ganoza Plasencia \n [ @drneox | cganozap@gmail.com ]')

    @staticmethod
    def add():
        '''
        this method add to a new client server
        '''
        name = input('Enter your name for host: ')
        hostname = input('Enter your hostname or IP: ')
        email = input('Enter your email: ')
        path = input('path to protect (example: /home/web ) :')
        client = Client(name=name, hostname=hostname, email=email, path=path)
        client.save()

    @staticmethod
    def delete():
        '''
        this method delete to a client server
        '''
        name = input('name of client: ')
        client = Client.objects(name=name)
        client.delete()

    @staticmethod
    def show():
        '''
        this method show to the all clients server
        '''
        clients = Client.objects()
        print(tabulate(clients.all().values_list('name', 'hostname', 'email', 'path', 'status'),
                       ['Name', 'Hostname', 'Email', 'Path', 'Monitoring']))

    @staticmethod
    def log():
        '''
        this method show all logs
        '''
        logs = Log.objects()
        print(tabulate(map(lambda x: [str(x[0].id), Client.objects(id=str(x[0].id), name__ne=None).first(), x[1], x[2], x[3]], logs.all(
        ).no_dereference().values_list('client', 'date', 'item', 'type')), ['Client', 'Date', 'Item']))

    @staticmethod
    def reset():
        '''
        this method allows the structure of a client-server to be updated
        '''
        name = input('name of client: ')
        client = Client.objects(name=name)[0]
        print(client.name)
        client.update(status=False)
        client.reload()
        print(client.status)


if __name__ == '__main__':
    menu = Menu()
    menu.main()
