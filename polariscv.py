import argparse

from polaris.client import Polaris


def run(args):
    p = Polaris()
    p.get_data(args.date, args.pages)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Get coronavirus data from WHO PDFs and store them into a CSV')
    parser.add_argument('date',
                        metavar='D',
                        help='Get a CSV containing tabular data from WHO PDF (format yyyy-mm-dd)')
    parser.add_argument('--pages',
                        metavar='P',
                        type=int,
                        nargs='+',
                        default=[2, 3, 4, 5, 6, 7, 8],
                        help='Get a CSV containing tabular data from WHO PDF (format yyyy-mm-dd)')
    args = parser.parse_args()
    run(args)
