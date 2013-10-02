# -*- coding: utf-8 -*-

import pywikibot, os, re
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
		
		# ID
		title = elementText(root.findall('./title')[0])
		pywikibot.output("\n>>>>> " + title + " <<<<<\n")
		
		# HispaniaEpigrafica ID
		hispId = fileName[0:-4] # Remove extension (.xml)
		pywikibot.output('HispaniaEpigrafica ID: ' + hispId)
		
		# IPR
		ipr = elementText(root.findall('./ipr')[0])[1:-1] # Strip quotes
		pywikibot.output('IPR: ' + ipr)
		
		# ES Translation
		esTranslation = elementText(root.findall('./text')[0])
		pywikibot.output('ES Translation: ' + esTranslation)
		
		# Author
		author = elementText(root.findall('./translator')[0])
		pywikibot.output('Author: ' + author)
		
		pywikibot.output('') # Newline
		
		if not all:
			choice = pywikibot.inputChoice(u"Proceed?",  ['Yes', 'No', 'All'], ['y', 'N', 'a'], 'N')
		else:
			choice = 'y'
		if choice in ['A', 'a']:
			all = True
			choice = 'y'
		if choice in ['Y', 'y']:
			page = pywikibot.ItemPage.createNew(site, labels={'es': title}) # New item
			
			addClaimToItem(site, page, 'P22', hispId)
			addClaimToItem(site, page, 'P25', ipr)
			
			transClaim = pywikibot.Claim(site, 'P14')
			transClaim.setTarget(esTranslation)
			page.addClaim(transClaim)
			
			authorClaim = pywikibot.Claim(site, 'P21')
			authorClaim.setTarget(author)
			transClaim.addSource(authorClaim)

# Adds a claim to an ItemPage.		
def addClaimToItem(site, page, id, value):
	claim = pywikibot.Claim(site, id)
	claim.setTarget(value)
	page.addClaim(claim)
	
# Get inner element text, stripping tags of sub-elements.
def elementText(elem):
	text = ''.join(elem.itertext()).strip()
	text = re.sub('\n', ' ', text)
	text = re.sub('\s{2,}', ' ', text)
	return text

if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()