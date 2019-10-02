import sys
from Node import Node
from Tree import ImportTree, PrintTable, Lookup, InsertPrefix, DeletePrefix, CompressTree, OptimalCompression
from IOFunctions import checkPrefix, read


#tree=ImportTree(sys.argv[1])
try:
	tree = ImportTree("inputfile.txt")
except Exception as e:
	print(e)
	print("There was an error opening the file. Starting with a blank table...")
	tree = Node(None)

while(1):
	print("\n")
	print("Options:")
	print("\t0) Print table")
	print("\t1) Table look up")
	print("\t2) Insert entry")
	print("\t3) Delete entry")
	print("\t4) Compress table")
	print("\t5) Compress ORTC")
	print("\t6) Print tree")
	print("\t7) Quit")
	val = int(read("\n> "))
	print("\n")
	
	if val is 0:
		print("Prefix Table")
		PrintTable(tree, "")
		
	elif val is 1:
		prefix = read("Prefix: ")
		if not checkPrefix(prefix):
			continue
		nexthop = Lookup(tree,prefix)
		if nexthop is not None:
			print("Next hop: " + nexthop)
		else:
			print("Packet dropped")
			
	elif val is 2:
		prefix = read("Prefix: ")
		if not checkPrefix(prefix):
			continue
		nexthop = read("Next hop: ")
		tree = InsertPrefix(tree, prefix, nexthop)
		
	elif val is 3:
		prefix = read("Prefix: ")
		if not checkPrefix(prefix):
			continue
		tree = DeletePrefix(tree, prefix)
		
	elif val is 4:
		CompressTree(tree)
		
	elif val is 6:
		tree.display()
	
	elif val is 5:
		tree = OptimalCompression(tree)

	elif val is 7:
		break

	else:
		print("Try again")