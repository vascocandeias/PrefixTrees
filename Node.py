class Node:
	
	def __init__(self, prev):
		self.prev=prev
		self.child=[None] * 2
		self.nexthop=None

	def addChild(self, num, child):
		self.child[num]=child

	def setNexthop(self, nexthop):
		self.nexthop=nexthop

	def removeNode(self):
		prev = self.prev
		if prev.child[0] is self:
			prev.child[0] = None
		else:
			prev.child[1] = None

		return prev