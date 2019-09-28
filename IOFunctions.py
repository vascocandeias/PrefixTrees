def read(command):
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
    if prefix is "e": return True

    try:
        int(prefix, 2)
    except ValueError :
        print("This prefix is not valid")
        return False
    return True