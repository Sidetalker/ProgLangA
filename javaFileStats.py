from os import listdir, getcwd
from os.path import isfile, isdir, join, dirname, getsize

# Retrieve basic statistics of the given java file
def getJavaStats(javaFile):
	# Open the java file for reading
	f = open(javaFile, 'r')
	multiCommentFlag = False
	singleCommentFlag = False

	# Track stats and get the filesize
	stats = [0 for x in range(5)]
	stats[0] = getsize(javaFile)

	# Scan through the file line by line
	for line in f:
		# Reset the single line comment flag
		singleCommentFlag = False

		# Pad the line for easier traversal
		letterCount = range(len(line))
		line += '       '

		# Scan through the line letter by letter
		# NOTE: This is probably not necessary but
		# avoids at least one corner case
		for i in letterCount:
			# Check for comment initiation/end
			if line[i:i+2] == '/*':
				multiCommentFlag = True
			if line[i:i+2] == '*/':
				multiCommentFlag = False
			if line[i:i+2] == '//':
				singleCommentFlag = True

			# Next letter if we're in a comment
			if multiCommentFlag or singleCommentFlag:
				continue

			# Check for public/private/try/catch
			if line[i:i+6] == 'public':
				stats[1] += 1
			if line[i:i+7] == 'private':
				stats[2] += 1
			if line[i:i+3] == 'try':
				stats[3] += 1
			if line[i:i+5] == 'catch':
				stats[4] += 1

	# Always close your file boys and girls
	f.close()

	return stats


# Maintain statistics for a single directory
class DirStat():
	def __init__(self, path):
		self.path = path
		self.subdirectories = []
		self.files = []
		self.totalSize = 0
		self.publicCount = 0
		self.privateCount = 0
		self.tryCount = 0
		self.catchCount = 0

	# Add a file to the statistics
	def addFile(self, path):
		self.files.append(path)

	# Add a subdirectory to the stats
	def addSubdir(self, path):
		self.subdirectories.append(path)

	# Import stats from another DirStat
	def importStats(self, stats):
		self.totalSize += stats[0]
		self.publicCount += stats[1]
		self.privateCount += stats[2]
		self.tryCount += stats[3]
		self.catchCount += stats[4]

	# This function will obtain stats from all
	# java files and distribute them among enclosing files
	def distributeStats(self, allStats):
		# Loop through all files
		for f in self.files:
			# Get and apply the statistics
			stats = getJavaStats(f)
			self.importStats(stats)

			# Let the stats flow down the tree
			for d in self.subdirectories:
				statSearch = [x for x in allStats if x.path == d]
				statSearch[0].importStats(stats)

	# Pretty print yourself
	def pprint(self):
		print("%s\nBytes: %d\nPublics: %d\nPrivates: %d\nTrys: %d\nCatches: %d\n" % 
			 (self.path, self.totalSize, self.publicCount, self.privateCount, self.tryCount, self.catchCount))

		print("Parents: %s\n" % '\n'.join(self.subdirectories))

		#print("DirStat:\n\tPath: %s\n\t\tSubdirs: %s\n\t\t Files: %s\n" % (self.path, '\n'.join(self.subdirectories), '\n'.join(self.files)))


# Scan all directories down from root and return list
def scanDirectories(curDir, fullList):
	# Obtain all .java files and directories in the current dir
	files = [join(curDir, f) for f in listdir(curDir) if (isfile(join(curDir,f)) and f[-5:] == '.java')]
	directories = [join(curDir, d) for d in listdir(curDir) if isdir(join(curDir,d))]
	
	# Recurse into all directories and add them to the list
	for d in directories:
		curPath = d
		fullList.append(DirStat(d))

		# Add each parent directory this subdirectory is part of
		while curPath != fullList[0].path:
			fullList[-1].addSubdir(dirname(curPath))

		# Add each file to the list
		for f in files:
			fullList[-1].addFile(f)

		# Recurse
		scanDirectories(d, fullList)

	return fullList


# Main Function
if __name__ == '__main__':
	# Obtain a list of DirStats for each directory
	stats = scanDirectories(getcwd(), [DirStat(getcwd())])

	# Distribute the obtained stats to all parent directories
	for s in stats:
		s.distributeStats(stats)

	# Print all the data
	for s in stats:
		s.pprint()

	# Make sure the numbers add up
	verification = [0 for x in range(5)]

	for i in range(1, len(stats)):
		verification[0] += stats[i].totalSize
		verification[1] += stats[i].publicCount
		verification[2] += stats[i].privateCount
		verification[3] += stats[i].tryCount
		verification[4] += stats[i].catchCount

	if verification[0] != stats[0].totalSize:
		print("Mismatch! Total %d, found %d\n" % (stats[0].totalSize, verification[0]))

	if verification[1] != stats[0].publicCount:
		print("Mismatch! Total %d, found %d\n" % (stats[0].publicCount, verification[1]))

	if verification[2] != stats[0].privateCount:
		print("Mismatch! Total %d, found %d\n" % (stats[0].privateCount, verification[2]))

	if verification[3] != stats[0].tryCount:
		print("Mismatch! Total %d, found %d\n" % (stats[0].tryCount, verification[3]))

	if verification[4] != stats[0].catchCount:
		print("Mismatch! Total %d, found %d\n" % (stats[0].catchCount, verification[4]))





	