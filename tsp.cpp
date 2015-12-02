
#include <fstream>
#include <iostream>
#include <cmath>
#include <vector>
#include <string>
#include <algorithm>
#include <cstdlib>
#include <ctime>

using namespace std;

class Point
{
	public:
		Point(int x, int y);
		int getRelativeDistance(const Point &p2) const;
		int getDistance(const Point &p2) const;
		int getX() const { return x; }
		int getY() const { return y; }
	private:
		int x, y;
};

Point::Point(int x, int y)
:x(x), y(y)
{
}

int Point::getRelativeDistance(const Point &p2) const
{
	int run = p2.x - x;
	int rise = p2.y - y;
	
	return (rise * rise) + (run * run);
}

int Point::getDistance(const Point &p2) const 
{
	return round(sqrt(getRelativeDistance(p2)));
}

typedef vector<Point> Points;

Points loadCities(const string &filename)
{
	ifstream infile(filename.c_str());
	
	Points cities;
	int city, x, y, lastCity = -1;
	while (infile) {
		infile >> city >> x >> y;
		if (city != lastCity)
			cities.push_back(Point(x, y));
		lastCity = city;
	}
	
	infile.close();
	return cities;
}

int getNextCity(int curCity, const Points &cities, const vector<int> &remainingCities)
{
	int closestCity = remainingCities[0];
	int minRelDistance = cities[curCity].getRelativeDistance(cities[closestCity]);
	
	for (int i = 1; i < remainingCities.size(); i++) {
		int relDistance = cities[curCity].getRelativeDistance(cities[remainingCities[i]]);
		if (relDistance < minRelDistance) {
			minRelDistance = relDistance;
			closestCity = remainingCities[i];
		}
	}
	//cout << closestCity << endl;
	return closestCity;
}

vector<int> nearestNeighborTSP(const Points &cities, int startingCity)
{
	vector<int> path;
	path.reserve(cities.size());
	
	vector<int> remainingCities;
	remainingCities.reserve(cities.size());
	
	for (int i = 0; i < cities.size(); i++)
		remainingCities.push_back(i);
		
	path.push_back(startingCity);
	
	int curCity = startingCity;

	remainingCities.erase(remove(remainingCities.begin(), remainingCities.end(), 
		startingCity), remainingCities.end());
	
	for (int i = 0; i < cities.size() - 1; i++) {
		int closestNeighbor = getNextCity(curCity, cities, remainingCities);

		remainingCities.erase(remove(remainingCities.begin(), remainingCities.end(), 
			closestNeighbor), remainingCities.end());
		path.push_back(closestNeighbor);
		curCity = closestNeighbor;
	}
	
	return path;
}

int getPathDistance(const vector<int> &path, const Points &cities)
{
	unsigned int length = 0;
	int psize = path.size();
	for (int i = 0; i < path.size() - 1; i++) {
		length += cities[path[i]].getDistance(cities[path[i + 1]]);
	}
	
	// add the last element
	length += cities[path[0]].getDistance(cities[path[psize - 1]]);
	
	return length;
}

vector<int> randomNearestNeighborTSP(const Points &cities)
{
	int startingCity = random() % cities.size();
	
	return nearestNeighborTSP(cities, startingCity);
}

void output(const string &filename, const vector<int> &path, int distance)
{
	ofstream outfile(filename.c_str());
	
	outfile << distance << endl;
	
	for (int i = 0; i < path.size(); i++) {
		outfile << path[i] << endl;
	}
	
	outfile.close();
}

vector<int> twoopt(const Points &cities, const vector<int> &path)
{
	vector<int> newPath = path;
	for (int i = 1; i < newPath.size() - 2; i++) {
		for (int k = i + 1; k < newPath.size() - 2; k++) {
			int city1 = newPath[i-1];
			int city2 = newPath[i];
			int city3 = newPath[k];
			int city4 = newPath[k+1];
			if ((cities[city1].getDistance(cities[city2]) + cities[city3].getDistance(cities[city4])) >
				(cities[city1].getDistance(cities[city3]) + cities[city2].getDistance(cities[city4]))) {
					reverse(newPath.begin() + i, newPath.begin() + k + 1);	
			}
		}
	}
return newPath;
}

vector<int> getApproximateTSP(const Points &cities)
{
	vector<int> path = randomNearestNeighborTSP(cities);
	
	const int ALT_PATHS = 5;
	for (int i = 0; i < ALT_PATHS; i++) {
		vector<int> altPath = randomNearestNeighborTSP(cities);
		if (getPathDistance(path, cities) > getPathDistance(altPath, cities))
			path = altPath;
	}
		
	vector<int> newPath = twoopt(cities, path);
		
	while (!equal(path.begin(), path.end(), newPath.begin())) {
		path = newPath;
		newPath = twoopt(cities, path);
	}
	
	return path;
}
		

int main(int argc, char **argv)
{
	if (argc < 2) {
		cerr << "usage: tsp input_filename" << endl;
		return 1;
	}

	srand(time(NULL));
	
	string filename(argv[1]);
	Points cities = loadCities(filename);
	
	vector<int> path = getApproximateTSP(cities);
	int distance = getPathDistance(path, cities);
	
	output(filename + ".path", path, distance);	
	
	return 0;
}
