#!/usr/bin/python

from __future__ import print_function
import math
import optparse

def loadCities(filename):
	input_file = open(filename, "r")
	cities = [map(int, line.split()) for line in input_file]
	input_file.close()
	
	return cities
	
def getDistance(p1, p2):
	return round(math.sqrt(pow((p2[0] - p1[0]), 2) + pow((p2[1] - p1[1]), 2)))
	
def getDistanceMatrix(cities):
	allDistances = {}
	for (city, x, y) in cities:
		distances = []
		for (otherCity, x2, y2) in cities:
			if city != otherCity:
				distances.append((getDistance((x, y), (x2, y2)), otherCity))
		distances.sort()
		allDistances[city] = distances
	
	return allDistances
	
def nearestNeighborTSP(cities, distances, startingCity):
	pathLength = 0
	path = []
	
	remainingCities = range(len(cities))
	
	path.append(startingCity)
	remainingCities.remove(startingCity)
	
	curCity = startingCity
	
	while len(remainingCities) > 0:
		# find closest un-used city
		i = 0
		while distances[curCity][i][1] not in remainingCities:
			i += 1
		
		closestNeighbor = distances[curCity][i][1]
		minDistance = distances[curCity][i][0]
				
		path.append(closestNeighbor)
		pathLength += minDistance
		remainingCities.remove(closestNeighbor)
		curCity = closestNeighbor
		
	return (int(pathLength), path)
	
def repativeNearestNeighborTSP(cities, distances):
	shortestPath = []
	shortestPathLength = float('inf')
	
	for startingCity in range(len(cities)):
		(distance, path) = nearestNeighborTSP(cities, distances, startingCity)
		if (distance < shortestPathLength):
			shortestPath = path
			shortestPathLength = distance
			
	return (shortestPathLength, shortestPath)
	
if __name__ == "__main__":
	p = optparse.OptionParser()
	
	opts, args = p.parse_args()
	
	cities = loadCities(args[0])
	
	distances = getDistanceMatrix(cities)
	
	(distance, path) = repativeNearestNeighborTSP(cities, distances)

	output_file = open(args[0] + ".path", "w")
	print(distance)
	for city in path:
		print(city)
