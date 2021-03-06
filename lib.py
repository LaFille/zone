#!/usr/bin/env python

import json
import random

# prend le nom d'un fichier et renvoie le dictionnaire correspondant
def file_to_dict(filename):
	with open(filename) as content:
		return unicode_to_ascii(json.loads(content.read()))

# convert the argument to asccii
def unicode_to_ascii(input):
	if isinstance(input, dict):
		return {unicode_to_ascii(key):unicode_to_ascii(value) for key,value in input.iteritems()}
	elif isinstance(input, list):
		return [unicode_to_ascii(element) for element in input]
	elif isinstance(input, unicode):
		return unicode_to_ascii(input.encode('utf-8'))
	elif isinstance(input, str) and input.isdigit():
		return int(input)
	else:
		return input

# renvoie toute les configurations
def configuration(datas,min,aleaf):
	all = []
	inv = inverse(datas)
	if aleaf:
		alea(inv,min,all,datas)
	else:
		vers(inv,datas,[],1,all,min)
	return all

# methode aleatoire pour obtenir des configuration elementaire
def alea(inv,nb,all,original):
	for _ in range(nb):
		config = []
		for zone,localcapteur in inv.iteritems():
			toadd = True
			for capteur in localcapteur:
				if capteur in config:
					toadd = False
					break
			if toadd:
				config.append(localcapteur[random.randint(0,len(localcapteur)-1)])
		ok = True
		config = elementarise(config,original)
		for x in all:
			if config_equal(config,x):
				ok = False
		if ok:
			all.append(config)
				

# parcour des donnes et place toute les confgurations dans data
def vers(tree,original,config,level,all,min):
	if (len(all)>=min and min!=0) or not elementaire(config,original):
		return
	if len(tree)<level:
		for x in all:
			if config_equal(config,x):
				return
		all.append(config)
		return
	for x in tree[level]:
		inter = config
		if x not in config:
			inter = list(config)
			inter.append(x)
		vers(tree, original, inter, level+1, all, min)

# renvoi vrai si ajouter x ferait que config reste elementare
def elementaire(config,original):
	all = []
	for capteur in config:
		all.extend(original[capteur]["zone"])
	for capteur in config:
		ok = False
		for zone in original[capteur]["zone"]:
			if all.count(zone)==1:
				ok = True
				break
		if not ok:
			return False
	return True

# rend la configuration elementarie
def elementarise(config,original):
	config = list(config)
	idx = 0
	while idx<len(config):
		current = list(original[config[idx]]["zone"])
		for capteur in config:
			if capteur==config[idx] :
				continue
			i = 0;
			while i < len(current):
				if current[i] in original[capteur]["zone"]:
					current.pop(i)
				else:
					i += 1
		if len(current)==0:
			config.pop(idx)
		else:
			idx += 1	
	return config

# renvoie vrai si les deux configuration sont eguale
def config_equal(config1,config2):
	if len(config1)!=len(config2):
		return False
	for x in config1:
		if x not in config2:
			return False
	return True

# renvoi le dictionnaire inverse: capteur en fonction des zonne: {zone:[capteur,capteur,etc],etc}
def inverse(datas):
	inverse = {}
	for capteur,all in datas.iteritems():
		for x in all["zone"]:
			if x in inverse:
				inverse[x].append(capteur)
			else:
				inverse[x] = [capteur]
	return inverse

# renvoie une inconnu correspondant a l'index
def inconu(index):
	if index>(ord("z")-ord("a")):
		return ("z" + str(index-ord("z")+ord("a")))
	return chr(ord("a")+index)
