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
    "Get a list of distances to each points in [around] from city 1"
    distances = []
    for i in range(len(around)):
        dist = distance(city1, around[i])
        distances.append(dist)
    return distances

def sortx(data, direction):
    "rearrange cities into x values order"
    order = []
    xaxis = divideaxis(data)[0]
    number = len(data)
    while len(order) < number:
        if direction == 'ascending':
            minx = min(xaxis)
        elif direction == 'descending':
            minx = max(xaxis)
        index = xaxis.index(minx)
        order.append(data[index])
        xaxis.pop(index)
        data.pop(index)
    return order

def decidenext(jyunban, ordered, area):
    "decides where the next destination is"
    if area == 'north':
        big = jyunban[0][0]
        small = ordered[-1][0]
    elif area == 'south':
        big = ordered[-1][0]
        small = jyunban[0][0]
    
    distances = getdistances(ordered[-1], jyunban)
    mindist = min(distances)
    index = distances.index(mindist)
    if big >= small:
        if abs(ordered[-1][1]-jyunban[index][1]) <= abs(ordered[-1][1]-jyunban[0][1]):
            ordered.append(jyunban[index])
            jyunban.pop(index)
        else:
            ordered.append(jyunban[0])
            jyunban.pop(0)
    else:
        ordered.append(jyunban[index])
        jyunban.pop(index)
    return (ordered)

def connectBelow(below, ordered = []):
    "Sort Southern cities into order"
    jyunban = sortx(below, 'ascending')
    minami = len(jyunban)
    ordered.append(jyunban[0])
    jyunban.pop(0)
    
    while len(ordered) < minami:
        decidenext(jyunban, ordered, 'south')
    
    return ordered

def connectAbove(above, ordered):
    "Sort Northern cities into order"
    jyunban = sortx(above, 'descending')
    
    while len(ordered) < numberofcities:
        decidenext(jyunban, ordered, 'north')
    
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
    "cities' locations and paths one will take"
    pyplot.figure()
    cmap = mpl.cm.cool
    for i in range(len(cities)):
        pyplot.plot(cities[i][0], cities[i][1], "o")
        try:
            pyplot.plot((cities[i][0], cities[i+1][0]), (cities[i][1],cities[i+1][1]), "-", color=cmap(i / float(len(cities))))
        except IndexError:
            pyplot.plot((cities[i][0], cities[0][0]), (cities[i][1],cities[0][1]), "-", color='purple')
    pyplot.show()

print 'Would you like to graph the result? Type yes or no.'
answer = raw_input()
if answer == 'yes':
    graph(allcities)
else:
    print'Sure? Ok then, bye~~'
