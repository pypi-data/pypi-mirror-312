# -*- coding: utf-8 -*-

from __future__ import annotations

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


class Cipher:
    def __init__(self, key: bytes = None, mode: int = AES.MODE_GCM, encoding: str = "UTF-8"):
        if not key:
            key = get_random_bytes(32 if mode == AES.MODE_SIV else 16)

        self.key = key
        self.encoding = encoding
        self.mode = mode

    def encrypt(self, data, *args, **kwargs):
        """ Encrypt the data """

    def decrypt(self, data, *args, **kwargs):
        """ Decrypt the data """
