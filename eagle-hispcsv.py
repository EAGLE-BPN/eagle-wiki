# -*- coding: utf-8 -*-

"""

Accepted options:
	
	-dry
		Dry run: don't edit the wiki, but process and print all the data.
		It's useful together with -always to check for crashes in the script before launching the bot.
		
	-always
		Don't ask for confirmation before submitting a new item to the wiki.
		
	-start:<bohry_id>
		Start from the item whose Bohry id is <dai_id>. Useful for resuming an interrupted import.

"""

import pywikibot, csv, re, urllib2
import xml.etree.ElementTree as ET

HeOl = [1,
10,
100,
101,
102,
103,
10338,
10353,
10418,
10452,
10454,
10456,
10481,
10499,
106,
107,
108,
109,
11,
110,
111,
112,
113,
114,
115,
116,
117,
11794,
118,
11823,
11839,
11842,
11990,
11994,
12,
12000,
12012,
12046,
12047,
12084,
12085,
12086,
12087,
12097,
121,
12102,
12103,
12133,
12160,
12179,
122,
12327,
12354,
12367,
12371,
12375,
12399,
124,
125,
12577,
126,
12623,
12626,
12643,
12644,
12657,
127,
12740,
12767,
12776,
12779,
12781,
12784,
12788,
12789,
12790,
12792,
12793,
12794,
12795,
128,
129,
13,
130,
131,
1316,
132,
133,
13333,
13335,
1338,
134,
135,
136,
137,
13769,
13770,
13771,
13772,
138,
14,
140,
14048,
141,
14145,
14147,
14149,
14151,
14152,
14154,
14171,
14180,
14184,
14191,
14195,
14197,
142,
14200,
14290,
143,
14300,
14391,
144,
14486,
14487,
145,
146,
147,
14742,
14743,
14745,
14748,
14749,
14750,
14751,
14752,
14753,
14754,
14773,
148,
14828,
14831,
14832,
14833,
14839,
14841,
14862,
14864,
14900,
14960,
14964,
14985,
14986,
14992,
14993,
14994,
14996,
15,
150,
15002,
15007,
15068,
15069,
15079,
151,
15264,
15272,
153,
15372,
154,
15427,
15435,
15437,
15440,
15441,
15442,
15470,
15499,
155,
15513,
15533,
156,
157,
15708,
15847,
1587,
16,
160,
16008,
16009,
16013,
16065,
16085,
161,
16107,
16108,
16109,
16110,
16135,
16140,
16141,
16142,
16143,
16144,
16150,
16158,
16264,
163,
1631,
16365,
16399,
16401,
16498,
165,
166,
167,
16753,
16755,
16756,
168,
16803,
16806,
16810,
16834,
16840,
16882,
16886,
169,
17,
170,
17009,
171,
17165,
17166,
17167,
17168,
17169,
17239,
17307,
17308,
17309,
17317,
17341,
17344,
17346,
17347,
17349,
17350,
17351,
17352,
17353,
174,
17423,
17434,
175,
1755,
17558,
17560,
17567,
17578,
17583,
17584,
17595,
176,
177,
178,
179,
18,
180,
181,
183,
184,
185,
18574,
186,
18765,
18777,
188,
19,
190,
19039,
19047,
19048,
19050,
19051,
19052,
19053,
19054,
192,
19213,
19236,
19239,
193,
19366,
194,
195,
196,
197,
198,
199,
19990,
2,
20,
200,
20014,
20026,
201,
202,
20343,
204,
205,
206,
20651,
207,
208,
209,
21,
21079,
211,
212,
213,
214,
215,
21622,
217,
21738,
218,
21808,
21809,
21811,
21812,
21813,
21814,
21816,
219,
22,
220,
221,
22150,
222,
224,
2242,
2247,
225,
22597,
226,
22682,
22683,
22684,
22685,
22698,
22729,
228,
22832,
229,
22949,
2299,
23,
230,
23025,
231,
23120,
232,
233,
23384,
234,
23431,
235,
236,
23619,
237,
239,
23902,
240,
24087,
241,
24100,
24101,
24103,
24104,
24105,
24112,
24114,
24118,
24123,
24126,
24130,
24137,
24138,
24139,
24155,
24178,
24180,
24189,
24200,
24201,
24205,
24206,
24207,
24212,
24219,
24222,
24223,
24224,
24225,
24228,
24230,
24231,
24232,
24233,
24234,
24235,
24236,
24237,
24238,
24247,
24250,
24251,
24253,
24258,
24260,
24268,
24269,
24270,
24271,
24272,
24274,
24275,
24276,
24277,
24278,
24279,
24280,
24282,
24284,
24285,
24286,
24287,
24288,
24289,
24290,
24292,
24293,
24296,
24297,
24298,
243,
24300,
24301,
24303,
24305,
24307,
24308,
24309,
24311,
24313,
24315,
24317,
24318,
24319,
24320,
24321,
24322,
24323,
24324,
24326,
24329,
24330,
24356,
24357,
24381,
24382,
24384,
24387,
24389,
24395,
24396,
24397,
24398,
24399,
244,
24402,
24403,
24404,
24406,
24407,
24408,
24409,
24410,
24411,
24412,
24413,
24414,
24416,
24417,
24418,
24419,
24420,
24421,
24422,
24423,
24424,
24425,
24426,
24427,
24428,
24429,
24430,
24431,
24432,
24433,
24434,
24435,
24437,
24439,
24440,
24441,
24443,
24444,
24445,
24446,
24447,
24448,
24449,
24450,
24451,
24452,
24453,
24454,
24455,
24456,
24457,
24458,
24459,
24460,
24461,
24462,
24463,
24464,
24465,
24466,
24467,
24468,
24469,
24470,
24471,
24472,
24473,
24474,
24475,
24476,
24478,
24479,
24480,
24481,
24482,
245,
24513,
24608,
24609,
24746,
24747,
24753,
24771,
24793,
248,
24824,
24831,
24850,
24851,
24852,
24853,
24854,
24855,
24901,
24907,
24908,
24918,
24919,
24923,
24925,
24926,
24927,
24928,
24929,
24933,
24945,
24979,
250,
251,
252,
253,
25462,
255,
2559,
256,
2562,
25629,
2563,
2565,
25665,
25666,
25678,
25680,
25681,
25682,
25683,
25684,
25686,
25687,
25688,
25689,
25690,
25691,
25692,
25693,
25695,
25696,
25697,
25698,
257,
25700,
25701,
25702,
25703,
25704,
25705,
25706,
25707,
25708,
25709,
2573,
25732,
2576,
2577,
2579,
258,
259,
2592,
2598,
25982,
25986,
26,
260,
26010,
261,
262,
263,
2648,
266,
267,
268,
269,
27,
270,
271,
272,
2722,
273,
274,
275,
276,
277,
2771,
2772,
2779,
2783,
2789,
279,
28,
280,
2803,
2804,
2805,
2807,
281,
282,
2826,
283,
284,
285,
286,
287,
288,
289,
2897,
29,
290,
291,
2919,
292,
2920,
2921,
2922,
2928,
2929,
293,
2930,
294,
295,
296,
2968,
297,
298,
2987,
299,
3,
30,
300,
301,
302,
303,
304,
305,
306,
307,
309,
310,
311,
312,
313,
314,
315,
316,
317,
318,
319,
32,
320,
321,
322,
323,
324,
325,
326,
327,
328,
329,
33,
330,
331,
332,
333,
334,
335,
336,
337,
338,
339,
34,
340,
341,
342,
343,
345,
346,
347,
348,
349,
35,
350,
351,
352,
353,
354,
355,
356,
357,
358,
359,
36,
360,
361,
362,
363,
364,
365,
367,
3670,
368,
369,
37,
370,
371,
372,
373,
374,
375,
376,
377,
378,
379,
3795,
38,
380,
381,
382,
383,
384,
385,
386,
387,
389,
39,
390,
391,
392,
393,
3933,
394,
395,
396,
397,
40,
4028,
4032,
4056,
4057,
4060,
4078,
4080,
4086,
41,
4134,
4139,
43,
431,
4323,
44,
45,
46,
4609,
47,
494,
4996,
4999,
5,
50,
51,
52,
53,
5378,
54,
55,
56,
5669,
57,
5783,
5788,
5796,
58,
5800,
59,
5967,
5969,
6,
60,
6007,
6009,
602,
6020,
6026,
6030,
6033,
6044,
61,
6151,
6152,
6162,
6173,
62,
6261,
63,
6346,
6376,
6384,
64,
6415,
6432,
6458,
65,
6520,
6567,
6578,
6579,
66,
6641,
6643,
6688,
67,
6715,
6730,
6731,
6732,
6740,
6741,
6743,
6745,
6746,
6747,
6748,
6750,
6751,
6752,
6754,
68,
6833,
6835,
6859,
6864,
69,
7,
70,
7005,
7006,
7045,
7047,
7052,
71,
7100,
7105,
7143,
7144,
7146,
7147,
7149,
7153,
7154,
7155,
7163,
72,
7206,
7213,
7253,
73,
7328,
7329,
7331,
7334,
7335,
7355,
7365,
7367,
74,
742,
7457,
7518,
7519,
7544,
7545,
7546,
7567,
76,
79,
8,
8030,
8031,
8032,
81,
8156,
82,
83,
84,
8421,
8424,
8425,
8426,
8427,
8428,
8429,
8430,
8431,
8432,
8433,
8435,
8436,
8437,
8446,
8464,
8472,
8473,
8474,
8475,
8476,
8507,
8512,
8513,
8518,
8519,
8523,
8527,
8528,
8529,
8554,
8555,
8556,
8557,
8558,
8563,
8567,
8568,
8569,
8573,
8585,
859,
8606,
8612,
8615,
8626,
8627,
8629,
8633,
8634,
8635,
8647,
8663,
87,
88,
8840,
8857,
8859,
8860,
8861,
8862,
8863,
8864,
8865,
8866,
8875,
8891,
8892,
8897,
8898,
8900,
8906,
8907,
8908,
8910,
8911,
8912,
8913,
8914,
8915,
8916,
8917,
8918,
8919,
8921,
8922,
8923,
8924,
8961,
8963,
8964,
8968,
9,
91,
9134,
9166,
9167,
92,
93,
9309,
9312,
9349,
9352,
9353,
9354,
9364,
9375,
9402,
9404,
9405,
9407,
9408,
9409,
9410,
9411,
9412,
9413,
9414,
9415,
9489,
95,
9567,
96,
9612,
9625,
9626,
9627,
9651,
9654,
9659,
97,
970,
99]

DATA_FILE = 'EAGLE-data/hepol_translations.csv'

def main():
	always = dryrun = startsWith = False
	
	# Handles command-line arguments for pywikibot.
	for arg in pywikibot.handleArgs():
		if arg == '-dry': # Performs a dry run (does not edit site)
			dryrun = True
		if arg == '-always': # Does not ask for confirmation
			always = True
		if arg.startswith('-start:'): # Example: -start:255
			startsWith = arg.replace('-start:', '')
	
	# pywikibot/families/eagle_family.py
	site = pywikibot.Site('en', 'eagle').data_repository()
	
	f = open(DATA_FILE, 'r')
	reader = csv.reader(f, delimiter=",")
	withtrans =[]
	notinwiki =[]

	for row in reader:
		if row[2] != 'NULL': 
			withtrans.append(row)

	for row in withtrans:
		if int(row[0]) not in HeOl:
			notinwiki.append(row)

	for row in notinwiki:
		ID = normalizeText(row[0])
		if startsWith:
			if ID != startsWith:
				continue # Skips files until start
			elif ID == startsWith:
				startsWith = False # Resets

		hep = normalizeText(row[0]) # Remove extension (.xml)
		label = 'HEp ' + hep
		pywikibot.output("\n>>>>> " + label + " <<<<<\n")
		pywikibot.output('HEp ID: ' + hep)
		
		translationEs = normalizeText(row[2])
		if translationEs == 'NULL':
			pywikibot.output('WARNING: no translation. Skipping.')
			continue
		pywikibot.output('Translation ES: ' + translationEs)
		
		ipr = "http://creativecommons.org/licenses/by-sa/3.0/"
		pywikibot.output('IPR: ' + ipr)
		
		author = normalizeText(row[3])
		if author == 'NULL':
			pywikibot.output('Author: Hispania Epigraphica Online')
		else:
			pywikibot.output('Author: ' + author)
		
		title = normalizeText(str(row[1]))
		pywikibot.output('Descriptions: ' + title)
		
		pywikibot.output('') # newline
		
		if not always:
			choice = pywikibot.inputChoice(u"Proceed?",  ['Yes', 'No', 'All'], ['y', 'N', 'a'], 'N')
		else:
			choice = 'y'
		if choice in ['A', 'a']:
			always = True
			choice = 'y'
		if not dryrun and choice in ['Y', 'y']:
			
			page = pywikibot.ItemPage(site)
			page.editEntity({'labels':{'en': label, 'es': label}, 'descriptions':{'es': title}})
			page.get()
				
			# ES translation
			transClaim = pywikibot.Claim(site, 'P14')
			transClaim.setTarget(translationEs)
			page.addClaim(transClaim)
		
			# Sources of translation
			if author:
				authorClaim = pywikibot.Claim(site, 'P21')
				authorClaim.setTarget(author)
				transClaim.addSource(authorClaim)
		
			
			# Other properties
			
			addClaimToItem(site, page, 'P25', ipr)
			addClaimToItem(site, page, 'P22', label) # HispEpOnline identifier
			

	f.close()
	
def addClaimToItem(site, page, id, value):
	"""Adds a claim to an ItemPage."""
	claim = pywikibot.Claim(site, id)
	claim.setTarget(value)
	page.addClaim(claim)

def normalizeText(text):
	"""Removes double spaces, newlines and spaces at the beginning or at the end of the string"""
	text = re.sub('\n', ' ', text.strip())
	text = re.sub('\s{2,}', ' ', text)
	return text


		
if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()