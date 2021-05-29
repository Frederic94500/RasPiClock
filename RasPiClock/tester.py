# -*- encoding: utf-8 -*-

import configparser, socket, sys
import Request as RQ

def main():
	try:
		conf = configparser.ConfigParser()
		conf.read("config.cfg")
		crypto(conf)
	except (ValueError, socket.error, socket.gaierror, socket.herror, socket.timeout): #Situation d'erreur de connexion
		print("Erreur de connexion.")
	finally:
		sys.exit()

def crypto(conf):
	print("Crypto:")
	for i in range(2):
		reponseCrypto = RQ.req_crypto(conf, "pair" + str(i + 1))

		if(reponseCrypto.status_code == 200):
			print(reponseCrypto.json()["symbol"] + ": " + f'{float(reponseCrypto.json()["lastPrice"]):.2f}')
			print(reponseCrypto.json()["priceChangePercent"] + "%")
		else:
			print("Erreur sur la paire " + str(i+1))

main()