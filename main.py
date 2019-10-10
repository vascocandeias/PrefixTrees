# ADRC - Project 1
# Main function
#
# by: Sofia Estrela (84186)
#     Vasco Candeias (84196)
#
# 18 October 2019
#
###############################

# import from the other files of this project
import sys
from Node import Node
from Tree import PrefixTree, PrintTable, LookUp, InsertPrefix, DeletePrefix, CompressTree, OptimalCompress, Backup
from IOFunctions import checkPrefix, read

# verifies if there is an input file in the arguments
try:
	tree = PrefixTree(sys.argv[1])
except Exception as e:
	print("There was an error opening the file. Starting with a blank table...")
	tree = Node()

backup = None

# Menu printing and get the user input
while(1):
	print()
	print("Options:")
	print("\t0) Print table")
	print("\t1) Table look up")
	print("\t2) Insert entry")
	print("\t3) Delete entry")
	print("\t4) Simple compression")
	print("\t5) Optimal compression")
	print("\t6) Print tree")
	print("\t7) Quit")
	val = read("\n> ")
	print()

	# in case of choosing one type of compression, create a backup tree
	if val in {"4", "5"} and backup is None:
		try:
			Backup(tree)
			backup = PrefixTree("backup.txt")
		except:
			print("There was an error backing up the table")
	
	# when the user wants to print a table
	if val == "0":
		print("Prefix Table")
		PrintTable(tree)
		
	# when the user wants to look up an IP/prefix
	elif val == "1":
		# IP input reading and check if valid
		ip = read("IP: ")
		if not checkPrefix(ip):
			continue
		# look up the ip to get the next hop
		nexthop = LookUp(tree, ip)
		if nexthop not in {None, "drop"}:
			print("Next hop: " + nexthop)
		else:
			print("Packet dropped")
	
	# in case the user wants to input a new prefix rule		
	elif val == "2":
		# get the value from user and validate it
		prefix = read("Prefix: ")
		if not checkPrefix(prefix):
			continue
		# get the next hop value and validate it
		nexthop = read("Next hop: ")
		if nexthop == "drop":
			print("drop is not a valid next hop")
			continue
		# get the tree from the backup in case it was compressed before
		if backup is not None:
			tree = backup
			backup = None
		# insert the prefix
		tree = InsertPrefix(tree, prefix, nexthop)
		
	
	# when the client wants to delete a prefix rule
	elif val == "3":
		# gets and verifies the prefix from the user
		prefix = read("Prefix: ")
		if not checkPrefix(prefix):
			continue
		# gets the backup tree in case the tree was compressed before
		if backup is not None:
			tree = backup
			backup = None
		# delete prefix
		tree = DeletePrefix(tree, prefix)
	
	# when the user wants to compress the tree (filter and agregation)
	elif val == "4":
		tree = CompressTree(tree)
	
	# when the user wants to compress the tree (ortc method)	
	elif val == "5":
		tree = OptimalCompress(tree)

	# if the user wants to print the tree in the screen
	elif val == "6":
		tree.display()

	# when the user wants to exit the program
	elif val == "7":
		break

	# in the option is not valid
	else:
		print("Try again")