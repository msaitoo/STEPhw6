import numpy
import sys
import matplotlib.pyplot as pyplot

if (len(sys.argv) != 2):
    print "usage: python %s N" % sys.argv[0]
    sys.exit()

citiesdata = sys.argv[1]
dat    = numpy.loadtxt(citiesdata, delimiter=',', skiprows=1)

numberofcities = len(dat)

def distance(city1, city2):
    return numpy.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def divideaxis(data):
    xaxis, yaxis = [], []
    xindex, yindex = [], []
    for i in range(len(data)):
        xaxis.append(data[i][0])
        xindex.append(i)
        yaxis.append(data[i][1])
        yindex.append(i)
    return (xaxis, yaxis)

def lowline (xaxis, yaxis, maxx, yindex, ordered):
    low = []
    while xaxis[yindex] < maxx:
        low.append([xaxis[yindex],yaxis[yindex]])
        xaxis.pop(yindex)
        yaxis.pop(yindex)
        miny = min(yaxis)
        yindex = yaxis.index(miny)
    
    axis = divideaxis(low)
    while len(axis[0]) > 0:
        smallx = min(axis[0])
        index = axis[0].index(smallx)
        ordered.append([axis[0][index], axis[1][index]])
        axis[0].pop(index)
        axis[1].pop(index)
    
    return (ordered, xaxis, yaxis)

def rearrangeCities(dat):
    xaxis = divideaxis(dat)[0]
    yaxis = divideaxis(dat)[1]
    
    ordered = []
    mindex = xaxis.index(min(xaxis))
    ordered.append([xaxis[mindex],yaxis[mindex]])
    xaxis.pop(mindex)
    yaxis.pop(mindex)
    
    maxx = max(xaxis)
    yindex = yaxis.index(min(yaxis))
    low = lowline(xaxis, yaxis, maxx, yindex, ordered)
    
    xaxis = low[1]
    yaxis = low[2]
    ordered = low[0]
    
    while len(ordered) < numberofcities:
        xmax = max(xaxis)
        maxdex = xaxis.index(xmax)
        ordered.append([xaxis[maxdex], yaxis[maxdex]])
        xaxis.pop(maxdex)
        yaxis.pop(maxdex)
    
    return ordered

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

pyplot.figure()
for i in range(len(cities)):
    pyplot.plot(cities[i][0], cities[i][1], "o")
pyplot.show()