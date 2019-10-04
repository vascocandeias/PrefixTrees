class Node:
	
	def __init__(self, prev):
		self.prev = prev
		self.child = [None] * 2
		self.nexthop = None

	def addChild(self, num, child):
		self.child[num] = child

	def getChild(self, num):
		if num in {0,1}:
			return self.child[num]
		else:
			return None

	def setNexthop(self, nexthop):
		self.nexthop = nexthop

	def getNexthop(self):
		return self.nexthop

	def removeNode(self):
		prev = self.prev

		if prev is None:
			return None

		if prev.child[0] is self:
			prev.child[0] = None
		else:
			prev.child[1] = None

		return prev

	def deletePath(self):
		node = self
		self.nexthop = None
		while node is not None and node.nexthop is None and all(x is None for x in node.child):
			node = node.removeNode()

	def recursiveCompression(self, nexthop):
		# takes care of aggregation
		if all(x is not None for x in self.child) and self.child[0].nexthop is self.child[1].nexthop:
			self.nexthop = self.child[0].nexthop	

		# takes care of filtering
		if self.nexthop is nexthop:
			self.deletePath()
		elif self.nexthop is not None:
			nexthop = self.nexthop

		for i in range(2):
			if self.child[i] is not None:
				self.child[i].recursiveCompression(nexthop)

	def recursiveORTC(self, nexthop):
		if self.nexthop is None:
			self.nexthop = nexthop
		else:
			self.nexthop = [self.nexthop]

		for i in range(2):
			if self.child[i] is None and self.child[not i] is not None:
				self.child[i] = Node(self)
			if self.child[i] is not None:
				self.child[i].recursiveORTC(self.nexthop)

		if self.child[0] is None:
			return

		intersect = self.intersection()
		if intersect:
			self.nexthop = intersect
		else:
			self.nexthop = self.child[0].nexthop + self.child[1].nexthop

	def intersection(self): 
		return list(set(self.child[0].nexthop) & set(self.child[1].nexthop)) 

	def step3(self, nexthop):
		if self.prev is not None and nexthop in self.nexthop:
			self.deletePath()
		else:
			self.nexthop = self.nexthop[0]
			nexthop = self.nexthop

		for i in range(2):
			if self.child[i] is not None:
				self.child[i].step3(nexthop)

	def display(self):
		lines, _, _, _ = self._display_aux()
		for line in lines:
			print(line)

	def _display_aux(self):
		"""Returns list of strings, width, height, and horizontal coordinate of the root. REF: https://stackoverflow.com/questions/34012886/print-binary-tree-level-by-level-in-python"""

		# No child.
		if self.child[1] is None and self.child[0] is None:
			line = '%s' % self.nexthop
			width = len(line)
			height = 1
			middle = width // 2
			return [line], width, height, middle

		# Only left child.
		if self.child[1] is None:
			lines, n, p, x = self.child[0]._display_aux()
			s = '%s' % self.nexthop
			u = len(s)
			first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
			second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
			shifted_lines = [line + u * ' ' for line in lines]
			return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

		# Only right child.
		if self.child[0] is None:
			lines, n, p, x = self.child[1]._display_aux()
			s = '%s' % self.nexthop
			u = len(s)
			first_line = s + x * '_' + (n - x) * ' '
			second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
			shifted_lines = [u * ' ' + line for line in lines]
			return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

		# Two children.
		left, n, p, x = self.child[0]._display_aux()
		right, m, q, y = self.child[1]._display_aux()
		s = '%s' % self.nexthop
		u = len(s)
		first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
		second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
		if p < q:
			left += [n * ' '] * (q - p)
		elif q < p:
			right += [m * ' '] * (p - q)
		zipped_lines = zip(left, right)
		lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
		return lines, n + m + u, max(p, q) + 2, n + u // 2