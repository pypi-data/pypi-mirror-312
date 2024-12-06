#! /usr/bin/env python

import json

from bcapi.client import Client
import sys

def main(verification_code=None):
    with Client(verification_code=verification_code):
        print("done")


if __name__ == "__main__":
    verification_code = sys.argv[1] if len(sys.argv) > 1 else None
    main(verification_code)
