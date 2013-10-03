# -*- coding: utf-8 -*-

import pywikibot, os, re, csv

DATA_FILE = '/Users/pietro/Dropbox/Dati/petrae_translation.csv'

def main():
	args = pywikibot.handleArgs()
	
	# pywikibot/families/eagle_family.py
	site = pywikibot.Site('en', 'eagle').data_repository()
	all = False
	
	f = open(DATA_FILE, 'r')
	reader = csv.reader(f, delimiter="\t")
	for row in reader:
		id = row[0]
		translationFr = row[1]
		image = row[2]
		
		pywikibot.output("\n>>>>> " + id + " <<<<<\n")
		if translationFr:
			pywikibot.output('Translation FR: ' + translationFr)
		else:
			pywikibot.output('WARNING: no translation!')
		pywikibot.output('Image: ' + image)
		
		pywikibot.output('') # Newline
		
		if not all:
			choice = pywikibot.inputChoice(u"Proceed?",  ['Yes', 'No', 'All'], ['y', 'N', 'a'], 'N')
		else:
			choice = 'y'
		if choice in ['A', 'a']:
			all = True
			choice = 'y'
		if choice in ['Y', 'y']:
			# New item
			page = pywikibot.ItemPage.createNew(site, labels={'fr': id})
			
			addClaimToItem(site, page, 'P33', id) # Petrae ID
			if translationFr:
				addClaimToItem(site, page, 'P15', translationFr)
			# addClaimToItem(site, page, 'P10', image)
			
	f.close()

# Adds a claim to an ItemPage.		
def addClaimToItem(site, page, id, value):
	claim = pywikibot.Claim(site, id)
	claim.setTarget(value)
	page.addClaim(claim)

if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()