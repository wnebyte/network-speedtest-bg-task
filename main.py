import speedtest
import schedule
import time
import csv
from pathlib import Path
import argparse
import functools
import socket

def validate_args(args):
    path = Path(args.dir)
    if not path.exists():
        try:
            path.mkdir()
        except:
            print('mkdir from path: ' + path.name + ' was not successful.')
            exit(0)
    if args.interval < 1:
        print('interval >= 1.')
        exit(0)
    if args.src is not None:
        for source in args.src:
            try:
                socket.inet_aton(source)
            except:
                print(source + ' is not a valid src address.')
                exit(0)
    return True


def process_dir_path(path):
    if not str(path).endswith('/') and not str(path).endswith('\\'):
        return str(path) + '/'
    return path


def parse_args():
    parser = argparse.ArgumentParser(description='Run a network speedtest.')
    parser.add_argument('-src', help='set the source IPv4 addresses', type=str, nargs='+')
    parser.add_argument('-interval', help='set the interval', type=int, default=15)
    parser.add_argument('-dir', help='set the output dir', type=str, default='results/')
    parser.add_argument('-exit', help='exit after one task iteration', action='store_true')
    args = parser.parse_args()
    validate_args(args)
    return args


def write_csv(filename, results):
    headers = ['Server ID', 'Server Name', 'Distance', 'Timestamp', 'Ping', 'Download', 'Upload']
    data = [results['server']['id'], results['server']['name'], results['server']['d'], results['timestamp'],
            results['ping'], int(results['download']) / pow(10, 6), int(results['upload']) / pow(10, 6)]

    if (Path(filename).exists()):
        mode = 'a'
    else:
        mode = 'w'

    with open(filename, mode) as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        if mode == 'w':
            csv_writer.writerow(headers)
        csv_writer.writerow(data)


def run_test(source=None, dir='results/'):
    try:
        if (source is not None):
            name = source
            s = speedtest.Speedtest(source_address=source)
        else:
            s = speedtest.Speedtest()
            name = 'default'
    except:
        return
    s.get_best_server()
    s.download()
    s.upload(pre_allocate=False)
    write_csv(dir + name + '.csv', s.results.dict())


def speed_test(args):
    if args.src is None:
        run_test(dir=process_dir_path(args.dir))
    else:
        for source in args.src:
            run_test(source=source, dir=process_dir_path(args.dir))


def main():
    args = parse_args()
    schedule.every(args.interval).minutes.do(functools.partial(speed_test, args))
    schedule.run_all(delay_seconds=0)
    if not args.exit:
        while True:
            schedule.run_pending()
            time.sleep(30)


if __name__ == '__main__':
    main()
