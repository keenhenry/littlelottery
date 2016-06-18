#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import string
import random
import hashlib

class LittleLottery(object):
    "This is a class which implements drawing lottery"

    def __init__(self, size=100):
        self.__size__ = size

    def draw(self):
        """Draw a winner

        Algorithm:

        1. Get a sha1 hash of a string which is a concatenation of current time stamp and a salt
        2. Convert the hash to an integer number and get a modulus of that number.
           The divisor of the modulo operation is self.__size__.

        Return (list): a database primary key id of a participant.
        """

        now = time.strftime('%c')
        salt = ''.join(random.SystemRandom().choice(string.ascii_letters) \
                       for _ in xrange(5))

        h = hashlib.sha1(now + salt).hexdigest()

        return int(h, 16) % self.__size__
