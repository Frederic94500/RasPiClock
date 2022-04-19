# -*- encoding: utf-8 -*-

import time

import requests

from APIObject import APIObject


class Crypto(APIObject):
    def __init__(self, url, key, config):
        super().__init__(self, url, key, config)

    def call(self):
        response = []
        for i in range(2):
            response.append(requests.get(
                "https://api.binance.com/api/v3/ticker/24hr?symbol=" + self.config[i].upper()))
        return response

    def test(self):
        response = self.call()
        for i in response:
            if i.status_code != 200:
                print("Erreur dans la config Crypto, veuillez vérifier votre saisie!")
                return False
        return True

    def print(self, papirus):
        response = self.call()
        papirus.AddText("Crypto:", 10, 10, size=20, fontPath="Ubuntu.ttf", Id="title")

        x = 10
        y = 45
        j = 0

        for i in response:
            jsoned = i.json()
            papirus.AddText(jsoned["symbol"] + ": " + f'{float(jsoned["lastPrice"]):.2f}', x, y, size=25, fontPath="Ubuntu.ttf", Id="pair" + str(j))
            papirus.AddText(jsoned["priceChangePercent"] + "%", x, y + 25 + 5, size=15, fontPath="Ubuntu.ttf", Id="pairpct" + str(j))
            y = y + 25 + 5 + 15 + 25
            j += 1

        papirus.AddText(time.strftime("%H:%M:%S", time.localtime()), 180, 10, size=20, fontPath="Ubuntu.ttf", Id="time")

        papirus.WriteAll(True)

    def print_update(self, papirus):
        response = self.call()
        j = 0
        for i in response:
            jsoned = i.json()
            papirus.UpdateText("pair" + str(j), jsoned["symbol"] + ": " + f'{float(jsoned["lastPrice"]):.2f}', fontPath="Ubuntu.ttf")
            papirus.UpdateText("pairpct" + str(j), jsoned["priceChangePercent"] + "%", fontPath="Ubuntu.ttf")
            j += 1

        papirus.UpdateText("time", time.strftime("%H:%M:%S", time.localtime()), fontPath="Ubuntu.ttf")

        papirus.WriteAll(True)
