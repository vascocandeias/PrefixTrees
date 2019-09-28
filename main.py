import sys
from Tree import ImportTree, PrintTable, Lookup, InsertPrefix, DeletePrefix, CompressTree
from IOFunctions import checkPrefix, read


#tree=ImportTree(sys.argv[1])
try:
	tree = ImportTree("inputfile.txt")
except:
	print("There was an error opening the file. Starting with a blank table...")

while(1):
	print("\n")
	print("Options:")
	print("\t0) Print table")
	print("\t1) Table look up")
	print("\t2) Insert entry")
	print("\t3) Delete entry")
	print("\t4) Compress table")
	print("\t5) Print tree")
	print("\t6) Quit")
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
		
	elif val is 5:
		tree.display()
		
	elif val is 6:
		break

	else:
		print("Try again")