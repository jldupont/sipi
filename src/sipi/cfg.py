"""
    Simple Configuration Information API

    Configuration files are kept in *~/.config/* 

    Configuration parameters are treated as "read-only".

    @created: on 2012-01-12
    @author: jldupont
"""
import sys


def get(param, default=None):
    """
    Get a configuration parameter
    """
    