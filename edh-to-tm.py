# -*- coding: utf-8 -*-

"""
	This script inserts the Trismegistos identifiers (P3) matching items with a CSV file.
	It does not insert the TM id if the claim is already set or EDH differs.
	
	CSV format:
	item_id, edh_id, tm_id
	"Qxxxx","HDxxxxx","123456"
"""

import pywikibot, csv

DATA_FILE = 'EAGLE-data/trismegistos_to_insert.csv'

def main():
	always = dryrun = startsWith = False
	
	# Handles command-line arguments for pywikibot.
	for arg in pywikibot.handleArgs():
		if arg == '-dry': # Performs a dry run (does not edit site)
			dryrun = True
		if arg == '-always': # Does not ask for confirmation
			always = True
		if arg.startswith('-start:'): # Example: -start:Q4700
			startsWith = arg.replace('-start:', '')
	
	# pywikibot/families/eagle_family.py
	site = pywikibot.Site('en', 'eagle').data_repository()
	
	f = open(DATA_FILE, 'r')
	reader = csv.reader(f)
	for row in reader:
		id = row[0]
		
		if startsWith:
			if id != startsWith:
				continue # Skips monuments until start
			elif id == startsWith:
				startsWith = False # Resets
		
		edh = row[1]
		tmid = row[2]
		
		pywikibot.output("\n>>>>> " + id + " <<<<<\n")
		pywikibot.output("EDH: " + edh)
		pywikibot.output("TM id to add: " + tmid)
		
		page = pywikibot.ItemPage(site, id)
		data = page.get()
		
		edhClaim = data['claims']['p24'][0]
		if edhClaim.getTarget() != edh:
			pywikibot.output('WARNING: existing EDH differs: ' + edhClaim.getTarget())
			pywikibot.output('Skipping...')
			continue
		
		if 'p3' in data['claims']:
			tmClaim = data['claims']['p3'][0]
			pywikibot.output('WARNING: existing TM id: ' + tmClaim.getTarget())
			pywikibot.output('Skipping...')
			continue
		
		pywikibot.output('') # newline
		
		if not always:
			choice = pywikibot.inputChoice(u"Proceed?",  ['Yes', 'No', 'All'], ['y', 'N', 'a'], 'N')
		else:
			choice = 'y'
		if choice in ['A', 'a']:
			always = True
			choice = 'y'
		if not dryrun and choice in ['Y', 'y']:	
			addClaimToItem(site, page, 'P3', tmid)
			
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