import argparse

from delete import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()

    delete_tail("whslabs-cardano-node-*", args.dry_run)
