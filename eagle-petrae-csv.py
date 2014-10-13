# -*- coding: utf-8 -*-

"""

Accepted options:

	-dry
		Dry run: don't edit the wiki, but process and print all the data.
		It's useful together with -always to check for crashes in the script before launching the bot.
		
	-always
		Don't ask for confirmation before submitting a new item to the wiki.

"""

import pywikibot, csv

DATA_FILE = '/Users/pietro/EAGLE-data/petrae_translation.csv'

def main():
	always = dryrun = False
	
	# Handles command-line arguments for pywikibot.
	for arg in pywikibot.handleArgs():
		if arg == '-dry': # Performs a dry run (does not edit site)
			dryrun = True
		if arg == '-always': # Does not ask for confirmation
			always = True
	
	# pywikibot/families/eagle_family.py
	site = pywikibot.Site('en', 'eagle').data_repository()
	
	f = open(DATA_FILE, 'r')
	reader = csv.reader(f, delimiter="\t")
	for row in reader:
		id = row[0]
		pywikibot.output("\n>>>>> " + id + " <<<<<\n")
		
		try:
			translationFr = row[1]
			image = row[2]
		except IndexError:
			pywikibot.output('ERROR: Data not found for id ' + id + '. Ignoring.')
		
		if translationFr:
			pywikibot.output('Translation FR: ' + translationFr)
		else:
			pywikibot.output('WARNING: no translation!')
		
		if image:
			pywikibot.output('Image: ' + image)
		else:
			pywikibot.output('WARNING: no image!')
		
		pywikibot.output('') # newline
		
		if not always:
			choice = pywikibot.inputChoice(u"Proceed?",  ['Yes', 'No', 'All'], ['y', 'N', 'a'], 'N')
		else:
			choice = 'y'
		if choice in ['A', 'a']:
			always = True
			choice = 'y'
		if not dryrun and choice in ['Y', 'y']:
			page = pywikibot.ItemPage(site)
			page.editEntity({'labels':{'fr': id}})
			page.get()
			
			addClaimToItem(site, page, 'P33', id) # Petrae ID
			if translationFr:
				addClaimToItem(site, page, 'P15', translationFr)
			
			# P10 wants Wikimedia Commons image link!
			# addClaimToItem(site, page, 'P10', image)
			
	f.close()
	
def addClaimToItem(site, page, id, value):
	"""Adds a claim to an ItemPage."""
	claim = pywikibot.Claim(site, id)
	claim.setTarget(value)
	page.addClaim(claim)

if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()