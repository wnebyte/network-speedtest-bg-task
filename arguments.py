import argparse
import socket
from pathlib import Path

class Arguments:

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-src', help='set the source IPv4 addresses', type=str, nargs='+')
        parser.add_argument('-interval', help='set the interval', type=int, default=15)
        parser.add_argument('-dir', help='set the output dir', type=str, default='results/')
        parser.add_argument('-exit', help='exit after one task iteration', action='store_true')
        self.__args = parser.parse_args()
        self.__args.dir = self.__process_dir()


    def __process_dir(self):
        if not str(self.__args.dir).endswith('/') and not str(self.__args.dir).endswith('\\'):
            return str(self.__args.dir) + '/'
        return self.__args.dir

    def validate(self):
        path = Path(self.__args.dir)

        if not path.exists():
            try:
                path.mkdir()
            except:
                print('mkdir from path: ' + path.name + ' was not successful.')
                exit(0)
        if self.__args.interval < 1:
            print('interval >= 1.')
            exit(0)
        if self.__args.src is not None:
            for source in self.__args.src:
                try:
                    socket.inet_aton(source)
                except:
                    print(source + ' is not a valid src address.')
                    exit(0)
        return self.__args

