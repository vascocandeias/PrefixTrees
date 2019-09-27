from Node import Node
 
def ImportTree(filename):
	f=open(filename)
	lines=f.read().splitlines()
	tree=Node(None)
	for x in lines:
		InsertPrefix(tree, *x.split())
	return tree

def PrintTable(node, path):
	#TODO verificar se pode ser esta a ordem de apresentação 
	if node.nexthop is not None:
		if path is "":
			print("e " + node.nexthop)
		else:
			print(path + " " + node.nexthop)
	for i in range(2):
		if node.child[i] is not None:
			PrintTable(node.child[i], path+str(i))
	
def Lookup(tree, prefix):
	nexthop = tree.nexthop
	node = tree

	for c in prefix:
		if node.child[int(c)] is None:
			break
		node=node.child[int(c)]
		if node.nexthop is not None:
			nexthop = node.nexthop

	return nexthop

def InsertPrefix(tree, prefix, nexthop):

	prefix = prefix.lstrip("e")

	node=tree

	for p in prefix:
		aux = int(p)
		if node.child[aux] is None:
			node.addChild(aux, Node(node))
		node=node.child[aux]

	node.setNexthop(nexthop)

def DeletePrefix(tree, prefix):
	node = tree

	prefix = prefix.lstrip("e")

	for c in prefix:
		if node.child[int(c)] is None: #caso o caminho não exista
			return False
		node=node.child[int(c)]
	
	if node.nexthop is None:
		return False #caso a entrada nao exista

	node.nexthop=None
	while (node.nexthop is None) and (node.child[0] is None) and (node.child[1] is None):
		node = node.removeNode()
	return True

def CompressTree():
	return