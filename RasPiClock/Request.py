# -*- encoding: utf-8 -*-

import requests

def req_crypto(conf, pair):
	reponseCrypto = requests.get("https://api.binance.com/api/v3/ticker/24hr?symbol=" + conf["CRYPTO"][pair].upper())
	return reponseCrypto
