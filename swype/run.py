import Leap, sys, Dictionary, PatternRecognizer
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture


class SwypeListener(Leap.Listener):	
	def on_init(self, controller):
		self.wordToGesture = Dictionary.wordToGesture()
		self.wordToFrequency = Dictionary.wordToFrequency()
		self.path = []
		print "Initialized"

	def on_connect(self, controller):
		print "Connected"
		print "Ready for gesturing..."

	def on_disconnect(self, controller):
		print "Disconnected"

	def on_exit(self, controller):
		print "Exited"

	def on_frame(self, controller):
		#print self.path
		frame = controller.frame()
		if frame.hands.empty == False:
			fingers = frame.hands[0].fingers
			if len(fingers) > 1:
				if len(self.path) > 40:
					letterPointsList = PatternRecognizer.getLetterPoints(self.path)
					if len(letterPointsList) > 1:
						letterPointsList = PatternRecognizer.eraseDuplicatePoints(letterPointsList)
					print letterPointsList
					self.path = []
					bestShapeScores = PatternRecognizer.compareShapes(letterPointsList, self.wordToGesture)
					results = PatternRecognizer.getBestResults(bestShapeScores, self.wordToFrequency)
					for i, scoreWord in enumerate(results):
						print str(i+1) + ": " + scoreWord[1] + " | " + str(int(scoreWord[0]))
			elif len(fingers) == 1:
				tipObject = fingers[0].tip_position
				position = (tipObject.x, tipObject.y) #ignores the z-position
				self.path.append(position)

def main():
	wordToGesture = Dictionary.wordToGesture()

	listener = SwypeListener()
	controller = Leap.Controller()
	controller.add_listener(listener)

    # Keep this process running until Enter is pressed
 	print "Press Enter to quit..."
	sys.stdin.readline()

    # Remove the listener when done
	controller.remove_listener(listener)


if __name__ == "__main__":
	main()
