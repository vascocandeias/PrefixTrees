import sys
from Tree import (ImportTree, PrintTable, Lookup, InsertPrefix, DeletePrefix, CompressTree)
 
#tree=ImportTree(sys.argv[1])
tree=ImportTree("inputfile.txt")
print("Sofia & Vasco - ADRC")

while(1):
	print("\n")
	print("Options:")
	print("\t0) Print table")
	print("\t1) Table look up")
	print("\t2) Insert entry")
	print("\t3) Delete entry")
	print("\t4) Compress table")
	print("\t5) Quit")
	val = int(input("\n> "))
	print("\n")
	if val is 0:
		print("Prefix Table")
		PrintTable(tree, "")
	elif val is 1:
		prefix = input("Prefix: ")
		nexthop = Lookup(tree,prefix)
		if nexthop is not None:
			print("Next hop: " + nexthop)
		else:
			print("Packet dropped")
	elif val is 2:
		prefix = input("Prefix: ")
		nexthop = input("Next hop: ")
		InsertPrefix(tree, prefix, nexthop)
	elif val is 3:
		prefix = input("Prefix: ")
		DeletePrefix(tree, prefix)
	elif val is 4:
		CompressTree()
	elif val is 5:
		break
	else:
		print("Try again")