# -*- encoding: utf-8 -*-

class APIObject:
    url = ""
    key = ""
    config = []

    def __init__(self, url, key, config):
        self.url = url
        self.key = key
        self.config = config

    def call(self):
        pass

    def test(self):
        pass

    def print(self, papirus):
        pass

    def print_update(self, papirus):
        pass
