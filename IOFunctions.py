def read(command):
	"""Gets the input value from the user"""
	userInput = None
	while userInput is None:
		try:
			userInput = input(command)
		except IOError :
			print("There was an error reading the value")
			continue
		except :
			print("\nSomething happened. Exiting...")
			exit()

	return userInput

def checkPrefix(prefix):
	"""Validation of the prefix """
	if prefix is "e":
		return True

	try:
		# check if the string is a binary number
		int(prefix, 2)
	except ValueError:
		print("This prefix is not valid")
		return False
	return True