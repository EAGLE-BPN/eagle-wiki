# -*- coding: utf-8 -*-

import pywikibot, operator
from pywikibot import pagegenerators

"""

Usage:
	python not_in_lists.py -listcat:<Category>
	
This script prints out a list of items (as links) which aren't present in any of the lists taken from a category.
The title of the category containing the lists to check is indicated by the -listcat parameter.

Examples:
	python not_in_lists.py -listcat:"Lists by translation language"
	python not_in_lists.py -listcat:"Lists by collection"

"""

ITEM_NAMESPACE = 120

def main():
	
	# Handles command-line arguments for pywikibot.
	categoryName = None
	for arg in pywikibot.handleArgs():
		if arg.startswith('-listcat:'): # Category containing lists
			categoryName = arg.replace('-listcat:', '')
	
	if categoryName == None:
		pywikibot.output("\nUsage:\n\tpython not_in_lists.py -listcat:\"Category_name\"\n")
		return
	
	# pywikibot/families/eagle_family.py
	site = pywikibot.Site('en', 'eagle')
	repo = site.data_repository()
	
	translatedItems = []
	listCat = pywikibot.Category(repo, 'Category:' + categoryName)
	pywikibot.output('Fetching lists from ' + listCat.title(asLink=True) + ' ...')
	for tList in listCat.articles():
		pywikibot.output(tList.title(asLink=True))
		for p in tList.linkedPages(namespaces=ITEM_NAMESPACE):
			translatedItems.append(p.title(withNamespace=False))
	
	pywikibot.output("\nList of items not in lists:\n")
	for p in repo.allpages(namespace=ITEM_NAMESPACE):
		if p.title(withNamespace=False) not in translatedItems:
			pywikibot.output('* [[' + p.title() + ']]', toStdout=True)
	
if __name__ == "__main__":
	try:
		main()
	finally:
		pywikibot.stopme()