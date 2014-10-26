# Wikimedia EAGLE import project

## About

The Python scripts import the EAGLE data into the [EAGLE Wikibase wiki](http://www.eagle-network.eu/wiki/index.php/).
Import scripts have been developed for the following datasets:
* IRT
* Hispania Epigrafica
* Ubi Erat Lupa
* Petrae
* Attic Inscriptions Online
* InsAph
* ELTE
* Universitatea Babeş-Bolyai
* Arachne - Deutsches Archäologisches Institut
* Last Statue of Antiquities
* Roman Inscriptions of Britain

More information on EAGLE here:
http://eagle-network.eu/

Using [pywikipediabot rewrite branch](https://github.com/wikimedia/pywikibot-core).

The script library needs and uses extensively the Python [regex](http://docs.python.org/2/library/re.html) module, the [csv](http://docs.python.org/2/library/csv.html) module, [BeautifulSoup 4](http://www.crummy.com/software/BeautifulSoup/bs4/doc/), and the [XML etree](http://docs.python.org/2/library/xml.etree.elementtree.html) module.

## Installation

This brief how-to covers the installation of the pywikibot "core" library as well the setup of this library for editing EAGLE Wiki.
Its aim is to give you a working environment for further development.

We'll assume that your shell is Bash and you're installing the scripts in the directory `~/eagle`. Change the paths accordingly.
We're also generating the user-config.py files from scratch; if you are an advanced user you'll just need to add the relevant line for EAGLE Wiki (family="eagle"; lang="en").

Please note that in the installation process we have to manually apply [this patch](https://gerrit.wikimedia.org/r/#/c/167532/) to the pywikibot source in order to ensure compatibility with the older version of Wikibase in EAGLE Wiki.

<pre>
$ <b>mkdir eagle</b>
$ <b>cd eagle</b>
$ <b>git clone --recursive https://gerrit.wikimedia.org/r/pywikibot/core.git</b>
$ <b>git clone https://github.com/EAGLE-BPN/eagle-wiki.git</b>
$ <b>cp eagle-wiki/eagle_family.py core/pywikibot/families/eagle_family.py</b>
$ <b>cd core</b>
$ <b>git fetch https://gerrit.wikimedia.org/r/pywikibot/core refs/changes/32/167532/2 && git cherry-pick FETCH_HEAD</b>

$ <b>python generate_user_files.py</b>

No user-config.py found in directory '/Users/alt/eagle/core'.

WARNING: Skipping loading of user-config.py.
WARNING: family and mylang are not set.
Defaulting to family='test' and mylang='test'.

Your default user directory is "/Users/alt/eagle/core"
How to proceed? ([K]eep, [c]hange) <b>K</b>
Do you want to copy user files from an existing Pywikibot installation? ([y]es, [n]o) <b>n</b>
Create user-config.py file? Required for running bots. ([y]es, [N]o) <b>y</b>
[...]
 3: commons
 4: eagle
 5: i18n
[...]
Select family of sites we are working on, just enter the number or name (default: wikipedia):  <b>eagle</b>
The only known language: en
The language code of the site we're working on (default: 'en'): 
Username on en:eagle: <b>Pietrodn</b>
Do you want to add any other projects? ([y]es, [N]o) <b>N</b>
Which variant of user_config.py? ([s]mall, [e]xtended (with further information)) <b>s</b>
'/Users/alt/eagle/core/user-config.py' written.
Create user-fixes.py file? Optional and for advanced users. ([y]es, [N]o) <b>N</b>


$ <b>python pwb.py login</b>

Password for user Pietrodn on eagle:en (no characters will be shown): 
Logging in to eagle:en as Pietrodn
Logged in on eagle:en as Pietrodn.


$ <b>echo "export PYWIKIBOT2_DIR=~/eagle/core/" >> ~/.profile</b>
$ <b>echo "export PYTHONPATH=$PYTHONPATH:~/eagle/core/" >> ~/.profile</b>
$ <b>source ~/.profile</b>
$ <b>cd ../eagle-wiki</b>
</pre>

Now we can run an example script:
<pre>
$ <b>python get_property_list.py -property:50 -show:property</b>
</pre>
