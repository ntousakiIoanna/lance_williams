#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Lance Williams algorithm implementation for integer clusters"""

__author__ = 'Ioanna Ntousaki'
__version__ = '3.10.11'

import sys

# read the a .txt file and store the data into a list
def readFile() : 
    
    with open(sys.argv[2],"r") as file:
        
        # store each i (separated by space) as an integer list, representing a cluster
        data = [[int(x)] for x in file.read().strip("\n").split(" ")]  
    return data

# give value to the variables ai, aj, b, g according to the single method 
def single() : 
    a = 1/2
    b = 1/2
    c = 0
    d = -1/2
    return a, b, c, d

# give value to the variables ai, aj, b, g according to the complete method        
def complete():
    a = 1/2
    b = 1/2
    c = 0
    d = 1/2
    return a, b, c, d

# give value to the variables ai, aj, b, g according to the average method
def average(cluster1 , cluster2):
    a = cluster1/(cluster1 + cluster2)
    b = cluster2/(cluster1 + cluster2)
    c = 0
    d = 0
    return a, b, c, d

# give value to the variables ai, aj, b, g according to the ward method      
def ward(cluster1 , cluster2, joinWith):
    a = (cluster1 + len(joinWith))/(cluster1 + cluster2 + len(joinWith))
    b = (cluster2 + len(joinWith))/(cluster1 + cluster2 + len(joinWith))
    c = -(len(joinWith))/(cluster1 + cluster2 + len(joinWith))
    d = 0
    return a, b, c, d

# find and print the the clusters' creation process till a single cluster emerges
def resolveTree(data, distance):
    
    if len(data) > 1 :  # continue with the process while there are still clusters to join
        
        # find minmum distance : the lists are always sorted so, search only in the first position of each table 
        minDist = 1000000000
        for i in range(0,len(data) - 1):
            if minDist > distance[i][0]:
                minDist = distance[i][0]  
        i = 0
        while i < len(distance) :
           
            if minDist == distance[i][0]:
                
                cl1, cl2 = len(data[i]),len(data[i+1])  # keep the length of the clusters that are being joined 
                    
                # initialize ai, aj, b, g according to the prefered method
                if sys.argv[1] == "single":
                    ai, aj, b, g = single()
                elif sys.argv[1] == "complete":
                    ai, aj, b, g = complete()
                elif sys.argv[1] == "average":
                    ai, aj, b, g = average(cl1, cl2)
                        
                print('(%s) (%s) %.2f %d' % (' '.join(str(x) for x in data[i]), ' '.join(str(x) for x in data[i+1]), minDist, len(data[i])+len(data[i+1])))
                    
                #   call the method to calculate variables ai aj b g
                data[i].extend(data[i+1])
                data.pop(i+1)
                    
                distance.insert(i, [])  # add one more row for the new cluster                                        
                    
                distance[i+1].pop(0)    # remove the distance between the joined clusters
                    
                    
                # the distances are stored in an upper triangular array (list of lists basically)
                # create a new list containing the distance of the new cluster with each cluster that is located after it in the array
                for x in range(0,len(distance[i+1])):
                    if sys.argv[1] == "ward": 
                        ai, aj, b, g = ward(cl1, cl2, data[i+x+1])
                    dist = ai * distance[i+1][x] + aj * distance[i+2][x] + b * minDist + g * abs(distance[i+1][x] - distance[i+2][x])
                    distance[i].append(dist)
                
                # update with the new clusters' distance the lists of the clusters that are located in the distance table before the new cluster list        
                x = i - 1
                for y in range(0,i):
                    if sys.argv[1] == "ward":
                        ai, aj, b, g = ward(cl1, cl2, data[y])
                    dist = ai * distance[y][x] + aj * distance[y][x+1] + b * minDist + g * abs(distance[y][x] - distance[y][x+1])
                    distance[y].pop(x)
                    distance[y].pop(x)
                    distance[y].insert(x,dist)
                    x-=1
                    
                # remove the joined clusters lists
                distance.pop(i+1)
                distance = [x for x in distance if x]   #   remove the empty lists 

                if len(distance) >= i+1:
                    distance.pop(i+1) 
                # reduce by two so that when it gets out of the if statement it is forwarded one 
                # position behind to re-check the new cluster combination for the min value  
                i = i - 2
                    
            # when i = -2 data[i] gets invalid 
            try:
                i = data.index(data[i]) + 1 
            except:
                i = 1
                break
            
        resolveTree(data, distance)
        
        
if __name__ == '__main__' :

    try:
        data = readFile()   # store the data read from the file into a list
        data.sort() # sort the table with the clusters
        minDist = 1000000000
        i = 0
        distance = [[] for x in range(len(data) - 1)]
        
        # fill the distance table with the initial distances of the integers given 
        for i in range(0,len(data)-1):
            for j in range(i+1,len(data)):
                distance[i].append(abs(data[j][0] - data[i][0]))
        
        resolveTree(data, distance)
    except:
        print("The command given must follow this format: 'python lance_williams.py <methodName> <fileName>'\n- methodName: 'single' 'complete' 'average' 'ward'")

