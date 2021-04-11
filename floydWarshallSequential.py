'''
Floyd Warshall Algorithm in python
source: https://www.programiz.com/dsa/floyd-warshall-algorithm?fbclid=IwAR2wIKx5uDuwwM8Kt59pe6Vu11lHm9jUrT7j_qAl1BmXUGk_-G-ALvtnJa4

'''


from graph import create_graph, loadGraph
from codetiming import Timer

#getting code execution time: python -m pip install codetiming
t = Timer(name="class")
t.start()


INF = 9999

# Algorithm implementation
def floyd_warshall(G):

    #execution time: approx. 25-30 seconds for 200 nodes, approx. 90 seconds for 300 nodes
    distance = G

    # Adding vertices individually
    for k in range(nV):
        for i in range(nV):
            for j in range(nV):
                distance[i][j] = min(distance[i][j], distance[i][k] + distance[k][j])
        #print(distance)
    #print_solution(distance)


# Printing the solution
def print_solution(distance):
    for i in range(nV):
        for j in range(nV):
            if(distance[i][j] == INF or distance[i][j] > 9000):
                print("INF", end=" ")
            else:
                print(distance[i][j], end="  ")
        print(" ")

    



G = loadGraph('testExample.txt')
nV = len(G)
'''
G =  [[0, 5, INF, 10],
        [INF, 0, 3, INF],
        [INF, INF, 0,   1],
        [INF, INF, INF, 0]
        ]
nV=len(G)
'''
floyd_warshall(G)

#t.stop() vraća lijepo formatiran rezultat pa nije potreban print
execution_time = t.stop()

