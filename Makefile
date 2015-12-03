#########################################################
# File: Makefile
# Description: Makefile for tsp
#########################################################

# define the C++ compiler
CXX = g++

#compilation flags
CXXFLAGS = -Wall -pedantic-errors
LDDFLAGS =
DEBUG = -g
OPTIMIZE = -O3
TESTING = -DTESTING

all: tsp

tsp: tsp.cpp
	${CXX} ${CXXFLAGS} ${OPTIMIZE} -o tsp tsp.cpp

clean:
	rm tsp
	
zip:
	zip tsp.zip tsp.cpp
