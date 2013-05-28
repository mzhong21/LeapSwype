import math

def getDistance(point1, point2):
	distance = 0
	distance = math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)
	return distance

def getAngle(point1, point2):
	y = point2[1]-point1[1]
	x = point2[0]-point1[0]
	return math.degrees(math.atan2(y,x))	

def normalizeLengths(lengths):
	normalizationConstant = sum(lengths)/len(lengths)
	normalizedLengths = [x/normalizationConstant for x in lengths]
	return normalizedLengths

def isSamePathDirection(path1, path2):
	MIN_MOVEMENT_DIST = 8.6
	ANGLE_CHANGE = 30
	path1Dist = getDistance(path1[0], path1[1])
	path2Dist = getDistance(path2[0], path2[1])
	if path1Dist < MIN_MOVEMENT_DIST or path2Dist < MIN_MOVEMENT_DIST:
		return True
		
	path1Angle = getAngle(path1[0], path1[1])
	path2Angle = getAngle(path2[0], path2[1])
	if math.fabs(path1Angle-path2Angle) <= ANGLE_CHANGE:
		return True
	else:
		return False