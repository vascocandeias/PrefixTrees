from Node import Node
 
def PrefixTree(filename):
	f = open(filename)
	lines = f.read().splitlines()
	tree = Node()
	for x in lines:
		InsertPrefix(tree, *x.split())
	f.close()
	return tree

def PrintTable(tree):
	if tree is None:
		return

	queue = []
	queue.append((tree, ""))
	while queue:
		node, path = queue.pop(0)
		nexthop = node.getNexthop()
		if nexthop is not None:
			if path is "":
				if nexthop is not "drop":
					print("e " + nexthop)
			else:
				print(path + " " + nexthop)
		for i in range(2):
			if node.getChild(i) is not None:
				queue.append((node.getChild(i), path+str(i)))
	
def LookUp(tree, prefix):
	prefix = prefix.lstrip("e")
	nexthop = tree.nexthop
	node = tree

	for c in prefix:
		aux = int(c)
		if node.getChild(aux) is None:
			break
		node = node.getChild(aux)
		if node.nexthop is not None:
			nexthop = node.getNexthop()

	return nexthop

def InsertPrefix(tree, prefix, nexthop):
	prefix = prefix.lstrip("e")
	node = tree

	for c in prefix:
		aux = int(c)
		if node.getChild(aux) is None:
			node.addChild(aux)
		node = node.getChild(aux)

	node.setNexthop(nexthop)
	return tree

def DeletePrefix(tree, prefix):
	if prefix is "e":
		tree.setNexthop(None)
		return tree

	tree.deletePath(prefix.lstrip("e"))

	return tree

def CompressTree(tree):
	if tree is not None:
		tree.recursiveCompression(None)
	return tree

def OptimalCompress(tree):
	if tree is None:
		return

	if tree.getNexthop is None:
		tree.setNexthop("drop")
		
	tree.ORTCStep1([tree.nexthop])
	tree.ORTCStep2(None)

	if tree.getNexthop() is "drop":
		tree.setNexthop(None)
	return tree