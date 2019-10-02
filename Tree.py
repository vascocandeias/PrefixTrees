from Node import Node
 
def ImportTree(filename):
	f = open(filename)
	lines = f.read().splitlines()
	tree = Node(None)
	for x in lines:
		InsertPrefix(tree, *x.split())
	return tree

def PrintTable(node, path):
	if node.nexthop is not None:
		if path is "":
			print("e " + node.nexthop)
		else:
			print(path + " " + node.nexthop)
	for i in range(2):
		if node.child[i] is not None:
			PrintTable(node.child[i], path+str(i))
	
def Lookup(tree, prefix):
	prefix = prefix.lstrip("e")
	nexthop = tree.nexthop
	node = tree

	for c in prefix:
		if node.child[int(c)] is None:
			break
		node = node.child[int(c)]
		if node.nexthop is not None:
			nexthop = node.nexthop

	return nexthop

def InsertPrefix(tree, prefix, nexthop):
	prefix = prefix.lstrip("e")
	node = tree

	for p in prefix:
		aux = int(p)
		if node.child[aux] is None:
			node.addChild(aux, Node(node))
		node = node.child[aux]

	node.setNexthop(nexthop)
	return tree

def DeletePrefix(tree, prefix):
	node = tree

	prefix = prefix.lstrip("e")

	for c in prefix:
		if node.child[int(c)] is None: #caso o caminho não exista
			return tree
		node = node.child[int(c)]
	
	if node.nexthop is None:
		return tree #caso a entrada nao exista

	node.deletePath()

	return tree

def CompressTree(tree):
	if tree is not None:
		recursiveCompression(tree, None)
	return tree

def recursiveCompression(node, nexthop):
	
	# takes care of aggregation
	if all(x is not None for x in node.child) and node.child[0].nexthop is node.child[1].nexthop:
		node.nexthop = node.child[0].nexthop	

	# takes care of filtering
	if node.nexthop is nexthop:
		node.deletePath()
	elif node.nexthop is not None:
		nexthop = node.nexthop

	for i in range(2):
		if node.child[i] is not None:
			recursiveCompression(node.child[i], nexthop)

def OptimalCompression(tree):
	tree.recursiveORTC([tree.nexthop])
	tree.nexthop = tree.nexthop[0]
	tree.step3(tree.nexthop)
	return tree