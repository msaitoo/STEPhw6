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

def divideCities(data):
    midpoint = sum(divideaxis(dat)[1]) / len(divideaxis(dat)[1])
    below, above = [], []
    
    for i in range(len(data)):
        if data[i][1] <= midpoint:
            below.append(data[i])
        else:
            above.append(data[i])
    return(below, above)

def check(data, start):
    for i in range(start, len(data)-2):
        if distance(data[i], data[i+1]) > distance(data[i], data[i+2]):
            chikai = data[i+2]
            tooi = data[i+1]
            data[i+1] = chikai
            data[i+2] = tooi
    return data

def connectBelow(below, ordered = []):
    xaxis = divideaxis(below)[0]
    yaxis = divideaxis(below)[1]
    
    while len(ordered) < len(below):
        minx = min(xaxis)
        index = xaxis.index(minx)
        ordered.append([xaxis[index], yaxis[index]])
        xaxis.pop(index)
        yaxis.pop(index)
    check(ordered, 0)
    return ordered

def connectAbove(above, ordered):
    xaxis = divideaxis(above)[0]
    yaxis = divideaxis(above)[1]
    start = len(ordered)
    
    while len(ordered) < numberofcities:
        maxx = max(xaxis)
        index = xaxis.index(maxx)
        ordered.append([xaxis[index], yaxis[index]])
        xaxis.pop(index)
        yaxis.pop(index)
    check(ordered, start)
    return ordered

def totaldistance(ordered):
    traveldistance = 0
    for i in range(len(ordered)):
        try:
            kyori = distance(ordered[i],ordered[i+1])
            traveldistance += kyori
        except IndexError:
            kyori = distance(ordered[i], ordered[0])
            traveldistance += kyori
    return traveldistance

SouthNorth = divideCities(dat)
south = connectBelow(SouthNorth[0])
cities = connectAbove(SouthNorth[1], south)

distance = totaldistance(cities)
print distance

pyplot.figure()
for i in range(len(cities)):
    pyplot.plot(cities[i][0], cities[i][1], "o")
pyplot.show()