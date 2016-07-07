def test(ordered):
    def straightline(data1, data2):
        try: 
            m = (data2[1]-data1[1])/(data2[0]-data1[0])
        except ZeroDivisionError:
            m = 0
        b = data1[1] - m*data1[0]
        return (m,b)
    
    def checkintercept(ordered, eqn = [], index = 0):
        for i in range(len(ordered)-1):
            eqn.append(straightline(ordered[i], ordered[i+1]))
        #print eqn
        while index <= len(ordered)-3:
            try:
                xintercept = (eqn[index][1] - eqn[-1][1]) / (eqn[-1][0] - eqn[index][0])
            except ZeroDivisionError:
                xintercept = False
            xlist1 = [ordered[index][0], ordered[index+1][0]]
            xlist2 = [ordered[-2][0], ordered[-1][0]]
            if xintercept != False:
                if max(min(xlist1),min(xlist2)) < xintercept < min(max(xlist1),max(xlist2)):
                    #print xintercept
                    yintercept = eqn[-1][0] * xintercept + eqn[-1][1]
                    ylist1 = [ordered[index][1], ordered[index+1][1]]
                    ylist2 = [ordered[-2][1], ordered[-1][1]]
                    if max(min(ylist1),min(ylist2)) < yintercept < min(max(ylist1),max(ylist2)):
                        #print ordered[index+1]
                        tsugi = ordered[-2]
                        for coordinate in range(index+1, len(ordered)-1):
                            kieru = ordered[coordinate]
                            ordered[coordinate] = tsugi
                            tsugi = kieru
            index += 1
        
        return ordered
    return ordered