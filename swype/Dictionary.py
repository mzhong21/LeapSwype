#generates the dictionaries word to frequency and word to gesture shape

import string, PatternRecognizer

def wordToFrequency():
	wordToFrequency = {}
	fp = open('dictionary.txt', 'r')
	for line in fp.readlines():
		(word, frequency) = line.split(',')
		wordToFrequency[word] = int(frequency)
	fp.close()
	return wordToFrequency

def wordToGesture():
	wordToGesture = {}
	fp = open('dictionary.txt', 'r')
	for line in fp.readlines():
		word = line.split(',')[0]
		alteredWord = word.translate(string.maketrans("",""),string.punctuation)
		pattern = PatternRecognizer.getPatternOfWord(alteredWord)
		wordLength = len(pattern)
		if len(pattern) > 1:
			pattern = PatternRecognizer.convertPatternToAngleAndLength(pattern)
		if wordLength in wordToGesture:
			wordToGesture[wordLength].append((word,pattern))
		else:
			wordToGesture[wordLength] = [(word,pattern)]
	return wordToGesture