import os

# Scan all directories down from root and return list
def scanDirectories(curDir, fullList):
	# Obtain all files and directories in the current dir
	files = [f for f in os.listdir(curDir) if os.path.isfile(join(curDir,f))]
	directories = [d for d in os.listdir(curDir) if os.path.isdir(join(curDir,d))]

	# Add all files to our list
	for f in files:
		fullList.append(join(curDir, f))

	# Recurse into all directories
	for d in directories:
		scanDirectories(d, fullList)






# Main Function
if __name__ == '__main__':
	# Set up debug logging
	logging.basicConfig()
	logger = logging.getLogger('main')
	logger.setLevel(10)

	# Obtain a list of all file paths
	self.files = scanDirectories(os.getcwd(), [])

	print self.files