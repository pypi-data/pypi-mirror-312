#!/usr/bin/env python3

"""
Usage:
   cmd <config_path>
   cmd --help
Arguments:
   config_path        path to config


Other options:
    -h, --help      Show this help message and exit.
"""

import yadopt

args = yadopt.parse(__doc__)
print(args)

# vim: expandtab tabstop=4 shiftwidth=4 fdm=marker
