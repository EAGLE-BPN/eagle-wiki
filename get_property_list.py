# -*- coding: utf-8 -*-

import pywikibot, operator
from pywikibot import pagegenerators

"""

This script prints out a list of ItemPages.
The title of the link is the content of the property specified via the -property parameter.

Parameters:
	-file:
		Optional argument. File containing the IDs of the elements to list, one per row, without brackets.
		If not specified, the script fetches all items containing the property indicated with -property.
	
	-property:
		Number of the property to get.
		Items not containing the specified property will be ignored.
		
	-sort:
		'titles': sorts by item title
		'props': sort by the property specified via -property (default)
		Optional argument.
	
Example:

python get_property_list.py -file:new_items.txt -property:24 -sort:titles

Content of new_items.txt:
Q4700
Q4701
Q4706

Output:

* [[Item:Q4700|HD016153]]
* [[Item:Q4701|HD065254]]
* [[Item:Q4706|HD065353]]

("HD..." is the property P24 of the items in this case)

"""

SORT_TITLES = 'titles'
SORT_PROP = 'prop'

def main():
	
	# pywikibot/families/eagle_family.py
	site = pywikibot.Site('en', 'eagle')
	repo = site.data_repository()
	
	sort = SORT_PROP
	fileName = None
	# Handles command-line arguments for pywikibot.
	for arg in pywikibot.handleArgs():
		if arg.startswith('-file:'):
			fileName = arg.replace('-file:', '')
		if arg.startswith('-property:'):
			prop = arg.replace('-property:', '')
		if arg.startswith('-sort:'):
			sort = arg.replace('-sort:', '')
	
	propertyId = 'p' + prop # Example: "p11"
	
	ids = [] # Array of item IDs
	if fileName:
		with open(fileName, 'r') as f:
			for id in f:
				id = id.strip() # strip newline
				ids.append(id)
	else:
		propPage = pywikibot.PropertyPage(repo, 'Property:P' + prop)
		refGen = pywikibot.pagegenerators.ReferringPageGenerator(propPage, followRedirects=False,
                           withTemplateInclusion=False,
                           onlyTemplateInclusion=False)
        for i in refGen:
        	if i.namespace() == 120: # quite ugly, to improve
        		ids.append(i.title(withNamespace=False))
			
	idString = '|'.join(ids) # Concatenated IDs for API call
	result = repo.loadcontent({'ids': idString}) # API call
	
	output = [] # List of dictionaries {title, prop}
	
	for id, item in result.items():
		if 'claims' in item.keys():
			if propertyId in item['claims'].keys():
				for claimDict in item['claims'][propertyId]:
					claim = pywikibot.Claim.fromJSON(repo, claimDict)
					output.append( { 'title': item['title'], 'prop': claim.getTarget() } )
	
	if sort == SORT_TITLES:
		output = sorted(output, key=operator.itemgetter('title'))
	elif sort == SORT_PROP:
		output = sorted(output, key=operator.itemgetter('prop'))
	
	for i in output:
		print '* [[' + i['title'] + '|' + i['prop'] + ']]'

if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()