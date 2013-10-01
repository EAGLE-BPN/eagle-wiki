# -*- coding: utf-8 -*-

import pywikibot, os
import xml.etree.ElementTree as ET

DATA_DIR = '/Users/pietro/Dropbox/Dati/Hispania epigrafica/'

def main():
	args = pywikibot.handleArgs()
	
	# pywikibot/families/eagle_family.py
	site = pywikibot.Site('en', 'eagle').data_repository()
	all = False
	
	for fileName in os.listdir(DATA_DIR):
		tree = ET.parse(DATA_DIR + fileName)
		root = tree.getroot()
		title = root.findall('./title')[0].text
	
		# ID
		pywikibot.output(">>>>> " + title + " <<<<<")
		
		if not all:
			choice = pywikibot.inputChoice(u"Proceed?",  ['Yes', 'No', 'All'], ['y', 'N', 'a'], 'N')
		else:
			choice = 'y'
		if choice in ['A', 'a']:
			all = True
			choice = 'y'
		if choice in ['Y', 'y']:
			page = pywikibot.ItemPage.createNew(site, labels={'es': title}) # New item
			
			# HispaniaEpigrafica ID
			addClaimToItem(site, page, 'P22', fileName[0:-4]) # Remove extension
			
			# IPR
			ipr = root.findall('./ipr')[0].text[1:-1] # Strip quotes
			addClaimToItem(site, page, 'P25', ipr)
			
			# ES Translation
			transClaim = pywikibot.Claim(site, 'P14')
			transClaim.setTarget(root.findall('./text')[0].text)
			page.addClaim(transClaim)
			
			# Author
			authorClaim = pywikibot.Claim(site, 'P21')
			authorClaim.setTarget(root.findall('./translator')[0].text)
			transClaim.addSource(authorClaim)

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