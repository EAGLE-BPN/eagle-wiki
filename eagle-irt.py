# -*- coding: utf-8 -*-

import pywikibot, csv

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
			
			# BSR ID
			addClaimToItem(site, page, 'P40', row[0])
			
			# IPR
			addClaimToItem(site, page, 'P25', row[2])
			
			# EN Translation
			transClaim = pywikibot.Claim(site, 'P11')
			transClaim.setTarget(row[4])
			page.addClaim(transClaim)
			
			periodicalClaim = pywikibot.Claim(site, 'P32')
			periodicalClaim.setTarget(row[3])
			
			authorClaim = pywikibot.Claim(site, 'P21')
			authorClaim.setTarget(row[1])
			
			transClaim.addSources([authorClaim, periodicalClaim])
			
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