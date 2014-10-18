# -*- coding: utf-8 -*-

import pywikibot, csv
import get_property_list

"""

Arguments:
	-identifier:<N>
		Number of the property needed to identify the items
	-insert:<N>
		Number of the property to add
	-file:<source.csv>
		CSV file which has two columns:
		1. the value of the property indicated in the argument -identifier;
		2. the valute of the property -insert, to add to the items.
		
		Format:
		X;Y

"""

def main():
	
	selectedSet = None
	always = False
	idProp = insertProp = filename = False
	
	# Handles command-line arguments for pywikibot.
	for arg in pywikibot.handleArgs():
		if arg.startswith('-identifier:'):
			idProp = arg.replace('-identifier:', '')
		if arg.startswith('-insert:'):
			insertProp = arg.replace('-insert:', '')
		if arg.startswith('-file:'):
			filename = arg.replace('-file:', '')
		if arg.startswith('-always'):
			always=True
	
	if idProp == None or insertProp == None or filename == None:
		pywikibot.output('All arguments are required!')
		return
	
	matchDict = {}
	with open(filename, 'r') as f:
		reader = csv.reader(f, delimiter=";")
		for row in reader:
			matchDict[row[0]] = row[1]
		
	bot = PropertyBot(always=always, idProp=idProp, insertProp=insertProp, matchDict=matchDict)
	bot.run()

class PropertyBot(pywikibot.bot.Bot):

	availableOptions = {
		'always': False,  # ask for confirmation when putting a page?
		'idProp': None,
		'insertProp': None,
		'matchDict': None,
	}
	
	def run(self):
		
		# pywikibot/families/eagle_family.py
		site = pywikibot.Site('en', 'eagle')
		repo = site.data_repository()
		
		idProp = self.getOption('idProp')
		insertProp = self.getOption('insertProp')
		matchDict = self.getOption('matchDict')
		
		itemList = get_property_list.getItemsForProperty(repo, idProp, additionalProperties=[insertProp])
		
		for i in itemList:
			if i['property'] not in matchDict:
				continue
			
			self.current_page = pywikibot.ItemPage(repo, i['title'])
			
			pywikibot.output('Item matched by P' + idProp + ': ' + i['property'])
			
			toInsert = matchDict[i['property']]
			pywikibot.output('Attempting to insert P' + insertProp + ': ' + toInsert)
			
			if insertProp in i['additionalProperties']:
				if i['additionalProperties'][insertProp] == toInsert:
					pywikibot.output('The item already has the property '
						+ insertProp + ' with an identical content. Skipping')
				else:
					pywikibot.output('The item already has the property '
					+ insertProp + ' with a different content: ' + i['additionalProperties'][insertProp] +
						'. Skipping')
				continue
			
			newClaim = pywikibot.Claim(repo, 'P' + insertProp)
			newClaim.setTarget(toInsert)
			if self.user_confirm('Do you really want do add the claim for property P' + insertProp + '?'):
				self.current_page.addClaim(newClaim)
			

if __name__ == "__main__":
	try:
		main()
	finally:
		pywikibot.stopme()