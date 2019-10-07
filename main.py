import sys
from Node import Node
from Tree import PrefixTree, PrintTable, LookUp, InsertPrefix, DeletePrefix, CompressTree, OptimalCompress, Backup
from IOFunctions import checkPrefix, read

try:
	tree = PrefixTree(sys.argv[1])
except Exception as e:
	print("There was an error opening the file. Starting with a blank table...")
	tree = Node()

backup = None

while(1):
	print()
	print("Options:")
	print("\t0) Print table")
	print("\t1) Table look up")
	print("\t2) Insert entry")
	print("\t3) Delete entry")
	print("\t4) Compress table")
	print("\t5) Compress ORTC")
	print("\t6) Print tree")
	print("\t7) Quit")
	val = read("\n> ")
	print()

	if val in {"4", "5"}:
		try:
			Backup(tree)
			backup = PrefixTree("backup.txt")
		except:
			print("There was an error backing up the table")
	
	if val is "0":
		print("Prefix Table")
		PrintTable(tree)
		
	elif val is "1":
		prefix = read("Prefix: ")
		if not checkPrefix(prefix):
			continue
		nexthop = LookUp(tree, prefix)
		if nexthop not in {None, "drop"}:
			print("Next hop: " + nexthop)
		else:
			print("Packet dropped")
			
	elif val is "2":
		prefix = read("Prefix: ")
		if not checkPrefix(prefix):
			continue
		nexthop = read("Next hop: ")
		if nexthop is "drop":
			print("drop is not a valid next hop")
			continue
		if backup is not None:
			tree = backup
			backup = None
		tree = InsertPrefix(tree, prefix, nexthop)
		
	elif val is "3":
		prefix = read("Prefix: ")
		if not checkPrefix(prefix):
			continue
		if backup is not None:
			tree = backup
			backup = None
		tree = DeletePrefix(tree, prefix)
		
	elif val is "4":
		tree = CompressTree(tree)
		
	elif val is "5":
		tree = OptimalCompress(tree)

	elif val is "6":
		tree.display()

	elif val is "7":
		break

	else:
		print("Try again")