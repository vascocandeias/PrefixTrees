from Node import Node
from collections import deque
from IOFunctions import checkPrefix
 
def PrefixTree(filename):
	"""Opens the input file, reads it and creates the tree based on the information contained"""

	f = open(filename)
	lines = f.read().splitlines()
	tree = Node()
	for x in lines:
		if not checkPrefix(x.split()[0]):
			f.close()
			raise Exception
		InsertPrefix(tree, *x.split())
	f.close()
	return tree

def PrintTable(tree):
	"""Using a Breadth First Search, print the table from the prefix tree"""
	if tree is None:
		return

	# create a FIFO queue
	queue = deque()
	queue.append((tree, ""))
	while queue:
		node, path = queue.popleft()
		nexthop = node.getNexthop()
		if nexthop is not None:
			if path == "":
				print("e " + nexthop)
			else:
				print(path + " " + nexthop)

		for i in range(2):
			if node.getChild(i) is not None:
				queue.append((node.getChild(i), path + str(i)))

def Backup(tree):
	"""Using a Breadth First Search, saves the table from the prefix tree in a file"""

	if tree is None:
		return

	f = open("backup.txt", "w")

	# create a FIFO queue
	queue = deque()
	queue.append((tree, ""))
	while queue:
		node, path = queue.popleft()
		nexthop = node.getNexthop()
		if nexthop is not None:
			if path == "":
				if nexthop is not "drop":
					f.write("e " + nexthop + "\n")
			else:
				f.write(path + " " + nexthop + "\n")
		for i in range(2):
			if node.getChild(i) is not None:
				queue.append((node.getChild(i), path + str(i)))
	f.close()

def LookUp(tree, prefix):
	"""By reading each bit from a given prefix, search in the prefix tree for the next hop value """

	prefix = prefix.lstrip("e")
	nexthop = tree.nexthop
	node = tree

	# for each bit in the prefix
	for c in prefix:
		aux = int(c)
		# finish the search if end of the wanted node does not exist
		if node.getChild(aux) is None:
			break
		#continue to the next child, if tree continues
		node = node.getChild(aux)
		if node.nexthop is not None:
			nexthop = node.getNexthop()

	return nexthop

def InsertPrefix(tree, prefix, nexthop):
	"""Given a new entry on the routing table, add it to the prefix tree"""

	prefix = prefix.lstrip("e")
	node = tree

	# find the node to which the prefix refers to
	for c in prefix:
		aux = int(c)
		#if the tree has no more children, create it
		if node.getChild(aux) is None:
			node.addChild(aux)
		node = node.getChild(aux)
	# sets the given value for the next hop in the final node
	node.setNexthop(nexthop)
	return tree

def DeletePrefix(tree, prefix):
	"""Delete a given prefix from the prefix tree """

	# if the prefix is the tree's root, just delete the nexthop
	if prefix == "e":
		tree.setNexthop(None)
		return tree

	tree.deletePath(prefix)

	return tree

def CompressTree(tree):
	"""Compress the tree using aggregation and filtering """	

	if tree is not None:
		tree.recursiveCompression(None)
	return tree

def OptimalCompress(tree):
	"""Compress the tree using ORTC compression algorithm """

	if tree is None:
		return

	# insert a dummy drop nextnode if the root does not have one
	if tree.getNexthop() is None:
		tree.setNexthop("drop")
		
	tree.ORTCStep1([tree.getNexthop()])
	tree.ORTCStep2(None)

	# remove the dummy next hop if it remained in the root
	if tree.getNexthop() == "drop":
		tree.setNexthop(None)
		
	return tree