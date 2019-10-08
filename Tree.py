from Node import Node
 
def PrefixTree(filename):
	""" Opens the input file, reads it and creats the tree based on the information contained"""
	f = open(filename)
	lines = f.read().splitlines()
	tree = Node()
	for x in lines:
		InsertPrefix(tree, *x.split())
	f.close()
	return tree

def PrintTable(tree):
	""" Using a Breadth First Search graph, print the table from the prefix tree"""
	if tree is None:
		return

	queue = []
	queue.append((tree, ""))
	while queue:
		node, path = queue.pop(0)
		nexthop = node.getNexthop()
		if nexthop is not None:
			if path is "":
				print("e " + nexthop)
			else:
				print(path + " " + nexthop)

		for i in range(2):
			if node.getChild(i) is not None:
				queue.append((node.getChild(i), path+str(i)))

def Backup(tree):
	""" Using a Breadth First Search graph, saves in a file the table from the prefix tree """
	if tree is None:
		return

	f = open("backup.txt", "w")

	queue = []
	queue.append((tree, ""))
	while queue:
		node, path = queue.pop(0)
		nexthop = node.getNexthop()
		if nexthop is not None:
			if path is "":
				if nexthop is not "drop":
					f.write("e " + nexthop + "\n")
			else:
				f.write(path + " " + nexthop + "\n")
		for i in range(2):
			if node.getChild(i) is not None:
				queue.append((node.getChild(i), path+str(i)))
	f.close()

def LookUp(tree, prefix):
	"""  By reading each bit from a given prefix, search in the prefix tree for the "next hop" value """
	prefix = prefix.lstrip("e")
	nexthop = tree.nexthop
	node = tree

	# for each bit in the prefix
	for c in prefix:
		aux = int(c)
		#finish the search if end of the tree is reached
		if node.getChild(aux) is None:
			break
		#continue to the next child, if tree continues
		node = node.getChild(aux)
		if node.nexthop is not None:
			nexthop = node.getNexthop()

	return nexthop

def InsertPrefix(tree, prefix, nexthop):
	""" given a new entry on the routing table, add it to the prefix tree"""
	prefix = prefix.lstrip("e")
	node = tree

	# for each bit in the prefix
	for c in prefix:
		aux = int(c)
		#if the tree has no more children, creates it
		if node.getChild(aux) is None:
			node.addChild(aux)
		node = node.getChild(aux)
	# sets the given value for the next hop in the final node
	node.setNexthop(nexthop)
	return tree

def DeletePrefix(tree, prefix):
	""" delete a given prefix from the prefix tree """

	#if the prefix is the tree's root
	if prefix is "e":
		tree.setNexthop(None)
		return tree

	#if not
	tree.deletePath(prefix)

	return tree

def CompressTree(tree):
	
	if tree is not None:
		tree.recursiveCompression(None)
	return tree

def OptimalCompress(tree):
	if tree is None:
		return

	if tree.getNexthop() is None:
		tree.setNexthop("drop")
		
	tree.ORTCStep1([tree.nexthop])
	tree.ORTCStep2(None)

	if tree.getNexthop() is "drop":
		tree.setNexthop(None)
	return tree