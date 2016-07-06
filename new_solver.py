import numpy
import sys
import matplotlib as mpl
import matplotlib.pyplot as pyplot

if (len(sys.argv) != 2):
    print "usage: python %s N" % sys.argv[0]
    sys.exit()

citiesdata = sys.argv[1]
dat    = numpy.loadtxt(citiesdata, delimiter=',', skiprows=1)

numberofcities = len(dat)

def distance(city1, city2):
    "Calculates the distance between two given cities."
    return numpy.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def divideaxis(data):
    "Make separate list for x and y axis points"
    xaxis, yaxis = [], []
    xindex, yindex = [], []
    for i in range(len(data)):
        xaxis.append(data[i][0])
        xindex.append(i)
        yaxis.append(data[i][1])
        yindex.append(i)
    return (xaxis, yaxis)

def divideCities(data):
    "Divides cities into South and North region"
    midpoint = sum(divideaxis(data)[1]) / len(divideaxis(data)[1])
    
    below, above = [], []
    
    for i in range(len(data)):
        if data[i][1] <= midpoint:
            below.append(data[i])
        else:
            above.append(data[i])
    return(below, above)

def getdistances(city1, around):
    distances = []
    
    for i in range(len(around)):
        dist = distance(city1, around[i])
        distances.append(dist)
    
    return distances

def ascendingx(data):
    order = []
    xaxis = divideaxis(data)[0]
    number = len(data)
    while len(order) < number:
        minx = min(xaxis)
        index = xaxis.index(minx)
        order.append(data[index])
        xaxis.pop(index)
        data.pop(index)
    return order

def descendingx(data):
    order = []
    xaxis = divideaxis(data)[0]
    number = len(data)
    while len(order) < number:
        minx = max(xaxis)
        index = xaxis.index(minx)
        order.append(data[index])
        xaxis.pop(index)
        data.pop(index)
    return order

def connectBelow(below, ordered = []):
    "Sort Southern cities into order"
    jyunban = ascendingx(below)
    minami = len(jyunban)
    ordered.append(jyunban[0])
    jyunban.pop(0)
    
    while len(ordered) < minami:
        around = []
        for i in range(len(jyunban)):
            around.append(jyunban[i])
        if around[0][0] <= ordered[-1][0]:
            distances = getdistances(ordered[-1], around)
            mindist = min(distances)
            index = distances.index(mindist)
            if abs(ordered[-1][1]-jyunban[index][1]) <= abs(ordered[-1][1]-jyunban[0][1]):
                ordered.append(jyunban[index])
                jyunban.pop(index)
            else:
                ordered.append(jyunban[0])
                jyunban.pop(0)
        else:
            distances = getdistances(ordered[-1], around)
            mindist = min(distances)
            index = distances.index(mindist)
            if abs(ordered[-1][1]-jyunban[index][1]) <= abs(ordered[-1][1]-jyunban[0][1]):
                ordered.append(jyunban[index])
                jyunban.pop(index)
            else:
                ordered.append(jyunban[0])
                jyunban.pop(0)
    
    return ordered

def connectAbove(above, ordered):
    "Sort Northern cities into order"
    jyunban = descendingx(above)
    
    while len(ordered) < numberofcities:
        around = []
        for i in range(len(jyunban)):
            around.append(jyunban[i])
        if around[0][0] >= ordered[-1][0]:
            distances = getdistances(ordered[-1], around)
            mindist = min(distances)
            index = distances.index(mindist)
            if abs(ordered[-1][1]-jyunban[index][1]) <= abs(ordered[-1][1]-jyunban[0][1]):
                ordered.append(jyunban[index])
                jyunban.pop(index)
            else:
                ordered.append(jyunban[0])
                jyunban.pop(0)
        else:
            distances = getdistances(ordered[-1], around)
            mindist = min(distances)
            index = distances.index(mindist)
            ordered.append(jyunban[index])
            jyunban.pop(index)
    
    return ordered

def totaldistance(ordered):
    "Calculates distance to travel in order of 'ordered' cities"
    traveldistance = 0
    for i in range(len(ordered)):
        try:
            kyori = distance(ordered[i],ordered[i+1])
            traveldistance += kyori
        except IndexError:
            kyori = distance(ordered[i], ordered[0])
            traveldistance += kyori
    return traveldistance

south = divideCities(dat)[0]
north = divideCities(dat)[1]
southcities = connectBelow(south)
allcities = connectAbove(north, southcities)

travel = totaldistance(allcities)
print travel

def graph(cities):
    "Locations of the cities"
    pyplot.figure()
    cmap = mpl.cm.cool
    for i in range(len(cities)):
        pyplot.plot(cities[i][0], cities[i][1], "o")
        try:
            pyplot.plot((cities[i][0], cities[i+1][0]), (cities[i][1],cities[i+1][1]), "-", color=cmap(i / float(len(cities))))
        except IndexError:
            pyplot.plot((cities[i][0], cities[0][0]), (cities[i][1],cities[0][1]), "-", color='purple')
    pyplot.show()