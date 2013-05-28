import urllib2, re

def readWebsite(url):
	site = url
	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
	       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
	       'Accept-Encoding': 'none',
	       'Accept-Language': 'en-US,en;q=0.8',
	       'Connection': 'keep-alive'}
	req = urllib2.Request(site, headers=hdr)
	page = urllib2.urlopen(req)
	return page.read()
	
def storeFrequencyCounts(listOfWords):
	dictionary = {}
	for i in listOfWords:
		if i[0] not in dictionary:
			dictionary[i[0]] = float(i[1])
	return dictionary

def populateWordFrequencies():
	def getWordsFromProjectGutenberg():
		def fetchWebsiteContents():
			wikipediaPageContents = []
			for i in (0,10000, 20000, 30000):
				begin = str(i+1)
				end = str(i+10000)
				url = "http://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/PG/2006/04/%s-%s" % (begin, end)
				wikipediaPageContents.append(readWebsite(url))
			return wikipediaPageContents
		def parsePGPages(contents):
			wordAndFreqs = []
			searchPattern1 = r"""<a href="/wiki/[a-zA-Z\-']+" title=\S+>([a-zA-Z\-']+)</a> = ([0-9.]+)"""
			searchPattern2 = r"""<a href="/w/index\S+title=.+>([a-zA-Z\-']+)</a> = ([0-9.]+) """
			#avoid the colon
			#<a href="/wiki/of" title="of">of</a> = 33950064 <a href="/wiki/and"
			#<a href="/w/index.php?title=
			for page in contents:
				wordAndFreqs += re.findall(searchPattern1, page)
				wordAndFreqs += re.findall(searchPattern2, page)
			return wordAndFreqs
		wikipediaPageContents = fetchWebsiteContents()
		wordAndFreqs = parsePGPages(wikipediaPageContents)
		return storeFrequencyCounts(wordAndFreqs)
		
	def getWordsFromWiktionaryTV():
		def fetchWebsiteContents():
			wiktionaryPageContents = []
			i = 0
			while True:
				if i < 10000:
					begin = str(i+1)
					end = str(i+1000)
				elif i < 40000:
					begin = str(i+1)
					end = str(i+2000)
				elif i == 40000:
					begin = 40001
					end = 41284
				url = "http://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/TV/2006/%s-%s" % (begin, end)
				wiktionaryPageContents.append(readWebsite(url))
				if i < 10000:
					i += 1000
				elif i < 40000:
					i += 2000
				else:
					break
			return wiktionaryPageContents
		def parsePages(contents):
			wordAndFreqs = []
			searchPattern = r"""<td><a href=.+>([a-zA-Z\-']+)</a></td>\s<td>([0-9]+)</td>"""
			for page in contents:
				wordAndFreqs += re.findall(searchPattern, page)
			return wordAndFreqs
			#<tr>
			#<td>986</td>
			#<td><a href="/wiki/present" title="present">present</a></td>
			#<td>2313</td>
			#</tr>
			
		wiktionaryPageContents = fetchWebsiteContents()
		wordAndFreqs = parsePages(wiktionaryPageContents)
		return storeFrequencyCounts(wordAndFreqs)
		
	def getPopularBabyNames():
		babyNamesFile = open("Popular Baby Names.html", "r")
		searchPattern = r"""<td>([A-Za-z]+)</td>\s*<td>([0-9,]+)</td>"""
		wordAndFreqs = re.findall(searchPattern, babyNamesFile.read())
		for i in xrange(0,len(wordAndFreqs)):
			wordAndFreqs[i] = (wordAndFreqs[i][0],int((wordAndFreqs[i][1]).replace(",", "")))
		return storeFrequencyCounts(wordAndFreqs)
		#<tr align="right">
		#<td>2</td> <td>Mason</td><td>19,396</td>
		#<td>Isabella</td>
		#<td>19,745</td>
		#</tr>
		
	def combineData(allDicts):
		frequencyOfDicts = []
		
		#calibrate weights of dictionaries
		for dictionary in allDicts:
			print len(dictionary)
			frequencyOfDicts.append(sum(dictionary.values()))
		weightOfPG = 1
		weightOfWiktionary = 1
		weightOfBabyNames = .017
		allWordsFrequency = {}
		
		#populate dictionary with all words
		for i, dictionary in enumerate(allDicts):
			for word in dictionary:
				if i == 0: #if the dictionary is the PG one
					weight = weightOfPG
				elif i == 1: #if Wiktionary
					weight = weightOfWiktionary
				elif i == 2: #if baby names
					weight = weightOfBabyNames
				weightedFrequency = dictionary[word]/float(frequencyOfDicts[i])*weight*1000000000
				if word in allWordsFrequency:
					allWordsFrequency[word] += dictionary[word]/float(frequencyOfDicts[i])*weight*1000000000
					allWordsFrequency[word] /= 2
				else:
					allWordsFrequency[word] = dictionary[word]/float(frequencyOfDicts[i])*weight*1000000000
		return allWordsFrequency
	def writeToFile(dictionary):
		fp = open("dictionary.txt", "w")
		for word in sorted(dictionary, key=dictionary.get, reverse=True):
			if dictionary[word] < .1:
				break
			lineToWrite = word + "," + str(int(dictionary[word])) + "\n"
			fp.write(lineToWrite)
		fp.close()
			
	
	dictionariesToCombine = []
	dictionariesToCombine.append(getWordsFromProjectGutenberg())
	dictionariesToCombine.append(getWordsFromWiktionaryTV())
	dictionariesToCombine.append(getPopularBabyNames())
	masterDict = combineData(dictionariesToCombine)
	writeToFile(masterDict)
	
	
	
	