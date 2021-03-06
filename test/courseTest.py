import oldCoursesGraph
from scheduling import *

from DataHelper.loadData import DataLoading


def loadData(major, specs, specsFilename, courseFilename, useTaken, takenFilename, useAvoid, avoidFilename, widthFuncFilename):
	specsCourse, specsTable = DataLoading().loadSpec(
									major=major, specs=specs, filename=specsFilename)
	graph = oldCoursesGraph()
	DataLoading().loadCourses(graph, courseFilename)
	graph.loadSpecs(specsCourse)
	graph.updateSatisfies()
	widthFuncTable = DataLoading().loadWidthFuncTable(widthFuncFilename)
	defaultUnits = 0
	startQ = 0
	if useTaken:
		startQ, defaultUnits = DataLoading().loadTaken(graph, specsTable, takenFilename)
	if useAvoid:
		DataLoading().loadAvoid(graph, avoidFilename)

	return graph, specsTable, defaultUnits, startQ, widthFuncTable



def printResult(L, bestBound, startQ):
	print("start quarter: ", startQ)
	# print("Taking %d credits per quarter: " % (creditsPerQuarter))
	for i, level in enumerate(L):
		i = i + startQ
		print("code %d :"%(level))

	print("best upper bound:",bestBound )


if __name__ == '__main__':
	# creditsPerQuarter = 16
	# data loading
	## for Computer Science graph
	graph, specsTable, defaultUnits, startQ, widthFuncTable = loadData(
		major="test",
		specs=["firstReq","secondReq"],
		specsFilename="./test_spec.txt",
		courseFilename="./testcourses.txt",
		useTaken=False,
		takenFilename="info/test/taken.txt.txt",
		useAvoid=False,
		avoidFilename="info/test/avoid.txt",
		widthFuncFilename="./test_widthFunc.txt"
	)
	# scheduling
	L, bestBound = CourseScheduling(graph, specsTable, startQ, 3-defaultUnits, widthFuncTable).findBestSchedule(20)
	printResult(L, bestBound, startQ)


"""
start quarter:  0
Taking 16 credits per quarter:
year 1 quarter 1: ['I&CSCI31', 'MATH2A', 'I&CSCI6B', 'HISTORY40A']
year 1 quarter 2: ['I&CSCI32', 'MATH2B', 'I&CSCI51']
year 1 quarter 3: ['I&CSCI33', 'STATS67', 'I&CSCI6D', 'MATH3A']
year 2 quarter 1: ['I&CSCI45C', 'COMPSCI169', 'POLSCI21A', 'WRITINGLOW1']
year 2 quarter 2: ['I&CSCI46', 'COMPSCI178', 'HISTORY40B', 'GEII-1']
year 2 quarter 3: ['HISTORY40C', 'GEIII-1', 'GEIII-2', 'GEVI-1']
year 3 quarter 1: ['COMPSCI161', 'COMPSCI171', 'GEVII-1', 'GEVIII-1']
year 3 quarter 2: ['COMPSCI162', 'COMPSCI116', 'COMPSCI175', 'WRITINGLOW2']
year 3 quarter 3: ['COMPSCI163', 'COMPSCI177', 'COMPSCI165', 'IN4MATX43']
year 4 quarter 1: ['COMPSCI179', 'I&CSCI90', 'I&CSCI139W']
year 4 quarter 2: ['COMPSCI164', 'I&CSCI53+53L']
best upper bound: year 2 quarter 3
"""
