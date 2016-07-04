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
    yaxis = []
    xindex = []
    yindex = []
    for i in range(numberofcities):
        xaxis.append(dat[i][0])
        xindex.append(i)
        yaxis.append(dat[i][1])
        yindex.append(i)
    
    order = []
    minx = min(xaxis)
    mindex = xaxis.index(minx)
    order.append([xaxis[mindex],yaxis[mindex]])
    xaxis.pop(mindex)
    yaxis.pop(mindex)
    
    maxx = max(xaxis)
    yindex = yaxis.index(min(yaxis))
    
    while xaxis[yindex] < maxx:
        miny = min(yaxis)
        yindex = yaxis.index(miny)
        order.append([xaxis[yindex],yaxis[yindex]])
        if xaxis[yindex] == maxx:
            break
        xaxis.pop(yindex)
        yaxis.pop(yindex)
    
    while len(order) < numberofcities:
        xmax = max(xaxis)
        maxdex = xaxis.index(xmax)
        order.append([xaxis[maxdex], yaxis[maxdex]])
        xaxis.pop(maxdex)
        yaxis.pop(maxdex)
    
    #while len(order) < numberofcities:
        #xmax = max(xaxis)
    
    #while len(order) < numberofcities:
        #minx = min(xaxis)
        #index = xaxis.index(minx)
        #xorder.append(dat[index])
        #xaxis[index] = max(xaxis)+1
    return order

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