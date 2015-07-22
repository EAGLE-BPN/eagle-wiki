# -*- coding: utf-8 -*-

"""

Accepted options:

	-dry
		Dry run: don't edit the wiki, but process and print all the data.
		It's useful together with -always to check for crashes in the script before launching the bot.
		
	-always
		Don't ask for confirmation before submitting a new item to the wiki.
		
	-start:<filename>
		Start from file "<filename>.xml". Useful for resuming an interrupted import.

"""

import requests
import xml.etree.ElementTree as ET
import pywikibot, os, webbrowser, re
from bs4 import BeautifulSoup

inwiki = ["Rationes Stele 2", "AIO Papers 4, 1138 (genre)", "AIO Papers 4, 1139 (l. 46)", "AIO Papers 4, 1140 (ll. 23, 29)", "AIO Papers 4, 1153 (l. 55)", "AIO Papers 5, pp. 1-11", "AIO Papers 5, pp. 9-11", "Agora XV 49", "Agora XVI 106F", "Agora XVI 106H", "Agora XVI 127", "Agora XVI 132", "Agora XVI 133", "Agora XVI 135", "Agora XVI 145", "Agora XVI 152", "Agora XVI 45", "Agora XVI 58", "Agora XVI 61", "Agora XVI 65", "Agora XVI 66", "Agora XVI 67", "Agora XVI 69", "Agora XVI 70", "Agora XVI 81", "Agora XVI 82", "Agora XVI 83", "Agora XVI 88", "Agora XVI 89", "Agora XVI 90", "Agora XVI 98", "Blok, Athena Nike 2", "IALD 115 no. 20", "IALD 131, 172 no. 134a, 395.", "IALD 139 no. 63", "IALD 148 no. 98, 315-19 no. 4, 339-43, 356 no. 6", "IALD 171 no. 125", "IALD 171 no. 127, 404", "IALD 171 no. 128", "IALD 171 no. 129", "IALD 171 no. 130", "IALD 174 no. 143", "IALD 174 no. 144", "IALD 178 no. 160", "IALD 178 no. 161", "IALD 178 no. 162", "IALD 187 no. 11", "IALD 192 no. 26", "IALD 196 no. 52", "IALD 197 no. 58", "IALD 197 no. 59", "IALD 38 no. 12", "IALD 405", "IALD 405", "IALD 405", "IALD 405", "IALD 405", "IALD 405", "IALD 406", "IALD 406", "IALD 406", "IALD 406", "IALD 406", "IALD 406", "IALD 406", "IALD 406", "IALD 406", "IALD 406", "IALD 5 n. 8, 10 no. 4, 22-26, 54, 322 n. 3, 327 n. 15, 332, 334", "IALD 56 no. 2, 57, 81 no. 8, 85-88, 173 n. 114, 380-81", "IALD 56 no. 3, 57, 81 no. 9, 88-89", "IG II 221", "IG II2 1", "IG II2 113", "IG II2 1156", "IG II2 125", "IG II2 149", "IG II2 1596 (= Rationes, Fragment 13)", "IG II2 1597", "IG II2 1603 (= Rationes, Fragment 2)", "IG II2 1629", "IG II2 171", "IG II2 184", "IG II2 204", "IG II2 205", "IG II2 206", "IG II2 207", "IG II2 208", "IG II2 209", "IG II2 210", "IG II2 211", "IG II2 212", "IG II2 213", "IG II2 215", "IG II2 218", "IG II2 219", "IG II2 220", "IG II2 221", "IG II2 222", "IG II2 223", "IG II2 224", "IG II2 225", "IG II2 226", "IG II2 228", "IG II2 229", "IG II2 230", "IG II2 231", "IG II2 232", "IG II2 233", "IG II2 234", "IG II2 235", "IG II2 236", "IG II2 237", "IG II2 238", "IG II2 239", "IG II2 240", "IG II2 241", "IG II2 242", "IG II2 243", "IG II2 244", "IG II2 251", "IG II2 254", "IG II2 255", "IG II2 256", "IG II2 257", "IG II2 258", "IG II2 260", "IG II2 263", "IG II2 264", "IG II2 266", "IG II2 267", "IG II2 269", "IG II2 270", "IG II2 271", "IG II2 272", "IG II2 275", "IG II2 276", "IG II2 281", "IG II2 2827", "IG II2 283", "IG II2 2838", "IG II2 284", "IG II2 285", "IG II2 286", "IG II2 288", "IG II2 290", "IG II2 292", "IG II2 293", "IG II2 294", "IG II2 295", "IG II2 296", "IG II2 297", "IG II2 298", "IG II2 299", "IG II2 301", "IG II2 302", "IG II2 303", "IG II2 306", "IG II2 307", "IG II2 310", "IG II2 311", "IG II2 312", "IG II2 313", "IG II2 314", "IG II2 315", "IG II2 316", "IG II2 320", "IG II2 322", "IG II2 323", "IG II2 325", "IG II2 326", "IG II2 328", "IG II2 329", "IG II2 330", "IG II2 331", "IG II2 333", "IG II2 334", "IG II2 335", "IG II2 336", "IG II2 337", "IG II2 339a", "IG II2 339b", "IG II2 340", "IG II2 342", "IG II2 343", "IG II2 344", "IG II2 345", "IG II2 346", "IG II2 347", "IG II2 348", "IG II2 349", "IG II2 351", "IG II2 352", "IG II2 353", "IG II2 354", "IG II2 356", "IG II2 357", "IG II2 359", "IG II2 360", "IG II2 361", "IG II2 362", "IG II2 363", "IG II2 365", "IG II2 367", "IG II2 368", "IG II2 369", "IG II2 370", "IG II2 371", "IG II2 372", "IG II2 375", "IG II2 375", "IG II2 376", "IG II2 377", "IG II2 399", "IG II2 402", "IG II2 403", "IG II2 405", "IG II2 406", "IG II2 408", "IG II2 409", "IG II2 410", "IG II2 411", "IG II2 412", "IG II2 414a", "IG II2 414b", "IG II2 414c", "IG II2 415", "IG II2 416a", "IG II2 416b", "IG II2 417", "IG II2 419", "IG II2 420", "IG II2 421", "IG II2 422", "IG II2 423", "IG II2 424", "IG II2 425", "IG II2 426", "IG II2 427", "IG II2 429", "IG II2 430", "IG II2 431", "IG II2 432", "IG II2 433", "IG II2 434", "IG II2 435", "IG II2 436", "IG II2 437", "IG II2 439", "IG II2 444", "IG II2 446", "IG II2 448", "IG II2 449", "IG II2 451", "IG II2 452", "IG II2 454", "IG II2 4630", "IG II2 539", "IG II2 543", "IG II2 544", "IG II2 546", "IG II2 547", "IG II2 548", "IG II2 551", "IG II2 564", "IG II2 575", "IG II2 579", "IG II2 581", "IG II2 601", "IG II2 705", "IG II2 738", "IG II2 800", "IG II2 824", "IG II3 1 1135", "IG II3 1 1136", "IG II3 1 1137", "IG II3 1 1138", "IG II3 1 1139", "IG II3 1 1140", "IG II3 1 1141", "IG II3 1 1142", "IG II3 1 1143", "IG II3 1 1144", "IG II3 1 1145", "IG II3 1 1146", "IG II3 1 1147", "IG II3 1 1148", "IG II3 1 1149", "IG II3 1 1150", "IG II3 1 1151", "IG II3 1 1152", "IG II3 1 1153", "IG II3 1 1154", "IG II3 1 1155", "IG II3 1 1156", "IG II3 1 1157", "IG II3 1 1158", "IG II3 1 1159", "IG II3 1 1160", "IG II3 1 1161", "IG II3 1 1162", "IG II3 1 1163", "IG II3 1 1164", "IG II3 1 1165", "IG II3 1 1166", "IG II3 1 1167", "IG II3 1 1168", "IG II3 1 1169", "IG II3 1 1170", "IG II3 1 1171", "IG II3 1 1172", "IG II3 1 1173", "IG II3 1 1174", "IG II3 1 1175", "IG II3 1 1176", "IG II3 1 1177", "IG II3 1 1178", "IG II3 1 1179", "IG II3 1 1180", "IG II3 1 1181", "IG II3 1 1182", "IG II3 1 1183", "IG II3 1 1184", "IG II3 1 1185", "IG II3 1 1186", "IG II3 1 1187", "IG II3 1 1188", "IG II3 1 1189", "IG II3 1 1190", "IG II3 1 1191", "IG II3 1 1191", "IG II3 1 1192", "IG II3 1 1192", "IG II3 1 1193", "IG II3 1 1193", "IG II3 1 1194", "IG II3 1 1195", "IG II3 1 1196", "IG II3 1 1196", "IG II3 1 1197", "IG II3 1 1198", "IG II3 1 1199", "IG II3 1 1200", "IG II3 1 1201", "IG II3 1 1202", "IG II3 1 1203", "IG II3 1 1204", "IG II3 1 1205", "IG II3 1 1206", "IG II3 1 1207", "IG II3 1 1208", "IG II3 1 1209", "IG II3 1 1210", "IG II3 1 1211", "IG II3 1 1212", "IG II3 1 1213", "IG II3 1 1214", "IG II3 1 1215", "IG II3 1 1216", "IG II3 1 1217", "IG II3 1 1218", "IG II3 1 1219", "IG II3 1 1220", "IG II3 1 1221", "IG II3 1 1222", "IG II3 1 1223", "IG II3 1 1224", "IG II3 1 1225", "IG II3 1 1226", "IG II3 1 1227", "IG II3 1 1228", "IG II3 1 1229", "IG II3 1 1230", "IG II3 1 1231", "IG II3 1 1232", "IG II3 1 1233", "IG II3 1 1234", "IG II3 1 1235", "IG II3 1 1236", "IG II3 1 1237", "IG II3 1 1238", "IG II3 1 1239", "IG II3 1 1240", "IG II3 1 1241", "IG II3 1 1242", "IG II3 1 1243", "IG II3 1 1244", "IG II3 1 1245", "IG II3 1 1246", "IG II3 1 1247", "IG II3 1 1248", "IG II3 1 1249", "IG II3 1 1250", "IG II3 1 1251", "IG II3 1 1252", "IG II3 1 1253", "IG II3 1 1254", "IG II3 1 1255", "IG II3 1 1284", "IG II3 1 326", "IG II3 1 363", "IG II3 1 364", "IG II3 1 368", "IG II3 1 372", "IG II3 1 374", "IG II3 1 377", "IG II3 1 383", "IG II3 1 386", "IG II3 1 391", "IG II3 1 396", "IG II3 1 397", "IG II3 1 400", "IG II3 1 405", "IG II3 1 421", "IG II3 1 422", "IG II3 1 423", "IG II3 1 425", "IG II3 1 427", "IG II3 1 435", "IG II3 1 436", "IG II3 1 438", "IG II3 1 451", "IG II3 1 460", "IG II3 1 461", "IG II3 1 510", "IG II3 1 513", "IG II3 1 520", "IG II3 1 523", "IG II3 1 524", "IG II3 1 525", "IG II3 1 534", "IG II3 1 536", "IG II3 1 537", "IG II3 1 539", "IG II3 1 546", "IG II3 1 547", "IG II3 1 549", "IG II3 1 553", "IG II3 1 554", "IG II3 1 558", "IG II3 1 559", "IG II3 1 563", "IG II3 1 567", "IG II3 1 572", "IG II3 1 929", "IG I3 11", "IG I3 14", "IG I3 227 bis", "IG I3 34", "IG I3 35", "IG I3 36", "IG I3 375", "IG I3 377", "IG I3 52", "IG I3 61", "IG I3 84", "IG VII 3499", "IG VII 4252", "IG VII 4253", "IG VII 4254", "IG VII 4255", "IG XII 3 1018", "ML 46", "ML 49", "ML 58", "ML 65", "ML 80", "ML 86", "ML 90", "ML 94", "Osborne, Naturalization D25e", "Osborne, Naturalization D25f", "Osborne, Naturalization D25g", "Osborne, Naturalization D25h", "Osborne, Naturalization D26", "Osborne, Naturalization X32", "RO 10", "RO 11", "RO 17", "RO 18", "RO 19", "RO 2 (decrees 2-3) (l. 74)", "RO 20", "RO 21", "RO 22", "RO 23", "RO 24", "RO 25", "RO 26", "RO 29", "RO 31", "RO 34", "RO 35", "RO 38", "RO 39", "RO 41", "RO 44", "RO 47", "RO 48", "RO 52", "RO 53", "Schwenk 16", "Schwenk 19", "Schwenk 34", "Schwenk 39", "Schwenk 5", "Schwenk 59", "Schwenk 6", "Schwenk 71", "Schwenk 72", "Schwenk 9", "Schwenk pp. 127-28", "SdA II 142", "SdA II 149", "SdA II 162", "SdA II 163", "SdA II 183", "SdA II 207", "SdA II 207a", "SdA II 208a", "Tod 72", "Walbank 65"]

DATA_DIR = requests.get('http://www.atticinscriptions.com/inscription/all.xml')

LICENSE = 'Creative Commons Attribution-ShareAlike 3.0 http://creativecommons.org/licenses/by-sa/3.0/'
AUTHOR = 'Stephen Lambert'
PUB_TITLE = 'Attic Inscriptions Online'
BASE_URL = 'http://www.atticinscriptions.com/inscription/'

def main():
	always = dryrun = startsWith = False
	
	# Handles command-line arguments for pywikibot.
	for arg in pywikibot.handleArgs():
		if arg == '-dry': # Performs a dry run (does not edit site)
			dryrun = True
		if arg == '-always': # Does not ask for confirmation
			always = True
		if arg.startswith('-start:'): # Example: -start:57
			startsWith = arg.replace('-start:', '')
	
	if not dryrun:
		# pywikibot/families/eagle_family.py
		site = pywikibot.Site('en', 'eagle').data_repository()
		
	data = BeautifulSoup(DATA_DIR.text)
	urls = []

	for aiourl in data.find_all('url'):
		urls.append(aiourl.text)
		
	for aiourlhttp in urls:
		ronefile = requests.get('http://' + aiourlhttp)
		onefile = BeautifulSoup(ronefile.text)
		if elementText2(onefile.translation_source)  not in inwiki:	
		# Label and description
			data['label'] = elementText(onefile.translation_source)
			data['description'] = elementText(onefile.root.translation_title)
		
			pywikibot.output("\n>>>>> " + data['label'] + " <<<<<\n")
			pywikibot.output('Processing file ' + onefile.aio_key.text)
			pywikibot.output('Label: ' + data['label'])
			pywikibot.output('Description: ' + data['description'])
		
		# ID and URL
			data['aioid'] = elementText(onefile.aio_key).split('_')[1]
			data['url'] = 'http://' + elementText(onefile.url)
			pywikibot.output('AIO ID: ' + data['aioid'])
			pywikibot.output('URL: ' + data['url'])
		
		# IPR (License)
			data['ipr'] = LICENSE
			pywikibot.output('IPR: ' + data['ipr'])
		
		# Translation EN:
			data['translationEn'] = elementText(onefile.translation)
			pywikibot.output('EN translation: ' + data['translationEn'])
		
		# Publication author
			data['pubAuthor'] = AUTHOR
			pywikibot.output('Publication author: ' + data['pubAuthor'])
		
		# Translation author
			authors = onefile.translators.find_all('item')
			data['transAuthors'] = []
			for i in authors:
				authorName = elementText(i)
				data['transAuthors'].append(authorName)
				pywikibot.output('Translation author: ' + authorName)
		
		# Publication title
			data['pubTitle'] = PUB_TITLE
			pywikibot.output('Publication title: ' + data['pubTitle'])
		
			pywikibot.output('') # newline
		
			choice = None
			while choice is None:
				if not always:
					choice = pywikibot.inputChoice(u"Proceed?",  ['Yes', 'No', 'All', 'open in browser'], ['y', 'N', 'a', 'b'], 'N')
				else:
					choice = 'y'
				if choice in ['A', 'a']:
					always = True
					choice = 'y'
				elif choice in ['B', 'b']:
					webbrowser.open(data['url'])
					choice = None # Re-ask
		
			if not dryrun and choice in ['Y', 'y']:
				page = pywikibot.ItemPage(site)
				page.editEntity({'labels':{'en': data['label']}, 'descriptions':{'en': data['description']}})
				page.get()
			
				aioidClaim = pywikibot.Claim(site, 'P51')
				aioidClaim.setTarget(data['aioid'])
				page.addClaim(aioidClaim)
			
				urlClaim = pywikibot.Claim(site, 'P52')
				urlClaim.setTarget(data['url'])
				aioidClaim.addSource(urlClaim)
			
				addClaimToItem(site, page, 'P25', data['ipr'])
			
				transClaim = pywikibot.Claim(site, 'P11')
				transClaim.setTarget(data['translationEn'])
				page.addClaim(transClaim)
			
				sources = []
			
				for i in data['transAuthors']:
					transAuthorClaim = pywikibot.Claim(site, 'P21')
					transAuthorClaim.setTarget(i)
					sources.append(transAuthorClaim)
			
				pubAuthorClaim = pywikibot.Claim(site, 'P46')
				pubAuthorClaim.setTarget(data['pubAuthor'])
				sources.append(pubAuthorClaim)
			
				pubClaim = pywikibot.Claim(site, 'P26')
				pubClaim.setTarget(data['pubTitle'])
				sources.append(pubClaim)
			
				transClaim.addSources(sources)

def addClaimToItem(site, page, id, value):
	"""Adds a claim to an ItemPage."""
	claim = pywikibot.Claim(site, id)
	claim.setTarget(value)
	page.addClaim(claim)

def replaceSuperscript(text):
	superRep = [
		(u'1', u'¹'),
		(u'2', u'²'),
		(u'3', u'³'),
		(u'4', u'⁴'),
		(u'5', u'⁵'),
		(u'6', u'⁶'),
		(u'7', u'⁷'),
		(u'8', u'⁸'),
		(u'9', u'⁹'),
		(u'0', u'⁰'),
	]
	for i in superRep:
		text = text.replace(i[0], u'%sup%' + i[1])
	return text

def elementText(elem):
	# We need to re-parse the XML in translation_source and translation_title because it's escaped.
	soup = BeautifulSoup(elem.get_text(' ', strip=True))
	
	sups = soup.find_all('sup')
	for i in sups:
		i.replaceWith(replaceSuperscript(i.string))
	text = soup.get_text(' ', strip=True)
	text = text.replace(u' %sup%', '')
	text = re.sub('\n', ' ', text)
	text = re.sub('\s{2,}', ' ', text)
	return text

def elementText2(elem):
	# We need to re-parse the XML in translation_source and translation_title because it's escaped.
	soup = BeautifulSoup(elem.get_text(' ', strip=True))
	
	sups = soup.find_all('sup')
	for i in sups:
		i.replaceWith(replaceSuperscript(i.string))
	text = soup.get_text(' ', strip=True)
	text = text.replace(u' %sup%', '')
	text = re.sub('\n', ' ', text)
	text = re.sub('\xb3', '3', text)
	text = re.sub('\xb2', '2', text)
	text = re.sub('\s{2,}', ' ', text)
	return text
'''
def normalizeText(text):
	"""Removes double spaces, newlines and spaces at the beginning or at the end of the string"""
	text = re.sub('\n', ' ', text.strip())
	text = re.sub('\s{2,}', ' ', text)
	text = re.sub("<i>", '', text)
	text = re.sub("</i>", '', text)
	text = re.sub("<sup>", '', text)
	text = re.sub("</sup>", '', text)
	return text
'''
if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()