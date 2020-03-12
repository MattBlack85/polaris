import argparse

from polaris.client import Polaris


def run(args):
    if 'get_latest' in args:
        p = Polaris()
        p.get_latest_csv_data()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Get coronavirus data from WHO PDFs and store them into a CSV')
    parser.add_argument('--get-latest',
                        help='Get latest data (yesterday\'s data)')
    args = parser.parse_args()
    run(args)
