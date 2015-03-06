#!/usr/bin/env python


class ParsingError(Exception):
    """
    General parsing error
    """


class OutOfBoundsError(Exception):
    """
    Out of bounds error arises when something unexpected happens with
    the input file or input data length
    """