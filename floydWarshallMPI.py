from mpi4py import MPI
import numpy as np
from graph import create_graph, loadGraph
from codetiming import Timer

# mpiexec -n 4 python floydWarshallMPI.py

#getting code execution time: python -m pip install codetiming
t = Timer(name="class")
t.start()


INF = 9999
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

generatedGraph = None


if rank==0:  
    generatedGraph = loadGraph('testExample.txt')

    #https://www.quora.com/Are-NumPy-arrays-faster-than-lists
    #bez konvertiranja numpy polja u listu je read i write duplo sporiji
    generatedGraph = generatedGraph.tolist()


generatedGraph = [[0, 5, INF, 10],
        [INF, 0, 3, INF],
        [INF, INF, 0,   1],
        [INF, INF, INF, 0]
        ]


graph = comm.bcast(generatedGraph, root=0)


n = comm.bcast(len(graph), root=0)



if(rank != 0):

    #raspodjela obrade podataka(matrice) po procesima
    #step -> promijenjiva vrijednost za određivanje početka i kraja rada svakog procesa
    #start -> varijabla koja određuje početak rada za pojedini proces
    #end -> varijabla koja određuje kraj rada pojedinog procesa
   
    step = int(len(graph) / size)
    start = (rank - 1)*step
    end = start + step
    if rank == size - 1:
        end = n

    
    #k -> središnji vrh (čvor kroz koji se traži najkraći put do vrha)
    for k in range(start, end):
        #print(k, rank)
        for i in range(0, n):

                for j in range(0, n):
                    if (i == j): continue
                    graph[i][j] = min(graph[i][j],
                                    graph[i][k] + graph[k][j])
    
        print('rank:', rank, 'k', k,  '\n', graph)
   
    sendmsg = comm.send(graph, dest=0)
    

else:
    minMatrix = np.full((n, n), 9999)

    for srcc in range(1, size):
        result = comm.recv(source=srcc)
        minMatrix = np.minimum(minMatrix,result)
    
    finalResult = minMatrix
    

    #t.stop() vraća lijepo formatiran rezultat pa nije potreban print za vrijeme
    #test: approx. 25 seconds for 300 nodes
    t.stop()       
    print('result:\n', np.asarray(finalResult))
    

