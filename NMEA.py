
class NMEAparse(object):
	def __init__(self):
		self.message='NAN'
		self.timestamp=0
		self.latitude=0
		self.hemisphereNS='N'
		self.longitude=0
		self.hemishereEW='W'
		self.quality=0
		self.altitude=0
		self.depth=0
		self.heading=0
		self.roll=0
		self.pitch=0
		self.eastRate=0
		self.northRate=0
		self.downRate=0
		self.pitchRate=0
		self.rollRate=0
		self.yawRate=0


	def parse(self,sentence):
		sentence = sentence.split('*')[0]
		brokenSentence=sentence.split(',')
		# print(brokenSentence)
		messageType=brokenSentence[0]
		self.timestamp=brokenSentence[1]
		if(messageType=='$BFACK'):
			self.message='ACK'


		elif(messageType=='$BFNVG'):
			self.message='NVG'
			self.latitude=float(brokenSentence[2])
			self.hemisphereNS=brokenSentence[3]
			self.longitude=float(brokenSentence[4])
			self.hemishereEW=brokenSentence[5]
			self.quality=float(brokenSentence[6])
			self.altitude=float(brokenSentence[7])
			self.depth=float(brokenSentence[8])
			self.heading=float(brokenSentence[9])
			self.roll=float(brokenSentence[10])
			self.pitch=float(brokenSentence[11])

		elif(messageType=='$BFNVR'):
			self.message='NVR'
			self.eastRate=float(brokenSentence[2])
			self.northRate=float(brokenSentence[3])
			self.downRate=float(brokenSentence[4])
			self.pitchRate=float(brokenSentence[5])
			self.rollRate=float(brokenSentence[6])
			self.yawRate=float(brokenSentence[7])

		else:
			print("Message type undefined")

		return self


	def updateNav(self,timestamp,heading,depth,depthMode,thrust,speedMode,horizontalMode):
		return '$BPRMB,'+str(timestamp)+','+str(heading)+','+str(depth)+','+str(depthMode)+','+str(thrust)+','+str(speedMode)+','+str(horizontalMode)

