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
	
	# Handles command-line arguments for pywikibot.
	for arg in pywikibot.handleArgs():
		if arg.startswith('-list-set:'):
			selectedSet = arg.replace('-list-set:', '')
	
	if selectedSet == None:
		pywikibot.output('Argument -list-set is mandatory!')
		return
		
	bot = ListBot(always=False, selectedSet=selectedSet)
	bot.run()

class ListBot(pywikibot.bot.Bot):
	
	list_set = {
		'translations': {
			'lists': {
				11: 'Translation EN',
				12: 'Translation DE',
				13: 'Translation IT',
				14: 'Translation ES',
				15: 'Translation FR',
				19: 'Translation HU',
			},
			'category': 'Lists by translation language',	
		},
		
		'identifiers': {
			'lists': {
				22: 'Translations of the Inscriptions of Hispania Epigrafica',
				24: 'EDH List',
				3: 'TM List',
				33: 'Petrae',
				34: 'UEL List',
				37: 'EDB List',
				38: 'EDR List',
				47: 'Last Statues of Antiquity',
				48: 'ELTE',
				50: 'Inscriptions of Aphrodisias',
				51: 'Attic Inscriptions Online',
				59: 'UBB',
				63: 'Roman Inscriptions of Britain',
			},
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
		
		for property, page_title in self.list_set[selectedSet]['lists'].items():
			self.current_page = pywikibot.Page(repo, page_title)
			
			oldtext = self.current_page.get()
			
			itemList = get_property_list.getItemsForProperty(repo, property, show='label', sort=None, labelLang='en', fileName=None)
			
			newtext = '<div style="column-count: 5; -webkit-column-count: 5; -moz-column-count: 5;">'
			for i in itemList:
				newtext += "\n" + '* [[' + i['title'] + '|' + i['label'] + ']]'
			newtext += "\n</div>\n\n[[Category:" +	self.list_set[selectedSet]['category'] + "]]\n"
			
			self.userPut(self.current_page, oldtext, newtext, comment='Updating list')

if __name__ == "__main__":
	try:
		main()
	finally:
		pywikibot.stopme()