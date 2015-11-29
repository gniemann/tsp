#!/usr/bin/python

from __future__ import print_function
import math
import optparse


#using greedy algorithm

def loadCities(filename):
	input_file = open(filename, "r")
	cities = [map(int, line.split()) for line in input_file]
	input_file.close()
	
	return cities
	
def getDistance(p1, p2):
	return round(math.sqrt(pow((p2[0] - p1[0]), 2) + pow((p2[1] - p1[1]), 2)))
	
def getEdges(cities):
	edges = []
	for (city1, x1, y1) in cities:
		for (city2, x2, y2) in cities:
			if city1 != city2:
				edges.append((getDistance((x1, y1), (x2, y2)), city1, city2))
				
	edges.sort()
	
	return edges
	
def greedyTSP(cities):
	edges = getEdges(cities)
	
	cityDegrees = [0 for i in range(len(cities))]
	
	pathEdges = []
	pathLength = 0
	
	for i in range(len(cities)):
		(distance, city1, city2) = edges.pop(0)
		while cityDegrees[city1] > 1 or cityDegrees[city2] > 1:
			(distance, city1, city2) = edges.pop(0)
		
		# now have the shortest edge with the constraint that each city has no more than 2 edges
		cityDegrees[city1] += 1
		cityDegrees[city2] += 1
		pathEdges.append((city1, city2))
		pathLength += distance
		
	# have the edges, now construct the path
	(startingCity, curCity) = pathEdges.pop()
	path = [startingCity, curCity]
	
	while len(pathEdges) > 0:
		[nextEdge for nextEdge in pathEdges if curCity in nextEdge]
		pathEdges.remove(nextEdge)
		(city1, city2) = nextEdge
		if curCity == city1:
			curCity = city2
		else:
			curCity = city1
			
		path.append(curCity)
		
	return (pathLength, path)
		

	
if __name__ == "__main__":
	p = optparse.OptionParser()
	
	opts, args = p.parse_args()
	
	cities = loadCities(args[0])
		
	(distance, path) = greedyTSP(cities)

	output_file = open(args[0] + ".path", "w")
	print(distance)
	for city in path:
		print(city)
