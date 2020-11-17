import csv
from pathlib import Path

"""Class for writing results of speedtest to csv file"""

class Writer:

    def __init__(self, path, results, delimiter=';', lineterminator='\n'):
        self.path = path
        self.headers = ['Server ID',
                        'Server Name',
                        'Distance',
                        'Timestamp',
                        'Ping',
                        'Download',
                        'Upload']

        self.data = [results['server']['id'],
                     results['server']['name'],
                     results['server']['d'],
                     results['timestamp'],
                     results['ping'],
                     int(results['download']) / pow(10, 6),
                     int(results['upload']) / pow(10, 6)]

        self.delimiter = delimiter
        self.lineterminator = lineterminator

        if Path(self.path).exists():
            self.mode = 'a'
        else:
            self.mode = 'w'

    def log(self):
        with open(self.path, self.mode) as csv_file:
            csv_writer = \
                csv.writer(csv_file, delimiter=self.delimiter, lineterminator=self.lineterminator,
                           quotechar='|', quoting=csv.QUOTE_MINIMAL)
            if self.mode == 'w':
                csv_writer.writerow(self.headers)
            csv_writer.writerow(self.data)


