#!/usr/bin/python

from __future__ import print_function
import math
import optparse
import random


class Point:
	'''This is a simple class which defines a point in 2D space
	It has two member functions which determine distance between two points'''
	def __init__(self, x, y):
		self.x = x
		self.y = y
	
	def getRelativeDistance(self, p2):
		'''Gets the relative distance between two points, useful only for comparing distances'''
		return pow(p2.x - self.x, 2) + pow(p2.y - self.y, 2)
		
	def getDistance(self, p2):
		'''Gets the actual distance between two points'''
		return int(round(math.sqrt(self.getRelativeDistance(p2))))

def loadCities(filename):
	input_file = open(filename, "r")
	cities = []
	for line in input_file:
		city, x, y = map(int, line.split())
		cities.append(Point(x, y))
		
	input_file.close()
	
	return cities
	

def getNextCity(curCity, cities, remainingCities):
	'''
	Iterate through the remaining cities, determine the relative distance between each
	And the current city. Select the smallest relative distance and return that city
	and the actual distance between the two
	'''
	
	minRelDistance = float('inf')
	closestCity = -1
	for otherCity in remainingCities:
		relDistance = cities[curCity].getRelativeDistance(cities[otherCity])
		if relDistance < minRelDistance:
			minRelDistance = relDistance
			closestCity = otherCity
			
	return (closestCity, cities[curCity].getDistance(cities[closestCity]))
		
def nearestNeighborTSP(cities, startingCity):
	'''
	Uses the Nearest Neighbor heuristic to find a path through all the cities,
	starting from the startingCity. Returns a 2-tuple of the length of the path
	and the path taken
	'''
	pathLength = 0
	path = []
	
	remainingCities = range(len(cities))
	
	path.append(startingCity)
	remainingCities.remove(startingCity)
	
	curCity = startingCity
	
	while len(remainingCities) > 0:
		(closestNeighbor, distance) = getNextCity(curCity, cities, remainingCities)

		pathLength += distance
		remainingCities.remove(closestNeighbor)
		path.append(closestNeighbor)
		curCity = closestNeighbor
		
	#add the last leg from the last city back to the first
	pathLength += cities[startingCity].getDistance(cities[curCity])
		
	return (int(pathLength), path)
	
def repeatitiveNearestNeighborTSP(cities):
	'''
	Runs the nearest neighbor algorithm on cities, starting from each city
	Selects the path (of the N tried) with the shortest path
	'''
	shortestPath = []
	shortestPathLength = float('inf')
	
	for startingCity in range(len(cities)):
		(distance, path) = nearestNeighborTSP(cities, startingCity)
		if (distance < shortestPathLength):
			shortestPath = path
			shortestPathLength = distance
			
	return (shortestPathLength, shortestPath)
	
def randomNearestNeighbor(cities):
	'''
	Runs the nearest neighbor on cities, starting from a random city
	'''
	startingCity = random.randint(0, len(cities))
	return nearestNeighborTSP(cities, startingCity)

def twoopt(cities, tour, distance):
	path = tour
	length = distance
	for i in range(1, len(path) - 2):
		for k in range(i + 1, len(path)-2):
			#city1 = i-1
			city1 = cities[path[i-1]]
			#city2 = i
			city2 = cities[path[i]]
			#city3 = k
			city3 = cities[path[k]]
			#city4 = k + 1
			city4 = cities[path[k+1]]
			if ((city1.getRelativeDistance(city2) + city3.getRelativeDistance(city4)) > (city1.getRelativeDistance(city3) + city2.getRelativeDistance(city4))):
				if ((city1.getDistance(city2) + city3.getDistance(city4)) > (city1.getDistance(city3) + city2.getDistance(city4))):
					#subtract the original distance and add the new distance
					length -= ((city1.getDistance(city2) + city3.getDistance(city4)) - (city1.getDistance(city3) + city2.getDistance(city4)))

					newPath = path[0:i]
					newPath += path[k:i-1:-1]
					newPath += path[k+1:]
					return twoopt(cities, newPath, length)
						
	return (length, path)

if __name__ == "__main__":
	p = optparse.OptionParser()
	
	opts, args = p.parse_args()
	
	cities = loadCities(args[0])
	
	#random.seed()
		
	(distance, path) = randomNearestNeighbor(cities)
	print("Distance with random nearest neighbor: ", distance)
	
	(distance, path) = twoopt(cities, path, distance)
	print("Distance after 2-opt", distance)

	output_file = open(args[0] + ".path", "w")
	print(distance, file=output_file)
	for city in path:
		print(city, file=output_file)
