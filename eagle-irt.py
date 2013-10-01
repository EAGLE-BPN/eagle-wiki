# -*- coding: utf-8 -*-

import pywikibot, csv

# Maps the CSV fields to Wikibase properties.
csvMap = {
		0: 'P40', # BSR ID
		1: 'P21', # Author
		2: 'P25', # IPR
		3: 'P32', # Periodical title
		4: 'P11', # EN translation
	}

def main():
	args = pywikibot.handleArgs()
	
	# pywikibot/families/eagle_family.py
	site = pywikibot.Site('en', 'eagle').data_repository()
	
	f = open('EAGLE-IRT.CSV', 'r')
	r = csv.reader(f, delimiter='	')
	next(r) # skips first item
	
	all = False
	
	for row in r:
		# ID
		pywikibot.output(">>>>> " + row[0] + " <<<<<")
		
		if not all:
			choice = pywikibot.inputChoice(u"Proceed?",  ['Yes', 'No', 'All'], ['y', 'N', 'a'], 'N')
		else:
			choice = 'y'
		if choice in ['A', 'a']:
			all = True
			choice = 'y'
		if choice in ['Y', 'y']:
			page = pywikibot.ItemPage.createNew(site, labels={"en": row[0]}) # New item
			for i in csvMap.keys():
				# These are separate edits/requests
				addClaimToItem(site, page, csvMap[i], row[i])
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