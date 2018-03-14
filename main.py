import importlib
import scrape_airbnb
from argparse import ArgumentParser

def main():
    parser = ArgumentParser()
    parser.add_argument('-c', '--config', type=str, required=True,
                        help='path to config module')

    # Process command line args
    args = parser.parse_args()

    # Load config module
    try:
        config = importlib.import_module(args.config)
    except ModuleNotFoundError as e:
        print(e)
        return

    # Start scraping
    scrape_airbnb.run(config)

if __name__ == '__main__':
    main()

