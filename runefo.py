import re
import sys
import json
import time
from const import *
from questScrape import *
from hiscores import Hiscores


class Player:
	def __init__(self, name):
		self.name = str(name)
		self.rawLevels = Hiscores(name)

		skillLevels = {}
		for skill in SKILLS:
			skillLevels[skill] = self.rawLevels.skills[skill].level

		self.levels = skillLevels


	def getLevels(self, key):
		return self.levels[key]

if __name__ == '__main__':
	playerInput = input("Enter player name and press enter: ").strip().replace(" ", "%20")
	while playerInput != "":
		try:
			print("Retrieving player info...")
			Hiscores(playerInput)
		except:
			print("Player not found")
			sys.exit()

		playerList = []
		playerList.append(Player(playerInput))
		print("\nDone!")
		time.sleep(1)

		playerInput = input("Enter another player name (or just enter to continue): ").strip().replace(" ", "%20")

	scrape()
	recurseReqs()

	questLevels = {}
	with open('quests.json') as json_file:
		questLibrary = json.load(json_file)
		for quest in questLibrary:
			questReqsList = re.findall('([0-9][0-9]\s\s('+'|'.join(map(str, SKILLS))+'))',quest['requirements'], re.IGNORECASE)
			reqsDict = {}
			for req in questReqsList:
				reqsDict[req[0].split()[1].lower()] = int(req[0].split()[0])
			questLevels[quest['name']] = reqsDict

	try:
		eligibleQuests = []
		for key, value in questLevels.items():
			eligibleQuests.append(key)
			for k, v in questLevels[key].items():
				for p in playerList:
					if questLevels[key][k] > p.getLevels(k):
						eligibleQuests.pop()
						break
	except:
		time.sleep(3)
		print("Player too n00by")
		time.sleep(1)
		sys.exit()


	print("Your player(s) meet the level requirements for the following quests: ")
	time.sleep(1)
	for quest in eligibleQuests:
		print("-->  " + quest)
		time.sleep(0.05)

