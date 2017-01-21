from datetime import time

"""
a course will have the name, teaching time(start time, end time),
the quarter it will be offered, its units, prerequisite, and the courses that it may partially satisfy their prerequisites
it is assumed that it will be offered at the same quarter for every year

for weekday: 1-5: represents Mon-Fri
for quarter: 1-3: represents Fall-Spring

I should also show the AND/OR relationship in prereq
cs 161 prereq:
( I&C SCI 23 ( min grade = C ) OR CSE 23 ( min grade = C ) OR I&C SCI H23 ( min grade = C ) OR I&C SCI 46 ( min grade = C ) OR CSE 46 ( min grade = C ) )
AND
I&C SCI 6B
AND
I&C SCI 6D
AND
( MATH 2B OR AP CALCULUS BC ( min score = 4 ) )
some courses, such as AP xxx, if they are not in the courses list, we can simply ignore it
when we are scheduling



Some thoughts:
1. What about the discussion/lab class? should I ignore the time conflict at the current stage?
2. I think currently I may only focus on:
 a. the quarter they are offered,
 b. prereq relationship,
 c. units
"""


class Course:
    def __init__(self, units, quarter, prereq=None, satisfy=None,
                 startTime=None, endTime=None, weekdays=None):
        self.quarter = quarter
        self.units = units
        self.prereq = prereq if prereq else []
        self.satisfy = satisfy if satisfy else set()
        self.startTime = startTime
        self.endTime = endTime
        self.weekdays = weekdays

    def __str__(self):
        return "units: {units}\n" \
               "quarters: {quar}\n" \
               "prereq: {prereq}\n" \
               "satisfy: {sat}".format(
            units=self.units, quar=self.quarter, prereq=self.prereq, sat=self.satisfy)

    def addPrereq(self, prereq):
        self.prereq.append(prereq)

    def addSatisfy(self, satisfy):
        self.satisfy.add(satisfy)

    def getPrereq(self):
        return self.prereq

    def hasPrereq(self):
        return len(self.prereq) != 0

    def getSatisfy(self):
        return self.satisfy

    def delPrereq(self, name):
        for pset in self.prereq:
            if name in pset:
                self.prereq.remove(pset)
        return True if not self.prereq else False

    def conflict(self, course):
        """time conflict of two courses"""
        return True


class CoursesGraph:
    def __init__(self, adjList=None):
        self.adjList = adjList if adjList else dict()

    def __str__(self):
        return "\n".join(
            "{name}: \n{course}".format(name=name, course=course) for name, course in self.adjList.items()) + "\n"
    def __contains__(self, item):
        return item in self.adjList

    def loadFromExcel(self, fileName):
        pass

    def addCourse(self, name, course):
        """
        add vertex
        """
        if name not in self.adjList:
            self.adjList[name] = course
            return True
        return False

    def delCourse(self, name):
        return self.adjList.pop(name)

    def addCourses(self, courses):
        """
        add vertices
        courses is an adjList
        """
        for name, course in courses.items():
            self.addCourse(name, course)

    def addPrereq(self, name, prereqSet):
        """
        this could only be called after all courses are added into the adjList.
        add edge
        a prereqSet is like: {"I&C SCI 45C", "I&C SCI 45J"}
        """
        if name in self.adjList:
            self.adjList[name].addPrereq(prereqSet)
            return True
        return False

    def updateSatisfies(self):
        for name, course in self.adjList.items():
            for preq in course.getPrereq():
                for sat in preq:
                    if sat in self.adjList:
                        self.adjList[sat].addSatisfy(name)

    def getCourses(self):
        """
        :return: a list of course names
        """
        return self.adjList.items()

    def getCourse(self, name):
        return self.adjList.get(name)

    def getCoursePrereqs(self, name):
        if name in self.adjList:
            return self.adjList[name].getPrereq()
        return None

    def getCourseSatisfies(self, name):
        if name in self.adjList:
            return self.adjList[name].getSatisfy()
        return None


if __name__ == "__main__":
    # SampleAdjList = {"COMPSCI 161": Course(quarter=[1, 2, 3],
    #                                        units=4.0,
    #                                        startTime=time(11, 00),
    #                                        endTime=time(11, 50),
    #                                        weekdays=[1, 3, 5],
    #                                        prereq=[{"I&C SCI 23", "CSE 23", "I&C SCI H23", "I&C SCI 46", "CSE 46"},
    #                                                {"I&C SCI 6B"}, {"I&C SCI 6D"},
    #                                                {"MATH 2B", "AP CALCULUS BC"}]),
    #                  "I&C SCI 46": Course(quarter=[1, 2, 3],
    #                                       units=4.0,
    #                                       startTime=time(10, 00),
    #                                       endTime=time(11, 20),
    #                                       weekdays={2, 4},
    #                                       prereq=[{"I&C SCI 45C", "I&C SCI 45J"}],
    #                                       satisfy={"COMPSCI 161"})
    #                  }
    adjList = {
        "a": Course(units=4.0, quarter=[1], prereq=[]),
        "b": Course(units=4.0, quarter=[2], prereq=[{"a"}]),
        "c": Course(units=2.0, quarter=[2, 3], prereq=[{"b"}]),
        "d": Course(units=1.5, quarter=[2, 3], prereq=[{"a", "c"}, {"k"}, {"e"}]),  # k is not in the adjList
        "e": Course(units=3.5, quarter=[2, 3], prereq=[])
    }
    graph = CoursesGraph(adjList)
    # print(graph)
    graph.updateSatisfies()
    print(graph)

"""
expected output form for course schedule:
[["a", "e"], ["b","c"],["d"]]
"""