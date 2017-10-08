#player class
class Player:

	def __init__(self, name, stats):
		self.name = name
		self.stat_tensor = stats

	def __str__(self):
		return 'This is {}'.format(self.name)

	def getStats(self):
		return self.stat_tensor

	def getName(self):
		return self.name