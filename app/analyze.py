class frame_analyze():
	def __init__(self):
		pass

	def analyze(self,position,last_positon,delta,lenth):
		tmp=position-last_position
		if tmp < 2*delta and tmp >0:
			return True
		elif tmp < 0:
			if -tmp > 0.99*lenth
				return True
			else:
				return False