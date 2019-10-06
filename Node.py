class Node:
	
	def __init__(self):
		self.child = [None] * 2
		self.nexthop = None

	def addChild(self, num):
		self.child[num] = Node()

	def getChild(self, num):
		if num in {0,1}:
			return self.child[num]
		else:
			return None

	def setNexthop(self, nexthop):
		self.nexthop = nexthop

	def getNexthop(self):
		return self.nexthop

	def deletePath(self, prefix):
		"""Recursive method to delete a prefix and the path from the root to that node"""

		# if this is the node to delete, set its nexthop to None to clear the entry
		if prefix is "":
			self.nexthop = None
		else:
			# otherwise continue down the path
			bit = int(prefix[0])
			rest = prefix[1:]

			# if the prefix doesn't exist, abort
			if self.child[bit] is None:
				return False
			# otherwise go down the path
			elif self.child[bit].deletePath(rest):
				# if the deletition returns True, the child should be deleted
				self.child[bit] = None

		# return whether the node is now a leaf. if it is, it should be deleted
		return self.nexthop is None and all(x is None for x in self.child)

	def recursiveCompression(self, nexthop):
		"""Compress the tree using only aggregation and filtering"""

		# aggregation: if both children have the same nexthop, use it as the parent's nexthop 
		if all(x is not None for x in self.child) and self.child[0].nexthop is self.child[1].nexthop and self.child[0].nexthop is not None:
			self.nexthop = self.child[0].nexthop	

		# filtering: if this node's nexthop is redundant, remove it
		if self.nexthop is nexthop:
			self.nexthop = None
		elif self.nexthop is not None:
			nexthop = self.nexthop

		# apply the algorithm to both children
		for i in range(2):
			if self.child[i] is not None:
				if self.child[i].recursiveCompression(nexthop):
					# if the child is an empty leaf, delete it
					self.child[i] = None

		# if this is an empty leaf, return true to be deleted
		if self.nexthop is None and all(x is None for x in self.child):
			return True

		return False

	def ORTCStep1(self, nexthop):
		"""Applies the first step of the ORTC algorithm"""

		# if a node has no nexthop, it inherits his parent's
		if self.nexthop is None:
			self.nexthop = nexthop
		else:
			# otherwise turn the value into a list
			self.nexthop = [self.nexthop]

		# if the node only has one child, create the other
		for i in range(2):
			if self.child[i] is None and self.child[not i] is not None:
				self.child[i] = Node()
			# if the node is not a leaf, apply the algorithm to its children
			if self.child[i] is not None:
				self.child[i].ORTCStep1(self.nexthop)

		# if the node is a leaf, do nothing
		if self.child[0] is None:
			return

		# otherwise nexthop is the # of the childrens' nexthops
		intersect = self.intersection()
		if intersect:
			self.nexthop = intersect
		else:
			self.nexthop = self.child[0].nexthop + self.child[1].nexthop

	def intersection(self): 
		"""Returns a list containing the intersection of two lists"""
		return list(set(self.child[0].nexthop) & set(self.child[1].nexthop)) 

	def ORTCStep2(self, nexthop):
		"""Applies the final step of the ORTC algorithm"""

		# clear redundant nexthops
		if nexthop in self.nexthop:
			self.nexthop = None
		else:
			# otherwise choose the first of the list
			self.nexthop = self.nexthop[0]
			nexthop = self.nexthop

		# apply thw algoritm to both children
		for i in range(2):
			if self.child[i] is not None:
				if self.child[i].ORTCStep2(nexthop):
					# remove the child if it is an empty leaf
					self.child[i] = None

		# if the node is an empty leaf, signal its deletition
		if self.nexthop is None and all(x is None for x in self.child):
			return True

		# otherwise, don't delete
		return False

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