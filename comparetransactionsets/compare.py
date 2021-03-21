from pprint import pformat
import comparetransactionsets.config


def exec(args):
    config = comparetransactionsets.config.read()
    print(f"Config:\n{pformat(config)}")
    for i in config['transaction-defs']:
        print(i)
