import Helpers, math, heapq

def getWhereMotionBegins(path):
	THRESHOLD = 2.5
	initial = path[0]
	i = 0
	for point in path:
		if Helpers.getDistance(initial, point) > THRESHOLD:
			break
		i += 1
	return i

def getLetterPoints(path):
	path = path[8:] #trim potential second finger distracting things
	path = path[getWhereMotionBegins(path):]
	path = path[:(len(path)-8)] #trim the end (where second finger comes into play)
	path = path[::14] # pick every nth frame
	
	letterPoints = [path[0]]
	if len(path) < 3:
		return letterPoints
	oldPoint = path[1]
	oldPath = (oldPoint, path[2])
	
	for i in xrange(2,len(path)):
		newPoint = path[i]
		newPath = (oldPoint, newPoint)
		if Helpers.isSamePathDirection(oldPath, newPath) == False:
			letterPoints.append(oldPoint)
		oldPath = newPath
		oldPoint = newPoint
	letterPoints.append(path[len(path)-1])
	return letterPoints

def eraseDuplicatePoints(letterPoints):
	THRESHOLD = 26
	listWithoutDuplicates = [letterPoints[0]]
	for i in xrange(1,len(letterPoints)):
		distance = Helpers.getDistance(letterPoints[i-1], letterPoints[i])
		if distance > THRESHOLD:
			listWithoutDuplicates.append(letterPoints[i])
	return listWithoutDuplicates
		

def mapCharToPoint(char, letterPoints):
	ctp = {}
	ctp['q'] = (0,.8)
	ctp['w'] = (.11,.8)
	ctp['e'] = (.22,.8)
	ctp['r'] = (.33,.8)
	ctp['t'] = (.44,.8)
	ctp['y'] = (.55,.8)
	ctp['u'] = (.66,.8)
	ctp['i'] = (.77,.8)
	ctp['o'] = (.88,.8)
	ctp['p'] = (1,.8)
	ctp['a'] = (.05,.4)
	ctp['s'] = (.16,.4)
	ctp['d'] = (.27,.4)
	ctp['f'] = (.38,.4)
	ctp['g'] = (.49,.4)
	ctp['h'] = (.6,.4)
	ctp['j'] = (.71,.4)
	ctp['k'] = (.82,.4)
	ctp['l'] = (.93,.4)
	ctp['z'] = (.1,0)
	ctp['x'] = (.21,0)
	ctp['c'] = (.32,0)
	ctp['v'] = (.43,0)
	ctp['b'] = (.54,0)
	ctp['n'] = (.65,0)
	ctp['m'] = (.76,0)
	desiredPoint = ctp[char]
	if len(letterPoints) > 0:
		if letterPoints[-1] == desiredPoint:
			letterPoints.pop(-1)
	if len(letterPoints) > 1:
		ANGLE_THRESHOLD = 18
		point1 = letterPoints[-2]
		point2 = letterPoints[-1]
		degree1 = Helpers.getAngle(point1,point2)
		degree2 = Helpers.getAngle(point2, desiredPoint)
		if math.fabs(degree1-degree2) < ANGLE_THRESHOLD:
			letterPoints.pop(-1)
	return desiredPoint
	
def getPatternOfWord(word):
	letterPoints = []
	for char in word.lower():
		charPoint = mapCharToPoint(char, letterPoints)
		letterPoints.append(charPoint)	
	return letterPoints
	
def convertPatternToAngleAndLength(letterPoints):
	patternInAngleAndLength = []
	oldPoint = letterPoints[0]
	for i in xrange(1,len(letterPoints)):
		newPoint = letterPoints[i]
		angle = Helpers.getAngle(oldPoint, newPoint)
		length = Helpers.getDistance(oldPoint, newPoint)
		patternInAngleAndLength.append((angle,length))
		oldPoint = newPoint
	return patternInAngleAndLength

def getAngleError(pattern1, pattern2):
	totalAngleError = 0
	for edge1, edge2 in zip(pattern1, pattern2):
		angle1 = edge1[0]
		angle2 = edge2[0]
		difference1 = math.fabs(angle1-angle2)
		difference2 = min(angle1,angle2)+360-max(angle1,angle2)
		totalAngleError += min(difference1,difference2)/180
	return totalAngleError/len(pattern1)

def getLengthError(pattern1, pattern2):
	totalLengthError = 0
	lengths1 = [x[1] for x in pattern1]
	lengths2 = [x[1] for x in pattern2]
	normalizedLengths1 = Helpers.normalizeLengths(lengths1)
	normalizedLengths2 = Helpers.normalizeLengths(lengths2)
	for length1, length2 in zip(normalizedLengths1, normalizedLengths2):
		totalLengthError += max(length1,length2)/min(length1,length2)-1
	return totalLengthError/len(pattern1)

def comparePatterns(pattern1, pattern2):
	#both patterns are guaranteed to have the same number of edges

	angleError = getAngleError(pattern1,pattern2)
	lengthError = getLengthError(pattern1, pattern2)
	
	error = 0.8*angleError+.2*lengthError
	return error	
	
def compareShapes(letterPoints, wordToGesture):
	if len(letterPoints) == 1:
		bestScores = []
		for wordPattern in wordToGesture[len(letterPoints)]:
			bestScores.append((1,wordPattern[0]))
		return bestScores
	patternInAngleAndLength = convertPatternToAngleAndLength(letterPoints)
	nBestScores = []
	for wordPattern in wordToGesture[len(letterPoints)]:
		(word, pattern) = (wordPattern[0],wordPattern[1])
		score = 1 - comparePatterns(patternInAngleAndLength, pattern)
		entry = (score,word)
		if len(nBestScores) < 30:
			heapq.heappush(nBestScores, entry)
		else:
			if nBestScores[0] < entry:
				heapq.heappop(nBestScores)
				heapq.heappush(nBestScores,entry)
	return nBestScores
			
def getBestResults(scoresAndWords, wordFrequencies):
	bestResults = []
	for scoreWord in scoresAndWords:
		shapeScore = scoreWord[0]
		freqScore = math.log(wordFrequencies[scoreWord[1]])/19
		totalScore = (0.75*shapeScore+.25*freqScore)*100
		entry = (totalScore,scoreWord[1])
		if len(bestResults) < 7:
			heapq.heappush(bestResults,entry)
		else:
			if bestResults[0] < entry:
				heapq.heappop(bestResults)
				heapq.heappush(bestResults,entry)
	bestResults = sorted(bestResults, key=lambda scoreWord: scoreWord[0])
	bestResults.reverse()
	return bestResults
		
		
		
		
		