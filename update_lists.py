# -*- coding: utf-8 -*-

import pywikibot
import get_property_list

"""

Automatically updates item lists.

Usage:
	python update_lists.py -list-set:translations
	python update_lists.py -list-set:identifiers

"""

def main():
	
	selectedSet = None
	always = False
	
	# Handles command-line arguments for pywikibot.
	for arg in pywikibot.handleArgs():
		if arg.startswith('-list-set:'):
			selectedSet = arg.replace('-list-set:', '')
		if arg.startswith('-always'):
			always=True
	
	if selectedSet == None:
		pywikibot.output('Argument -list-set is mandatory!')
		return
		
	bot = ListBot(always=always, selectedSet=selectedSet)
	bot.run()

class ListBot(pywikibot.bot.Bot):
	
	list_set = {
		'translations': {
			'lists': [
				{'page': 'Translation EN', 'property': 11, 'show': 'label'},
				{'page': 'Translation DE', 'property': 12, 'show': 'label'},
				{'page': 'Translation IT', 'property': 13, 'show': 'label'},
				{'page': 'Translation ES', 'property': 14, 'show': 'label'},
				{'page': 'Translation FR', 'property': 15, 'show': 'label'},
				{'page': 'Translation HU', 'property': 19, 'show': 'label'},
			],
			'category': 'Lists by translation language',	
		},
		
		'identifiers': {
			'lists': [
				{'page': 'Translations of the Inscriptions of Hispania Epigrafica', 'property': 22, 'show': 'label'},
				{'page': 'EDH List', 'property': 24, 'show': 'property'},
				{'page': 'TM List', 'property': 3, 'show': 'property'},
				{'page': 'Petrae', 'property': 33, 'show': 'label'},
				{'page': 'UEL List', 'property': 34, 'show': 'label'},
				{'page': 'EDB List', 'property': 37, 'show': 'label'},
				{'page': 'EDR List', 'property': 38, 'show': 'label'},
				{'page': 'Last Statues of Antiquity', 'property': 47, 'show': 'label'},
				{'page': 'ELTE', 'property': 48, 'show': 'label'},
				{'page': 'Inscriptions of Aphrodisias', 'property': 50, 'show': 'label'},
				{'page': 'Attic Inscriptions Online', 'property': 51, 'show': 'label'},
				{'page': 'UBB', 'property': 59, 'show': 'label'},
				{'page': 'Roman Inscriptions of Britain', 'property': 63, 'show': 'label'},
				{'page': 'Translations of the Inscriptions of Roman Tripolitania', 'property': 40, 'show': 'label'},
			],
			'category': 'Lists by collection',	
		},
	}

	availableOptions = {
		'always': False,  # ask for confirmation when putting a page?
		'selectedSet': None,
	}
	
	def run(self):
		
		# pywikibot/families/eagle_family.py
		site = pywikibot.Site('en', 'eagle')
		repo = site.data_repository()
		
		selectedSet = self.getOption('selectedSet')
		
		for i in self.list_set[selectedSet]['lists']:
			self.current_page = pywikibot.Page(repo, i['page'])
			
			oldtext = self.current_page.get()
			
			itemList = get_property_list.getItemsForProperty(repo, i['property'], show=i['show'], sort=None, labelLang='en')
			
			newtext = '<div style="column-count: 5; -webkit-column-count: 5; -moz-column-count: 5;">'
			for j in itemList:
				linkTitle = j[i['show']]
				newtext += "\n" + '* [[' + j['title'] + '|' + linkTitle + ']]'
			newtext += "\n</div>\n\n[[Category:" +	self.list_set[selectedSet]['category'] + "]]"
			
			self.userPut(self.current_page, oldtext, newtext, comment='Updating list')

if __name__ == "__main__":
	try:
		main()
	finally:
		pywikibot.stopme()