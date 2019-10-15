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
		# check if it has 16 bits or less
		if len(prefix) > 16:
			raise ValueError()
	except ValueError:
		print("This prefix is not valid: " + prefix)
		return False
	return True

def checkIP(ip):
	"""Validation of the IP """

	try:
		# check if the string is a binary number
		int(ip, 2)
		# check if it has 16 bits
		if len(ip) != 16:
			raise ValueError()
	except ValueError:
		print("This IP is not valid: " + ip)
		return False
	return True