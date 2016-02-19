#!/usr/bin/env python

from common import *
import sys

def parse_arguments():
    arg_dict = {}

    if len(sys.argv) > 1:
        try:
            arguments_dict[_DATABASE_KEY_] = sys.argv[sys.argv.index(_DATABASE_ARGUMENT_)+1]
        except ValueError:
            return arg_dict
        return arg_dict
