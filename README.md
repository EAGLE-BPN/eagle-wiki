Wikimedia EAGLE import project
=====

The Python scripts import the EAGLE data into the [EAGLE Wikibase wiki](http://www.eagle-network.eu/wiki/index.php/).
Import scripts have been developed for the following datasets:
* IRT
* Hispania Epigrafica
* Ubi Erat Lupa
* Petrae
* Attic Inscriptions Online
* InsAph
* ELTE

More information on EAGLE here:
http://eagle-network.eu/

Using [pywikipediabot rewrite branch](https://github.com/wikimedia/pywikibot-core).
A [patch](https://gerrit.wikimedia.org/r/#/c/76527/4) was manually applied to pywikipediabot in order to create new items in Wikibase.

The script uses extensively the Python [regex](http://docs.python.org/2/library/re.html) module, the [csv](http://docs.python.org/2/library/csv.html) module, [BeautifulSoup 4](http://www.crummy.com/software/BeautifulSoup/bs4/doc/), and the [XML etree](http://docs.python.org/2/library/xml.etree.elementtree.html) module.
