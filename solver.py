import numpy
import sys

if (len(sys.argv) != 2):
    print "usage: python %s N" % sys.argv[0]
    sys.exit()

citiesdata = sys.argv[1]
dat    = numpy.loadtxt(citiesdata, delimiter=',', skiprows=1)

numberofcities = len(dat)

def distance(city1, city2):
    return numpy.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def rearrangeCities(dat):
    xaxis =[]
    xindex = []
    for i in range(numberofcities):
        xaxis.append(dat[i][0])
        xindex.append(i)
    
    xorder = []
    while len(xorder) < numberofcities:
        minx = min(xaxis)
        index = xaxis.index(minx)
        xorder.append(dat[index])
        xaxis[index] = max(xaxis)+1
    return xorder

def connectCities(xorder):
    traveldistance = 0
    for i in range(len(xorder)):
        try:
            kyori = distance(xorder[i],xorder[i+1])
            traveldistance += kyori
        except IndexError:
            kyori = distance(xorder[i], xorder[0])
            traveldistance += kyori
    return traveldistance

cities = rearrangeCities(dat)
distance = connectCities(cities)

print distance